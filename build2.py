"""안개 도감 데이터 빌드: tricky.lol raw JSON(ko/en) -> data.json"""
import json,re,sys,os
RAW=sys.argv[1] if len(sys.argv)>1 else 'raw'
def L(n,loc): return json.load(open(os.path.join(RAW,f'{n}_{loc}.json')))
KW={'haste':'이동 속도 증가','exhausted':'탈진','broken':'치료 불능','exposed':'약점 노출','undetectable':'감지 불가능',
    'oblivious':'인지 불가능','endurance':'인내','hindered':'이동 속도 감소','blindness':'실명','elusive':'회피',
    'hemorrhage':'출혈','mangled':'근육 손상','deepwound':'깊은 상흔','madness':'광기','incapacitated':'무능력'}
INP={'activatablebutton1':'능력 활성화','activatablebutton2':'보조 능력','useitem':'아이템 사용'}
RAR={'common':0,'uncommon':1,'rare':2,'veryrare':3,'visceral':4,'ultrarare':4,'artifact':5,'limited':5,'specialevent':5}
unresolved=[]
def num(x):
    if isinstance(x,float):
        x=round(x,2); return str(int(x)) if x==int(x) else str(x)
    return str(x)
def fill(s,tun,ctx):
    if not s: return ''
    tl={k.lower():v for k,v in (tun or {}).items()}
    def rep(m):
        kind,rest=m.group(1),m.group(2)
        if kind=='Keyword': return '<b>'+KW.get(rest.lower(),rest)+'</b>'
        if kind=='Input': return '<b>'+INP.get(rest.lower(),rest)+'</b>'
        if kind=='Tunable':
            key=rest.split('.')[-1].lower()
            v=tl.get(key)
            if v is None: unresolved.append((ctx,rest)); return '?'
            if isinstance(v,list):
                vals=[num(x) for x in v]; return vals[0] if len(set(vals))==1 else '/'.join(vals)
            return num(v)
        unresolved.append((ctx,m.group(0))); return '?'
    s=re.sub(r'\{(Keyword|Input|Tunable)\.([^}]+)\}',rep,s)
    s=re.sub(r'\{[^}]*\}', lambda m:(unresolved.append((ctx,m.group(0))) or '?'), s)
    return s
def clean(s):
    s=s or ''
    s=re.sub(r'<span class="Highlight\d">(.*?)</span>',r'<em>\1</em>',s,flags=re.S)
    s=re.sub(r'</?(?!/?(?:b|i|li|ul|br|em)\b)[^>]*>','',s)
    s=re.sub(r'(%)(?=%)','',s)  # "50%%" guard
    s=re.sub(r'(\d)%%',r'\1%',s)
    s=re.sub(r'\ufffd+','…',s)  # 원본 데이터에서 잘린 글자
    s=re.sub(r'^(\s*<br>)+|(<br>\s*)+$','',s.strip())
    return s
ck,ce=L('characters','ko'),L('characters','en')
ik,ie=L('items','ko'),L('items','en')
pk,pe=L('perks','ko'),L('perks','en')
ak,ae=L('addons','ko'),L('addons','en')
ok_,oe=L('offerings','ko'),L('offerings','en')
ICONS=json.load(open('icons.json')) if os.path.exists('icons.json') else {'map':{},'cols':{},'cell':64}
IM=ICONS['map']
def ic(img): return IM.get(os.path.splitext(os.path.basename(img or ''))[0].lower())
out={'icons':{'cols':ICONS['cols']},'version':json.load(open(os.path.join(RAW,'versions_ko.json')))['perks']['version'],'killers':[],'survivors':[],'entries':[]}
power_owner={}
chars={}
for key,c in ck.items():
    e=ce.get(key,{})
    cid=c['id']; chars[key]=cid
    rec={'id':cid,'ko':c['name'],'en':e.get('name',''),'d':clean(fill(c.get('bio'),c.get('tunables'),cid)),
         'story':clean(fill(c.get('story'),None,cid)),'perks':c.get('perks') or [],'dlc':c.get('dlc'),'ic':IM.get('char:'+cid)}
    if c['role']=='killer':
        it=c.get('item'); power_owner[it]=cid
        p=ik.get(it,{}); pen=ie.get(it,{})
        rec['power']={'ko':p.get('name',''),'en':pen.get('name',''),'d':clean(fill(p.get('description'),p.get('tunables'),it))}
        out['killers'].append(rec)
    else: out['survivors'].append(rec)
def E(r): return {k:v for k,v in r.items() if v not in ('',None,[])}
for key,p in pk.items():
    owner=chars.get(str(p.get('character'))) if p.get('character') is not None else None
    out['entries'].append(E({'c':'sp' if p['role']=='survivor' else 'kp','id':key,'ko':p['name'].strip(),'en':pe.get(key,{}).get('name','').strip(),
        'd':clean(fill(p['description'],p.get('tunables'),key)),'o':owner,'ic':ic(p.get('image'))}))
