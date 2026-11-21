"""產生廈門旅遊手冊（B6，12.8 × 18.2 公分，可彩色印刷、騎馬釘裝訂）。

用法（在 repo 根目錄）：
    python3 book/make_book.py
會產生：
    book/book.html                          版面原始檔
    book/xiamen-travel-book-b6-print.pdf    給印刷店（四邊各多 3mm 出血）
    book/xiamen-travel-book-b6.pdf          看電子檔、自己印用（已裁切尺寸）
行程時間、地址、美食從 assets/data.js 讀；景點介紹寫在下面的 SPOT。
照片在 book/img/（來源記在 book/credits.json），使用者自己提供的照片沿用 img/ 裡的檔案。
"""
import html, json, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, 'book')
OUT_HTML = os.path.join(BOOK, 'book.html')
OUT_PRINT = os.path.join(BOOK, 'xiamen-travel-book-b6-print.pdf')
OUT_VIEW = os.path.join(BOOK, 'xiamen-travel-book-b6.pdf')


def load_trip():
    js = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.TRIP))"
    return json.loads(subprocess.check_output(['node', '-e', js, os.path.join(ROOT, 'assets', 'data.js')]))


T = load_trip()
P = T['places']
DAYS = {d['id']: d for d in T['days']}
CREDITS = {c['key']: c for c in json.load(open(os.path.join(BOOK, 'credits.json')))}
USER_PHOTOS = {'hotel': '飯店', 'caier': '採耳', 'massage': '泰印象 SPA', 'yujian': '嶼見閩南'}
used = []
e = html.escape

PREP = '#3E8FB8'      # 行前準備
EAT = '#E0503A'
BUY = '#B5651D'
CAR = '#1D3557'


# ---------------------------------------------------------------- 小工具
def icon(code, cls=''):
    return '<img class="%s" src="icons/%s.svg" alt="">' % (cls, code)


def src(key):
    if os.path.exists(os.path.join(BOOK, 'img', key + '.jpg')):
        if key not in used:
            used.append(key)
        return 'img/%s.jpg' % key
    if key in USER_PHOTOS:
        return '../img/%s.webp' % key
    raise SystemExit('找不到照片：' + key)


# 直的照片放進橫的框時，要看哪一部分（object-position）
FOCUS = {'u-trail6': '50% 30%', 'u-dmg': '50% 45%', 'u-cabin': '50% 62%', 'u-shuitou': '50% 30%', 'u-jc1': '50% 42%', 'u-yj1': '50% 55%', 'u-kmair1': '50% 30%',
         'u-xiagu1': '50% 18%', 'u-zhcity': '50% 30%', 'u-npt1': '50% 40%', 'u-bashi1': '50% 72%',
         'u-zs2': '50% 35%', 'u-gly2': '50% 40%', 'u-xcx2': '50% 45%', 'u-spw2': '50% 60%', 'u-xiagu2': '50% 55%'}


def pol(key, cap='', size='sm', extra=''):
    c = '<figcaption>%s</figcaption>' % e(cap) if cap else ''
    st = ' style="object-position:%s"' % FOCUS[key] if key in FOCUS else ''
    return '<figure class="pol %s %s"><img src="%s" alt=""%s>%s</figure>' % (size, extra, src(key), st, c)


def row(*items):
    return '<div class="row">%s</div>' % ''.join(items)


def fitrow(*items, lo=False):
    return '<div class="row fit%s">%s</div>' % (' lo' if lo else '', ''.join(items))


def head(title, kick=None):
    k = '<div class="kick">%s</div>' % kick if kick else ''
    return k + '<h1 class="hd"><span>%s</span></h1>' % e(title)


def ul(pts):
    return '<ul class="ul">%s</ul>' % ''.join('<li>%s</li>' % p for p in pts)


def book_tag(b):
    if not b:
        return ''
    return '<span class="book">%s</span>' % e(b if isinstance(b, str) else '怡君代訂')


def addr(key, label='地址（給司機看）'):
    pl = P[key]
    lang = 'zh-Hant' if pl.get('tw') else 'zh-Hans'
    return ('<div class="addr"><div class="addr-k">%s</div><div class="addr-n" lang="zh-Hans">%s</div>'
            '<div class="addr-a" lang="%s">%s</div></div>') % (label, e(pl['sc']), lang, e(pl['addr']))


def daykick(did, t=None):
    d = DAYS[did]
    s = '第 %d 天・%d/%d（%s）' % (int(did[1:]), T['month'], d['d'], d['wk'])
    return s + ('・' + t if t else '')


pages = []   # (body, cls, color, tab)
toc = []     # (名稱, 頁碼, 小字)


def page(body, cls='', color=None, tab=None, mark=None, sub=''):
    pages.append((body, cls, color, tab))
    if mark:
        toc.append((mark, len(pages), sub))


