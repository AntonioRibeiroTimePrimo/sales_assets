# -*- coding: utf-8 -*-
"""Encurta os links de FCIA e ATIA que faltam para os closers ativos.
Idempotente: reaproveita o que ja esta em links_gerados.json."""
import os, json, time, urllib.parse as up, requests

TOK = os.environ['ENCURTADOR_TOKEN']
H = {'accept': '*/*', 'authorization': 'Manager ' + TOK, 'content-type': 'application/json',
     'origin': 'https://gestao.timeprimo.com', 'referer': 'https://gestao.timeprimo.com/',
     'service': 'Finclass'}

PMP_TPL = {
    'fcia': 'LAN-VIN-TVD-INT-BLAN-20260617-ORG-FIA0001-FIA-{}',
    'atia': 'LAN-VIN-TVD-INT-BLAN-20260818-ORG-ATIA0002-ATIA-{}',
}
# closers com is_active = true no BigQuery
ATIVOS = ['BPS','CCL','DDP','EZB','FAL','HDZ','HLM','HMD','HUM','JKC','JPP','JPS',
          'LCO','MBR','MDR','NCS','PHM','RPN','THS','TJS']

inv = json.load(open('inventario.json'))
CACHE = 'links_gerados.json'
out = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def parametriza(base, pmp):
    sep = '&' if up.urlsplit(base).query else '?'
    return '%s%ssrc=%s&sck=%s' % (base, sep, pmp, pmp)

def encurta(url, desc):
    for tent in range(4):
        try:
            r = requests.post('https://r.timeprimo.com/app/create', headers=H, timeout=40,
                              json={'longURL': url, 'businessUnit': 'LANCAMENTOS',
                                    'description': desc})
            d = r.json()
            if d.get('status'):
                return d['data']['short']['shortURL']
            print('  ! resposta sem status:', str(d)[:160])
        except Exception as e:
            print('  ! erro:', e)
        time.sleep(2 ** tent)
    raise SystemExit('falhou em ' + desc)

novos = reaproveitados = 0
for prod, dados in inv.items():
    out.setdefault(prod, {})
    for of in dados['ofertas']:
        dest = of['destino']
        out[prod].setdefault(dest, {})
        for pmp in ATIVOS:
            if pmp in out[prod][dest]:
                continue
            pronto = of['short'].get(pmp)
            if pronto:                       # ja existia no arquivo de links
                out[prod][dest][pmp] = pronto
                reaproveitados += 1
                continue
            url = parametriza(of['base'], PMP_TPL[prod].format(pmp))
            out[prod][dest][pmp] = encurta(url, '%s %s %s' % (prod.upper(), dest, pmp))
            novos += 1
            if novos % 10 == 0:
                json.dump(out, open(CACHE, 'w'), indent=1, ensure_ascii=False)
                print('  ... %d novos' % novos, flush=True)
json.dump(out, open(CACHE, 'w'), indent=1, ensure_ascii=False)
print('novos encurtados:', novos, '| reaproveitados do arquivo:', reaproveitados)
