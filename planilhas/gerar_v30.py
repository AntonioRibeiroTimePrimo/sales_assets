# -*- coding: utf-8 -*-
"""Script Personalizado v25 -> v29.

1. FPF Lista Script  -> fechamento vira seletor Aluno / Nao aluno
2. Seletores         -> opcoes do seletor oferta_lista
3. Closers (fpf)     -> PMP (BigQuery) + Link / Link_LP (arquivo de links + encurtador)
4. Leia-me           -> changelog

PMP: grupo-primo-prd.staging_google_sheets.stg_google_sheets__map_sellers_tvd
     (seller_email -> seller_pmp, is_active), casado por e-mail com a aba Closers.
Links novos: encurtados em https://r.timeprimo.com/app/create (ver CLAUDE.md).
"""
import json, sys
from copy import copy
import openpyxl

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

# --- blocos do fluxo, na ordem em que o closer usa ------------------------------
# Regra: cada bloco termina num ponto real de [AGUARDAR RESPOSTA] do doc, nunca
# numa pergunta retorica ("ok?", "certo?"). O doc tem 3 pontos de espera:
# "Faz sentido ate aqui?", o fechamento, e "O que acha?".
ABORDAGEM = (
    'Oi, [Nome]! Eu sou [Closer_artigo] [Closer], especialista do Grupo Primo.\n'
    '---\n'
    'Prazer em te conhecer, vou te ajudar com suas dúvidas sobre a Formação de '
    'Planejador Financeiro.\n'
    '---\n'
    'Vou te passar as principais informações e nossa condição válida somente hoje, ok?\n'
    '---\n'
    'A Formação de Planejador Financeiro é uma formação completa para quem quer '
    'aprender a atuar em uma das profissões mais promissoras do mercado financeiro, '
    'ajudando pessoas e famílias a organizarem a vida financeira com mais clareza, '
    'estratégia e segurança.\n'
    '---\n'
    'Nessa turma, você garante:\n'
    '• Formação completa de Planejador Financeiro;\n'
    '• 30 horas de aulas gravadas, 100% online;\n'
    '• Aulas semanais ao vivo para tirar dúvidas;\n'
    '• Formação técnica, comercial e comportamental;\n'
    '• Preparação para começar mesmo sem experiência prévia no mercado financeiro;\n'
    '• Possibilidade de seguir para o processo de associação com a Grão, empresa de '
    'planejamento financeiro do Grupo Primo;\n'
    '• Acesso à metodologia usada por planejadores do ecossistema do Grupo Primo.\n'
    '---\n'
    'E disponibilizamos para hoje uma série de bônus exclusivos para acelerar sua '
    'carreira como planejador:\n'
    '• Curso Investidor em 33 Dias;\n'
    '• Acesso ao Do Mil ao Milhão, do Thiago Nigro;\n'
    '• 1 ano de Finclass;\n'
    '• Curso Protocolo Zero Timidez - El Professor;\n'
    '• Curso preparatório CPA pela TopInvest.\n'
    '---\n'
    'Depois de concluir a formação e cumprir os pré-requisitos, você pode seguir para '
    'o processo de associação com a Grão, empresa de planejamento financeiro do Grupo '
    'Primo.\n'
    'Ou seja, você não precisa começar completamente sozinho!\n'
    '---\n'
    'Faz sentido até aqui?'
)
ATUACAO = (
    'Lembrando que a atuação pode ser 100% remota e com flexibilidade de horários.\n'
    '---\n'
    'Ou seja, o Grupo Primo está interessado em formar profissionais que realmente '
    'atuem e cresçam dentro da carreira, com a possibilidade real de remunerar '
    'R$10.000 por mês dentro de 1 ano.\n'
    '---\n'
    'Além disso, existe a possibilidade de cashback da formação para quem se associar '
    'ao Grupo Primo e alcançar 60 clientes ativos em até 12 meses!\n'
    '---\n'
    'E para o dia de hoje preparamos um desconto exclusivo na sua matrícula!'
)
NAO_E_ALUNO = (
    'Entendi, [Nome]. Esse desconto de R$500 é uma condição exclusiva para quem já é '
    'aluno do Grupo Primo.\n'
    '---\n'
    'Mas, se você tiver interesse em concluir agora, posso conversar com meu supervisor '
    'e tentar liberar essa condição pra você também, pra gente finalizar sua inscrição '
    'juntos.\n'
    '---\n'
    'O que acha?'
)
LINK = (
    'Segue o link oficial para garantir sua inscrição na Formação de Planejador '
    'Financeiro:\n'
    '---\n'
    '[link]\n'
    '---\n'
    'Assim que finalizar o pagamento, me avise, que te ajudo com os próximos passos. '
    'Combinado?'
)
JA_FALOU = (
    'Vi que você já conversou com o nosso time e chegou a avaliar a Formação de '
    'Planejador Financeiro, mas acabou não avançando naquele momento.\n'
    '---\n'
    'Antes de te mostrar a condição que estamos trabalhando hoje, me conta: o que '
    'acabou te impedindo de seguir naquele momento?'
)