# ---------------------------------------------------------------- 景點內容
# photos：第一張是大照片；pts：重點；story／tip：小故事、小知識；place：地址
SPOT = {
    'plane': dict(day='d1', t='11:10', title='坐飛機到金門', layout='one',
                  photos=[('plane', '國內線飛機'), ('tsa', '台北松山機場'), ('kmair', '金門機場')],
                  pts=['11:10 從台北松山機場起飛（華信 AE2065）', '起飛前 1 小時先到機場報到', '12:30 抵達金門機場', '坐計程車約 10 分鐘去吃鍋貼']),
    'gt': dict(day='d1', t='12:45', title='午餐：佑昇生億鍋貼', layout='one',
               photos=[('u-guotie', '招牌蛋液鍋貼')],
               pts=['從機場坐計程車約 10 分鐘', '一定要點招牌<b>蛋液鍋貼</b>：外皮酥脆、內餡多汁', '炒滷味也很多人點', '<b>入口不明顯</b>，像一般民宅、沒有大招牌：看到鐵門直接推門進去', '吃完叫車到水頭碼頭，約 20 分鐘'],
               place='guotie'),
    'ship': dict(day='d1', t='15:30', title='小三通：坐船到廈門', layout='two',
                 photos=[('u-ship', '金廈小三通的船'), ('u-cabin', '船艙裡，坐約 30 分鐘'), ('u-kinmen', '金門水頭港一帶'), ('wutong', '廈門五通碼頭'), ('wutong2', '五通碼頭入境出口')],
                 pts=['金門水頭碼頭 → 廈門五通碼頭', '15:30 開船，船名「和平新星」', '坐船大約 30 分鐘，天氣好看得到廈門的高樓', '入境後坐車約 40 分鐘到飯店'],
                 story='2001 年 1 月 2 日，金門的客輪「太武號」和「浯江號」載著大約 180 位金門鄉親開到廈門，這是兩岸隔了五十多年後，第一次有客船直接往來。以前要去大陸，得先繞到香港。到現在，坐小三通往來金廈的旅客已經超過兩千四百萬人次。',
                 place='wutong'),
    'zs': dict(day='d1', t='18:00', title='中山路步行街', layout='two',
               photos=[('zs', '中山路夜景'), ('u-zs2', '晚上的招牌很熱鬧'), ('zs2', '中山路的牌樓'), ('zs3', '騎樓老房子'), ('u-zs1', '白天的中山路')],
               pts=['飯店就在旁邊，走路就到', '整條街都是行人徒步區', '兩邊是騎樓老房子，小吃、伴手禮店很多', '看到想吃的就進去吃晚餐'],
               story='中山路大約在 1925 年開始興建，全長約 1.2 公里，從海邊的輪渡碼頭一路往東。兩旁的騎樓，多半是 1920 年代從南洋回鄉的華僑蓋的，樓上住人、樓下開店，下雨天也淋不到雨，跟台灣的老街很像。現在被評為「中國歷史文化名街」。',
               place='zsroad'),
    'peanut': dict(day='d2', t='07:30', title='早餐：黃則和花生湯', layout='one', place='peanut',
                   photos=[('peanut', '黃則和花生湯老店')],
                   pts=['中山路上的老店，從 1945 年開到現在', '花生湯是甜湯，花生煮到入口即化', '也可以吃廈門人早餐常吃的麵線糊']),
    'bashi': dict(day='d2', t='08:30', title='八市逛早市', layout='two', place='bashi',
                  photos=[('u-bashi2', '八市的海鮮攤'), ('u-bashi1', '八市的街口')],
                  pts=['從飯店走路約 10 分鐘', '早上海鮮剛送到，最熱鬧', '可以看活海鮮、看在地人買菜', '買芒果乾當伴手禮，想吃什麼就買一點'],
                  story='聽老一輩的廈門人說，八市大約在 1920、30 年代就形成了。因為離輪渡碼頭近，漁船一靠岸，海鮮就直接送來賣，一直是廈門最新鮮的海鮮集散地。八市其實是兩個市場合起來的：裡面的營平市場和外面的開禾市場。'),
    'zwy': dict(day='d2', t='10:15', title='廈門園林植物園', layout='two', book='門票怡君代訂',
                photos=[('zwy', '多肉植物區的仙人掌'), ('zwy2', '雨林世界'), ('zwy3', '南洋杉草坪'), ('zwy4', '園裡的湖'), ('zwy5', '半山觀景台看廈門市區')],
                pts=['從八市坐車約 15 分鐘，從<b>西門</b>進去', '坐園內的觀光車逛，走累了就在站牌等車', '必看：多肉植物區、雨林世界、南洋杉草坪', '12:30 叫車回中山路吃午餐'],
                tip='雨林世界會定時噴出霧氣，像走進雲霧森林。冬天大約上午 9 到 11 點、下午 2 到 4 點噴霧，我們 10 點多到，先去雨林世界剛好看得到。',
                place='zwy'),
    'lunch2': dict(day='d2', t='12:45', title='中山路附近吃午餐', photo='zs4',
                   pts=['看到想吃的就進去，不用訂位', '推薦：沙茶麵、麵線糊、海蠣煎', '吃完回飯店午休']),
    'ear': dict(day='d2', t='15:45', title='悅享採耳', photo='u-ear', place='ear',
                pts=['從飯店走路約 5 分鐘', '請師傅清耳朵，躺著約 1 小時', '不想做的人可以在附近逛逛']),
    'xcx': dict(day='d2', t='17:00', title='小埕戲・海景晚餐', layout='two',
                photos=[('u-xcx1', '小埕戲的海景座位'), ('u-xcx2', '小埕戲入口'), ('heping', '和平碼頭'), ('dusk', '從碼頭看鼓浪嶼的黃昏'), ('dusk2', '鼓浪嶼的夜景')],
                pts=['和平碼頭大樓 4 樓，在廈門這一邊，<b>不用坐船</b>', '靠窗正對鼓浪嶼，看夕陽和夜景', '招牌菜：紅蟳米糕、薑母鴨'],
                story='這個碼頭很有故事：2001 年第一班小三通的船，就是從金門開到這個和平碼頭靠岸。我們第一天坐的小三通，就是從那一天開始的。',
                place='xcx'),
    'sm': dict(day='d4', t='10:00', title='SM 城市廣場', layout='one',
               photos=[('sm', 'SM 城市廣場'), ('sm2', '地下一樓的超市')],
               pts=['坐車約 20 分鐘，室內有冷氣，逛累了隨時坐', '地下一樓超市：逛零食、茶葉、醬料，買伴手禮', '11:30 在五樓的餐廳或美食廣場吃午餐'],
               place='sm'),
    'spa': dict(day='d4', t='14:00', title='泰印象主題 SPA', layout='one', place='foot',
                photos=[('massage', '泰印象 SPA 的包廂')],
                pts=['跟飯店同一條路，在 2 樓', '足療＋全身按摩，約 80 分鐘', '太大力就說「輕一點」']),
    'trail': dict(day='d3', t='15:10', title='山海步道・看夕陽', layout='one',
                  photos=[('sh2', '步道上的夕陽')],
                  pts=['14:40 叫車到<b>梅海花台</b>（6-1 號口），約 25 分鐘', '全程約 4 公里，幾乎一路<b>下坡</b>，約 2 個半小時', '17:25 左右在盼歸塔看日落', '山上風大帶外套；天快黑時打開手機手電筒', '走累了：在萬石滄海旁的三官道院叫車'],
                  place='trail'),
    'zcc': dict(day='d3', t='18:00', title='曾厝垵：逛小巷、吃晚餐', layout='two',
                photos=[('zcc', '曾厝垵的牌坊'), ('zcc2', '晚上的小吃街'), ('zcc3', '巷子裡的小吃攤'), ('zcc4', '旁邊就是海灘'), ('zcc5', '村子裡的老廟')],
                pts=['從天泉步道廣場走過來約 10 分鐘', '巷子裡都是小吃、甜品、茶飲和小店', '晚餐不用訂位，看到想吃的就進去', '推薦吃：<b>現炒海鮮、海蠣煎、沙茶麵</b>，飯後來碗花生湯或燒仙草', '19:30 左右叫車回飯店'],
                story='「厝」是房子、「垵」是海邊的小村，以前這裡住的大多姓曾，是有八百多年歷史的漁村，明朝時商船出海前會在這裡停靠檢查。2000 年環島路開通後，老房子慢慢變成民宿、小吃和小店，現在被叫做「最文藝的漁村」。',
                place='zcc'),
    'spw': dict(day='d3', t='09:45', title='沙坡尾', layout='two',
                photos=[('u-spw3', '老漁港和彩色房子'), ('u-spw1', '彩繪小店，後面就是雙子塔'), ('u-spw2', '沙坡尾的街角'), ('spw2', '港邊的漁船'), ('spw3', '避風塢')],
                pts=['以前的老漁港，漁船還停在港邊', '彩色老房子、咖啡店、文創小店', '散步看風景，看到喜歡的咖啡店就坐坐'],
                story='這一帶以前叫「玉沙坡」，是廈門最早的漁港。1920 年代廈門沿著海邊築堤蓋馬路，原本的小漁港被填掉，漁船就搬到沙坡尾，蓋了新的避風塢，颱風天可以躲進來。後來漁業慢慢沒落，老工廠、老倉庫改成藝術區和咖啡店。',
                place='spw'),
    'lunch4': dict(day='d3', t='11:30', title='沙坡尾找午餐', layout='one',
                   photos=[('u-spw4', '水邊步道，兩邊都是小吃和小店'), ('shacha', '沙茶麵'), ('u-oyster', '海蠣煎')],
                   pts=['不用訂位，看到想吃的就進去', '推薦吃：<b>沙茶麵、海蠣煎、魚丸湯、麵線糊</b>', '吃不下就少點一點，大家分著吃']),
    'pack': dict(day='d4', t='15:30', title='收行李・最後一晚', layout='one',
                 photos=[('u-zs2', '最後一晚的中山路')],
                 pts=['15:30 回飯店收行李，<b>大袋子</b>拿出來裝伴手禮', '17:30 在中山路吃最後一頓晚餐', '伴手禮還沒買齊，晚上在中山路補買', '肉做的東西不能帶回台灣（看第 {ban} 頁）']),
    'back': dict(day='d5', t='13:30', title='坐船回金門', layout='one',
                 photos=[('u-cabin', '回金門的船艙'), ('u-shuitou', '水頭碼頭的「抵港」入口')],
                 pts=['11:30 退房，坐車約 40 分鐘到五通碼頭', '12:30 報到（開船前 1 小時）', '13:30 開船，船名「迅安」', '坐約 30 分鐘回到水頭碼頭'],
                 place='wutong'),
    'mofan': dict(day='d5', t='14:30', title='金城模範街', layout='two',
                  photos=[('u-jc1', '掛滿紅燈籠的模範街'), ('mofan', '紅磚拱廊'), ('u-jc2', '金城的廟宇牌樓')],
                  pts=['從水頭碼頭坐計程車約 15 分鐘', '買貢糖、吃點小吃', '整條街是紅磚拱廊的老店屋', '15:30 叫車到機場，約 15 分鐘'],
                  story='模範街 1924 年開始興建、1925 年完成，由當時的商會會長傅錫琪發起。他希望這條街成為以後建設的「模範」，所以叫模範街。',
                  tip='金門貢糖是用花生和麥芽糖做的，口感酥鬆。其實貢糖最早來自廈門，後來在金門發揚光大；1959 年在全國商品展得到最優等，從此成為金門最有名的伴手禮。',
                  place='mofan'),
    'home': dict(day='d5', t='17:40', title='飛回台北松山', layout='one',
                 photos=[('u-kmair1', '金門航空站'), ('u-kmair2', '機場的候機室'), ('tsa', '回到台北松山機場')],
                 pts=['15:45 到金門機場報到', '17:40 起飛（華信 AE2074）', '18:50 回到台北松山機場', '旅途愉快，辛苦了！']),
}


