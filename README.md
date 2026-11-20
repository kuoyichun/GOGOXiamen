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
- `audio/`：每個喇叭按鈕的語音檔（台灣國語女聲 HsiaoChen）
- `tools/make_audio.py`：重新產生語音檔
- `sw.js`：沒網路時也能打開看過的頁面

## 常見修改

- **船班時間確定後**：在 `assets/data.js` 改那一項的 `t`，順便把 `tbd: true` 拿掉、改 `say` 裡唸的時間，再跑 `python3 tools/make_audio.py` 重錄有改到的語音。
- **測試「現在」列**：網址後面加 `?now=2026-12-18T15:20`，就會假裝現在是那個時間。

## 旅行手札（B6 印刷版）

- `book/xiamen-travel-book-b6-print.pdf`：給印刷店，B6（12.8 × 18.2 公分）72 頁，四邊各多 3mm 出血，可騎馬釘裝訂
- `book/xiamen-travel-book-b6.pdf`：同一本的裁切尺寸版，看電子檔或自己印
- 內容：行李清單、託運和隨身行李規定、不能帶的東西、交通票卡、碼頭流程、住宿、每日行程和地圖、景點介紹、必吃、伴手禮、給司機看、花費紀錄、筆記
- 重新產生：`python3 book/make_book.py`（行程、地址、美食從 `assets/data.js` 讀，景點介紹寫在 `book/make_book.py` 的 `SPOT`）
- 照片在 `book/img/`，來源和授權在 `book/credits.json`；圓體字是 jf open 粉圓（`book/fonts/`，SIL OFL），封面貼紙和圖示是 Microsoft Fluent Emoji（MIT，`book/stickers/`、`book/icons/`）
