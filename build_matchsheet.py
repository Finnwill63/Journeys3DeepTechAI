# -*- coding: utf-8 -*-
import json, html
d=json.load(open('/root/work/_matches.json',encoding='utf-8'))
def esc(s): return html.escape(str(s),quote=True)

cards=''
for t in d:
    tags=' · '.join(t['needtags'][:5])
    rows=''
    for i,m in enumerate(t['matches'],1):
        rows+=(f'<div class="mrow"><span class="rk">{i}</span>'
               f'<span class="mn">{esc(m["name"])}</span>'
               f'<span class="wy">{esc(m["why"])}</span></div>')
    cards+=(f'<div class="card"><div class="ch"><span class="tn">{esc(t["team"])}</span>'
            f'<span class="nt">{esc(tags)}</span></div>{rows}</div>')

CSS='''
@page{size:A4;margin:11mm 10mm}
*{box-sizing:border-box}
body{margin:0;font-family:"Hanken Grotesk",system-ui,sans-serif;color:#1A1A2E;font-size:9px;line-height:1.4}
h1{font-family:"Newsreader",Georgia,serif;margin:0}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #2563A8;padding-bottom:7px;margin-bottom:4px}
.eyebrow{font-family:"IBM Plex Mono",monospace;font-size:8.5px;letter-spacing:.14em;text-transform:uppercase;color:#2563A8}
h1{font-size:20px;letter-spacing:-.01em;margin-top:2px}
.conf{font-family:"IBM Plex Mono",monospace;font-size:8px;letter-spacing:.1em;text-transform:uppercase;color:#B0592B;border:1px solid #B0592B;border-radius:5px;padding:4px 8px;white-space:nowrap}
.intro{color:#4a4a63;font-size:9.5px;margin:6px 0 10px;max-width:60em}
.intro b{color:#2563A8}
.grid{column-count:2;column-gap:14px}
.card{break-inside:avoid;border:1px solid #E6E8F0;border-radius:9px;padding:8px 10px 7px;margin-bottom:8px;background:#fff}
.ch{display:flex;justify-content:space-between;align-items:baseline;gap:8px;border-bottom:1px solid #EDEFF5;padding-bottom:4px;margin-bottom:5px}
.tn{font-family:"Newsreader",serif;font-weight:600;font-size:14px;letter-spacing:-.01em}
.nt{font-family:"IBM Plex Mono",monospace;font-size:7.5px;letter-spacing:.03em;text-transform:uppercase;color:#8A8FA6;text-align:right;line-height:1.25}
.mrow{display:grid;grid-template-columns:15px 1fr;gap:5px;align-items:baseline;padding:2.5px 0;column-gap:6px}
.mrow{grid-template-columns:15px auto 1fr}
.rk{font-family:"IBM Plex Mono",monospace;font-weight:600;font-size:9px;color:#fff;background:#2563A8;border-radius:4px;width:15px;height:15px;display:inline-flex;align-items:center;justify-content:center;line-height:1}
.mn{font-weight:700;font-size:10px;white-space:nowrap}
.wy{font-size:8.7px;color:#5b5b74}
.rk.r2{background:#5c86bf}.rk.r3{background:#93aacb}
.foot{margin-top:8px;padding-top:7px;border-top:1px solid #E6E8F0;font-family:"IBM Plex Mono",monospace;font-size:8px;color:#8A8FA6;line-height:1.5}
'''
HTML=f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,600&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style></head><body>
<div class="top">
  <div><div class="eyebrow">Journeys 3 · Deep Tech &amp; AI · Mentor Matching</div>
  <h1>Best mentor fits — 3 per venture</h1></div>
  <div class="conf">Internal · Will &amp; Fabian</div>
</div>
<p class="intro">Top three mentor matches for each of the 12 ventures, scored on <b>expertise ↔ each team&#39;s stated needs</b> and <b>sector fit</b>. Drawn from 14 founder responses (11 teams; White Hat from assessment) and 21 mentor sign-ups. Rank badge = fit order. Pool excludes Will (host) and Samuli (declined); &ldquo;tentative&rdquo; = mentor not yet fully confirmed.</p>
<div class="grid">{cards}</div>
<div class="foot">Need tags summarize each team&#39;s &ldquo;where I want mentor help&rdquo; answers. &ldquo;Regulatory/clinical&rdquo; boosts health-sector mentors. Locations shown = based abroad (remote-first). Capacity &amp; availability detail is in the mentor bench analysis. A mentor may be a top fit for more than one team — final 1:1 assignment is yours to balance.</div>
</body></html>'''
# apply rank colors r2/r3
HTML=HTML.replace('<span class="rk">2</span>','<span class="rk r2">2</span>').replace('<span class="rk">3</span>','<span class="rk r3">3</span>')
open('/root/work/_matchsheet.html','w',encoding='utf-8').write(HTML)
print('wrote _matchsheet.html')