def spot_one(key):
    s = SPOT[key]
    d = DAYS[s['day']]
    ph = s['photos']
    body = head(s['title'], daykick(s['day'], s.get('t')))
    card = '<div class="card tape"><div class="meta"><span class="label">%s</span>%s</div>%s</div>' % (
        e(s['t']), book_tag(s.get('book')), ul(s['pts']))
    if len(ph) == 2:
        body += row(pol(ph[0][0], ph[0][1], 'mid', 'rot1'), pol(ph[1][0], ph[1][1], 'mid', 'rot2')).replace('class="row"', 'class="row fit"')
        body += card
    else:
        body += pol(ph[0][0], ph[0][1], 'big', 'rot1 fit') + card
        if len(ph) > 1:
            body += row(*[pol(k, c, 'xs', 'rot%d' % (i % 3 + 1)) for i, (k, c) in enumerate(ph[1:])])
    if s.get('place'):
        body += addr(s['place'])
    page(body, 'spot', d['color'], int(s['day'][1:]))


def spot_two(key):
    s = SPOT[key]
    d = DAYS[s['day']]
    ph = s['photos']
    body = head(s['title'], daykick(s['day'], s.get('t')))
    body += pol(ph[0][0], ph[0][1], 'big', 'rot1 fit')
    body += '<div class="card tape"><div class="meta"><span class="label">%s</span>%s</div>%s</div>' % (
        e(s['t']), book_tag(s.get('book')), ul(s['pts']))
    page(body, 'spot', d['color'], int(s['day'][1:]))
    # 第二頁：小故事、更多照片、地址
    body = '<div class="kick">%s</div>' % daykick(s['day'])
    body += '<h1 class="hd" style="font-size:17pt"><span>%s</span></h1>' % e(s['title'])
    more = ph[1:]
    if more:
        if len(more) >= 4:
            body += row(pol(more[0][0], more[0][1], 'xs', 'rot2'), pol(more[1][0], more[1][1], 'xs', 'rot1'))
            more = more[2:]
        elif len(more) == 3:
            body += fitrow(*[pol(k, c, 'xs', 'rot%d' % (i % 3 + 1)) for i, (k, c) in enumerate(more)])
            more = []
    if s.get('story'):
        body += '<div class="card tape pink story"><span class="label">小故事</span><p>%s</p></div>' % e(s['story'])
    if s.get('tip'):
        body += '<div class="card tape blue r story"><span class="label navy">小知識</span><p>%s</p></div>' % e(s['tip'])
    if more:
        body += fitrow(*[pol(k, c, 'sm', 'rot%d' % (i % 3 + 2)) for i, (k, c) in enumerate(more)], lo=True)
    if s.get('place'):
        body += addr(s['place'])
    page(body, 'spot', d['color'], int(s['day'][1:]))


def sc_card(key):
    s = SPOT[key]
    if s.get('photo'):
        ph = '<img class="ph" src="%s" alt="">' % src(s['photo'])
    else:
        ph = '<div class="emo">%s</div>' % icon(s['emo'])
    a = ''
    if s.get('place'):
        pl = P[s['place']]
        a = '<div class="sc-addr"><b>地址</b><span lang="zh-Hans">%s</span></div>' % e(pl['addr'])
    return ('<div class="card sc">%s<div><div class="meta"><span class="label">%s</span>%s</div>'
            '<div class="ct">%s</div>%s%s</div></div>') % (ph, e(s['t']), book_tag(s.get('book')), e(s['title']), ul(s['pts']), a)


def spot_pair(a, b):
    s = SPOT[a]
    d = DAYS[s['day']]
    page(head('景點介紹', daykick(s['day'])) + sc_card(a) + sc_card(b), 'spot', d['color'], int(s['day'][1:]))


def trail_steps():
    """山海步道：一站一站怎麼走"""
    d = DAYS['d3']
    body = '<div class="kick">%s</div>' % daykick('d3')
    body += '<h1 class="hd" style="font-size:17pt"><span>山海步道怎麼走</span></h1>'
    body += steps([
        ('15:10 梅海花台下車', '看到「6-1」柱子就是步道入口', 'u-trail6'),
        ('往下走到萬石滄海', '約 1.6 公里，下坡為主，約 45 分鐘', 'u-mhht'),
        ('萬石滄海：螺旋觀景梯', '往下看上李水庫和山景', 'u-trailspiral'),
        ('走到盼歸塔', '中間有一小段上坡，慢慢走', 'sh3'),
        ('17:00 盼歸塔看夕陽', '360 度看海，17:25 左右日落', 'sh1'),
        ('下坡到天泉步道廣場', '約 20 分鐘，從 7 號口出來就是海邊', 'sh4'),
    ])
    body += '<p class="note" style="text-align:center;margin-top:2mm">出 7 號口後，沿環島路走 10 分鐘到曾厝垵吃晚餐。</p>'
    page(body, 'spot', d['color'], 3)


def spot(key):
    {'one': spot_one, 'two': spot_two}[SPOT[key]['layout']](key)


# ---------------------------------------------------------------- 封面（Fluent Emoji 貼紙＋照片拼貼）
def stk(name, x, y, w, rot=0):
    """貼紙；x、y 是離裁切線左上角幾公釐"""
    return ('<img class="stk" src="stickers/%s.svg" alt="" style="left:calc(var(--b) + %.1fmm);top:calc(var(--b) + %.1fmm);'
            'width:%.1fmm;transform:rotate(%ddeg)">') % (name, x, y, w, rot)


def cpol(key, x, y, w, h, rot, cap=''):
    st = ';object-position:%s' % FOCUS[key] if key in FOCUS else ''
    c = '<figcaption>%s</figcaption>' % e(cap) if cap else ''
    return ('<figure class="cpol" style="left:calc(var(--b) + %.1fmm);top:calc(var(--b) + %.1fmm);width:%.1fmm;transform:rotate(%ddeg)">'
            '<img src="%s" alt="" style="height:%.1fmm%s">%s</figure>') % (x, y, w, rot, src(key), h, st, c)


def cover():
    return ''.join([
        '<div class="cv-sea"></div>',
        cpol('gly', 5, 95, 44, 34, -8, '鼓浪嶼'),
        cpol('u-jc1', 80, 97, 43, 34, 7, '金門'),
        cpol('u-spw1', 41, 90, 46, 36, 2, '沙坡尾'),
        '<div class="cv-label"><div class="cv-k">2026 冬天・五天四夜</div><h1>廈門</h1><div class="cv-sub"><span>旅遊手冊</span></div>'
        '<div class="cv-date">12/16（三）— 12/20（日）</div><div class="cv-where">金門・廈門・鼓浪嶼</div></div>',
        stk('airplane', 3, 4, 21, -12), stk('sun-behind-small-cloud', 102, 3, 22, 0),
        stk('red-paper-lantern', 109, 30, 12, 6), stk('red-paper-lantern', 4, 33, 11, -6),
        stk('musical-keyboard', 2, 62, 17, -14), stk('teacup-without-handle', 110, 62, 14, 8),
        stk('lion', 104, 80, 17, -6), stk('sparkles', 14, 82, 10, 0),
        stk('steaming-bowl', 28, 133, 15, -8), stk('peanuts', 68, 135, 12, 12),
        stk('ferry', 6, 145, 27, 0), stk('crab', 52, 152, 15, -10), stk('tropical-fish', 76, 160, 12, 8),
        stk('luggage', 99, 140, 22, 6),
    ])


# ---------------------------------------------------------------- 1 封面
page(cover(), 'cover')

# 2 聯絡
page(head('旅伴資料') +
     '<div class="card tape"><div class="ct">聯絡電話</div>'
     '<div class="fill"><span>同行</span></div><div class="fill"><span>同行</span></div>'
     '<div class="fill"><span>同行</span></div><div class="fill"><span>台灣家人</span></div></div>'
     '<div class="card tape pink r"><div class="ct">出發前知道一下</div>' + ul([
         '時間：跟台灣一樣，不用調手錶',
         '天氣：12 月白天約 15–20 度，早晚 10 多度',
         '電壓：220V，手機充電器可以直接用',
         '付錢：同行夥伴會先代付，身上帶一點人民幣',
         '在廈門：<b>護照收好</b>，<b>台胞證</b>帶在身上',
         '網路：連當地 Wi-Fi，LINE、YouTube、臉書<b>不能用</b>',
     ]) + '</div>', 'info', PREP)

# 3 目錄（最後再填）
page('{{TOC}}', 'info', PREP)

