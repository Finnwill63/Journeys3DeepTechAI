# -*- coding: utf-8 -*-
import json, re, html
MAT=json.load(open('/root/work/_materials.json',encoding='utf-8'))
p='/root/work/syllabus.html'
h=open(p,encoding='utf-8').read()

if '.smat-syl{' not in h:
    css=('.smat-syl{font-family:"IBM Plex Mono",monospace;font-size:11px;margin:0 0 10px}'
         '.smat-syl a{color:var(--found);text-decoration:none;display:inline-flex;align-items:center;gap:5px}'
         '.smat-syl a:hover{text-decoration:underline}.smat-syl .ext{font-size:10px}\n')
    h=h.replace('</style>', css+'</style>', 1)

count={'n':0}
def fix_section(m):
    sec=m.group(0)
    if 'class="smat-syl"' in sec: return sec
    wt=re.search(r'<span class="wt">([^<]*)</span>', sec)
    if not wt: return sec
    date=wt.group(1).split(' - ',1)[0].strip()
    if date not in MAT: return sec
    url=html.escape(MAT[date], quote=True)
    link=(f'<div class="smat-syl"><a href="{url}" target="_blank" rel="noopener noreferrer">'
          f'Session materials <span class="ext">&#8599;</span></a></div>')
    # insert after the whost div if present, else after the wk-h header div
    if '<div class="whost">' in sec:
        sec=re.sub(r'(<div class="whost">.*?</div>)', r'\1'+link, sec, count=1, flags=re.S)
    else:
        sec=re.sub(r'(<div class="wk-h">.*?</div>)', r'\1'+link, sec, count=1, flags=re.S)
    count['n']+=1
    return sec

h=re.sub(r'<section class="wk[^"]*">.*?</section>', fix_section, h, flags=re.S)
open(p,'w',encoding='utf-8').write(h)
print('syllabus material links added:', count['n'])
