"""Prepare the Pages artifact with the same verified metrics in HTML and JSON."""
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from update_scholar import validate

ROOT = Path(__file__).resolve().parent


def render_metrics(source, metrics):
    validate(metrics)
    stamp = datetime.fromisoformat(metrics["updated_at"].replace("Z", "+00:00"))
    date = f"{stamp.day} {stamp.strftime('%b %Y')}"
    replacements = {
        "scholar-citations": f"{metrics['citations']:,}",
        "scholar-h-index": str(metrics["h_index"]),
        "scholar-status": f"Last verified: {date} · i10-index: {metrics['i10_index']}.",
    }
    for element_id, text in replacements.items():
        pattern = rf'(<[^>]+\bid="{element_id}"[^>]*>)[^<]*(</[^>]+>)'
        source, count = re.subn(pattern, lambda m: m[1] + text + m[2], source)
        if count != 1:
            raise ValueError(f"Expected one {element_id} element, found {count}")
    return source


def build(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    metrics = json.loads((ROOT / "scholar-metrics.json").read_text(encoding="utf-8"))
    source = render_metrics((ROOT / "index.html").read_text(encoding="utf-8"), metrics)
    for pattern in (
        "styles.css", "script.js", "portrait.jpg", "portrait-*", "favicon.png", "favicon-32.png",
        "icon-192.png", "apple-touch-icon.png", "og-image.jpg", "research-*.webp",
        "robots.txt", "sitemap.xml", "scholar-metrics.json", ".nojekyll",
        "journal-covers.json", "collaboration-network.json", "logo-*",
        "publications.bib", "publications.json",
    ):
        for asset in ROOT.glob(pattern):
            if asset.is_file():
                shutil.copy2(asset, destination / asset.name)
    if (ROOT / "citations").is_dir():
        shutil.copytree(ROOT / "citations", destination / "citations", dirs_exist_ok=True)
    (destination / "index.html").write_text(source, encoding="utf-8")
    return destination


if __name__ == "__main__":
    build(ROOT / "_site")
