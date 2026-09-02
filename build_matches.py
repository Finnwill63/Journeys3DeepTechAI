# -*- coding: utf-8 -*-
import csv, json

S=list(csv.reader(open('/root/work/_survey.csv',encoding='utf-8')))
M=list(csv.reader(open('/root/work/_mentors.csv',encoding='utf-8')))

# ---------- mentors ----------
EXP={'strat':'Strategy & Business Model','gtm':'Go-to-market, Sales & Business Development',
 'fund':'Fundraising & Investor Readiness','team':'Team, Leadership & Operations',
 'corp':'Corporate Partnerships & Ecosystems','mkt':'Marketing, Brand & Communications',
 'prod':'Product & Design','finip':'Finance, Legal & IP'}
SEC=['AI/ML & Data','Hardware, Materials & Manufacturing','Software / Cloud / Telecom',
 'Energy, Climate & Sustainability','Health & Bio','Defence & Dual-use','Space & Sensing']
EXCLUDE={'Will Cardwell','Samuli Salmela'}  # host + declined

mentors=[]
for r in M[1:]:
    if len(r)>16: r=r[:5]+[r[5]+' '+r[6]]+r[7:]  # fix embedded-quote row (Michael)
    name=r[1].strip()
    if name in EXCLUDE: continue
    join=r[2].strip()
    if join.startswith('Unfortunately'): continue
    exp={k for k,v in EXP.items() if v in r[4]}
    secs={s for s in SEC if s in r[3]}
    cross = 'work across sectors' in r[3]
    mentors.append({'name':name,'tent': join.startswith('Not'),
      'exp':exp,'secs':secs,'cross':cross,
      'cap':r[7].strip().split(',')[0] or '-','base': ('Finland' if r[10].strip()=='Finland' else (r[11].strip() or 'Abroad')),
      'mode':r[9].strip(),'want':r[5].strip()})

# ---------- teams (needs) ----------
# domain -> strong mentor sectors
def team_from_survey():
    # group survey rows by team, merge needs (col32) across members
    by={}
    for r in S[1:]:
        by.setdefault(r[6].strip(),[]).append(r)
    return by
by=team_from_survey()

# map survey team key -> (display, domain sectors)
TEAMS=[
 ('AccuPredix','AccuPredix',['AI/ML & Data'],'AI demand-forecasting for SMEs'),
 ('AgentFormers','AgentFormers',['AI/ML & Data','Software / Cloud / Telecom'],'On-prem enterprise AI agents'),
 ('flowø','Flowø',['AI/ML & Data','Software / Cloud / Telecom'],'AI governance for SMEs'),
 ('LEVIE','LEVIE',['Health & Bio','Hardware, Materials & Manufacturing'],'Acoustic-levitation breath diagnostics'),
 ('MedFinnity','Medfinity',['Health & Bio','AI/ML & Data'],'Med-student study platform'),
 ('Ossify Health','Ossify Health',['Health & Bio'],'Fracture / osteoporosis risk decision support'),
 ('RadiXpert AI','RadiXpert AI',['Health & Bio','AI/ML & Data'],'AI radiology imaging'),
 ('Selkotili','Selkotili',['AI/ML & Data'],'AI accounting & bookkeeping'),
 ('STRAIM','Straim',['AI/ML & Data'],'B2B AI music streaming'),
 ('Teal Security','Teal',['Software / Cloud / Telecom','AI/ML & Data'],'Automated scam-baiting'),
 ('VALOX','Valox',['Hardware, Materials & Manufacturing','Energy, Climate & Sustainability'],'Green-chemistry photocatalysis'),
]
# White Hat has no survey -> needs from assessment
WHITEHAT_NEEDS=['Go-to-market / sales','Customer discovery & validation','Hiring & team building',
                'Corporate & B2B partnerships','Fundraising (angel / pre-seed)']

# need substring -> list of (expertise_key, weight)
def need_to_exp(need):
    n=need.lower(); out=[]
    if 'go-to-market' in n or 'sales' in n: out+=[('gtm',2)]
    if 'customer discovery' in n: out+=[('gtm',1.5),('strat',0.5)]
    if 'fundrais' in n or 'pitching' in n or 'investor material' in n: out+=[('fund',2)]
    if 'grants' in n or 'public funding' in n: out+=[('fund',1),('finip',0.5)]
    if 'pricing' in n or 'business model' in n: out+=[('strat',2)]
    if 'legal' in n or 'company structure' in n: out+=[('finip',2)]
    if 'ip' == n.strip() or 'ip strategy' in n or 'intellectual' in n: out+=[('finip',2)]
    if 'corporate' in n or 'b2b partner' in n or 'partnerships' in n: out+=[('corp',2)]
    if 'hiring' in n or 'team building' in n: out+=[('team',2)]
    if 'founder dynamic' in n or 'co-founder' in n: out+=[('team',1.5)]
    if 'product manage' in n or 'product management' in n: out+=[('prod',2)]
    if 'international expansion' in n: out+=[('gtm',1),('corp',1)]
    if 'finance, cap table' in n or 'cap table' in n or 'modelling' in n: out+=[('finip',2)]
    return out

