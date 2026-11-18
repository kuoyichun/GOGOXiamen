# GOGOXiamen

廈門 12/16–12/20 五天四夜行程網頁，給長輩用手機看：字大、圖多，每個行程都有喇叭按鈕可以唸出來。

## 檔案

- `index.html`：網頁本體
- `assets/data.js`：**行程內容都在這裡**（時間、標題、語音稿、附近餐廳）
- `assets/map.js`：地圖上的地標和每天的路線
- `assets/app.js`：畫面、上方「現在」列、語音按鈕
- `assets/style.css`：樣式
- `assets/land.js`：廈門、金門海岸線（OpenStreetMap）
- `img/`：照片（Wikimedia Commons，來源列在網頁最下面）
- `sw.js`：沒網路時也能打開看過的頁面

## 常見修改

- **船班時間確定後**：在 `assets/data.js` 改那一項的 `t`，順便把 `tbd: true` 拿掉、改 `say` 裡唸的時間。
- **測試「現在」列**：網址後面加 `?now=2026-12-18T15:20`，就會假裝現在是那個時間。
- **傳到 LINE**：網址後面加 `?openExternalBrowser=1`，點開會直接用手機瀏覽器開，語音按鈕才能用（LINE 內建瀏覽器在 Android 上不能唸）。
