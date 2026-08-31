# -*- coding: utf-8 -*-
"""Gera as linhas de fcia / atia / fce da aba Closers, para todo closer ativo."""
import json, re

ATIVOS = {  # PMP -> lista de e-mails ativos no BigQuery (o closer pode logar com qualquer um)
    'BPS': ['bruna.sa@timeprimo.com'],
    'CCL': ['camila.silva@timeprimo.com'],
    'DDP': ['ext.daiane.deperon@timeprimo.com'],
    'EZB': ['enzo.bonoldi@timeprimo.com', 'ext.enzo.bonoldi@timeprimo.com'],
    'FAL': ['ext.fernando.alvarenga@timeprimo.com'],
    'HDZ': ['ext.henrique.passos@timeprimo.com'],
    'HLM': ['herison.silva@timeprimo.com'],
    'HMD': ['henrique.cunha@timeprimo.com', 'ext.henrique.cunha@timeprimo.com'],
    'HUM': ['ext.hudson.morais@timeprimo.com'],
    'JKC': ['ext.jackson.araujo@timeprimo.com', 'ext.jackson.cardoso@timeprimo.com'],
    'JPP': ['ext.joao@timeprimo.com'],
    'JPS': ['ext.joao.oliveira@timeprimo.com'],
    'LCO': ['ext.lincon.nascimento@timeprimo.com'],
    'MBR': ['ext.maressa.barros@timeprimo.com'],
    'MDR': ['monica.rodrigues@timeprimo.com'],
    'NCS': ['ext.nathan.castanho@timeprimo.com'],
    'PHM': ['ext.pedro.ferreira@timeprimo.com'],
    'RPN': ['ext.raphael.nunes@timeprimo.com'],
    'THS': ['ext.thayna.santos@timeprimo.com'],
    'TJS': ['ext.tamiles.jesus@timeprimo.com'],
}
NOME_BQ = {'DDP': 'Daiane Deperon', 'MBR': 'Maressa Barros', 'RPN': 'Raphael Nunes'}
GENERO_BQ = {'DDP': 'F', 'MBR': 'F', 'RPN': 'M'}

PMP_TPL = {
    'fcia': 'LAN-VIN-TVD-INT-BLAN-20260617-ORG-FIA0001-FIA-{}',
    'atia': 'LAN-VIN-TVD-INT-BLAN-20260818-ORG-ATIA0002-ATIA-{}',
    'fce':  None,   # o script do FCE nao usa [link], so [Closer]
}
LP = {'fcia': 'Formação Consultor de IA Checkout LP', 'atia': None, 'fce': None}

def rotulo(destino, valor):
    """'Formação Consultor de IA - 250OFF PI*' + 6938 -> '250OFF PI* (R$ 6.938)'"""
    d = re.sub(r'^(Formação Consultor de IA|Automatizando tudo com IA)\s*', '', destino)
    d = d.replace('-', ' ').strip() or 'Checkout'
    d = re.sub(r'\s+', ' ', d)
    t = str(valor).replace('R$', '').strip()
    if re.fullmatch(r'\d+(\.\d+)?', t):          # ja vem como float: 6938.0
        v = float(t)
    elif re.fullmatch(r'[\d.]+,\d{2}', t):        # formato BR: 7.188,00
        v = float(t.replace('.', '').replace(',', '.'))
    else:
        return d
    return '%s (R$ %s)' % (d, format(int(round(v)), ',d').replace(',', '.'))

def montar(links, perfis):
    """perfis: email -> (nome, genero) vindo das linhas que ja existem na aba"""
    linhas, faltando = [], []
    for prod in ('fcia', 'atia', 'fce'):
        ofertas = links.get(prod, {})
        lp_dest = LP[prod]
        for pmp in sorted(ATIVOS):
            for email in ATIVOS[pmp]:
                nome, genero = perfis.get(email, (NOME_BQ.get(pmp), GENERO_BQ.get(pmp)))
                if not nome:
                    faltando.append((prod, pmp, email))
                    continue
                pmp_str = PMP_TPL[prod].format(pmp) if PMP_TPL[prod] else None
                if prod == 'fce':
                    linhas.append([email, nome, prod, None, None, None, genero, None, None, None])
                    continue
                lp = ofertas.get(lp_dest, {}).get(pmp) if lp_dest else None
                for dest, porpmp in ofertas.items():
                    if dest == lp_dest:
                        continue
                    link = porpmp.get(pmp)
                    if not link:
                        faltando.append((prod, pmp, dest))
                        continue
                    linhas.append([email, nome, prod, pmp_str, ROT[prod][dest], link,
                                   genero, lp, None, None])
    return linhas, faltando

if __name__ == '__main__':
    import openpyxl
    links = json.load(open('links_gerados.json'))
    inv = json.load(open('inventario.json'))
    ROT = {p: {o['destino']: rotulo(o['destino'], o['valor']) for o in d['ofertas']}
           for p, d in inv.items()}
    globals()['ROT'] = ROT
    ws = openpyxl.load_workbook('Script_Personalizado_30.xlsx', data_only=True)['Closers']
    perfis = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and r[1]:
            perfis.setdefault(r[0].strip().lower(), (r[1], r[6]))
    linhas, faltando = montar(links, perfis)
    for p in ('fcia', 'atia', 'fce'):
        n = len([l for l in linhas if l[2] == p])
        print('%-5s %3d linhas' % (p, n))
    print('total', len(linhas), '| faltando', faltando[:10])
    print('rotulos fcia:', sorted(set(l[4] for l in linhas if l[2] == 'fcia')))
    print('rotulos atia:', sorted(set(l[4] for l in linhas if l[2] == 'atia')))
    json.dump(linhas, open('closers_extra.json', 'w'), ensure_ascii=False)
