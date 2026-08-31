# -*- coding: utf-8 -*-
"""Atualiza a planilha Script Personalizado (v25 -> v28).

1. FPF Lista Script  -> fechamento vira seletor Aluno/Nao aluno
2. Seletores         -> opcoes do seletor oferta_lista
3. Closers (fpf)     -> preenche PMP / Link / Link_LP
4. Leia-me           -> changelog desta versao
"""
import openpyxl, re, sys
from copy import copy

SRC = '/root/.claude/uploads/fc833a99-1395-53a1-b261-fc0af633860c/3dacfb7f-Script_Personalizado_25.xlsx'
LINKS = '/root/.claude/uploads/fc833a99-1395-53a1-b261-fc0af633860c/59749727-Links_Vendedores_2026_.xlsx'
OUT = sys.argv[1]

wb = openpyxl.load_workbook(SRC)

# ---------------------------------------------------------------- 1. FPF Lista
ws = wb['FPF Lista Script']

FECH_NAO_ALUNO = (
    'O valor para inscrição na Formação de Planejador Financeiro fica por:\n'
    '---\n'
    '12x de R$507 ou R$5.097 à vista para não alunos\n'
    '12x de R$ 455,79 ou R$ 4.582,20 à vista para alunos\n'
    '---\n'
    'Você é ou já foi aluno do Grupo Primo?'
)
FECH_ALUNO = (
    'O valor para inscrição na Formação de Planejador Financeiro, com o desconto '
    'de R$1.000 liberado para hoje, fica por:\n'
    '---\n'
    'De 12x de R$ 507,00\n'
    'Por *12x de R$ 405,50*\n'
    '---\n'
    'Lembrando que este desconto é válido somente para hoje!\n'
    '---\n'
    'Posso gerar seu link de inscrição?'
)

# atalho 5 passa a ser o seletor
ws.cell(row=6, column=2).value = 'Fechamento (Aluno / Não aluno)'
ws.cell(row=6, column=4).value = '[oferta_lista]'

# fallback: os dois fechamentos literais, desligados
def clone_style(dst_row, src_row=6):
    for c in range(1, 6):
        dst = ws.cell(row=dst_row, column=c)
        dst._style = copy(ws.cell(row=src_row, column=c)._style)

for row, atalho, nome, texto in (
    (9,  '8', 'Fechamento — Não aluno (fallback sem seletor)', FECH_NAO_ALUNO),
    (10, '9', 'Fechamento — Aluno (fallback sem seletor)', FECH_ALUNO),
):
    clone_style(row)
    ws.cell(row=row, column=1).value = atalho
    ws.cell(row=row, column=2).value = nome
    ws.cell(row=row, column=3).value = None
    ws.cell(row=row, column=4).value = texto
    ws.cell(row=row, column=5).value = 'NÃO'

# ---------------------------------------------------------------- 2. Seletores
ws = wb['Seletores']
seletores = [
    ('oferta_lista', 'fpf', 'Não aluno (R$500 off)',   FECH_NAO_ALUNO, 1, 'SIM'),
    ('oferta_lista', 'fpf', 'Aluno (R$1.000 off)',     FECH_ALUNO,     2, 'SIM'),
]
for i, row in enumerate(seletores, start=2):
    for c, v in enumerate(row, start=1):
        ws.cell(row=i, column=c).value = v

# ---------------------------------------------------------------- 3. Closers
lwb = openpyxl.load_workbook(LINKS, data_only=True)
lws = lwb['FPF']

CHECKOUT = 'Checkout - Formação de Planejador Financeiro'
PAGINA = 'Pagina - Formação de Planejador Financeiro'

links = {}   # pmp -> {destino: (short, pmp_string)}
for r in lws.iter_rows(min_row=3, values_only=True):
    if not r[0] or not r[4]:
        continue
    links.setdefault(r[4].strip(), {})[(r[2] or '').strip()] = (r[5], r[7])

# nome do closer -> PMP (coluna PMP das linhas l2x da propria aba Closers + aba
# Vendedores da planilha de links). Guilherme Penariol foi ignorado: a linha l2x
# dele carrega o PMP da Bruna (BPS), erro de cadastro.
NOME_PMP = {
    'Bianca Siqueira': 'BSB',
    'Bruna Palmieri': 'BPS',
    'Camila Silva': 'CCL',
    'Enzo Bonoldi': 'EZB',
    'Fernando Alvarenga': 'FAL',
    'Henrique Cunha': 'HMD',
    'Henrique Diniz': 'HDZ',
    'Herison da Silva': 'HLM',
    'Hudson Morais': 'HUM',
    'Jackson Cardoso': 'JKC',
    'João Oliveira': 'JPS',
    'João Pedro Pacheco': 'JPP',
    'Lincon Nascimento': 'LCO',
    'Monica Rodrigues': 'MDR',
    'Nathan Castanho': 'NCS',
    'Pedro Henrique Meira Ferreira': 'PHM',
    'Tamiles Jesus': 'TJS',
    'Thayna Santos': 'THS',
}

