/* 廈門行程資料
 * 時間都是當地時間（廈門、金門、台灣都是 UTC+8）。
 * 船班時間確認後，改 t 就好，上方「現在」列和地圖會跟著變。
 *
 * 每一項：
 *   t     開始時間
 *   kind  'stop' 大卡片（有照片）｜'mini' 小列｜'move' 交通｜'opt' 沒累再去
 *   mode  交通方式：car 車、ship 船、walk 走路、plane 飛機
 *   nb    上方「現在」列顯示的短名稱
 *   say   喇叭按鈕唸的內容（時間寫成國字，語音才唸得順）
 */
window.TRIP = {
  year: 2026,
  month: 12,
  endAt: { d: 20, t: '19:00' },
  hotel: {
    name: '壺香悅（中山路步行街店）',
    show: ['壶香悦', '（厦门中山路步行街店）'],
    addr: '厦门市思明区定安路61-2号',
    say: '我們住的飯店是壺香悅，中山路步行街店，地址是廈門市思明區定安路六十一之二號。迷路的時候，把這個畫面給司機或路人看就可以了。'
  },
  days: [
    {
      id: 'd1', d: 16, wk: '三', color: '#C0392B', title: '出發・到廈門',
      say: '第一天，十二月十六號，星期三。中午先坐飛機到金門，再坐船到廈門。下午四點左右住進飯店，晚上在中山路步行街散步、吃晚餐。',
      items: [
        { id: 'd1-air', t: '12:30', kind: 'stop', icon: 'plane', title: '抵達金門機場', nb: '金門機場', img: 'kinmen-airport',
          pts: ['出來坐計程車去水頭碼頭'],
          say: '中午十二點半，飛機到金門機場。出來以後，大家一起坐計程車去水頭碼頭，大約二十分鐘。' },
        { kind: 'move', mode: 'car', text: '計程車 約 20 分鐘' },
        { id: 'd1-st', t: '13:15', kind: 'stop', icon: 'ticket', title: '水頭碼頭 報到', nb: '水頭碼頭', img: 'shuitou',
          pts: ['辦報到、出境', '證件拿在手上，跟著領隊走'],
          say: '下午一點十五分到水頭碼頭，辦報到和出境。證件先拿在手上，跟著領隊走就好。' },
        { id: 'd1-ship', t: '14:00', kind: 'stop', icon: 'ship', title: '坐船到廈門', nb: '坐船到廈門', img: 'ferry', tbd: true,
          pts: ['船程約 30 分鐘'],
          say: '下午兩點坐船到廈門的五通碼頭，大約三十分鐘。船班時間還在確認，以領隊通知為準。' },
        { id: 'd1-wt', t: '14:30', kind: 'stop', icon: 'ticket', title: '五通碼頭 入境', nb: '五通碼頭', img: 'wutong',
          pts: ['辦入境、拿行李'],
          say: '兩點半左右到廈門五通碼頭，辦入境，拿好行李。' },
        { id: 'd1-car', t: '15:15', kind: 'move', mode: 'car', text: '叫車到飯店 約 40 分鐘', nb: '前往飯店' },
        { id: 'd1-hotel', t: '16:00', kind: 'stop', icon: 'bed', title: '入住飯店', sub: '壺香悅（中山路步行街店）', nb: '入住飯店', img: 'hotel-street', hotel: true,
          pts: ['就在中山路步行街旁邊', '先休息一下'],
          say: '下午四點住進壺香悅飯店，就在中山路步行街旁邊。先休息一下。' },
        { id: 'd1-zs', t: '17:00', kind: 'stop', icon: 'food', title: '逛中山路・吃晚餐', nb: '逛中山路', img: 'zhongshan',
          pts: ['看到想吃的就進去', '不知道吃什麼？看最下面「附近吃什麼」'],
          say: '傍晚五點，出去逛中山路步行街。五點半左右天就黑了，街上的燈很漂亮。看到想吃的就進去吃晚餐。' },
        { id: 'd1-back', t: '19:30', kind: 'mini', icon: 'home', title: '回飯店休息', nb: '回飯店休息',
          say: '晚上七點半回飯店休息。' }
      ]
    },
    {
      id: 'd2', d: 17, wk: '四', color: '#2E7D4F', title: '土樓・海景晚餐',
      say: '第二天，十二月十七號，星期四。早上包車去雲水謠看土樓，車程大約兩個小時。下午回到中山路，可以去採耳放鬆。傍晚去吃海景晚餐，看鼓浪嶼的夕陽和夜景。',
      items: [
        { id: 'd2-bf', t: '07:30', kind: 'stop', icon: 'food', title: '早餐', sub: '麵線糊、花生湯', nb: '早餐', img: 'breakfast',
          pts: ['飯店附近吃'],
          say: '早上七點半，在飯店附近吃早餐，可以試試廈門的麵線糊和花生湯。' },
        { id: 'd2-car', t: '08:15', kind: 'move', mode: 'car', text: '包車出發 約 2 小時', nb: '包車去土樓' },
        { id: 'd2-tl', t: '10:15', kind: 'stop', icon: 'camera', title: '雲水謠 看土樓', nb: '雲水謠土樓', img: 'tulou', map: 'tulou',
          pts: ['客家人住的大土樓，有圓的也有方的', '老榕樹、小溪、水車'],
          say: '上午十點十五分到雲水謠。這裡有客家人住的大土樓，有圓的也有方的，還有很大的老榕樹和小溪。慢慢走、慢慢看。' },
        { id: 'd2-lunch', t: '12:30', kind: 'mini', icon: 'food', title: '在土樓吃午餐', nb: '土樓午餐',
          say: '中午十二點半，在土樓當地吃午餐。' },
        { id: 'd2-back', t: '13:30', kind: 'move', mode: 'car', text: '坐車回中山路 約 2 小時', nb: '坐車回中山路' },
        { id: 'd2-ear', t: '15:45', kind: 'stop', icon: 'spa', title: '採耳放鬆', nb: '採耳', img: 'ear',
          pts: ['躺著清耳朵，約 1 小時', '不想做的人回飯店休息'],
          say: '下午三點四十五分回到中山路，去採耳，就是請師傅清耳朵，躺著休息大約一個小時。不想做的人可以先回飯店休息。' },
        { kind: 'move', mode: 'car', text: '叫車 約 10 分鐘' },
        { id: 'd2-dinner', t: '17:00', kind: 'stop', icon: 'food', title: '海景晚餐', sub: '小埕戲・閩南菜', nb: '海景晚餐', img: 'gulangyu-dusk',
          pts: ['窗外就是鼓浪嶼，看夕陽和夜景', '招牌：紅蟳米糕、薑母鴨'],
          say: '傍晚五點，叫車到和平碼頭旁邊的小埕戲吃閩南菜。窗外就是鼓浪嶼，可以一邊吃飯一邊看夕陽和夜景。招牌菜有紅蟳米糕和薑母鴨。' },
        { id: 'd2-home', t: '19:00', kind: 'mini', icon: 'home', title: '叫車回飯店', nb: '回飯店休息',
          say: '晚上七點叫車回飯店。' }
      ]
    },
    {
      id: 'd3', d: 18, wk: '五', color: '#1F6FB2', title: '鼓浪嶼・泡腳按摩',
      say: '第三天，十二月十八號，星期五。早上坐船去鼓浪嶼，看老洋房和海邊。中午回來吃飯、午休。下午泡腳按摩，傍晚喝功夫茶看夕陽。',
      items: [
        { id: 'd3-bf', t: '07:30', kind: 'mini', icon: 'food', title: '早餐', nb: '早餐',
          say: '早上七點半吃早餐。' },
        { kind: 'move', mode: 'car', text: '叫車到碼頭' },
        { id: 'd3-pier', t: '08:15', kind: 'stop', icon: 'ticket', title: '廈鼓碼頭', nb: '廈鼓碼頭', img: 'pier',
          pts: ['每個人都要帶台胞證', '用台胞證換上船的憑證'],
          say: '早上八點十五分，叫車到郵輪中心的廈鼓碼頭。每個人都要用自己的台胞證換上船的憑證，記得帶在身上。' },
        { id: 'd3-ship', t: '09:30', kind: 'move', mode: 'ship', text: '坐船上鼓浪嶼 約 15 分鐘', nb: '坐船上鼓浪嶼' },
        { id: 'd3-gly', t: '09:45', kind: 'stop', icon: 'camera', title: '鼓浪嶼', nb: '鼓浪嶼', img: 'gulangyu',
          pts: ['看老洋房、走海邊', '累了就坐電瓶車', '日光岩不爬上去'],
          say: '九點四十五分上島。鼓浪嶼上沒有汽車，有很多一百年前的老洋房。我們只走平路和海邊，累了就坐電瓶車，日光岩不爬上去。' },
        { id: 'd3-back', t: '12:00', kind: 'move', mode: 'ship', text: '坐船回廈門', nb: '坐船回廈門' },
        { id: 'd3-lunch', t: '12:30', kind: 'mini', icon: 'food', title: '中山路附近吃午餐', nb: '午餐',
          say: '中午十二點半，回到中山路附近吃午餐。' },
        { id: 'd3-bashi', kind: 'opt', icon: 'basket', title: '沒累的話：八市', sub: '第八市場', img: 'market', map: 'bashi',
          pts: ['在市場裡吃小吃當午餐', '看活海鮮、買芒果乾', '地板濕滑，慢慢走'],
          say: '如果還不累，可以去八市，就是第八市場。在市場裡吃麵線糊、海蠣煎當午餐，看看活海鮮，也可以買芒果乾當伴手禮。地板比較濕滑，要慢慢走，逛一個小時就好。' },
        { id: 'd3-nap', t: '13:15', kind: 'mini', icon: 'bed', title: '回飯店午休', nb: '回飯店午休',
          say: '下午一點十五分，回飯店睡午覺。' },
        { kind: 'move', mode: 'walk', text: '走路就到（同一條路）' },
        { id: 'd3-foot', t: '15:00', kind: 'stop', icon: 'spa', title: '泡腳＋按摩', nb: '泡腳按摩', img: 'foot',
          pts: ['約 1 個半小時，四個人一間', '太大力就說「輕一點」'],
          say: '下午三點，走路到同一條路上的悅馨，泡腳加按摩，大約一個半小時，四個人一間包廂。如果按得太大力，就跟師傅說「輕一點」。有人推銷辦卡，就說我們是遊客，不辦卡，謝謝。' },
        { kind: 'move', mode: 'walk', text: '走到海邊' },
        { id: 'd3-tea', t: '16:30', kind: 'stop', icon: 'tea', title: '喝功夫茶・看夕陽', nb: '喝茶看夕陽', img: 'tea',
          pts: ['大窗戶正對鼓浪嶼', '有鋼琴演奏'],
          say: '四點半，走到海邊的「不只有茶」喝功夫茶。大窗戶正對著鼓浪嶼，還有鋼琴演奏，可以坐著看夕陽。' },
        { id: 'd3-dinner', t: '17:45', kind: 'mini', icon: 'food', title: '中山路一帶吃晚餐', nb: '晚餐',
          say: '五點四十五分，在中山路一帶吃晚餐。' },
        { id: 'd3-home', t: '19:00', kind: 'mini', icon: 'home', title: '回飯店，早點休息', nb: '回飯店休息',
          say: '晚上七點回飯店，早點休息。' }
      ]
    },
    {
      id: 'd4', d: 19, wk: '六', color: '#C26A12', title: '環島路・嶼見閩南',
      say: '第四天，十二月十九號，星期六。早上沿著環島路看海，參觀胡里山砲台。中午在雙子塔吃海景午餐。下午去嶼見閩南看表演。隔天要早起坐船，晚上早點回飯店收行李。',
      items: [
        { id: 'd4-bf', t: '07:30', kind: 'mini', icon: 'food', title: '早餐', nb: '早餐',
          say: '早上七點半吃早餐。' },
        { id: 'd4-road', t: '09:00', kind: 'stop', icon: 'car', title: '環島路看海', nb: '環島路', img: 'huandao',
          pts: ['坐車沿著海邊走'],
          say: '早上九點，坐車沿著環島路看海。' },
        { id: 'd4-huli', t: '10:00', kind: 'stop', icon: 'camera', title: '胡里山砲台', nb: '胡里山砲台', img: 'hulishan',
          pts: ['清朝的大砲，旁邊就是海', '有坡和樓梯，累了在入口看就好'],
          say: '十點到胡里山砲台，看清朝留下來的大砲，旁邊就是海。裡面有坡和樓梯，累了在入口附近看看就好。' },
        { id: 'd4-lunch', t: '11:30', kind: 'stop', icon: 'food', title: '海景午餐', sub: '一席・雙子塔 5 樓', nb: '海景午餐', img: 'shimao',
          pts: ['窗外是海和演武大橋'],
          say: '十一點半，到世茂雙子塔五樓的一席吃午餐，窗外是海和演武大橋。' },
        { id: 'd4-car', t: '13:00', kind: 'move', mode: 'car', text: '叫車 約 30 分鐘', nb: '前往嶼見閩南' },
        { id: 'd4-show', t: '13:30', kind: 'stop', icon: 'show', title: '嶼見閩南 看表演', nb: '嶼見閩南', img: 'puppet',
          pts: ['都在室內，有冷氣，坐著看', '表演都付過了', '換衣服、做手工、買吃的才另外付錢'],
          say: '下午一點半進嶼見閩南，全部在室內，有冷氣。裡面有大型表演、提線木偶、飛天表演，還有坐著看的鼓浪風雲。表演全部都已經付過錢了，只有換衣服、做手工、買吃的才要另外付錢。需要的話，有免費輪椅可以借。' },
        { id: 'd4-dinner', t: '17:00', kind: 'mini', icon: 'food', title: '館內小吃街吃晚餐', nb: '晚餐',
          say: '傍晚五點，在館內的小吃街吃晚餐。' },
        { id: 'd4-home', t: '18:00', kind: 'stop', icon: 'bag', title: '回飯店・收行李', nb: '回飯店收行李', img: 'souvenir',
          pts: ['附近買最後的伴手禮', '肉乾、香腸不能帶回台灣'],
          say: '晚上六點叫車回飯店，在附近買最後的伴手禮，然後收行李。記得肉乾、香腸這些肉做的東西不能帶回台灣。' }
      ]
    },
    {
      id: 'd5', d: 20, wk: '日', color: '#7B4FA8', title: '回台灣',
      say: '最後一天，十二月二十號，星期日。早上坐船回金門，在金門逛一逛、吃午餐、買貢糖。傍晚五點四十分坐飛機回台北松山。',
      items: [
        { id: 'd5-bf', t: '07:30', kind: 'mini', icon: 'food', title: '早餐，吃快一點', nb: '早餐',
          say: '早上七點半吃早餐，今天要吃快一點。' },
        { id: 'd5-out', t: '08:00', kind: 'move', mode: 'car', text: '退房，叫車到五通碼頭', nb: '前往五通碼頭' },
        { id: 'd5-wt', t: '08:45', kind: 'stop', icon: 'ticket', title: '五通碼頭 報到', nb: '五通碼頭', img: 'wutong',
          pts: ['辦報到、出境'],
          say: '八點四十五分到五通碼頭，辦報到和出境。' },
        { id: 'd5-ship', t: '09:30', kind: 'stop', icon: 'ship', title: '坐船回金門', nb: '坐船回金門', img: 'ferry', tbd: true,
          pts: ['船程約 30 分鐘'],
          say: '九點半坐船回金門，大約三十分鐘。船班時間還在確認，以領隊通知為準。' },
        { id: 'd5-st', t: '10:00', kind: 'mini', icon: 'ticket', title: '水頭碼頭 入境', nb: '水頭碼頭',
          say: '十點到金門水頭碼頭，辦入境。' },
        { id: 'd5-tour', t: '10:30', kind: 'stop', icon: 'car', title: '包車逛金門', nb: '逛金門', img: 'kinmen',
          pts: ['行李放車上就好'],
          say: '十點半，包計程車逛金門，行李放在車上就好。' },
        { id: 'd5-lunch', t: '12:00', kind: 'stop', icon: 'food', title: '金城吃午餐・買貢糖', nb: '金城午餐', img: 'kinmen-old',
          pts: ['金門貢糖是伴手禮'],
          say: '中午在金城吃午餐，然後買金門貢糖當伴手禮。' },
        { id: 'd5-air', t: '15:45', kind: 'mini', icon: 'ticket', title: '金門機場報到', nb: '機場報到',
          say: '下午三點四十五分到金門機場報到。' },
        { id: 'd5-fly', t: '17:40', kind: 'stop', icon: 'plane', title: '飛回台北松山', nb: '飛回松山', img: 'plane',
          pts: ['17:40 起飛'],
          say: '傍晚五點四十分，坐飛機回台北松山機場。旅途愉快，辛苦了！' }
      ]
    }
  ],

  eats: [
    { name: '楊鑫麗・廈門菜小海鮮', what: '夫妻小店，現點現炒', price: 100, addr: '升平路 48-101 號' },
    { name: '醉壹號海鮮大排檔', what: '海鮮池自己挑', price: 95, addr: '思明北路 第四市場 1-3 號' },
    { name: '鷺江賓館・觀海餐廳', what: '港式點心，看海', price: 115, addr: '鷺江道 54 號' },
    { name: '桃喜老廈門私廚', what: '薑母鴨、香煎蟹', price: 81, addr: '中山路一帶' },
    { name: '吳紅英海鮮砂鍋粥', what: '熱熱的海鮮粥', price: 86, addr: '中山路一帶' }
  ]
};