BLOCOS = [
    ('1', 'Abordagem',                                    ABORDAGEM,      'SIM'),
    ('2', 'Atuação, cashback e gancho do desconto',        ATUACAO,        'SIM'),
    ('3', 'Fechamento (Aluno / Não aluno)',                '[oferta_lista]','SIM'),
    ('4', 'Não é aluno',                                   NAO_E_ALUNO,    'SIM'),
    ('5', 'Link',                                          LINK,           'SIM'),
    ('6', 'Já falou com o time (abertura alternativa)',     JA_FALOU,       'SIM'),
    ('7', 'Fechamento — Não aluno (fallback sem seletor)',  FECH_NAO_ALUNO, 'NÃO'),
    ('8', 'Fechamento — Aluno (fallback sem seletor)',      FECH_ALUNO,     'NÃO'),
]

def clone_style(dst_row, src_row=2):
    for c in range(1, 6):
        ws.cell(row=dst_row, column=c)._style = copy(ws.cell(row=src_row, column=c)._style)

for i, (atalho, nome, texto, ativo) in enumerate(BLOCOS, start=2):
    clone_style(i)
    ws.cell(row=i, column=1).value = atalho
    ws.cell(row=i, column=2).value = nome
    ws.cell(row=i, column=3).value = None
    ws.cell(row=i, column=4).value = texto
    ws.cell(row=i, column=5).value = ativo

# ---------------------------------------------------------------- 2. Seletores
ws = wb['Seletores']
for i, row in enumerate((
    ('oferta_lista', 'fpf', 'Não aluno (R$500 off)', FECH_NAO_ALUNO, 1, 'SIM'),
    ('oferta_lista', 'fpf', 'Aluno (R$1.000 off)',   FECH_ALUNO,     2, 'SIM'),
), start=2):
    for c, v in enumerate(row, start=1):
        ws.cell(row=i, column=c).value = v