# 4 五天總覽
rows = ''
for did in ['d1', 'd2', 'd3', 'd4', 'd5']:
    d = DAYS[did]
    rows += ('<div style="display:grid;grid-template-columns:auto 1fr;align-items:center;gap:2.4mm;padding:1.3mm 0;border-bottom:.3mm dashed #CFE0E6">'
             '<span class="pill" style="background:%s;text-align:center">%d/%d（%s）</span><span class="hn" style="font-size:15pt;line-height:1.3">%s</span></div>') % (
        d['color'], T['month'], d['d'], d['wk'], e(d['title']))
page(head('五天總覽') + '<div class="card mapcard"><img class="mapimg" src="img/map-all.png" alt="" style="height:70mm;object-fit:cover"></div>'
     '<div class="card" style="padding:1.6mm 4mm">%s</div>' % rows, 'info', PREP, mark='五天總覽')

# 5 這樣玩最開心（出遊的心情，用「我們的約定」的口吻）
PROMISE = [
    ('1f60b', '沒吃過的，點來試試看', '好吃，多一個喜歡的味道；不合口味，也多一個回家可以說的故事。'),
    ('1f4f8', '多拍照', '風景、美食、大家的笑臉，都拍下來，回家再慢慢看。'),
    ('1f695', '走累了就叫車', '不用硬撐著走，腳顧好，後面幾天才玩得盡興。'),
    ('1f39f', '想進去看，就進去', '門票、車錢都排進預算了，難得來一趟，不用替大家省。'),
    ('1f30f', '「台灣也有」？不太一樣喔', '同樣是蚵仔煎、老街，在廈門吃、在廈門走，味道和心情都不同。'),
]
page(head('這樣玩最開心', '出發前，我們先說好') +
     '<div class="card tape promise">%s</div>' % ''.join(
         '<div class="pm">%s<div><b>%s</b><p>%s</p></div></div>' % (icon(c), e(t), e(d)) for c, t, d in PROMISE) +
     '<div class="pm-end"><span>不用去想值不值這個價錢——</span><b>是我們，值得好好玩這一趟。</b></div>',
     'info', PREP)

# 6–9 行李清單
def chk(items):
    return '<ul class="chk">%s</ul>' % ''.join(
        '<li><i class="box"></i>%s<div><b>%s</b>%s</div></li>' % (icon(c), e(t), ('<span>%s</span>' % e(n)) if n else '') for c, t, n in items)


def chk2(items, blanks=0):
    """兩欄的小清單：(圖示, 名稱, 小字)"""
    li = ''.join('<li><i class="box"></i>%s<div><b>%s</b>%s</div></li>' % (icon(c), e(t), ('<span>%s</span>' % e(n)) if n else '')
                 for c, t, n in items)
    li += '<li class="blank"><i class="box"></i><div class="fill"></div></li>' * blanks
    return '<ul class="chk2">%s</ul>' % li


page(head('行李清單', '1・證件和電子用品') + '<div class="card tape">' + chk([
    ('1faaa', '身分證', '坐國內線飛機要用'),
    ('1f4d7', '護照', '金門出入境用；到廈門後收好'),
    ('1f4b3', '台胞證', '到廈門後每天帶著，景點、坐船都會用到'),
    ('1f45b', '一點人民幣和新台幣', '大部分由同行夥伴先代付'),
    ('1f4f1', '手機、充電線、充電頭', '兩腳扁插頭在廈門可以直接插'),
    ('1f50b', '行動電源', '放手提，不能託運'),
    ('1f453', '眼鏡、老花眼鏡', ''),
    ('1f4d4', '這本旅遊手冊', ''),
]) + '</div><div class="warn">%s證件效期要夠，出發前看一下</div>' % icon('26a0'), 'info', PREP, 0, mark='行李清單')

LAYER = [('1f455', '裡面', '長袖上衣<br>或發熱衣'), ('1f9f6', '中間', '薄毛衣<br>或刷毛衣'), ('1f9e5', '外面', '防風<br>保暖外套')]
page(head('衣服怎麼帶？', '2・衣服') +
     '<div class="card tape pink"><div class="ct" style="font-size:15pt">12 月的廈門</div>' + ul([
         '白天 15～20 度，早晚 10 多度',
         '跟台北冬天差不多，海邊風大會更冷',
     ]) + '<div class="layers">%s</div><p class="kind-n">一層一層穿，熱了脫一件、冷了加一件。</p></div>' % ''.join(
         '<div class="layer">%s<b>%s</b><span>%s</span></div>' % (icon(c), k, t) for c, k, t in LAYER) +
     '<div class="card tape blue r"><div class="ct" style="font-size:15pt">外套帶一厚一薄</div>' + ul([
         '<b>厚的</b>：防風、保暖，穿在身上',
         '<b>薄的</b>：刷毛或薄外套，放行李，白天熱可以換',
     ]) + '</div>'
     '<div class="warn">%s厚外套和鞋子穿在身上，行李就輕很多</div>' % icon('1f4a1'),
     'info', PREP, 0)

page(head('行李清單', '2・衣服（5 天）') + '<div class="card tape pink">' + chk2([
    ('1f9e5', '厚外套 ×1', '穿在身上'),
    ('1f9e5', '薄外套 ×1', '刷毛或薄外套'),
    ('1f9f6', '薄毛衣 ×1', ''),
    ('1f455', '長袖上衣 ×3', '可以輪流穿'),
    ('1f525', '發熱衣 ×2', '怕冷的人'),
    ('1f456', '長褲 ×2', ''),
    ('1fa72', '內衣褲 ×5', ''),
    ('1f9e6', '襪子 ×5', ''),
    ('1f6cf', '睡衣 ×1', ''),
    ('1f9e3', '圍巾、毛帽', '海邊風大'),
    ('1f9e4', '手套', '怕冷的人'),
    ('1f45f', '好走的鞋子', '穿在身上'),
    ('1fa74', '室內拖鞋', '飯店不一定有'),
], blanks=1) + '</div>', 'info', PREP, 0)

page(head('行李清單', '3・洗臉、保養、日用品') + '<div class="card tape">' + chk2([
    ('1faa5', '牙刷、牙膏', '飯店不一定提供'),
    ('1f9fc', '洗面乳', ''),
    ('1f9f4', '保養品、乳液', '小瓶的放手提'),
    ('1f484', '護唇膏', '冬天嘴唇乾'),
    ('1f9f4', '護手霜', ''),
    ('2600', '防曬乳', ''),
    ('1fa92', '刮鬍刀', '刀片的放託運'),
    ('1fa86', '梳子', ''),
    ('1f380', '髮夾、髮圈', ''),
    ('1f484', '化妝品', ''),
    ('2702', '指甲剪', '放託運'),
    ('1f9fb', '面紙、濕紙巾', '廁所常沒有紙'),
], blanks=2) + '</div><p class="note" style="text-align:center;margin-top:2mm">大陸的飯店通常不主動提供牙刷、梳子這些拋棄式用品，自己帶最方便。</p>',
     'info', PREP, 0)

page(head('行李清單', '4・藥和其他') + '<div class="card tape pink">' + chk2([
    ('1f48a', '平常吃的藥', '多帶兩天，放手提'),
    ('1f922', '暈船藥', '坐船約 30 分鐘'),
    ('1f321', '感冒藥', ''),
    ('1f48a', '腸胃藥', ''),
    ('1fa79', 'OK 繃', ''),
    ('1fa79', '痠痛貼布', ''),
    ('1f637', '口罩', ''),
    ('2602', '摺疊傘', '12 月雨不多'),
    ('1f6cd', '環保袋', ''),
    ('1f964', '保溫杯', '過安檢前倒空'),
    ('1f58a', '原子筆', '寫筆記、填資料'),
], blanks=1) + '</div>'
     '<div class="card tape blue r bigbag">%s<div><div class="ct" style="font-size:15pt">摺疊大行李袋</div>'
     '<p>去程摺好放在行李箱裡。回程拿出來裝伴手禮，自己提上船、上飛機。怎麼帶看第 {weight} 頁。</p></div></div>' % icon('1f45c'),
     'info', PREP, 0)

# 7 託運？手提？（給不常出國的人）
def flow(items):
    out = ''
    for i, (ic, t) in enumerate(items):
        if i:
            out += '<i class="fl-a">›</i>'
        out += '<div class="fl-s">%s<span>%s</span></div>' % (icon(ic), t)
    return '<div class="flow">%s</div>' % out


