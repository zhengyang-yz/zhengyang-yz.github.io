# Zheng Yang 个人学术网站



域名：https://zhengyang-yz.github.io/



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
