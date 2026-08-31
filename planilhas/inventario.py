# -*- coding: utf-8 -*-
"""Le FIA0001 e ATIA0002 e monta: base de cada oferta + link encurtado ja existente."""
import openpyxl, collections, json, re, urllib.parse as up

LINKS = '/root/.claude/uploads/fc833a99-1395-53a1-b261-fc0af633860c/59749727-Links_Vendedores_2026_.xlsx'
wb = openpyxl.load_workbook(LINKS, data_only=True)

def strip_src(u):
    """tira src/sck do link parametrizado, sobra a base da oferta"""
    p = up.urlsplit(u)
    qs = [(k, v) for k, v in up.parse_qsl(p.query, keep_blank_values=True)
          if k not in ('src', 'sck')]
    return up.urlunsplit((p.scheme, p.netloc, p.path, up.urlencode(qs), ''))

def ler(sheet, tpl_re):
    ws = wb[sheet]
    base, valor, short, pmp_tpl = {}, {}, collections.defaultdict(dict), None
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0] or not r[5]:
            continue
        d = (r[2] or '').strip()
        pmp = r[5].strip()
        if r[8] and d not in base:
            base[d] = strip_src(r[8])
            valor[d] = r[3]
        s = r[7] or r[6]
        if s and isinstance(s, str) and s.startswith('http') and pmp not in short[d]:
            short[d][pmp] = s
        if r[9] and not pmp_tpl:
            pmp_tpl = re.sub(tpl_re, '{}', r[9])
    return base, valor, dict(short), pmp_tpl

fia = ler('FIA0001', r'-[A-Z]{3}$')
atia = ler('ATIA0002', r'-[A-Z]{3}$')

out = {}
for nome, (base, valor, short, tpl) in (('fcia', fia), ('atia', atia)):
    print('=' * 25, nome, ' pmp_tpl =', tpl)
    out[nome] = {'pmp_tpl': tpl, 'ofertas': []}
    for d in base:
        print('  %-50s %-12s tem %2d  %s' % (d[:50], valor[d], len(short.get(d, {})),
                                             sorted(short.get(d, {}))))
        print('       %s' % base[d])
        out[nome]['ofertas'].append({'destino': d, 'base': base[d],
                                     'valor': str(valor[d]), 'short': short.get(d, {})})
json.dump(out, open('inventario.json', 'w'), indent=1, ensure_ascii=False)
