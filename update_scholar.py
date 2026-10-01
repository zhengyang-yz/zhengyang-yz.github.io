"""Refresh public Scholar metrics; preserve the last verified snapshot on failure."""
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROFILE_ID = "NhYiCs4AAAAJ"
PROFILE_URL = f"https://scholar.google.com/citations?user={PROFILE_ID}&hl=en"
SITE_URL = "https://zhengyang.rocks/scholar-metrics.json"
DATA_PATH = Path(__file__).with_name("scholar-metrics.json")


class MetricsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.capture = False
        self.cells = []
        self.labels = []
        self.is_label = False
        self.cell = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and attrs.get("id") == "gsc_rsb_st":
            self.in_table = True
        classes = attrs.get("class", "").split()
        if self.in_table and tag == "td" and ("gsc_rsb_std" in classes or "gsc_rsb_sc1" in classes):
            self.capture = True
            self.is_label = "gsc_rsb_sc1" in classes
            self.cell = ""

    def handle_data(self, data):
        if self.capture:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == "td" and self.capture:
            target = self.labels if self.is_label else self.cells
            target.append(self.cell.strip().replace(",", ""))
            self.capture = False
        if tag == "table":
            self.in_table = False


def validate(data):
    if data.get("profile_id") != PROFILE_ID:
        raise ValueError("Unexpected Scholar profile")
    for key in ("citations", "h_index", "i10_index"):
        if type(data.get(key)) is not int or data[key] < 0:
            raise ValueError(f"Invalid {key}")
    if data["citations"] < data["h_index"] ** 2:
        raise ValueError("Inconsistent citation and h-index values")
    datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
    return data


def parse_metrics(html):
    parser = MetricsParser()
    parser.feed(html)
    if parser.labels != ["Citations", "h-index", "i10-index"] or len(parser.cells) != 6 or not all(value.isdecimal() for value in parser.cells):
        raise ValueError("Scholar metrics unavailable (possibly a challenge page)")
    return validate({"profile_id": PROFILE_ID, "profile_url": PROFILE_URL,
                     "citations": int(parser.cells[0]), "h_index": int(parser.cells[2]),
                     "i10_index": int(parser.cells[4]),
                     "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds")})


def fetch(url):
    request = Request(url, headers={"User-Agent": "ZhengYangWebsiteMetrics/1.0", "Accept-Language": "en"})
    with urlopen(request, timeout=25) as response:
        return response.read(2_000_000).decode("utf-8")


def refresh():
    previous = validate(json.loads(DATA_PATH.read_text(encoding="utf-8")))
    published_unavailable = False
    try:
        published = validate(json.loads(fetch(SITE_URL)))
        if published["updated_at"] > previous["updated_at"]:
            previous = published
    except HTTPError as error:
        published_unavailable = error.code != 404  # A first deployment has no snapshot yet.
    except Exception:
        published_unavailable = True
    try:
        current = parse_metrics(fetch(PROFILE_URL))
        status = "ok"
        print(f"Scholar verified: {current['citations']} citations, h-index {current['h_index']}")
    except Exception as error:
        if published_unavailable:
            raise RuntimeError("Both published snapshot and Scholar unavailable; leave live website unchanged") from error
        current = {key: previous[key] for key in ("profile_id", "profile_url", "citations", "h_index", "i10_index", "updated_at")}
        status = "unavailable"
        reason = f"HTTP {error.code}" if isinstance(error, HTTPError) else type(error).__name__
        print(f"::warning::Scholar sync unavailable ({reason}); retaining verified values")
    today = datetime.now(timezone.utc).isoformat(timespec="seconds")
    history = previous.get("history", [])
    if status == "ok":
        day = today[:10]
        history = [row for row in history if row.get("date") != day]
        history.append({"date": day, **{key: current[key] for key in ("citations", "h_index", "i10_index")}})
    current.update(sync_status=status, last_attempt_at=today, history=history[-365:])
    DATA_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return current


if __name__ == "__main__":
    refresh()
