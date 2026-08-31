import json, subprocess, urllib.parse as up, concurrent.futures as cf
TPL={'fcia':'LAN-VIN-TVD-INT-BLAN-20260617-ORG-FIA0001-FIA-{}',
     'atia':'LAN-VIN-TVD-INT-BLAN-20260818-ORG-ATIA0002-ATIA-{}'}
d=json.load(open('links_gerados.json'))
alvo=[(p,dest,pmp,u) for p,ds in d.items() for dest,m in ds.items() for pmp,u in m.items()]
def check(t):
    p,dest,pmp,u=t
    r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{redirect_url}','-m','25',u],
                     capture_output=True,text=True).stdout
    q=dict(up.parse_qsl(up.urlsplit(r).query))
    return (p,dest,pmp,u,r,q.get('src'),q.get('sck'))
ruins=[]
with cf.ThreadPoolExecutor(12) as ex:
    for p,dest,pmp,u,r,src,sck in ex.map(check, alvo):
        esperado=TPL[p].format(pmp)
        if not r.startswith('http') or src!=esperado or sck!=esperado:
            ruins.append({'produto':p,'destino':dest,'pmp':pmp,'url':u,'src':src,'sck':sck,'destino_final':r[:120]})
print('total', len(alvo), '| divergentes', len(ruins))
for x in ruins: print(' ', x['produto'], x['pmp'], x['destino'][:40], '| src=', x['src'])
json.dump(ruins, open('links_divergentes.json','w'), indent=1, ensure_ascii=False)