page(head('託運？手提？', '行李有兩種') +
     '<div class="card tape kind"><div class="rule-h">%s<div class="ct">託運行李<small>大的行李箱，交給櫃台</small></div></div>' % icon('1f9f3') +
     flow([('1f6c5', '報到時<br>交給櫃台'), ('1f3f7', '過秤、<br>貼行李條'), ('2708', '放進飛機<br>或船的貨艙'), ('1f6c4', '到了<br>再領回來')]) +
     '<p class="kind-n">路上<b>拿不到</b>，到了以後在「行李轉盤」或領行李的地方拿回來。</p></div>'
     '<div class="card tape pink r kind"><div class="rule-h">%s<div class="ct">手提行李<small>也叫「隨身行李」</small></div></div>' % icon('1f392') +
     flow([('1f6b6', '自己<br>帶著走'), ('1f50d', '先過<br>X 光檢查'), ('1f4ba', '放座位上方<br>或腳前面')]) +
     '<p class="kind-n">一路都在自己身邊，<b>隨時拿得到</b>。小包包、外套、雨傘不算件數。</p></div>'
     '<div class="warn">%s藥、證件、錢、手機，一定放手提</div>' % icon('26a0'),
     'info', PREP, 0, mark='託運？手提？')

# 能帶多重
WEIGHT_PAGE = len(pages) + 1
page(head('能帶多重？', '飛機和船的規定不一樣') +
     '<div class="card tape"><div class="rule-h">%s<div class="ct">飛機<small>台北松山 ⇄ 金門（國內線）</small></div></div>'
     '<div class="nums"><div class="num"><div class="k">手提</div><div class="v">7<small>公斤</small></div><div class="s">1 件・約 20 吋登機箱大小</div></div>'
     '<div class="num"><div class="k">免費託運</div><div class="v">10<small>公斤</small></div><div class="s">每人</div></div></div></div>' % icon('2708') +
     '<div class="card tape blue r"><div class="rule-h">%s<div class="ct">小三通船<small>金門水頭 ⇄ 廈門五通</small></div></div>'
     '<div class="nums"><div class="num"><div class="k">手提</div><div class="v">17<small>公斤</small></div><div class="s">最多 2 件，加起來</div></div>'
     '<div class="num hot"><div class="k">免費託運</div><div class="v">5<small>公斤</small></div><div class="s">超過就要付錢</div></div></div></div>' % icon('26f4') +
     '<p class="note" style="text-align:center;margin-top:2.4mm">2026 年 10 月的規定，以航空公司、船公司現場為準。</p>',
     'info', PREP, 0)

# 建議這樣帶（冬天衣服重，託運額度又低）
def plan(title, cls, rows):
    out = ''.join('<div class="pl-r">%s<div><b>%s</b><span>%s</span></div></div>' % (icon(c), t, d) for c, t, d in rows)
    return '<div class="card tape %s plan"><div class="ct" style="font-size:16pt">%s</div>%s</div>' % (cls, title, out)


page(head('行李怎麼帶最省？', '冬天衣服重，這樣帶不用多付錢') +
     plan('去程', '', [
         ('1f9f3', '一個行李箱', '裡面摺一個大行李袋，先不用'),
         ('2708', '飛機：行李箱託運', '10 公斤以內'),
         ('26f4', '船：行李箱自己拖上船', '手提 17 公斤以內，不用託運'),
     ]) +
     plan('回程', 'pink r', [
         ('1f45c', '大袋子拿出來', '伴手禮、多的衣服裝進去'),
         ('26f4', '船：行李箱＋大袋子都帶上船', '兩件加起來 17 公斤以內'),
         ('2708', '飛機：行李箱託運，大袋子手提', '託運 10 公斤＋手提 7 公斤'),
     ]) +
     '<div class="warn">%s菜刀、高粱酒放進要託運的行李箱</div>' % icon('26a0'),
     'info', PREP, 0, mark='行李怎麼帶最省？')

# 9 放哪裡
def tiles(items):
    return '<div class="tiles">%s</div>' % ''.join('<div class="tile">%s<span>%s</span></div>' % (icon(c), t) for c, t in items)


BAN_PAGE = len(pages) + 1
page(head('東西放哪裡？') +
     '<div class="card sort ok"><div class="sort-h">%s放手提（隨身包）</div>' % icon('2705') +
     tiles([('1faaa', '證件'), ('1f45b', '錢包'), ('1f4f1', '手機'), ('1f50b', '行動電源'), ('1f48a', '常吃的藥'), ('1f453', '眼鏡')]) +
     '<p class="sort-n">行動電源<b>不能託運</b>；飛機上不能用、不能充電，每人最多 2 個。</p></div>'
     '<div class="card sort ck"><div class="sort-h">%s放託運</div>' % icon('1f9f3') +
     tiles([('1f52a', '刀子<br>菜刀'), ('2702', '剪刀'), ('1f9f4', '大瓶乳液<br>洗髮精'), ('1f376', '高粱酒'), ('1fad9', '沙茶醬<br>瓶罐醬料')]) +
     '<p class="sort-n">刀剪<b>不能手提</b>。小瓶的乳液、藥水放手提沒關係。</p></div>'
     '<div class="card sort bad"><div class="sort-h">%s都不能帶</div>' % icon('274c') +
     tiles([('1f356', '肉乾肉鬆<br>香腸'), ('1f34e', '新鮮水果'), ('1f525', '瓦斯罐<br>噴漆')]) +
     '<p class="sort-n">肉做的食物去廈門、回台灣都不行，會被<b>重罰</b>。</p></div>',
     'info', PREP, 0, mark='東西放哪裡？')

# 10 打包和安檢小撇步
page(head('打包和安檢', '小撇步') +
     '<div class="card tape"><div class="rule-h">%s<div class="ct">打包的時候</div></div>' % icon('1f9f3') + ul([
         '行李箱掛名牌，寫名字和電話',
         '綁一條彩色帶子，領行李時好認',
         '瓶子蓋緊，裝進夾鏈袋',
         '藥多帶兩天份，放手提',
         '在家先秤，行李箱 10 公斤以內',
     ]) + '</div>'
     '<div class="card tape pink r"><div class="rule-h">%s<div class="ct">過安全檢查</div></div>' % icon('1f50d') + ul([
         '包包、外套放進籃子過 X 光',
         '口袋的手機、鑰匙、零錢先拿出來',
         '被叫住檢查不用緊張，照著做就好',
     ]) + '</div>'
     '<div class="card tape blue"><div class="rule-h">%s<div class="ct">領行李</div></div>' % icon('1f6c4') + ul([
         '行李條的收據收好，行李不見要用',
     ]) + '</div>', 'info', PREP, 0)

# 9–10 交通資訊（票卡）
def ticket(ic, kind, date, a, b, ta, tb, foot):
    return ('<div class="ticket"><div class="tk-s">%s<span>%s</span></div><div class="tk-b"><div class="tk-d">%s</div>'
            '<div class="tk-r"><div><b>%s</b></div><i>⟶</i><div><b>%s</b></div></div>'
            '<div class="tk-t"><span>%s</span><span></span><span>%s</span></div><div class="tk-f">%s</div></div></div>') % (
        icon(ic), kind, date, a, b, ta, tb, foot)


FILL = '<u></u>'
page(head('交通資訊・去程', '12/16（三）') +
     '<div class="warn">%s護照和台胞證拿在手上</div>' % icon('26a0') +
     ticket('2708', '飛機', '12/16（三）・國內線', '台北松山', '金門', '11:10 起飛', '12:30 到', '華信 <b>AE2065</b>・起飛前 1 小時報到') +
     ticket('26f4', '船', '12/16（三）・小三通', '金門水頭', '廈門五通', '15:30 開船', '約 16:00 到', '船名：和平新星') +
     '<div class="card tape" style="margin-top:4mm"><div class="ct" style="font-size:14pt">每一段要拿出來的證件</div>' + ul([
         '坐飛機：<b>身分證</b>',
         '金門出境：<b>護照</b>',
         '廈門入境：<b>台胞證</b>',
         '到了廈門：只拿台胞證，<b>護照收好</b>',
     ]) + '</div>',
     'info', PREP, 0, mark='交通資訊')

page(head('交通資訊・回程', '12/20（日）') +
     '<div class="warn">%s中午才坐船，11:30 前退房就好</div>' % icon('26a0') +
     ticket('26f4', '船', '12/20（日）・小三通', '廈門五通', '金門水頭', '13:30 開船', '約 14:00 到', '船名：迅安') +
     ticket('2708', '飛機', '12/20（日）・國內線', '金門', '台北松山', '17:40 起飛', '18:50 到', '華信 <b>AE2074</b>・15:45 報到') +
     '<div class="card tape pink" style="margin-top:4mm"><div class="ct" style="font-size:14pt">回程記得</div>' + ul([
         '廈門出境：<b>台胞證</b>；金門入境：<b>護照</b>',
         '肉做的東西不能帶回台灣',
         '飛機：行李箱託運，大袋子手提',
         '菜刀、高粱酒放進要託運的行李箱',
     ]) + '</div>', 'info', PREP, 0)

