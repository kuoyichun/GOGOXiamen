"""產生語音檔：把 assets/data.js 裡每個 say 唸成 mp3，放到 audio/。

用法（在 repo 根目錄）：
    pip install edge-tts
    python3 tools/make_audio.py

只會重做文字有變的檔案（記錄在 audio/manifest.json）。
聲音：台灣國語女聲 HsiaoChen，語速稍慢 5%。
"""
import asyncio, hashlib, json, os, ssl, subprocess, sys

import edge_tts
import edge_tts.communicate as communicate

VOICE = 'zh-TW-HsiaoChenNeural'
RATE = '-5%'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'audio')

# 經過公司或雲端代理時，用指定的憑證檔（例如 TTS_CA=/path/ca.crt）
if os.environ.get('TTS_CA'):
    communicate._SSL_CTX = ssl.create_default_context(cafile=os.environ['TTS_CA'])


def load_trip():
    js = "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.TRIP))"
    return json.loads(subprocess.check_output(['node', '-e', js, os.path.join(ROOT, 'assets', 'data.js')]))


def jobs(trip):
    out = {'howto': trip['howto'], 'hotel': trip['hotel']['say']}
    for d in trip['days']:
        out[d['id']] = d['say']
        for it in d['items']:
            if it.get('id') and it.get('say'):
                out[it['id']] = it['say']
    for f in trip.get('foods', []):
        out[f['id']] = f['say']
    return out


async def make(name, text):
    path = os.path.join(OUT, name + '.mp3')
    for attempt in range(4):
        try:
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(path)
            if os.path.getsize(path) > 1000:
                return
        except Exception as e:  # 網路偶爾會斷，重試
            print('  重試', name, e, file=sys.stderr)
        await asyncio.sleep(3 + attempt * 3)
    raise SystemExit('產生失敗：' + name)


async def main():
    os.makedirs(OUT, exist_ok=True)
    man_path = os.path.join(OUT, 'manifest.json')
    man = json.load(open(man_path)) if os.path.exists(man_path) else {}
    todo = jobs(load_trip())
    for name, text in todo.items():
        key = hashlib.sha1((VOICE + RATE + text).encode()).hexdigest()[:12]
        if man.get(name) == key and os.path.exists(os.path.join(OUT, name + '.mp3')):
            continue
        print('產生', name, text[:24])
        await make(name, text)
        man[name] = key
    for name in list(man):  # 刪掉已經不用的檔案
        if name not in todo:
            p = os.path.join(OUT, name + '.mp3')
            if os.path.exists(p):
                os.remove(p)
            del man[name]
    json.dump(man, open(man_path, 'w'), ensure_ascii=False, indent=1, sort_keys=True)
    # 網頁用這個版本號抓語音：語音重錄後網址會變，手機就不會一直播舊的
    ver = os.path.join(os.path.dirname(OUT), 'assets', 'audio-version.js')
    open(ver, 'w').write('/* 由 tools/make_audio.py 產生，不要手改 */\nwindow.AUDIO_V = '
                         + json.dumps(man, ensure_ascii=False, sort_keys=True) + ';\n')
    print('完成，共', len(todo), '個檔案')


asyncio.run(main())
