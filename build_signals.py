# -*- coding: utf-8 -*-
import json, re, html, sys

CATCLASS={"Funding":"c-fund","Non-dilutive":"c-nd","Regulatory":"c-reg",
          "Research":"c-res","Market":"c-mkt","GTM":"c-gtm"}
data=json.load(open('/root/work/_signals.json',encoding='utf-8'))

SEC_RE=re.compile(r'<section>\s*<div class="sh"><h2>This week\'s developments</h2>.*?</section>', re.S)

def esc(s): return html.escape(str(s), quote=True)
def escurl(u): return u.replace('&','&amp;').replace('"','&quot;')

def item_html(it):
    cls=CATCLASS[it["category"]]
    return (f'        <a class="dev {cls}" href="{escurl(it["url"])}" target="_blank" rel="noopener noreferrer">\n'
            f'          <div class="dev-meta"><span class="date">{esc(it["date"])}</span><span class="cat {cls}">{esc(it["category"])}</span></div>\n'
            f'          <h3>{esc(it["headline"])} <span class="ext">↗</span></h3>\n'
            f'          <p class="what">{esc(it["what"])}</p>\n'
            f'          <p class="why"><span class="whytag">Why it matters</span>{esc(it["why"])}</p>\n'
            f'          <div class="src">{esc(it["source"])}</div>\n'
            f'        </a>\n')

def build_section(items):
    items=sorted(items, key=lambda x: x["date"], reverse=True)
    n=len(items)
    body=''.join(item_html(it) for it in items)
    return ('<section>\n'
            '  <div class="sh"><h2>This week\'s developments</h2>'
            f'<span class="n">{n} signals</span></div>\n'
            '  <p class="sub">Global developments that intersect your profile and the program - sorted newest first. Each is framed by why it matters to your venture.</p>\n'
            '  <div class="feed">\n'
            f'{body}</div>\n </section>')

changed=0
for fname, items in data.items():
    path=f'/root/work/teams/{fname}'
    h=open(path,encoding='utf-8').read()
    m=SEC_RE.findall(h)
    if len(m)!=1:
        print(f"!! {fname}: expected 1 section, found {len(m)} -- SKIPPED"); continue
    h2=SEC_RE.sub(lambda _: build_section(items), h, count=1)
    open(path,'w',encoding='utf-8').write(h2)
    changed+=1
    print(f"{fname}: {len(items)} signals injected")
print("files updated:", changed)