# 11–12 碼頭怎麼走
def steps(items):
    out = ''
    for i, (t, d, ph) in enumerate(items, 1):
        st = ' style="object-position:%s"' % FOCUS[ph] if ph in FOCUS else ''
        th = '<img class="th" src="%s" alt=""%s>' % (src(ph), st) if ph else '<span></span>'
        out += '<li><span class="n">%d</span><div><b>%s</b>%s</div>%s</li>' % (i, e(t), ('<span>%s</span>' % e(d)) if d else '', th)
    return '<ul class="steps">%s</ul>' % out


page(head('碼頭怎麼走・去程', '金門 → 廈門') + steps([
    ('坐計程車去吃午餐', '鍋貼店，約 10 分鐘', 'u-guotie'),
    ('14:30 水頭碼頭報到', '領船票，行李箱自己拖上船', 'u-kinmen'),
    ('出境：給海關看護照', '', None),
    ('15:30 上船，坐約 30 分鐘', '船名「和平新星」', 'u-ship'),
    ('五通碼頭入境：台胞證', '', 'wutong2'),
    ('領行李，坐車到飯店', '約 40 分鐘', 'wutong'),
]), 'info', PREP, 0, mark='碼頭怎麼走')

page(head('碼頭怎麼走・回程', '廈門 → 金門 → 台北') + steps([
    ('11:45 坐車到五通碼頭', '約 40 分鐘', 'wutong'),
    ('12:30 報到、領船票', '行李箱和大袋子自己帶上船', None),
    ('出境：給海關看台胞證', '', None),
    ('13:30 上船，坐約 30 分鐘', '船名「迅安」', 'u-cabin'),
    ('入境：給海關看護照', '從「抵港」入口進去', 'u-shuitou'),
    ('金城買貢糖，再到機場', '15:45 報到，17:40 起飛', 'u-kmair2'),
]), 'info', PREP, 0)

# 13 住宿
page(head('住宿資訊', '12/16 – 12/20・四晚') + pol('hotel', '壺香悅：紅白色的洋樓，門口是圓拱玻璃門', 'big', 'rot1 fit') +
     '<div class="card tape"><div class="ct">壺香悅<small>中山路步行街店</small></div>' + ul([
         '就在中山路步行街旁邊',
         '走路可到：中山路、八市、泰印象 SPA、悅享採耳',
     ]) + '</div>' + addr('hotel', '飯店地址（迷路時給人看）'), 'spot', PREP, 0, mark='住宿資訊')

# ---------------------------------------------------------------- 每一天
MOVE_ICON = {'car': '1f695', 'walk': '1f6b6', 'ship': '26f4', 'plane': '2708'}
MEAL = ('早餐', '午餐', '晚餐')
DAY_NOTE = {
    'd1': ['起飛前 1 小時到松山機場', '入境後<b>護照收好</b>，不要拿出來', '連飯店 Wi-Fi，LINE、YouTube、臉書不能用'],
    'd2': ['<b>台胞證</b>帶在身上，護照收好', '植物園門票怡君代訂', '植物園坐觀光車，不用走太多路'],
    'd3': ['傍晚山上風大，<b>帶件外套</b>', '步道只走下坡，走累了在涼亭坐一下', '曾厝垵人多、巷子窄，大家走在一起'],
    'd4': ['SM 商場的超市可以順便買伴手禮', '伴手禮：包裝寫「肉松」「肉」的不要買', '晚上收行李，<b>大袋子</b>拿出來裝伴手禮'],
    'd5': ['11:30 前退房，別忘了東西', '廈門出境用<b>台胞證</b>，到金門才拿護照', '肉做的東西不能帶回台灣'],
}
ORDER = {
    'd1': [('one', 'plane'), ('one', 'gt'), ('two', 'ship'), ('two', 'zs')],
    'd2': [('one', 'peanut'), ('two', 'bashi'), ('two', 'zwy'), ('pair', 'lunch2', 'ear'), ('two', 'xcx')],
    'd3': [('two', 'spw'), ('one', 'lunch4'), ('one', 'trail'), ('steps',), ('two', 'zcc')],
    'd4': [('one', 'sm'), ('one', 'spa'), ('one', 'pack')],
    'd5': [('one', 'back'), ('two', 'mofan'), ('one', 'home')],
}


def gly_pages():
    did = 'd3'
    c = DAYS[did]['color']
    body = head('鼓浪嶼', daykick(did, '09:45')) + pol('gly', '黃榮遠堂：島上有名的老洋房', 'big', 'rot1 fit')
    body += '<div class="card tape"><div class="meta"><span class="label">09:45</span></div>' + ul([
        '島上沒有汽車，到處是百年老洋房',
        '散步看建築、看海景，放慢腳步輕鬆逛',
        '12:00 午餐：龍頭路上的蛋滿灌',
        '13:00 坐船回廈門，回飯店休息',
    ]) + '</div>'
    page(body, 'spot', c, 3)
    body = '<div class="kick">%s</div><h1 class="hd" style="font-size:17pt"><span>鼓浪嶼散步看什麼</span></h1>' % daykick(did)
    body += fitrow(pol('church', '天主堂', 'sm', 'rot2'), pol('piano', '鋼琴博物館', 'sm', 'rot1'))
    body += fitrow(pol('glybeach', '海邊沙灘', 'sm', 'rot3'), pol('gly2', '老洋樓', 'sm', 'rot2'))
    body += fitrow(pol('u-gly2', '1935 年的老洋房', 'sm', 'rot1'), pol('sunrock', '日光岩', 'sm', 'rot3'))
    page(body, 'spot', c, 3)
    body = '<div class="kick">%s</div><h1 class="hd" style="font-size:17pt"><span>鼓浪嶼</span></h1>' % daykick(did)
    body += ('<div class="card tape pink story"><span class="label">小故事</span><p>島的西南邊海灘上，有一塊兩公尺多高、中間有洞的礁石，'
             '漲潮時海浪打進洞裡，聲音像打鼓一樣，叫做「鼓浪石」，島也在明朝時因此改名「鼓浪嶼」，在那之前叫「五龍嶼」。</p></div>')
    body += ('<div class="card tape blue r story"><span class="label navy">小知識</span><p>清朝末年，很多國家的領事館、商人和傳教士住進鼓浪嶼，'
             '蓋了洋樓、教堂和學校，有「萬國建築博覽」的稱號。島上鋼琴特別多，又叫「鋼琴之島」。2017 年被列為世界文化遺產。</p></div>')
    body += fitrow(pol('u-gly1', '鼓浪嶼碼頭', 'xs', 'rot2'), pol('sanqiu', '三丘田碼頭', 'xs', 'rot1'), lo=True)
    body += addr('gly')
    page(body, 'spot', c, 3)


for did in ['d1', 'd2', 'd3', 'd4', 'd5']:
    d = DAYS[did]
    n = int(did[1:])
    lis = ''
    for it in d['items']:
        if it['kind'] == 'move':
            lis += '<li class="mv"><span>%s%s</span></li>' % (icon(MOVE_ICON.get(it.get('mode'), '1f695')), e(it.get('text') or it.get('nb') or ''))
            continue
        t = it['title']
        meal = next((m for m in MEAL if m in t), None)
        bk = '<i class="bk">%s</i>' % ('怡君代預約' if '預約' in str(it['book']) else '怡君代訂') if it.get('book') else ''
        ml = '<i class="meal">%s</i>' % meal if meal and not t.startswith(meal) else ''
        lis += '<li class="st"><b>%s</b><span>%s%s%s</span></li>' % (e(it['t']), e(t), ml, bk)
    dense = ' dense' if lis.count('<li') > 12 else ''
    page(head('每日行程', '第 %d 天' % n) +
         '<div class="card%s"><div class="tl-top"><span class="pill">%d/%d（%s）</span><span class="tl-title">%s</span></div>'
         '<span class="dayrib">DAY %d</span><ul class="tl">%s</ul></div>' % (dense, T['month'], d['d'], d['wk'], e(d['title']), n, lis),
         'dayp', d['color'], n, mark='第 %d 天' % n, sub='%d/%d %s' % (T['month'], d['d'], d['title']))
    page(head('今天去哪裡', daykick(did)) +
         '<div class="card mapcard"><img class="mapimg" src="img/map-%s.png" alt=""><div class="lg"><span><i></i>坐車</span><span><i class="ship"></i>坐船</span><span><i class="walk"></i>走路</span></div></div>' % did +
         '<div class="card tape"><div class="ct" style="font-size:14pt">今天記得</div>%s</div>' % ul(DAY_NOTE[did]),
         'dayp', d['color'], n)
    for o in ORDER[did]:
        if o[0] == 'pair':
            spot_pair(o[1], o[2])
        elif o[0] == 'steps':
            trail_steps()
        elif o[0] == 'gly':
            gly_pages()
        else:
            spot(o[1])

