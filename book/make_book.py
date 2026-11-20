"""產生廈門旅行手札（B6，12.8 × 18.2 公分，可彩色印刷、騎馬釘裝訂）。

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
FOCUS = {'u-xiagu1': '50% 18%', 'u-zhcity': '50% 30%', 'u-npt1': '50% 40%', 'u-bashi1': '50% 72%',
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
    return '<span class="book">%s</span>' % e(b if isinstance(b, str) else '要事先訂')


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
    'plane': dict(day='d1', t='12:30', title='坐飛機到金門', layout='one',
                  photos=[('plane', '國內線飛機'), ('tsa', '台北松山機場'), ('kmair', '金門機場')],
                  pts=['從台北松山機場出發', '12:30 抵達金門機場', '出機場坐計程車到水頭碼頭，約 20 分鐘']),
    'ship': dict(day='d1', t='14:00', title='小三通：坐船到廈門', layout='two',
                 photos=[('ferry', '金廈小三通的船'), ('ferry2', '金門水頭港'), ('wutong', '廈門五通碼頭'), ('wutong2', '五通碼頭入境出口')],
                 pts=['金門水頭碼頭 → 廈門五通碼頭', '坐船大約 30 分鐘', '天氣好時，船上就看得到廈門的高樓', '入境後坐車約 40 分鐘到飯店'],
                 story='2001 年 1 月 2 日，金門的客輪「太武號」和「浯江號」載著大約 180 位金門鄉親開到廈門，這是兩岸隔了五十多年後，第一次有客船直接往來。以前要去大陸，得先繞到香港。到現在，坐小三通往來金廈的旅客已經超過兩千四百萬人次。',
                 place='wutong'),
    'zs': dict(day='d1', t='17:00', title='中山路步行街', layout='two',
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
    'npt': dict(day='d2', t='10:15', title='南普陀寺', layout='two', book=True,
                photos=[('u-npt1', '南普陀寺和五老峰'), ('u-npt2', '南普陀寺山門'), ('npt2', '放生池和寶塔'), ('npt4', '山上的「佛」字石刻'), ('npt', '放生池邊看寺廟')],
                pts=['從八市坐車約 15 分鐘', '千年閩南古寺，可以進去拜拜', '依山而建，往上走可以看到五老峰', '參觀要事先預約'],
                story='南普陀寺始建於唐末五代，最早叫「泗洲院」，宋朝改稱「無盡岩」，明朝又叫「普照寺」。清朝康熙年間重修，加蓋了供奉觀音菩薩的大悲殿。浙江的普陀山是有名的觀音道場，這座寺在它的南邊，所以叫「南普陀」。',
                place='npt'),
    'veg': dict(day='d2', t='11:30', title='南普陀素菜館', emo='1f962', place='nptveg', book=True,
                pts=['就在寺裡，是很有名的素菜館', '菜名很雅緻，像「半月沉江」「南海金蓮」']),
    'ear': dict(day='d2', t='15:45', title='悅享採耳', photo='u-ear', place='ear', book=True,
                pts=['從飯店走路約 5 分鐘', '請師傅清耳朵，躺著約 1 小時', '不想做的人可以在附近逛逛']),
    'xcx': dict(day='d2', t='17:00', title='小埕戲・海景晚餐', layout='two', book=True,
                photos=[('u-xcx1', '小埕戲的海景座位'), ('u-xcx2', '小埕戲入口'), ('heping', '和平碼頭'), ('dusk', '從碼頭看鼓浪嶼的黃昏'), ('dusk2', '鼓浪嶼的夜景')],
                pts=['和平碼頭 4 樓，閩南古厝裝潢', '靠窗正對鼓浪嶼，看夕陽和夜景', '招牌菜：紅蟳米糕、薑母鴨'],
                story='這個碼頭很有故事：2001 年第一班小三通的船，就是從金門開到這個和平碼頭靠岸。我們第一天坐的小三通，就是從那一天開始的。',
                place='xcx'),
    'pier': dict(day='d3', t='08:15', title='廈鼓碼頭：坐船去鼓浪嶼', layout='one', book='船票要事先訂',
                 photos=[('u-xiagu1', '郵輪中心裡的「廈鼓輪渡」入口'), ('u-xiagu2', '候船大廳'), ('glyship', '去鼓浪嶼的船')],
                 pts=['碼頭在國際郵輪中心裡面，找「廈鼓輪渡」', '每個人用自己的台胞證換上船憑證', '坐船約 15 分鐘，在三丘田碼頭上岸'],
                 place='xiagu'),
    'spa': dict(day='d3', t='15:00', title='泰印象主題 SPA', photo='massage', place='foot', book=True,
                pts=['跟飯店同一條路，在 2 樓', '足療＋全身按摩，約 80 分鐘', '包廂裡可以看電影']),
    'tea': dict(day='d3', t='16:40', title='不只有茶', photo='glyview', place='tea', book=True,
                pts=['海景茶館，大窗正對鼓浪嶼', '喝功夫茶、看夕陽', '12 月大約五點半天黑']),
    'zhcity': dict(day='d3', t='17:45', title='中華城逛逛・吃晚餐', layout='one',
                   photos=[('u-zhcity', '中華城'), ('zhcity', '中華城一角')],
                   pts=['從茶館走過來約 10 分鐘，回飯店也近', '閩南風格的街區，有小吃和文創小店', '看到想吃的就進去吃晚餐'],
                   place='zhcity'),
    'spw': dict(day='d4', t='09:45', title='沙坡尾', layout='two',
                photos=[('u-spw1', '彩繪小店，後面就是雙子塔'), ('u-spw2', '沙坡尾的街角'), ('spw', '掛著燈籠的老街'), ('spw2', '港邊的漁船'), ('spw3', '避風塢')],
                pts=['以前的老漁港，漁船還停在港邊', '彩色老房子、咖啡店、文創小店', '散步看風景，看到喜歡的咖啡店就坐坐'],
                story='這一帶以前叫「玉沙坡」，是廈門最早的漁港。1920 年代廈門沿著海邊築堤蓋馬路，原本的小漁港被填掉，漁船就搬到沙坡尾，蓋了新的避風塢，颱風天可以躲進來。後來漁業慢慢沒落，老工廠、老倉庫改成藝術區和咖啡店。',
                place='spw'),
    'yixi': dict(day='d4', t='11:30', title='雙子塔・一席海景午餐', layout='two', book=True,
                 photos=[('shimao', '世茂雙子塔'), ('shimao2', '雙子塔和海邊'), ('shimao3', '從雙子塔往下看'), ('yanwu', '演武大橋夜景'), ('yanwu2', '演武大橋日落')],
                 pts=['從沙坡尾走路約 5 分鐘', '在 5 樓的一席吃海景午餐', '窗外就是海和演武大橋'],
                 tip='世茂海峽大廈是兩棟像船帆的高樓，大約 300 公尺高，2015 年完工，大家都叫它「雙子塔」，是廈門很醒目的地標。',
                 place='yixi'),
    'yj': dict(day='d4', t='13:30', title='嶼見閩南・看表演', layout='two', book='門票要事先訂',
               photos=[('yujian', '嶼見閩南')],
               pts=['坐車約 30 分鐘，在海上世界 4–5 樓', '全部在室內，有冷氣', '像走進一座閩南古城，表演一場接一場', '晚餐在館內的小吃街吃'],
               story='2025 年 5 月才開幕。裡面分成宋朝、海上絲路、市井煙火、南洋四個時空，每天有將近 30 場表演：大型實景演出《千年回響》、提線木偶、飛天表演，還有《鼓浪風雲》大戲。',
               tip='表演全部都已經付過了，只有換古裝、做手工、買吃的才要另外付錢。提線木偶是泉州的傳統戲，一尊木偶有十幾條到三十幾條線，全靠師傅的手指操控。',
               place='yujian'),
    'pack': dict(day='d4', t='18:00', title='回飯店・收行李', layout='one',
                 photos=[('zs4', '中山路的小吃和伴手禮')],
                 pts=['在中山路買最後的伴手禮', '隔天要早起坐船，晚上先把行李收好', '肉做的東西不能帶回台灣（看第 {ban} 頁）']),
    'back': dict(day='d5', t='08:45', title='坐船回金門', layout='one',
                 photos=[('wutong', '五通碼頭'), ('ferry2', '回到金門水頭港')],
                 pts=['退房後坐車約 40 分鐘到五通碼頭', '坐船約 30 分鐘回到水頭碼頭', '船班時間以領隊通知為準'],
                 place='wutong'),
    'km': dict(day='d5', t='10:30', title='包計程車逛金門', layout='two',
               photos=[('juguang', '莒光樓'), ('settle', '水頭聚落'), ('deyue', '水頭的得月樓'), ('lion', '風獅爺'), ('lion2', '村口的風獅爺')],
               pts=['在水頭碼頭坐上包車，行李放車上', '司機帶路，看金門的地標和老房子', '像是莒光樓、水頭聚落、風獅爺'],
               story='在金門的村子口，常看到石頭雕的獅子，叫「風獅爺」。以前金門風沙很大，村民立風獅爺來擋風、保平安，現在成了金門的代表。地標莒光樓 1952 年建成，是金門最有名的建築之一。'),
    'mofan': dict(day='d5', t='12:00', title='金城模範街', layout='two',
                  photos=[('mofan', '模範街'), ('mofan2', '紅磚拱廊'), ('mofan3', '金城老街')],
                  pts=['中午在金城吃午餐、買貢糖', '整條街是紅磚拱廊的老店屋'],
                  story='模範街 1924 年開始興建、1925 年完成，由當時的商會會長傅錫琪發起。他希望這條街成為以後建設的「模範」，所以叫模範街。',
                  tip='金門貢糖是用花生和麥芽糖做的，口感酥鬆。其實貢糖最早來自廈門，後來在金門發揚光大；1959 年在全國商品展得到最優等，從此成為金門最有名的伴手禮。',
                  place='mofan'),
    'home': dict(day='d5', t='17:40', title='飛回台北松山', layout='one',
                 photos=[('kmair2', '金門機場'), ('tsa', '回到台北松山機場')],
                 pts=['15:45 到金門機場報到', '17:40 起飛，回到台北松山機場', '旅途愉快，辛苦了！']),
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


def spot(key):
    {'one': spot_one, 'two': spot_two}[SPOT[key]['layout']](key)


# ---------------------------------------------------------------- 封面
def waves(y, amp, n, color, h=188):
    w = 134.0 / n
    d = 'M0,%.1f ' % y
    for i in range(n):
        x0 = i * w
        d += 'Q%.1f,%.1f %.1f,%.1f Q%.1f,%.1f %.1f,%.1f ' % (x0 + w / 4, y - amp, x0 + w / 2, y, x0 + 3 * w / 4, y + amp, x0 + w, y)
    d += 'L134,%d L0,%d Z' % (h, h)
    return '<path d="%s" fill="%s"/>' % (d, color)


def egret(x, y, s=1.0):
    return ('<g transform="translate(%.1f %.1f) scale(%.2f)" stroke="#1D3557" stroke-width=".45" stroke-linejoin="round">'
            '<path d="M14,8 C18,-4 28,-6 34,1 C27,2 23,5 21,9 Z" fill="#fff"/>'
            '<path d="M2,8 C8,6 20,7 27,9 C22,12.5 11,12.5 5,11 Z" fill="#fff"/>'
            '<path d="M18,9 C24,4 32,4 37,7 C31,8 26,10 22,12 Z" fill="#F4FAFB"/>'
            '<path d="M5,9.5 C2,8.5 1,6.5 2,5 C3,4 4.6,4.4 4.6,5.6" fill="none"/>'
            '<path d="M2.2,5 L-1.8,6 L2.2,5.9 Z" fill="#FFD45C" stroke-width=".3"/>'
            '<path d="M27,10 L34,12.6 M26.4,10.6 L33,13.6" stroke-width=".5" fill="none"/></g>') % (x, y, s)


COVER_ART = ''.join([
    '<svg class="cv-art" viewBox="0 0 134 188" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">',
    '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#A9DCDD"/><stop offset="1" stop-color="#E6F5EF"/></linearGradient></defs>',
    '<rect width="134" height="188" fill="url(#sky)"/>',
    '<circle cx="104" cy="36" r="19" fill="#FFD45C" opacity=".28"/><circle cx="104" cy="36" r="13" fill="#FFD45C"/>',
    '<g fill="#fff" opacity=".85"><rect x="60" y="20" width="32" height="4" rx="2"/><rect x="74" y="27" width="46" height="4" rx="2"/>',
    '<rect x="96" y="60" width="30" height="3.4" rx="1.7"/><rect x="58" y="88" width="24" height="3.4" rx="1.7"/></g>',
    # 鼓浪嶼和日光岩
    '<path d="M18,124 C28,110 40,106 50,108 C58,98 70,94 80,97 C86,90 98,86 108,92 C118,94 127,101 134,105 L134,134 L18,134 Z" fill="#7DC29A"/>',
    '<path d="M74,99 C73,89 79,82 86,83 C93,84 95,91 94,99 Z" fill="#E2CFA6" stroke="#B89B6A" stroke-width=".5"/>',
    '<path d="M81,83.2 L86,79.6 L91,83.2 Z" fill="#C8553D"/><rect x="83" y="83" width="6" height="2.4" fill="#F6E7C8"/>',
    '<path d="M0,128 C14,119 30,117 44,121 C49,122.5 53,126 56,131 L56,140 L0,140 Z" fill="#9ED3A8"/>',
    # 閩南紅磚厝（燕尾脊）
    '<rect x="96" y="100" width="25" height="14" fill="#D2563E"/>',
    '<path d="M93,100.4 L124,100.4 L121,96.6 Q108.5,94.6 96,96.6 Z" fill="#9E3A2C"/>',
    '<path d="M92.2,93.4 Q94.6,96.4 97.6,96 Q108.5,94.4 119.4,96 Q122.4,96.4 124.8,93.4" fill="none" stroke="#9E3A2C" stroke-width="1.3" stroke-linecap="round"/>',
    '<rect x="98.6" y="103.4" width="4" height="4" fill="#F6D8A8"/><rect x="114.4" y="103.4" width="4" height="4" fill="#F6D8A8"/>',
    '<path d="M106,114 L106,107.6 Q108.5,105 111,107.6 L111,114 Z" fill="#7A2E22"/>',
    # 海
    waves(126, 2.2, 7, '#8ACDDA'),
    waves(140, 2.4, 6, '#62B5CD'),
    waves(155, 2.6, 5, '#4299C0'),
    waves(171, 2.8, 5, '#2F7FAA'),
    '<g stroke="#fff" stroke-width=".7" fill="none" stroke-linecap="round" opacity=".75">',
    '<path d="M70,134 q3,-2 6,0"/><path d="M100,147 q3,-2 6,0"/><path d="M14,150 q3,-2 6,0"/><path d="M58,163 q3,-2 6,0"/><path d="M110,166 q3,-2 6,0"/></g>',
    # 小三通的船
    '<g transform="translate(14 120)"><path d="M0,10 L30,10 L27,15 L3,15 Z" fill="#fff" stroke="#1D3557" stroke-width=".45"/>',
    '<rect x="2" y="11.6" width="26" height="1.2" fill="#3E8FB8"/>',
    '<path d="M6,10 L7,5 L22,5 L24,10 Z" fill="#fff" stroke="#1D3557" stroke-width=".45"/>',
    '<g fill="#3E8FB8"><circle cx="10" cy="7.4" r=".9"/><circle cx="13.5" cy="7.4" r=".9"/><circle cx="17" cy="7.4" r=".9"/><circle cx="20.5" cy="7.4" r=".9"/></g></g>',
    egret(58, 52, 1.0), egret(30, 92, .55),
    '</svg>'])


def back_art():
    return ''.join(['<svg class="cv-art" viewBox="0 0 134 188" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">',
                    waves(158, 2.2, 6, '#8ACDDA'), waves(168, 2.4, 5, '#62B5CD'), waves(178, 2.6, 5, '#4299C0'),
                    egret(18, 22, .7), '</svg>'])


# ---------------------------------------------------------------- 1 封面
page(COVER_ART + '<div class="cv-t"><div class="cv-year">2026</div><h1>廈門</h1><div class="cv-side">旅行手札</div></div>'
     '<div class="cv-d"><b>12/16（三）— 12/20（日）</b><span>金門・廈門・鼓浪嶼</span></div>', 'cover')

# 2 聯絡
page(head('旅伴資料') +
     '<div class="card tape"><div class="ct">聯絡電話</div>'
     '<div class="fill"><span>領隊</span></div><div class="fill"><span>同行</span></div>'
     '<div class="fill"><span>同行</span></div><div class="fill"><span>台灣家人</span></div></div>'
     '<div class="card tape pink r"><div class="ct">出發前知道一下</div>' + ul([
         '時間：跟台灣一樣，不用調手錶',
         '天氣：12 月白天約 15–20 度，早晚 10 多度',
         '電壓：220V，手機充電器可以直接用',
         '付錢：由領隊處理，身上帶一點人民幣',
     ]) + '</div>'
     '<div class="card"><div class="ct">四晚都住</div><div style="font-size:13pt;font-weight:700;margin-top:1mm">壺香悅（中山路步行街店）</div>'
     '<div lang="zh-Hans" style="font-size:11pt">厦门市思明区定安路61-2号</div></div>', 'info', PREP)

# 3 目錄（最後再填）
page('{{TOC}}', 'info', PREP)

# 4 五天總覽
rows = ''
for did in ['d1', 'd2', 'd3', 'd4', 'd5']:
    d = DAYS[did]
    rows += ('<div style="display:grid;grid-template-columns:22mm 1fr;align-items:center;gap:2.4mm;padding:1.3mm 0;border-bottom:.3mm dashed #CFE0E6">'
             '<span class="pill" style="background:%s;text-align:center">%d/%d（%s）</span><span class="hn" style="font-size:13.5pt;line-height:1.3">%s</span></div>') % (
        d['color'], T['month'], d['d'], d['wk'], e(d['title']))
page(head('五天總覽') + '<div class="card mapcard"><img class="mapimg" src="img/map-all.png" alt="" style="height:76mm;object-fit:cover"></div>'
     '<div class="card" style="padding:1.6mm 4mm">%s</div>' % rows, 'info', PREP, mark='五天總覽')

# 5–6 行李清單
def chk(items):
    return '<ul class="chk">%s</ul>' % ''.join(
        '<li><i class="box"></i>%s<div><b>%s</b>%s</div></li>' % (icon(c), e(t), ('<span>%s</span>' % e(n)) if n else '') for c, t, n in items)


page(head('行李清單', '證件・錢・手機') + '<div class="card tape">' + chk([
    ('1faaa', '身分證', '坐國內線飛機要用'),
    ('1f4d7', '護照', '在金門出境、回來入境要用'),
    ('1f4b3', '台胞證', '進廈門要用；坐船去鼓浪嶼也要用'),
    ('1f45b', '一點人民幣和新台幣', '大部分由領隊付'),
    ('1f4f1', '手機和充電線', ''),
    ('1f50b', '行動電源', '放隨身包，不能託運'),
    ('1f48a', '平常吃的藥', '放隨身包'),
    ('1f453', '眼鏡、老花眼鏡', ''),
]) + '</div><div class="warn">%s證件效期要夠，出發前看一下</div>' % icon('26a0'), 'info', PREP, 0, mark='行李清單')

page(head('行李清單', '衣服・日用品') + '<div class="card tape pink">' + chk([
    ('1f9e5', '防風外套', '海邊風大，早晚冷'),
    ('1f9e3', '圍巾或薄毛衣', '洋蔥式穿法最方便'),
    ('1f455', '換洗衣服（5 天）', ''),
    ('1f45f', '好走的鞋子', '每天都會走路逛街'),
    ('2602', '摺疊傘', '12 月雨不多，帶著安心'),
    ('1faa5', '牙刷、牙膏、保養品', '自己帶最習慣'),
    ('1f9fb', '面紙、濕紙巾', '外面廁所不一定有衛生紙'),
    ('1f6cd', '環保袋', '裝伴手禮'),
]) + '<ul class="chk"><li><i class="box"></i><span></span><div class="fill" style="height:8mm"></div></li>'
     '<li><i class="box"></i><span></span><div class="fill" style="height:8mm"></div></li></ul></div>', 'info', PREP, 0)

# 7 行李規定
page(head('託運和隨身行李', '飛機和船的規定不一樣') +
     '<div class="card tape"><div class="rule-h">%s<div class="ct">飛機<small>台北松山 ⇄ 金門（國內線）</small></div></div>'
     '<div class="nums"><div class="num"><div class="k">手提行李</div><div class="v">7<small>公斤</small></div><div class="s">1 件・56×36×23 公分以內</div></div>'
     '<div class="num"><div class="k">免費託運</div><div class="v">10<small>公斤</small></div><div class="s">經濟艙每人</div></div></div></div>' % icon('2708') +
     '<div class="card tape blue r"><div class="rule-h">%s<div class="ct">小三通船<small>金門水頭 ⇄ 廈門五通</small></div></div>'
     '<div class="nums"><div class="num"><div class="k">隨身行李</div><div class="v">17<small>公斤</small></div><div class="s">最多 2 件，合計</div></div>'
     '<div class="num hot"><div class="k">免費託運</div><div class="v">5<small>公斤</small></div><div class="s">超過就要付錢</div></div></div></div>' % icon('26f4') +
     '<div class="card"><div class="ct" style="font-size:14pt">建議這樣帶</div>' + ul([
         '一人一個 20 吋以內的登機箱（7 公斤以內）',
         '再加一個隨身小包，放證件、藥和行動電源',
         '回程伴手禮變多，飛機那段可以改託運',
     ]) + '<p class="note" style="margin-top:1.6mm">2026 年 10 月的規定，以航空公司、船公司現場為準。</p></div>',
     'info', PREP, 0, mark='行李規定')

# 8 不能帶的東西
BAN_PAGE = len(pages) + 1
page(head('這些東西要注意') + '<div class="card tape">' + ''.join(
    '<div class="ban">%s<div><b>%s</b>%s<p>%s</p></div></div>' % (icon(c), e(t), tag, e(d)) for c, t, tag, d in [
        ('1f50b', '行動電源', '<span class="no-x">不能託運</span>', '一定放隨身包。飛機上不能使用、不能充電，每人最多帶 2 個。'),
        ('1f52a', '刀子、金門菜刀', '<span class="no-x">不能手提</span>', '要放託運行李。在金門買了菜刀，記得託運。'),
        ('1f356', '肉做的食物', '<span class="no-x">不能帶</span>', '肉乾、肉鬆、香腸、肉餡的餅，帶去廈門不行，帶回台灣也不行，被查到會重罰。'),
        ('1f34e', '新鮮水果', '<span class="no-x">不能帶</span>', '去廈門、回台灣都不要帶。'),
        ('1f376', '高粱酒、沙茶醬', '<span class="no-x ok-o">放託運</span>', '瓶瓶罐罐放託運行李最安心。'),
    ]) + '</div>', 'info', PREP, 0)

# 9–10 交通資訊（票卡）
def ticket(ic, kind, date, a, b, ta, tb, foot):
    return ('<div class="ticket"><div class="tk-s">%s<span>%s</span></div><div class="tk-b"><div class="tk-d">%s</div>'
            '<div class="tk-r"><div><b>%s</b></div><i>⟶</i><div><b>%s</b></div></div>'
            '<div class="tk-t"><span>%s</span><span></span><span>%s</span></div><div class="tk-f">%s</div></div></div>') % (
        icon(ic), kind, date, a, b, ta, tb, foot)


FILL = '<u></u>'
page(head('交通資訊・去程', '12/16（三）') +
     '<div class="warn">%s證件拿在手上，跟著領隊走</div>' % icon('26a0') +
     '<div style="height:4mm"></div>' +
     ticket('2708', '飛機', '12/16（三）・國內線', '台北松山', '金門', '', '12:30 到', '航班%s起飛%s' % (FILL, FILL)) +
     ticket('26f4', '船', '12/16（三）・小三通', '金門水頭', '廈門五通', '', '', '開船時間%s坐船約 30 分鐘' % FILL) +
     '<div class="card tape" style="margin-top:4mm"><div class="ct" style="font-size:14pt">每一段要拿出來的證件</div>' + ul([
         '坐飛機：<b>身分證</b>',
         '金門出境：<b>護照</b>',
         '廈門入境：<b>台胞證</b>',
     ]) + '<p class="note" style="margin-top:1.4mm">開船時間確定後，領隊會再通知，可以寫在上面。</p></div>',
     'info', PREP, 0, mark='交通資訊')

page(head('交通資訊・回程', '12/20（日）') +
     '<div class="warn">%s早上要早起，前一晚先收好行李</div>' % icon('26a0') +
     '<div style="height:4mm"></div>' +
     ticket('26f4', '船', '12/20（日）・小三通', '廈門五通', '金門水頭', '', '', '開船時間%s坐船約 30 分鐘' % FILL) +
     ticket('2708', '飛機', '12/20（日）・國內線', '金門', '台北松山', '17:40 起飛', '', '15:45 到機場報到') +
     '<div class="card tape pink" style="margin-top:4mm"><div class="ct" style="font-size:14pt">回程記得</div>' + ul([
         '廈門出境：<b>台胞證</b>；金門入境：<b>護照</b>',
         '肉做的東西不能帶回台灣',
         '菜刀、高粱酒放託運行李',
     ]) + '</div>', 'info', PREP, 0)

# 11–12 碼頭怎麼走
def steps(items):
    out = ''
    for i, (t, d, ph) in enumerate(items, 1):
        th = '<img class="th" src="%s" alt="">' % src(ph) if ph else '<span></span>'
        out += '<li><span class="n">%d</span><div><b>%s</b>%s</div>%s</li>' % (i, e(t), ('<span>%s</span>' % e(d)) if d else '', th)
    return '<ul class="steps">%s</ul>' % out


page(head('碼頭怎麼走・去程', '金門 → 廈門') + steps([
    ('金門機場坐計程車', '到水頭碼頭，約 20 分鐘', 'kmair'),
    ('碼頭報到、託運行李', '領船票，大行李交給櫃台', 'ferry2'),
    ('出境：給海關看護照', '', None),
    ('上船，坐約 30 分鐘', '天氣好可以看到廈門', 'ferry'),
    ('五通碼頭入境：台胞證', '', 'wutong2'),
    ('領行李，坐車到飯店', '約 40 分鐘', 'wutong'),
]), 'info', PREP, 0, mark='碼頭怎麼走')

page(head('碼頭怎麼走・回程', '廈門 → 金門 → 台北') + steps([
    ('退房，坐車到五通碼頭', '約 40 分鐘', 'wutong'),
    ('報到、託運行李', '', None),
    ('出境：給海關看台胞證', '', None),
    ('上船，坐約 30 分鐘', '回到金門水頭碼頭', 'ferry'),
    ('入境：給海關看護照', '', None),
    ('包車逛金門，再到機場', '15:45 報到，17:40 起飛', 'kmair2'),
]), 'info', PREP, 0)

# 13 住宿
page(head('住宿資訊', '12/16 – 12/20・四晚') + pol('hotel', '壺香悅：紅白色的洋樓，門口是圓拱玻璃門', 'big', 'rot1 fit') +
     '<div class="card tape"><div class="ct">壺香悅<small>中山路步行街店</small></div>' + ul([
         '就在中山路步行街旁邊',
         '走路可到：中山路、八市、中華城、泰印象 SPA、悅享採耳、不只有茶',
     ]) + '</div>' + addr('hotel', '飯店地址（迷路時給人看）'), 'spot', PREP, 0, mark='住宿資訊')

# ---------------------------------------------------------------- 每一天
MOVE_ICON = {'car': '1f695', 'walk': '1f6b6', 'ship': '26f4'}
MEAL = ('早餐', '午餐', '晚餐')
DAY_NOTE = {
    'd1': ['證件拿在手上，跟著領隊走', '晚餐看到想吃的就進去吃'],
    'd2': ['南普陀寺要事先預約', '下午採耳前可以回飯店午休'],
    'd3': ['<b>台胞證一定要帶</b>，坐船去鼓浪嶼要用', '鼓浪嶼走路多，穿好走的鞋'],
    'd4': ['嶼見閩南的表演提早 10 分鐘到', '晚上先把行李收好'],
    'd5': ['早點起床，退房別忘了東西', '肉做的東西不能帶回台灣'],
}
ORDER = {
    'd1': [('one', 'plane'), ('two', 'ship'), ('two', 'zs')],
    'd2': [('one', 'peanut'), ('two', 'bashi'), ('two', 'npt'), ('pair', 'veg', 'ear'), ('two', 'xcx')],
    'd3': [('one', 'pier'), ('gly',), ('pair', 'spa', 'tea'), ('one', 'zhcity')],
    'd4': [('two', 'spw'), ('two', 'yixi'), ('two', 'yj'), ('one', 'pack')],
    'd5': [('one', 'back'), ('two', 'km'), ('two', 'mofan'), ('one', 'home')],
}


def gly_pages():
    did = 'd3'
    c = DAYS[did]['color']
    body = head('鼓浪嶼', daykick(did, '09:45')) + pol('gly', '黃榮遠堂：島上有名的老洋房', 'big', 'rot1 fit')
    body += '<div class="card tape"><div class="meta"><span class="label">09:45</span></div>' + ul([
        '島上沒有汽車，到處是百年老洋房',
        '散步看建築、看海景，放慢腳步輕鬆逛',
        '島上也有電瓶車可以坐',
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
             '蓋了各式各樣的洋樓、教堂和學校，有「萬國建築博覽」的稱號。島上鋼琴特別多，又叫「鋼琴之島」。2017 年被列為世界文化遺產。</p></div>')
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
        bk = '<i class="bk">要事先訂</i>' if it.get('book') else ''
        ml = '<i class="meal">%s</i>' % meal if meal and not t.startswith(meal) else ''
        lis += '<li class="st"><b>%s</b><span>%s%s%s</span></li>' % (e(it['t']), e(t), ml, bk)
    dense = ' dense' if lis.count('<li') > 13 else ''
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
        elif o[0] == 'gly':
            gly_pages()
        else:
            spot(o[1])

# ---------------------------------------------------------------- 必吃美食
FOOD_IMG = {'f-shacha': 'shacha', 'f-oyster': 'oyster', 'f-duck': 'duck', 'f-peanut': 'peanut', 'f-mianxian': 'mianxian',
            'f-zongzi': 'zongzi', 'f-crab': None, 'f-congee': None, 'f-seafood': 'shellfish', 'f-tusun': 'tusun'}
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
    page(head('必吃美食', '廈門的道地味道') + cards, 'food', EAT, '吃', mark='必吃美食' if i == 0 else None)

# ---------------------------------------------------------------- 伴手禮
def gifts(items):
    out = ''
    for name, note, ph, emo in items:
        inner = '<img class="p" src="%s" alt="">' % src(ph) if ph else icon(emo, 'e')
        out += '<div class="gift"><div class="cir">%s</div><b>%s</b><span>%s</span></div>' % (inner, e(name), e(note))
    return '<div class="gifts">%s</div>' % out


page(head('必買伴手禮', '廈門') + '<div class="card tape">' + gifts([
    ('鼓浪嶼餡餅', '挑綠豆口味；肉鬆口味不能帶回台灣', None, '1f96e'),
    ('南普陀素餅', '素的，可以安心帶', None, '1f36a'),
    ('鐵觀音', '福建有名的烏龍茶', 'tea', None),
    ('芒果乾', '八市、中山路都買得到', None, '1f96d'),
    ('沙茶醬', '沙茶麵的味道，放託運', None, '1fad9'),
    ('青津果', '鼓浪嶼的蜜餞橄欖', None, '1fad2'),
]) + '</div><div class="warn">%s肉做的東西不能帶回台灣</div>' % icon('26a0'), 'food', BUY, '買', mark='必買伴手禮')

page(head('必買伴手禮', '金門') + '<div class="card tape pink">' + gifts([
    ('貢糖', '花生做的，酥酥的', None, '1f95c'),
    ('菜刀', '砲彈鋼做的，要託運', 'knife', None),
    ('高粱酒', '放託運行李', 'liquor', None),
    ('風獅爺小物', '金門的守護神', 'lion', None),
    ('一條根', '金門的藥草，做成貼布', None, '1f33f'),
    ('麵線', '金門手工麵線', None, '1f35c'),
]) + '</div><div class="warn">%s菜刀不能手提，記得託運</div>' % icon('26a0'), 'food', BUY, '買')

# ---------------------------------------------------------------- 說法對照
WORDS = [('計程車', '出租車・打車'), ('捷運', '地鐵'), ('廁所', '衛生間'), ('塑膠袋', '塑料袋'),
         ('冷氣', '空調'), ('鳳梨', '菠蘿'), ('馬鈴薯', '土豆')]
page(head('台灣說法・廈門說法') + '<div class="card tape"><table class="words">%s</table></div>' % ''.join(
    '<tr><td>%s</td><td>→</td><td>%s</td></tr>' % (e(a), e(b)) for a, b in WORDS) +
     '<div class="card tape pink r"><div class="ct" style="font-size:14pt">幾句好用的話</div><ul class="say">%s</ul></div>' % ''.join(
         '<li><b>%s</b><span lang="zh-Hans">%s</span></li>' % (e(a), e(b)) for a, b in [
             ('廁所在哪裡？', '请问卫生间在哪里？'), ('不要辣', '不要辣，谢谢'), ('請送我到這裡', '请送我到这里')]) +
     '<p class="note" style="text-align:center;margin-top:1.6mm">廈門人也講閩南話，跟台語很像，可以說說看！</p>', 'info', PREP, mark='台灣說法・廈門說法')

# ---------------------------------------------------------------- 給司機看
DRIVER = ['hotel', 'npt', 'xcx', 'xiagu', 'spw', 'yixi', 'yujian', 'wutong']


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
            '<p>飯店、中山路、八市、南普陀寺、採耳、小埕戲、廈鼓碼頭、鼓浪嶼、泰印象 SPA、中華城、沙坡尾、嶼見閩南的部分照片為自行提供。其他照片來自 Wikimedia Commons：</p>%s'
            '<p>地圖海岸線：© OpenStreetMap 貢獻者（ODbL）。圖示：Twemoji（CC BY 4.0）。字型：jf open 粉圓（SIL OFL）、思源黑體（SIL OFL）。</p>'
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
        toc.append(('筆記', first_memo, ''))

hp = P['hotel']
page(back_art() + '<!--IN--><div class="bk-card"><div class="bk-k">迷路的時候，請把這頁給人看</div><div class="drv" lang="zh-Hans" style="flex:none">'
     '<p class="p" style="margin-top:3mm">请送我到这里，谢谢</p><p class="n">壶香悦<small>（厦门中山路步行街店）</small></p>'
     '<p class="a">%s</p></div></div>' % e(hp['addr']), 'back')

# 照片來源要等所有頁面都用過照片才能寫
pages[CRED_INDEX] = (credits_page(), 'info', PREP, None)

# 目錄
toc_html = '<ul>%s</ul>' % ''.join('<li><b>%02d</b><span>%s%s</span></li>' % (n, e(name), ('<small>%s</small>' % e(sub)) if sub else '')
                                   for name, n, sub in toc)
pages[2] = (head('目錄') + '<div class="toc">%s</div>' % toc_html, 'info', PREP, None)
pages[:] = [(b.replace('{ban}', str(BAN_PAGE)), c, col, t) for b, c, col, t in pages]

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
        inner = '<div class="in">%s</div>' % body
    out.append('<section class="pg %s %s"%s>%s%s%s</section>' % (cls, side, style, inner, tabh, num))
doc = ('<!DOCTYPE html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><title>廈門旅行手札</title>'
       '<link rel="stylesheet" href="book.css"><style id="sz"></style></head><body>%s</body></html>') % '\n'.join(out)
open(OUT_HTML, 'w').write(doc)
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