# ---------------------------------------------------------------- 3. Closers
# e-mail -> (PMP, is_active), do BigQuery. guilherme.fracasso+gp e alias do
# guilherme.fracasso (mesma pessoa, GPF).
SELLERS = {
    'ext.bianca.bezerra@timeprimo.com': ('BSB', False),
    'bruna.sa@timeprimo.com': ('BPS', True),
    'ext.camila.fagundes@timeprimo.com': ('CAF', False),
    'ext.camila.ricci@timeprimo.com': ('ICC', False),
    'camila.silva@timeprimo.com': ('CCL', True),
    'ext.daiane.deperon@timeprimo.com': ('DDP', True),
    'danilo.rodrigues@timeprimo.com': ('DBR', False),
    'enzo.bonoldi@timeprimo.com': ('EZB', True),
    'ext.enzo.bonoldi@timeprimo.com': ('EZB', False),
    'ext.fernando.alvarenga@timeprimo.com': ('FAL', True),
    'ext.franciele.silva@timeprimo.com': ('FRS', False),
    'guilherme.fracasso@timeprimo.com': ('GPF', False),
    'guilherme.fracasso+gp@timeprimo.com': ('GPF', False),
    'henrique.cunha@timeprimo.com': ('HMD', True),
    'ext.henrique.cunha@timeprimo.com': ('HMD', False),
    'ext.henrique.passos@timeprimo.com': ('HDZ', True),
    'herison.silva@timeprimo.com': ('HLM', True),
    'ext.hudson.morais@timeprimo.com': ('HUM', True),
    'ext.igor.mendes@timeprimo.com': ('IGM', False),
    'ext.jackson.cardoso@timeprimo.com': ('JKC', False),
    'ext.jackson.araujo@timeprimo.com': ('JKC', True),
    'ext.joao.oliveira@timeprimo.com': ('JPS', True),
    'ext.joao@timeprimo.com': ('JPP', True),
    'julia.silva@timeprimo.com': ('JFS', False),
    'ext.lincon.nascimento@timeprimo.com': ('LCO', True),
    'ext.maressa.barros@timeprimo.com': ('MBR', True),
    'monica.rodrigues@timeprimo.com': ('MDR', True),
    'ext.nathan.castanho@timeprimo.com': ('NCS', True),
    'ext.nicoly.santos@timeprimo.com': ('NYS', False),
    'ext.pedro.ferreira@timeprimo.com': ('PHM', True),
    'ext.raphael.nunes@timeprimo.com': ('RPN', True),
    'ext.richard.pedrosa@timeprimo.com': ('RHP', False),
    'ext.ryan.xavier@timeprimo.com': ('RYX', False),
    'ext.tamiles.jesus@timeprimo.com': ('TJS', True),
    'ext.thayna.santos@timeprimo.com': ('THS', True),
    'victor.pereira@timeprimo.com': ('VPB', False),
    'ext.wesley.oliveira@timeprimo.com': ('WLO', False),
}
# PMPs com pelo menos um cadastro ativo
ATIVOS = {p for p, a in SELLERS.values() if a}

# links prontos do arquivo Links_Vendedores_2026_
CHECKOUT = 'Checkout - Formação de Planejador Financeiro'
PAGINA = 'Pagina - Formação de Planejador Financeiro'
links = {}
for r in openpyxl.load_workbook(LINKS, data_only=True)['FPF'].iter_rows(min_row=3, values_only=True):
    if r[0] and r[4]:
        links.setdefault(r[4].strip(), {})[(r[2] or '').strip()] = (r[5], r[7])

# links encurtados nesta versao (r.timeprimo.com/app/create)
NOVOS = json.load(open('novos_links.json'))

PMP_TPL = 'FIN-VIN-TVD-INT-BFIN-20250423-ORG-FPF-VT-{}'

ws = wb['Closers']
C = {'Email': 1, 'Nome': 2, 'Produto': 3, 'PMP': 4, 'Link': 6, 'Link_LP': 8}

do_arquivo, novos_usados, inativos, sem_cadastro = [], [], [], []
for row in range(2, ws.max_row + 1):
    if (ws.cell(row=row, column=C['Produto']).value or '') != 'fpf':
        continue
    email = (ws.cell(row=row, column=C['Email']).value or '').strip().lower()
    nome = (ws.cell(row=row, column=C['Nome']).value or '').strip()
    reg = SELLERS.get(email)
    if not reg:
        sem_cadastro.append('%s <%s>' % (nome, email))
        continue
    pmp, _ = reg
    ws.cell(row=row, column=C['PMP']).value = PMP_TPL.format(pmp)

    if pmp not in ATIVOS:
        inativos.append('%s (%s)' % (nome, pmp))
        for col in ('Link', 'Link_LP'):          # limpa placeholder de texto
            ws.cell(row=row, column=C[col]).value = None
        continue

    if pmp in links and CHECKOUT in links[pmp]:
        ws.cell(row=row, column=C['PMP']).value = links[pmp][CHECKOUT][1] or PMP_TPL.format(pmp)
        ws.cell(row=row, column=C['Link']).value = links[pmp][CHECKOUT][0]
        ws.cell(row=row, column=C['Link_LP']).value = links[pmp].get(PAGINA, (None,))[0]
        do_arquivo.append('%s (%s)' % (nome, pmp))
    elif pmp in NOVOS:
        ws.cell(row=row, column=C['Link']).value = NOVOS[pmp]['checkout']
        ws.cell(row=row, column=C['Link_LP']).value = NOVOS[pmp]['pagina']
        novos_usados.append('%s (%s)' % (nome, pmp))
    else:
        raise SystemExit('PMP ativo sem link: %s (%s)' % (nome, pmp))