BASE_CHECKOUT = 'https://pay.hotmart.com/J96484696I?checkoutMode=10&off=ww2krujq'
BASE_PAGINA = 'https://pv.oprimorico.com.br/fpf/index/'
PMP_TPL = 'FIN-VIN-TVD-INT-BFIN-20250423-ORG-FPF-VT-{}'

ws = wb['Closers']
COL = {'Email': 1, 'Nome': 2, 'Produto': 3, 'PMP': 4, 'Valor': 5, 'Link': 6,
       'Genero': 7, 'Link_LP': 8}

preenchidos, gerados, sem_pmp = [], [], []
for row in range(2, ws.max_row + 1):
    if (ws.cell(row=row, column=COL['Produto']).value or '') != 'fpf':
        continue
    nome = (ws.cell(row=row, column=COL['Nome']).value or '').strip()
    pmp = NOME_PMP.get(nome)
    if not pmp:
        sem_pmp.append(nome)
        # limpa os placeholders de texto que estavam na coluna Link
        v = ws.cell(row=row, column=COL['Link']).value
        if v and not str(v).startswith('http'):
            ws.cell(row=row, column=COL['Link']).value = None
        continue

    pmp_str = PMP_TPL.format(pmp)
    if pmp in links and CHECKOUT in links[pmp]:
        link = links[pmp][CHECKOUT][0]
        pmp_str = links[pmp][CHECKOUT][1] or pmp_str
        lp = links[pmp].get(PAGINA, (None, None))[0]
        preenchidos.append(nome)
    else:
        link = '{}&src={}&sck={}'.format(BASE_CHECKOUT, pmp_str, pmp_str)
        lp = '{}?src={}&sck={}'.format(BASE_PAGINA, pmp_str, pmp_str)
        gerados.append('%s (%s)' % (nome, pmp))

    ws.cell(row=row, column=COL['PMP']).value = pmp_str
    ws.cell(row=row, column=COL['Link']).value = link
    ws.cell(row=row, column=COL['Link_LP']).value = lp

print('preenchidos do arquivo de links:', len(preenchidos), sorted(set(preenchidos)))
print('gerados (falta encurtar):', len(gerados), sorted(set(gerados)))
print('sem PMP conhecido:', len(sem_pmp), sorted(set(sem_pmp)))

# ---------------------------------------------------------------- 4. Leia-me
ws = wb['Leia-me']
ws.cell(row=1, column=1).value = 'PLANILHA "Script Personalizado" -- versao 28 (31/08/2026)'

# acha a primeira linha vazia no fim
last = ws.max_row
while last > 1 and all(c.value in (None, '') for c in ws[last]):
    last -= 1

