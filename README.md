# Zheng Yang 个人学术网站



域名：https://zhengyang.rocks/



页面版权署名：© 2026 Zheng Yang. All rights reserved.





## 修改资料



- `index.html`：姓名、简介、论文、新闻、经历、荣誉、专利和联系方式。

- `styles.css`：字体、颜色、桌面和手机布局。

- `script.js`：论文搜索、年份筛选、高被引筛选、手机菜单和版权年份。

- `portrait.jpg`：当前头像（用户提供）；`rmre.png`、`eg.png`、`jrmge.png`：原论文配图。

- 若使用其他自有域名，需要同步修改 canonical、社交分享元数据、结构化数据、robots.txt 和 sitemap.xml。


## Google Scholar 指标追踪

引用总数、H-index、i10-index 取自公开主页的 All 列。每天 UTC 05:23 通过 `.github/workflows/scholar-pages.yml` 尝试同步，也在 main 更新或手动运行时同步；调度可能延迟。Pages 发布方式现为 GitHub Actions。

首次核对为 1,112 次引用、H-index 21、i10-index 33。Google 会限制云端自动请求，首次 GitHub 抓取未成功；获取失败时保留最近成功快照，并在网站显示 Sync delayed。不会绕过验证码，不保证每日获取成功。

`scholar-metrics.json` 保存最近成功日期及最多 365 天记录，`update_scholar.py` 获取和验证数据。工作流沿用 Pages 发布权限，不写入仓库，不需个人访问令牌。公开仓库长期无活动时，GitHub 可能自动停用定时任务，可在 Actions 页面重新启用。

## Publication tools and static metrics (4 November 2026)

- The 16 representative publications include DOI links, plain citation copying, expandable BibTeX, individual `.bib` downloads and a combined `publications.bib`. Verified Crossref metadata and source URLs are kept in `publications.json`.
- `prepare_site.py` copies the public assets and renders citation count, H-index and verification date from `scholar-metrics.json` into the HTML. Pages runs it after `update_scholar.py`, so HTML and the same-origin JSON use one snapshot. Failed Scholar refreshes retain the previously verified values.
- Run `python prepare_site.py` for a local static artifact in `_site/`. Preview it with `python -m http.server --directory _site`.
- Copy controls use the Clipboard API with a selectable-text dialog fallback. Without JavaScript, publications, BibTeX downloads, profile content and verified metrics remain readable.
- Official institutional artwork and the user-selected journal order are retained. Captions supply readable institution names. CV download is intentionally unchanged.

## 2026-11-05 优化

- 头像：`portrait-400.webp` / `portrait-800.webp`（`portrait-800.jpg` 为兜底），原 `portrait.jpg`（1.47 MB）仅保留给旧链接。
- 图标：`favicon-32.png`、`icon-192.png`、`apple-touch-icon.png`；社交分享图：`og-image.jpg`（1200×630）。
- 研究方向配图：`research-*.webp`，由 `eg.png`、裂纹分类示意图和 EFM 2024 实验图裁剪压缩而来（不附论文链接）；大 PNG 和 `cover-*` 期刊封面不再发布到 `_site`，仍保留在仓库中。
- Publication venues 改为文字链接列表；`journal-covers.json` 保留以便恢复封面墙。
- 支持系统暗色模式（`styles.css` 末尾的 `prefers-color-scheme: dark`）。
