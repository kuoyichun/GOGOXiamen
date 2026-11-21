"""改完網頁後跑這支：把 sw.js 的快取版本加 1，index.html 裡 css/js 的 ?v= 也一起換，
手機就會抓新的檔案，不會一直顯示舊的行程。
用法（在 repo 根目錄）：python3 tools/bump_version.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sw_path = os.path.join(ROOT, 'sw.js')
html_path = os.path.join(ROOT, 'index.html')

sw = open(sw_path).read()
v = int(re.search(r"xiamen-v(\d+)", sw).group(1)) + 1
sw = re.sub(r"xiamen-v\d+", 'xiamen-v%d' % v, sw)
sw = re.sub(r"'(assets/[\w.-]+\.(?:js|css))(?:\?v=\d+)?'", lambda m: "'%s?v=%d'" % (m.group(1), v), sw)
open(sw_path, 'w').write(sw)

html = open(html_path).read()
html = re.sub(r'((?:src|href)="assets/[\w.-]+\.(?:js|css))(?:\?v=\d+)?"', lambda m: '%s?v=%d"' % (m.group(1), v), html)
open(html_path, 'w').write(html)
print('version', v)