novo = [
    '',
    '=======================================================================================',
    'VERSAO 28 -- ALTERACAO MANUAL (nao veio do gerar_planilha.py; regerar sobrescreve)',
    '=======================================================================================',
    '',
    '--- FPF Lista de Espera: fechamento virou SELETOR Aluno / Nao aluno --------------------',
    'Os dois docs novos ("FPF_Script_Lista_Aluno" e "FPF_Script_Lista_Nao_Aluno") sao o MESMO',
    'fluxo; o que muda entre eles e so o bloco de fechamento (o preco). Em vez de duas abas ou',
    'de uma segmentacao (nao ha campo no deal que diga se o lead e aluno antes da conversa), o',
    'fechamento virou um seletor que o closer escolhe na hora:',
    '',
    '  Atalho 5 "Fechamento (Aluno / Nao aluno)"  ->  texto = [oferta_lista]',
    '  aba Seletores, placeholder "oferta_lista", produto "fpf", 2 opcoes:',
    '    Nao aluno (R$500 off)   12x R$507 / R$5.097 a vista, e a pergunta "voce e aluno?"',
    '    Aluno (R$1.000 off)     de 12x R$507 por 12x R$405,50, validade so hoje',
    '',
    'O atalho 6 ("Nao e aluno") continua sendo o follow-up do caminho Nao aluno.',
    'Os atalhos 1 a 4 e o 7 nao mudaram: conferidos linha a linha contra os dois docx, zero',
    'divergencia. A lista de bonus e a mesma nos dois docs (muda so a diagramacao), entao o',
    'bloco 3 seguiu unico.',
    '',
    'ATENCAO ANTES DE AVISAR OS CLOSERS: esta e a primeira vez que a aba Seletores sai vazia.',
    'Rode o preview/diag e confirme que [oferta_lista] e mesmo substituido -- se nao for, o',
    'closer manda o literal "[oferta_lista]" pro cliente. Se falhar, o plano B ja esta pronto:',
    'os atalhos 8 e 9 sao os dois fechamentos escritos por extenso, com Ativo = NAO. Basta',
    'ligar os dois (2 celulas) e desligar o atalho 5.',
    'Se a coluna Placeholder esperar o token com colchetes, troque "oferta_lista" por',
    '"[oferta_lista]" nas 2 linhas da aba Seletores (a aba Fragmentos guarda o Slot sem',
    'colchetes, foi essa a convencao seguida aqui).',
    '',
    'DIVERGENCIA DE PRECO ENTRE OS DOIS DOCS -- confirmar com o time:',
    '  doc Nao Aluno diz que o preco de ALUNO e 12x R$455,79 (desconto de R$500)',
    '  doc Aluno     diz que o preco de ALUNO e 12x R$405,50 (desconto de R$1.000)',
    'Os dois foram para o seletor exatamente como estao nos docs. Sao numeros que vao pro',
    'cliente: se a condicao certa for so uma, desligar a outra opcao (coluna Ativo).',
    'Quando a campanha acabar, desligar as 2 opcoes e o atalho 5.',
    '',
    '--- FPF Carrinho: NADA a mudar ---------------------------------------------------------',
    'O doc "FPF_Script_Carrinho" foi conferido bloco a bloco contra a aba "FPF Carrinho',
    'Script" da versao 25: mesmo texto em Abordagem, A formacao, Bonus, Fechamento, Cliente',
    'reclamou do pagamento, Boas-vindas e Cliente deu negativa. A aba ja estava atualizada.',
    'A "[Abordagem Fale com Especialista]" que aparece no mesmo doc e a abertura da aba',
    '"FPF Especialista Script", que tambem ja estava correta. Os atalhos 2 e 3 (Perguntas e',
    'Perguntas opcionais) nao estao neste doc, mas vieram de doc anterior e foram mantidos.',
    '',
    '--- Closers: links de pagamento do FPF -------------------------------------------------',
    'Fonte: "Links_Vendedores_2026_.xlsx", aba FPF (12 PMPs) + aba Vendedores.',
    'Preenchidas as colunas PMP, Link (checkout) e Link_LP (pagina de vendas).',
    'Link  = destino "Checkout - Formacao de Planejador Financeiro" (off=ww2krujq, R$5.097).',
    '        NAO foi usado o "Checkout ... Hibrido" (off=059lj05a) -- confirmar se e esse o',
    '        checkout certo para estes fluxos.',
    '',
    '  17 linhas com link encurtado (r.clique.ly) vindo direto do arquivo:',
    '    CCL EZB FAL HDZ HLM HMD HUM JKC JPP MDR NCS THS',
    '',
    '  6 linhas com link PARAMETRIZADO LONGO, montado no padrao src/sck (FALTA ENCURTAR):',
    '    BPS BSB JPS LCO PHM TJS  -- estes PMPs nao tem linha na aba FPF do arquivo de links.',
    '    O padrao usado foi FIN-VIN-TVD-INT-BFIN-20250423-ORG-FPF-VT-<PMP>, igual aos outros.',
    '',
    '  13 linhas SEM PMP conhecido, seguem em branco -- nao da pra inventar o codigo, ele tem',
    '  de bater com o cadastro:',
    '    Camila Fagundes, Camila Ricci, Danilo Rodrigues, Franciele Silva, Guilherme,',
    '    Guilherme Fracasso, Igor Mendes, Julia Fernanda Silva, Nicoly Santos,',
    '    Richard Pedrosa, Ryan Xavier, Victor Biagini, Wesley Oliveira',
    '  (os textos "Link Guilherme" e "Link/[ID Usuario]" que estavam na coluna Link eram',
    '   placeholder, nao link -- foram limpos.)',
    '',
    'As 3 linhas da Thayna Santos (Valor 9000/8000/7000) receberam o mesmo link: a aba FPF do',
    'arquivo de links so tem uma oferta, de R$5.097. Esses valores parecem sobra de outro',
    'produto -- vale revisar.',
    '',
    'NAO ha link de checkout para o preco com desconto (R$455,79 / R$405,50): a aba Cupons do',
    'arquivo de links nao tem cupom de FPF. Se o desconto do seletor precisa de um checkout',
    'proprio, ele ainda falta.',
]
for i, txt in enumerate(novo, start=last + 1):
    ws.cell(row=i, column=1).value = txt

wb.save(OUT)
print('salvo em', OUT)