for label, v in (('do arquivo', do_arquivo), ('encurtados agora', novos_usados),
                 ('inativos (so PMP)', inativos), ('sem cadastro no BQ', sem_cadastro)):
    print('%-20s %2d  %s' % (label, len(v), sorted(set(v))))

# ---------------------------------------------------------------- 4. Leia-me
ws = wb['Leia-me']
ws.cell(row=1, column=1).value = 'PLANILHA "Script Personalizado" -- versao 30 (31/08/2026)'
last = ws.max_row
while last > 1 and all(c.value in (None, '') for c in ws[last]):
    last -= 1

TXT = """
=======================================================================================
VERSAO 30 -- ALTERACAO MANUAL (nao veio do gerar_planilha.py; regerar sobrescreve)
=======================================================================================

--- FPF Lista de Espera: fechamento virou SELETOR Aluno / Nao aluno --------------------
Os dois docs novos ("FPF_Script_Lista_Aluno" e "FPF_Script_Lista_Nao_Aluno") sao o MESMO
fluxo; o que muda entre eles e so o bloco de fechamento (o preco). Em vez de duas abas ou
de uma segmentacao (nao ha campo no deal que diga se o lead e aluno antes da conversa), o
fechamento virou um seletor que o closer escolhe na hora:

  Atalho 3 "Fechamento (Aluno / Nao aluno)"  ->  texto = [oferta_lista]
  aba Seletores, placeholder "oferta_lista", produto "fpf", 2 opcoes:
    Nao aluno (R$500 off)   12x R$507 / R$5.097 a vista, e a pergunta "voce e aluno?"
    Aluno (R$1.000 off)     de 12x R$507 por 12x R$405,50, validade so hoje

As duas condicoes estao certas e sao ofertas diferentes -- confirmado com o Antonio em
31/08/2026. Quando a campanha acabar, desligar as 2 opcoes (coluna Ativo) e o atalho 3.

--- FPF Lista de Espera: os blocos foram REAGRUPADOS ------------------------------------
Regra aplicada: cada bloco termina num ponto real de [AGUARDAR RESPOSTA] do doc, nunca
numa pergunta retorica ("ok?"). O doc tem 3 pontos de espera -- "Faz sentido ate aqui?",
o fechamento, e "O que acha?" -- entao a aba passou de 7 para 6 blocos:

  1  Abordagem                              vai ate "Faz sentido ate aqui?"
     (era o antigo bloco 1, que parava em "...somente hoje, ok?", + o bloco 3 inteiro
      + a primeira metade do bloco 4)
  2  Atuacao, cashback e gancho do desconto  (a segunda metade do antigo bloco 4)
  3  Fechamento (Aluno / Nao aluno)          seletor
  4  Nao e aluno                             follow-up do caminho Nao aluno
  5  Link
  6  Ja falou com o time (abertura alternativa)  -- era o atalho 2; nao esta nos docs
     novos, veio de doc anterior, e foi pro fim por ser abertura alternativa, nao um
     passo do meio do fluxo.

A lista de bonus e a mesma nos dois docx (muda so a diagramacao). Ficou a diagramacao do
doc de Aluno: os 7 itens do "Nessa turma, voce garante" numa mensagem e os 5 bonus em
outra, com a chamada "E disponibilizamos para hoje uma serie de bonus exclusivos".

ATENCAO ANTES DE AVISAR OS CLOSERS: esta e a primeira vez que a aba Seletores sai
preenchida. Rode o preview/diag e confirme que [oferta_lista] e mesmo substituido -- se
nao for, o closer manda o literal "[oferta_lista]" pro cliente. Se falhar, o plano B ja
esta pronto: os atalhos 7 e 8 sao os dois fechamentos escritos por extenso, com
Ativo = NAO. Basta ligar os dois e desligar o atalho 3.
Se a coluna Placeholder esperar o token com colchetes, troque "oferta_lista" por
"[oferta_lista]" nas 2 linhas da aba Seletores (a aba Fragmentos guarda o Slot sem
colchetes, foi essa a convencao seguida aqui).

--- FPF Carrinho: NADA a mudar ---------------------------------------------------------
O doc "FPF_Script_Carrinho" foi conferido bloco a bloco contra a aba "FPF Carrinho
Script" da versao 25: mesmo texto em Abordagem, A formacao, Bonus, Fechamento, Cliente
reclamou do pagamento, Boas-vindas e Cliente deu negativa. A aba ja estava atualizada.
A "[Abordagem Fale com Especialista]" que aparece no mesmo doc e a abertura da aba
"FPF Especialista Script", que tambem ja estava correta. Os atalhos 2 e 3 (Perguntas e
Perguntas opcionais) nao estao neste doc, mas vieram de doc anterior e foram mantidos.

--- Closers: PMP e links de pagamento do FPF -------------------------------------------
PMP: casado por E-MAIL com a tabela de vendedores do BigQuery
     grupo-primo-prd.staging_google_sheets.stg_google_sheets__map_sellers_tvd
     (seller_email, seller_pmp, is_active). Todas as 36 linhas de fpf tem PMP agora.
     guilherme.fracasso+gp@ e alias de guilherme.fracasso@ (GPF).

Link    = checkout, destino "Checkout - Formacao de Planejador Financeiro"
          (off=ww2krujq, R$5.097). NAO foi usado o "Checkout ... Hibrido"
          (off=059lj05a) -- confirmar se e esse o checkout certo para estes fluxos.
Link_LP = pagina de vendas (pv.oprimorico.com.br/fpf).

  17 linhas com link ja pronto no "Links_Vendedores_2026_", aba FPF:
    CCL EZB FAL HDZ HLM HMD HUM JKC JPP MDR NCS THS

  6 linhas com link novo, encurtado em 31/08/2026 via r.timeprimo.com/app/create
  (businessUnit LANCAMENTOS, service Finclass) -- todos testados, redirecionam certo:
    BPS  checkout https://r.clique.ly/6e51f6182b   pagina https://r.clique.ly/9bfbb2745c
    JPS  checkout https://r.clique.ly/cab84d41a7   pagina https://r.clique.ly/514a7a173e
    LCO  checkout https://r.clique.ly/2cee24eb2b   pagina https://r.clique.ly/c36ba728ad
    PHM  checkout https://r.clique.ly/f803d09d34   pagina https://r.clique.ly/b1bf83137c
    TJS  checkout https://r.clique.ly/6b1ab5b839   pagina https://r.clique.ly/0a8d913122
  Padrao do parametro: FIN-VIN-TVD-INT-BFIN-20250423-ORG-FPF-VT-<PMP> em src e sck.

  14 linhas com is_active = FALSE no BigQuery: receberam o PMP, mas NAO receberam link
  (nao faz sentido gerar link de vendedor desligado). REVISAR se ainda devem estar na
  aba Closers:
    Bianca Siqueira (BSB), Camila Fagundes (CAF), Camila Ricci (ICC),
    Danilo Rodrigues (DBR), Franciele Silva (FRS), Guilherme (GPF),
    Guilherme Fracasso (GPF), Igor Mendes (IGM), Julia Fernanda Silva (JFS),
    Nicoly Santos (NYS), Richard Pedrosa (RHP), Ryan Xavier (RYX),
    Victor Biagini (VPB), Wesley Oliveira (WLO)
  Se algum voltou a vender, e so encurtar o link no mesmo padrao acima.
  (os textos "Link Guilherme" e "Link/[ID Usuario]" que estavam na coluna Link eram
   placeholder, nao link -- foram limpos.)

As 3 linhas da Thayna Santos (Valor 9000/8000/7000) receberam o mesmo link: a aba FPF do
arquivo de links so tem uma oferta, de R$5.097. Esses valores parecem sobra de outro
produto -- vale revisar.

NAO ha link de checkout para o preco com desconto (R$455,79 / R$405,50): a aba Cupons do
arquivo de links nao tem cupom de FPF. Se o desconto do seletor precisa de um checkout
proprio, ele ainda falta.
""".strip('\n').split('\n')

for i, txt in enumerate([''] + TXT, start=last + 1):
    ws.cell(row=i, column=1).value = txt

wb.save(OUT)
print('salvo em', OUT)
