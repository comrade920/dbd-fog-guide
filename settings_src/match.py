import json,re,difflib,sys
d=json.load(open('data.json'))
norm=lambda s:re.sub(r'[\s\'"“”‘’.,:!?\-·&()]','',(s or '').lower())
perks={norm(e['ko']):e for e in d['entries'] if e['c'] in('sp','kp')}
kperks={k:v for k,v in perks.items() if v['c']=='kp'}
killers={norm(k['ko']):k for k in d['killers']}
addons={}
for e in d['entries']:
    if e['c']=='ka': addons.setdefault(e.get('o'),{})[norm(e['ko'])]=e
TXT=open('settings_src/raw.txt').read().splitlines()
out=[];miss=[];cur=None
# 원문(커뮤니티) 표기 -> 게임 데이터 표기
PA={'모든 수단을 동원':'교착 상태','무제한 대기':'가장 좋은 것은 마지막에','재앙의 갈고리: 진물의 상처':'재앙의 갈고리: 고통의 선물',
    '주술: 운명의 노리개':'주술: 노리개','바베큐&칠리':'바비큐 & 칠리','바베큐 & 칠리':'바비큐 & 칠리'}
AA={'장 박힌 부츠':'징 박힌 부츠','윤활제 혼합물':'톰슨제 혼합물','굽힌 자':'긁힌 자','적철광 인장':'적철석 인장','광신자의 목걸이':'헌신자의 아뮬렛',
    '절단된 발가락':'잘린 발가락','기도문 석판 조각':'기도 석판 조각','사자 이빨':'사자의 이빨','렌지로의 피투성이 장갑':'렌지로의 피 묻은 장갑',
    '박살난 선채':'조각난 선체','감옥 쇠사슬':'감옥 체인','골드 크리크 위스키':'골드 크릭 위스키','보안관 배지':'집행관의 배지',
    '현상수배 전단지':'현상 수배 전단','조 스페셜':'조 스매셔','입막이 천':'침묵의 천','썩어가는 짐승 시체':'썩어가는 시체',
    '거부된 요청 방식':'거부된 요청 양식','회약통':'화약통','뱃줄 스파이크':'밧줄 스파이크','스파이크가 박힌 칼라':'징 박힌 목줄',
    '보리를 으깬 곡물':'보릿가루','배 선수상':'선수상','뒷머리':'닭 머리','진지라의 손':'잔지라의 손','기계 부품 상자':'기계부품 가방',
    '울슨의 지갑':'올슨의 지갑','가시돋힌 덩굴 식물':'가시돋친 덩굴 식물','미네킹 발':'마네킹 발','갈손된 잉크 리본':'감손된 잉크 리본',
    '핏빛 우로보로스 약병':'핏빛 우로보로스 유리병','달걀(황금)':'계란 (황금)','램버트의 별지리표':'램버트의 별자리표',
    '핏빛 비열한 어둠의 책':'무지갯빛 비열한 어둠의 책','카스의 검':'날카로운 검','위축의 지팡이':'시든 지팡이','라피스 라줄리':'라피스 라즐리'}
def mp(name):
    name=PA.get(name,name)
    n=norm(name)
    if n in kperks: return kperks[n]['id'],None
    c=difflib.get_close_matches(n,list(kperks),1,0.6)
    return None,(kperks[c[0]]['ko'] if c else None)
def ma(name,kid):
    name=AA.get(name,name)
    n=norm(name); pool=addons.get(kid,{})
    if n in pool: return pool[n]['id'],None
    c=difflib.get_close_matches(n,list(pool),1,0.5)
    return None,(pool[c[0]]['ko'] if c else None)
for line in TXT:
    if line.startswith('#') or not line.strip(): continue
    p=line.split('|')
    if p[0]=='K':
        k=killers.get(norm(p[2])); assert k,p[2]
        cur={'k':k['id'],'ko':k['ko'],'num':int(p[1]),'diff':[p[3],p[4]],'sets':[]}; out.append(cur); continue
    _,name,perkstr,addstr,desc=p
    slots=[]
    for s in perkstr.split(';'):
        m=re.match(r'(.*)\((.*)\)$',s.strip()); nm,role=m.group(1),m.group(2)
        alts=[]
        for a in nm.split(' or '):
            pid,sug=mp(a.strip())
            if not pid: miss.append(('perk',cur['ko'],a.strip(),sug))
            alts.append(pid or '?'+a.strip())
        slots.append({'alts':alts,'role':role})
    combos=[]
    for combo in addstr.split(' / '):
        parts=[]
        for part in combo.split('+'):
            alts=[]
            for a in part.split(' or '):
                aid,sug=ma(a.strip(),cur['k'])
                if not aid: miss.append(('addon',cur['ko'],a.strip(),sug))
                alts.append(aid or '?'+a.strip())
            parts.append(alts)
        combos.append(parts)
    cur['sets'].append({'name':name,'perks':slots,'addons':combos,'desc':desc})
json.dump(out,open('settings_src/parsed.json','w'),ensure_ascii=False,indent=0)
print(len(out),'killers',sum(len(k['sets']) for k in out),'sets; miss',len(miss))
seen=set()
for m in miss:
    if (m[0],m[2]) in seen: continue
    seen.add((m[0],m[2])); print(m)

# settings.json 생성 (원문 정보는 기존 settings.json 값을 유지)
import os
SRC={'author':'라스쿠','title':'자주쓰는 살인마 세팅 업데이트(v2026_2차)','board':'디시인사이드 데드바이데이라이트 마이너 갤러리',
     'url':'https://gall.dcinside.com/mgallery/board/view/?id=dbd&no=2606672','version':'v2026_2차','updated':'2026-09-13','copied':'2026-10-01'}
if os.path.exists('settings.json'): SRC=json.load(open('settings.json')).get('source',SRC)
if miss: print('연결 안 된 이름이 있어 settings.json을 만들지 않았습니다. PA/AA 표에 추가하세요.')
else:
    S={'source':SRC,'killers':{}}
    for k in out:
        S['killers'][k['k']]={'num':k['num'],'diff':k['diff'],'sets':[{'name':s['name'],'desc':s['desc'],
            'perks':[{'alts':['kp:'+a for a in sl['alts']],'role':sl['role']} for sl in s['perks']],
            'addons':[[['ka:'+a for a in part] for part in combo] for combo in s['addons']]} for s in k['sets']]}
    json.dump(S,open('settings.json','w'),ensure_ascii=False,indent=1)
    print('settings.json 저장')
