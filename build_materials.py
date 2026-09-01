# -*- coding: utf-8 -*-
import json, re, html
MAT=json.load(open('/root/work/_materials.json',encoding='utf-8'))
p='/root/work/schedule.html'
h=open(p,encoding='utf-8').read()

# add .smat CSS once
if '.smat{' not in h:
    css=('.smat{flex-basis:100%;font-family:"IBM Plex Mono",monospace;font-size:11px;'
         'color:var(--found);text-decoration:none;margin-top:2px;display:inline-flex;align-items:center;gap:5px}'
         '.smat:hover{text-decoration:underline}'
         '.smat .ext{font-size:10px}\n')
    h=h.replace('</style>', css+'</style>', 1)

count={'n':0}
def add_link(m):
    row=m.group(0)
    sdm=re.search(r'<span class="sd">([^<]*)</span>', row)
    if not sdm: return row
    sd=sdm.group(1).strip()
    if sd not in MAT: return row
    if 'class="smat"' in row: return row  # idempotent
    url=html.escape(MAT[sd], quote=True)
    link=(f'<a class="smat" href="{url}" target="_blank" rel="noopener noreferrer">'
          f'Session materials <span class="ext">&#8599;</span></a>')
    # insert just before the sbody+srow closing </span></div>
    row=row[:-len('</span></div>')] + link + '</span></div>'
    count['n']+=1
    return row

h=re.sub(r'<div class="srow[^"]*">(?:(?!<div class="srow).)*?</span></div>', add_link, h, flags=re.S)
open(p,'w',encoding='utf-8').write(h)
print("material links added:", count['n'])