# ---------------------------------------------------------------- 必吃美食
FOOD_IMG = {'f-shacha': 'shacha', 'f-oyster': 'u-oyster', 'f-duck': 'duck', 'f-peanut': 'peanut', 'f-mianxian': 'mianxian',
            'f-zongzi': 'zongzi', 'f-crab': 'u-crab', 'f-congee': 'u-congee', 'f-seafood': 'shellfish', 'f-tusun': 'tusun'}
FOOD_EMO = {'f-crab': '1f980', 'f-congee': '1f372'}
foods = T['foods']
for i in range(0, len(foods), 2):
    cards = ''
    for f in foods[i:i + 2]:
        k = FOOD_IMG.get(f['id'])
        ph = '<img class="ph" src="%s" alt="">' % src(k) if k else '<div class="emo">%s</div>' % icon(FOOD_EMO[f['id']])
        at = f.get('at')
        at = P[at] if isinstance(at, str) else at
        where = '<div class="where">想吃可以去：<b>%s</b></div>' % e(at['n']) if at else ''
        cards += '<div class="card fd tape%s">%s<div><div class="ct">%s</div><div class="what">%s</div>%s%s</div></div>' % (
            ' r' if i % 4 else '', ph, e(f['name']), e(f['what']), ul([e(p) for p in f['pts']]), where)
    page(head('必吃美食', '沒吃過的，點一份大家分著吃') + cards, 'food', EAT, '吃', mark='必吃美食' if i == 0 else None)

# ---------------------------------------------------------------- 伴手禮
def gifts(items):
    out = ''
    for name, note, ph, emo, *bad in items:
        inner = '<img class="p" src="%s" alt="">' % src(ph) if ph else icon(emo, 'e')
        cls = ' bad' if bad else ''
        out += '<div class="gift%s"><div class="cir">%s</div><b>%s</b><span>%s</span></div>' % (cls, inner, e(name), e(note))
    return '<div class="gifts">%s</div>' % out


page(head('必買伴手禮', '廈門') + '<div class="card tape">' + gifts([
    ('南普陀素餅', '全素，可以安心帶', 'u-subing', None),
    ('沙茶醬', '成分有肉的不要買；放託運', 'u-shacha', None),
    ('鐵觀音', '福建有名的烏龍茶', 'tea', None),
    ('芒果乾', '八市、中山路都買得到', None, '1f96d'),
    ('青津果', '鼓浪嶼的蜜餞橄欖', None, '1fad2'),
    ('不能帶回台灣', '肉鬆口味的餅、肉乾、香腸', None, '1f356', True),
]) + '</div><div class="warn">%s包裝寫「肉松」「肉」的不要買</div>' % icon('26a0'), 'food', BUY, '買', mark='必買伴手禮')

page(head('必買伴手禮', '金門') + '<div class="card tape pink">' + gifts([
    ('貢糖', '花生做的，酥酥的', 'u-gongtang', None),
    ('菜刀', '砲彈鋼做的，要託運', 'knife', None),
    ('高粱酒', '放託運行李', 'liquor', None),
    ('風獅爺小物', '金門的守護神', 'lion', None),
    ('一條根', '金門的藥草，做成貼布', None, '1f33f'),
    ('麵線', '金門手工麵線', None, '1f35c'),
]) + '</div><div class="warn">%s菜刀不能手提，記得託運</div>' % icon('26a0'), 'food', BUY, '買')

# ---------------------------------------------------------------- 說法對照
WORDS = [('計程車', '出租車・打車'), ('捷運', '地鐵'), ('廁所', '衛生間'), ('塑膠袋', '塑料袋'), ('鳳梨', '菠蘿')]
page(head('台灣說法・廈門說法') + '<div class="card tape"><table class="words">%s</table></div>' % ''.join(
    '<tr><td>%s</td><td>→</td><td>%s</td></tr>' % (e(a), e(b)) for a, b in WORDS) +
     '<div class="card tape pink r"><div class="ct" style="font-size:14pt">幾句好用的話</div><ul class="say">%s</ul></div>' % ''.join(
         '<li><b>%s</b><span lang="zh-Hans">%s</span></li>' % (e(a), e(b)) for a, b in [
             ('廁所在哪裡？', '请问卫生间在哪里？'), ('不要辣', '不要辣，谢谢'), ('請送我到這裡', '请送我到这里')]) +
     '<p class="note" style="text-align:center;margin-top:1.6mm">廈門人也講閩南話，跟台語很像，可以說說看！</p>', 'info', PREP, mark='台灣說法・廈門說法')

# ---------------------------------------------------------------- 給司機看
DRIVER = ['hotel', 'zwy', 'xcx', 'spw', 'trail', 'zcc', 'sm', 'wutong']


def drv(key):
    pl = P[key]
    cut = pl['sc'].find('（')
    name = e(pl['sc'][:cut]) + '<small>%s</small>' % e(pl['sc'][cut:]) if cut > 0 else e(pl['sc'])
    return ('<div class="card drv"><div class="tw">%s</div><div lang="zh-Hans"><p class="p">请送我到这里，谢谢</p>'
            '<p class="n">%s</p><p class="a">%s</p></div></div>') % (e(pl['n']), name, e(pl['addr']))


for i in range(0, len(DRIVER), 2):
    page(head('給司機看', '要坐車時，把這頁給司機看') + drv(DRIVER[i]) + drv(DRIVER[i + 1]),
         'driver', CAR, '車', mark='給司機看' if i == 0 else None)

# ---------------------------------------------------------------- 花費紀錄
page(head('花費紀錄') + '<table class="cost"><tr><th style="width:22mm">日期</th><th>買了什麼</th><th style="width:26mm">多少錢</th></tr>%s</table>'
     % ('<tr><td></td><td></td><td></td></tr>' * 13), 'info', PREP, mark='花費紀錄')


# ---------------------------------------------------------------- 照片來源
def clean_author(a):
    a = (a or '').split('\n')[0].strip()
    if a.startswith('http'):
        a = a.split('/')[2].replace('www.', '')
    return a.replace('User:', '')[:40] or '佚名'


def credits_page():
    groups = {}
    for k in used:
        if k.startswith('u-'):
            continue
        c = CREDITS[k]
        groups.setdefault((clean_author(c['author']), c['lic']), []).append(c['what'])
    lines = ['<p><b>%s</b>（%s）：%s</p>' % (e(a), e(l), e('、'.join(dict.fromkeys(w)))) for (a, l), w in groups.items()]
    return (head('照片來源') + '<div class="card"><div class="cred">'
            '<p>金門機場、水頭碼頭、小三通的船、飯店、中山路、八市、採耳、小埕戲、泰印象 SPA、沙坡尾、山海步道入口、金城模範街、金門鍋貼、海蠣煎、紅蟳米糕、海鮮砂鍋粥、貢糖、沙茶醬、南普陀素餅的照片為自行提供。其他照片來自 Wikimedia Commons：</p>%s'
            '<p>地圖海岸線：© OpenStreetMap 貢獻者（ODbL）。貼紙和圖示：Microsoft Fluent Emoji（MIT）。字型：jf open 粉圓（SIL OFL）、思源黑體（SIL OFL）。</p>'
            '<p>完整來源：github.com/kuoyichun/GOGOXiamen 的 book/credits.json</p></div></div>') % ''.join(lines)


CRED_INDEX = len(pages)
page('', 'info', PREP)

# 補筆記頁到 4 的倍數（最後一頁是封底）
first_memo = None
while (len(pages) + 1) % 4 or first_memo is None or len(pages) - first_memo < 1:
    leaf = icon('1f343', 'leaf')
    page(head('Memo') + '<div class="memo">%s</div>' % leaf.replace('class="leaf"', 'class="leaf" style="right:3mm;bottom:3mm"'),
         'info', PREP)
    if first_memo is None:
        first_memo = len(pages)

