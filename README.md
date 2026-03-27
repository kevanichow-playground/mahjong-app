# 🀄 9388 Mckim Way 麻雀龍虎榜

## 本地運行

```bash
npm install
npm start
# 打開 http://localhost:3000
```

## 部署到 Railway（免費，可分享連結）

1. 去 https://railway.app 註冊免費帳號（用 GitHub 登入）
2. 點 **New Project → Deploy from GitHub repo**
3. 上傳此 folder 到 GitHub（或用 Railway CLI）
4. Railway 自動偵測 Node.js，點 **Deploy**
5. 部署完成後在 Settings → Networking → Generate Domain
6. 複製連結分享給朋友 🎉

## 或用 Render（免費）

1. 去 https://render.com 註冊
2. New → Web Service → 上傳代碼
3. Build Command: `npm install`
4. Start Command: `node server.js`
5. 部署完成，獲得永久連結

## 功能

- 🏆 龍虎榜 — 完整排行 + 點擊跳轉個人頁
- 📊 勝率圖 — 勝負柱狀圖 + 正確累積走勢
- 📅 星期運勢 — 每人最佳出戰日
- 👤 個人檔案 — 六角形能力分析 + 走勢
- 📈 走勢預測 — 3場/5場均線 + 趨勢預測
- 🎲 賠率投注 — 選手手選 + 當日賠率
- ✏️ 輸入分數 — 新增場次，自動更新所有分析