for key,a in ak.items():
    par=(a.get('parents') or [None])[0]
    r={'id':key,'ko':(a['name'] or '').strip(),'en':(ae.get(key,{}).get('name') or '').strip(),
       'd':clean(fill(a['description'],a.get('tunables'),key)),'r':RAR.get(a.get('rarity')),'ic':ic(a.get('image'))}
    if a['type']=='poweraddon':
        r['c']='ka'; r['o']=power_owner.get(par)
    else:
        r['c']='sa'; r['it']=a.get('item_type')
    if not r['ko'] or r['ko'].startswith('@#'): continue
    out['entries'].append(E(r))
for key,i in ik.items():
    if i['type']!='item' or not i.get('name'): continue
    out['entries'].append(E({'c':'it','id':key,'ko':i['name'].strip(),'en':(ie.get(key,{}).get('name') or '').strip(),
        'd':clean(fill(i['description'],i.get('tunables'),key)),'r':RAR.get(i.get('rarity')),'it':i.get('item_type'),'ic':ic(i.get('image'))}))
for key,o in ok_.items():
    if o.get('retired') or not o.get('name'): continue
    out['entries'].append(E({'c':'of','id':key,'ko':o['name'].strip(),'en':(oe.get(key,{}).get('name') or '').strip(),
        'd':clean(fill(o['description'],o.get('tunables'),key)),'r':RAR.get(o.get('rarity')),'role':o.get('role') or 'shared','ic':ic(o.get('image'))}))
# ---- 이번 주 신전 (raw/shrine.json 이 있으면) ----
sp_path=os.path.join(RAW,'shrine.json')
if os.path.exists(sp_path):
    try:
        sh=json.load(open(sp_path))
        if isinstance(sh,dict) and 'perks' not in sh and len(sh)==1: sh=next(iter(sh.values()))
        perk_keys={k.lower():k for k in pk}
        name_keys={(pe.get(k,{}).get('name') or '').lower():k for k in pk}
        ids=[]
        for p in sh.get('perks',[]):
            pid=p.get('id') if isinstance(p,dict) else p
            pid=str(pid or '')
            k=perk_keys.get(pid.lower()) or name_keys.get(pid.lower())
            if k: ids.append(k)
            else: print('신전 기술 매칭 실패:',pid)
        out['shrine']={'perks':ids,'start':sh.get('start'),'end':sh.get('end')}
        print('신전',len(ids),'개')
    except Exception as ex:
        print('신전 데이터 읽기 실패:',ex)

# ---- 패치 변경점: 직전 data.json과 비교 ----
def keyed(data): return {e['c']+':'+e['id']:e for e in data.get('entries',[])}
if os.path.exists('data.json'):
    try: prev=json.load(open('data.json'))
    except Exception: prev={}
    if prev.get('version') and prev.get('version')!=out['version']:
        P,N=keyed(prev),keyed(out); items=[]
        for k,e in N.items():
            if k not in P: items.append({'k':k,'t':'add'})
            elif P[k].get('d')!=e.get('d') or P[k].get('ko')!=e.get('ko'):
                items.append({'k':k,'t':'mod','old':P[k].get('d',''),'oldko':P[k].get('ko') if P[k].get('ko')!=e.get('ko') else None})
        for k,e in P.items():
            if k not in N: items.append({'k':k,'t':'del','ko':e.get('ko'),'c':e.get('c')})
        out['changes']={'from':prev['version'],'to':out['version'],'items':items}
        print('패치 변경점',prev['version'],'->',out['version'],len(items),'개')
    elif prev.get('changes'):
        out['changes']=prev['changes']
json.dump(out,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
import collections
print('version',out['version'],'killers',len(out['killers']),'survivors',len(out['survivors']))
print(collections.Counter(e['c'] for e in out['entries']))
print('ka no owner',sum(1 for e in out['entries'] if e['c']=='ka' and not e.get('o')),'sa no type',sum(1 for e in out['entries'] if e['c']=='sa' and not e.get('it')),'no rarity',collections.Counter(e['c'] for e in out['entries'] if e['c'] in('ka','sa','it','of') and e.get('r') is None))
print('unresolved',len(unresolved),unresolved[:12])
print(os.path.getsize('data.json')//1024,'KB')
# template.html이 있으면 데이터를 넣어 완성된 페이지를 만든다
if os.path.exists('template.html'):
    page=open('template.html').read().replace('__DATA__',open('data.json').read().replace('</','<\\/'))
    open('dbd-fog-guide.html','w').write(page); print('dbd-fog-guide.html 생성')
# GitHub Pages 등 일반 호스팅용: 문서 뼈대(doctype, charset, viewport)를 갖춘 index.html
if os.path.exists('dbd-fog-guide.html'):
    body=open('dbd-fog-guide.html').read()
    head=('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
          '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
          '<meta name="description" content="데드 바이 데이라이트 기술·애드온·아이템·공물·캐릭터 한국어 검색 도감">\n'
          '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n')
    open('index.html','w').write(head+body+'\n</body>\n</html>\n'); print('index.html 생성')