hp = P['hotel']
page('<div class="cv-sea"></div>' + stk('luggage', 6, 8, 20, -8) + stk('airplane', 98, 10, 22, 10) + stk('hibiscus', 104, 118, 14, 0)
     + stk('sparkles', 10, 118, 11, 0) + stk('ferry', 50, 150, 26, 0) + '<!--IN--><div class="bk-card"><div class="bk-k">迷路的時候，請把這頁給人看</div><div class="drv" lang="zh-Hans" style="flex:none">'
     '<p class="p" style="margin-top:3mm">请送我到这里，谢谢</p><p class="n">壶香悦<small>（厦门中山路步行街店）</small></p>'
     '<p class="a">%s</p></div></div>' % e(hp['addr']), 'back')

# 照片來源要等所有頁面都用過照片才能寫
pages[CRED_INDEX] = (credits_page(), 'info', PREP, None)

# 目錄
toc_html = '<ul>%s</ul>' % ''.join('<li><b>%02d</b><span>%s%s</span></li>' % (n, e(name), ('<small>%s</small>' % e(sub)) if sub else '')
                                   for name, n, sub in toc)
pages[2] = (head('目錄') + '<div class="toc">%s</div>' % toc_html, 'info', PREP, None)
pages[:] = [(b.replace('{ban}', str(BAN_PAGE)).replace('{weight}', str(WEIGHT_PAGE + 1)), c, col, t) for b, c, col, t in pages]

# ---------------------------------------------------------------- 輸出
TAB_K = {0: 0, '吃': 6, '買': 7, '車': 8}


def tab_html(tab):
    k = TAB_K.get(tab, tab)
    label = {0: '<b>行</b>前', '吃': '<b>吃</b>', '買': '<b>買</b>', '車': '<b>車</b>'}.get(tab, '<b>%s</b>天' % tab)
    return '<div class="tab" style="top:calc(var(--b) + %.1fmm)">%s</div>' % (10 + k * 17, label)


out = []
for i, (body, cls, color, tab) in enumerate(pages, 1):
    side = 'odd' if i % 2 else 'even'
    style = (' style="--c:%s"' % color) if color else ''
    tabh = tab_html(tab) if tab is not None else ''
    num = '' if cls in ('cover', 'back') else '<div class="no">%d</div>' % i
    if cls == 'cover':
        inner = body
    elif '<!--IN-->' in body:
        a, b = body.split('<!--IN-->')
        inner = a + '<div class="in">%s</div>' % b
    else:
        inner = '<div class="in">%s<!--TRIVIA--></div>' % body
    out.append('<section class="pg %s %s"%s>%s%s%s</section>' % (cls, side, style, inner, tabh, num))


def write_doc():
    doc = ('<!DOCTYPE html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><title>廈門旅遊手冊</title>'
           '<link rel="stylesheet" href="book.css"><style id="sz"></style></head><body>%s</body></html>') % '\n'.join(out)
    open(OUT_HTML, 'w').write(doc)


# ---------------------------------------------------------------- 冷知識：塞進有空位的頁面底下，不增加頁數
TRIVIA = [
    ('「金門」這個名字，來自明朝 1387 年築城守海防，取「固若金湯，雄鎮海門」的意思。以前這裡叫「浯洲」。',
     ['坐飛機到金門', '午餐：佑昇生億鍋貼', '金城模範街']),
    ('金門的縣鳥是戴勝，頭上的羽毛像一把小扇子，常在古厝的牆縫裡做窩。',
     ['金城模範街', '飛回台北松山', '午餐：佑昇生億鍋貼', '坐船回金門']),
    ('2018 年起，金門有一部分自來水是從福建用海底水管送過來的。金門和廈門，連水都連在一起。',
     ['小三通：坐船到廈門', '午餐：佑昇生億鍋貼', '坐船回金門', '碼頭怎麼走・去程']),
    ('廈門以前有很多白鷺鷥，所以又叫「鷺島」，白鷺也是廈門的市鳥。在海邊看到白色的鳥，就是牠。',
     ['中山路步行街', '住宿資訊', '五天總覽']),
    ('「沙茶」其實就是南洋烤肉串「沙嗲」的閩南話念法，是早年下南洋的人帶回來的味道。',
     ['img/u-shacha.jpg', 'img/shacha.jpg']),
    ('海蠣煎用台語念，就是「蚵仔煎」。廈門跟台灣寫法不一樣，念起來一模一樣。',
     ['>海蠣煎</div>', 'img/u-oyster.jpg']),
    ('金門菜刀是用以前打到金門的砲彈鋼打成的。從砲彈變成菜刀，是金門最特別的伴手禮。',
     ['砲彈鋼', '刀子<br>菜刀']),
]
SKIP = ('cover', 'back', 'driver')
NEED = 66   # 一則冷知識大約要的高度（px）


def measure():
    js = r'''
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[1], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  const r = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((s, i) => {
    const el = s.querySelector('.in'); if (!el) return null;
    const kids = [...el.children]; if (!kids.length) return null;
    const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
    const h = s.querySelector('.hd span');
    // 會自動放大的照片（.fit）可以縮回最小高度，讓出空間
    const give = [...el.querySelectorAll(':scope > .fit')].reduce((t, f) =>
      t + Math.max(0, f.getBoundingClientRect().height - parseFloat(getComputedStyle(f).minHeight || 0)), 0);
    return { i, free: Math.round(el.getBoundingClientRect().bottom - bottom + give),
             title: h ? h.textContent : '', memo: !!s.querySelector('.memo, .cost, .cred, .toc') };
  }).filter(Boolean));
  console.log(JSON.stringify(r)); await b.close();
})();
'''
    return json.loads(subprocess.check_output(['node', '-e', js, OUT_HTML]))


write_doc()
info = [x for x in measure() if not x['memo'] and pages[x['i']][1] not in SKIP]
taken = set()
for text, prefer in TRIVIA:
    # prefer：頁面標題，或頁面內容裡會出現的字
    ok = [x for x in info if x['free'] >= NEED and x['i'] not in taken]
    cand = [x for t in prefer for x in ok if x['title'] == t] + [x for t in prefer for x in ok if t in out[x['i']]]
    if not cand:
        cand = sorted([x for x in info if x['free'] >= NEED and x['i'] not in taken], key=lambda x: -x['free'])
    if not cand:
        print('冷知識放不下：', text[:12])
        continue
    k = cand[0]['i']
    taken.add(k)
    out[k] = out[k].replace('<!--TRIVIA-->', '<div class="trivia"><span>冷知識</span>%s</div>' % e(text))
    print('冷知識 → 第 %d 頁（%s）' % (k + 1, cand[0]['title']))
write_doc()
print('pages:', len(pages), ' photos used:', len(used))

# 用 Chromium 印成 PDF（出血版、裁切版），並檢查有沒有內容擠出頁面
js = r"""
const { chromium } = require('playwright');
(async () => {
  const [html, printPdf, viewPdf] = process.argv.slice(1);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + html, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(600);
  const over = await p.evaluate(() => [...document.querySelectorAll('.pg')].map((s, i) => {
    const el = s.querySelector('.in'); if (!el) return null;
    const kids = [...el.children]; const bottom = Math.max(...kids.map(k => k.getBoundingClientRect().bottom));
    const lim = el.getBoundingClientRect().bottom;
    const toc = s.querySelector('.toc');
    if (toc && toc.scrollHeight > toc.clientHeight + 1) return (i + 1) + ':toc';
    return bottom > lim + 1 ? (i + 1) + ':' + Math.round(bottom - lim) + 'px' : null;
  }).filter(Boolean));
  console.log('overflow pages:', over.join(' ') || 'none');
  for (const [pdf, bleed] of [[printPdf, 3], [viewPdf, 0]]) {
    await p.evaluate((bl) => {
      document.documentElement.style.setProperty('--b', bl + 'mm');
      document.getElementById('sz').textContent = '@page{size:' + (128 + 2 * bl) + 'mm ' + (182 + 2 * bl) + 'mm;margin:0}';
    }, bleed);
    await p.waitForTimeout(300);
    await p.pdf({ path: pdf, preferCSSPageSize: true, printBackground: true });
  }
  await b.close();
})();
"""
subprocess.run(['node', '-e', js, OUT_HTML, OUT_PRINT, OUT_VIEW], check=True)
print('pdf:', OUT_PRINT)
print('pdf:', OUT_VIEW)