def parse_needs(cell):
    # split a col32 multi-select on commas but keep known phrases; simplest: split on comma
    parts=[p.strip() for p in cell.split(',') if p.strip()]
    return parts

HEALTH={'Health & Bio'}
def score(team_needs, domain, m):
    # expertise overlap
    want={}
    for need in team_needs:
        for k,w in need_to_exp(need):
            want[k]=max(want.get(k,0),w)
    s=0.0; hit=[]
    for k,w in want.items():
        if k in m['exp']:
            s+=w; hit.append(k)
    # sector fit
    strong=set(domain)
    inter=strong & m['secs']
    if inter:
        s+= 3 if (strong & HEALTH & m['secs']) else 2
        sec_note=next(iter(inter))
    elif m['cross']:
        s+=1; sec_note='cross-sector'
    else:
        sec_note=None
    # health/regulatory teams: boost health-sector mentors even without expertise overlap
    health_need=any(('clinical' in nd.lower() or 'regulatory' in nd.lower() or 'healthcare' in nd.lower()) for nd in team_needs)
    if health_need and 'Health & Bio' in m['secs']:
        s+=2
        if not sec_note or sec_note=='cross-sector': sec_note='Health & Bio'
    # tie-breakers
    if m['base']=='Finland': s+=0.3
    if m['cap'] in ('Two','More'): s+=0.15
    if m['tent']: s-=0.5   # slight penalty for tentative
    return s, hit, sec_note

EXPNAME={'strat':'strategy/BM','gtm':'GTM/sales','fund':'fundraising','team':'team/ops',
 'corp':'partnerships','mkt':'marketing','prod':'product','finip':'finance/legal/IP'}

SECSHORT={'AI/ML & Data':'AI/data sector','Health & Bio':'health sector',
 'Hardware, Materials & Manufacturing':'hardware sector','Energy, Climate & Sustainability':'climate sector',
 'Software / Cloud / Telecom':'software sector','Defence & Dual-use':'defence sector',
 'Space & Sensing':'space sector','cross-sector':'cross-sector'}
def reason(hit, sec_note, m):
    bits=[EXPNAME[k] for k in ['gtm','fund','strat','finip','corp','team','prod','mkt'] if k in hit]
    if sec_note: bits.append(SECSHORT.get(sec_note,'cross-sector'))
    r=' · '.join(bits)
    tags=[]
    if m['tent']: tags.append('tentative')
    if m['base']!='Finland' and m['base']!='Abroad': tags.append(m['base'])
    if tags: r+='  ('+', '.join(tags)+')'
    return r

TAGNAME={'gtm':'GTM/sales','fund':'Fundraising','strat':'Business model','finip':'Legal/IP',
 'corp':'Partnerships','team':'Team/hiring','prod':'Product','mkt':'Marketing'}
def need_tags(needs):
    keys=[]
    for nd in needs:
        for k,w in need_to_exp(nd):
            if k not in keys: keys.append(k)
    order=['gtm','fund','strat','finip','corp','team','prod','mkt']
    tags=[TAGNAME[k] for k in order if k in keys]
    if any(('clinical' in nd.lower() or 'regulatory' in nd.lower() or 'healthcare' in nd.lower()) for nd in needs):
        tags.append('Regulatory/clinical')
    return tags

results=[]
def do_team(disp, needs, domain, blurb):
    ranked=[]
    for m in mentors:
        sc,hit,sec=score(needs,domain,m)
        ranked.append((sc,m,hit,sec))
    ranked.sort(key=lambda x:-x[0])
    top=ranked[:3]
    results.append({'team':disp,'blurb':blurb,
      'needtags':need_tags(needs),
      'matches':[{'name':t[1]['name'],'score':round(t[0],1),'why':reason(t[2],t[3],t[1]),
                  'cap':t[1]['cap'],'base':t[1]['base']} for t in top]})

for key,disp,domain,blurb in TEAMS:
    rows=by[key]
    needs=[]
    for r in rows: needs+=parse_needs(r[32])
    do_team(disp,needs,domain,blurb)
# White Hat
do_team('White Hat', WHITEHAT_NEEDS, ['Software / Cloud / Telecom','AI/ML & Data'],'AI construction PM (from assessment; no survey)')

# order to match site (alphabetical by display)
order=['AccuPredix','AgentFormers','Flowø','LEVIE','Medfinity','Ossify Health','RadiXpert AI','Selkotili','Straim','Teal','Valox','White Hat']
results.sort(key=lambda x: order.index(x['team']))
json.dump(results, open('/root/work/_matches.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
for r in results:
    print('\n'+r['team'])
    for mm in r['matches']:
        print(f"   {mm['score']:>4}  {mm['name']:<26} {mm['why']}")
