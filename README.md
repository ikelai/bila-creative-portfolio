# BILA Creative 必樂創意行銷 — 官方網站

純靜態多頁網站（HTML + CSS），GitHub Pages 部署。設計語言基於 sy-dive 參考（深色、全屏 hero、細字重）。

- 首頁：`index.html`
- 作品：`works.html` → `work/<case>.html`
- 服務：`services.html`
- 關於：`about.html`

案例內容：`data/cases.json`；圖片：`images/<case>/`。

## 自動化與安全

- 驗證：`python3 scripts/validate_site.py`
- 重建首頁與案例頁：`python3 scripts/generate_site.py`
- GitHub Pull Request 與 `main` 更新會自動執行相同檢查。
- ChatGPT／Hermes 交接契約位於 `automation/`。
- NAS 原始資料永遠唯讀；本 repo 只接收已策展、可公開的網站輸出。
- 禁止直接推送 `main`，工作分支使用 `agent/*` 並透過 Pull Request 交付。

網站是靜態 HTML；`data/cases.json` 是首頁與案例頁的內容來源。CI 會阻止產生頁面過期、缺圖、斷鏈、舊版頁面樣式與來源檔外洩。
