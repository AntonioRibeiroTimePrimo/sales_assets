"""Gera 'Controle de Reunioes - SDR Educacao.xlsx'.

Mesma arquitetura do Controle LDX (aba por SDR -> espelho 'Agendamentos' ->
Dashboard + Config), com tres mudancas pedidas:
  1. coluna unica 'Quando (data e hora)' em Agendamentos, para o Closer ordenar
     em ordem crescente dentro da visualizacao de filtro (um clique, um criterio);
  2. colunas Produto e Origem preenchidas pelo SDR (lista suspensa vinda da Config);
  3. Dashboard com quebra por Produto e por Origem.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as gcl

# ---------------------------------------------------------------- parametros
N_SDR = 10
LINHAS_POR_SDR = 500          # linhas 4..503 em cada aba de SDR
PRIMEIRA_LINHA_SDR = 4
N_CLOSERS = 15
N_PRODUTOS = 12
N_ORIGENS = 12
DIAS_DASH = 45

SDRS = [f"SDR {i:02d}" for i in range(1, N_SDR + 1)]
CLOSERS = ["Closer 01", "Closer 02", "Closer 03", "Closer 04", "Closer 05"]
COMPARECEU = ["REALIZADA", "NO-SHOW", "REAGENDADA", "CANCELADA"]
RESULTADO = ["VENDA", "NAO VENDEU", "EM NEGOCIACAO", "SEM CONTATO"]
PRODUTOS = [f"PRODUTO {i}" for i in range(1, 9)]
ORIGENS = ["INBOUND", "OUTBOUND", "INDICACAO", "EVENTO", "WEBINAR",
           "TRAFEGO PAGO", "ORGANICO", "REMARKETING", "LISTA FRIA", "BASE ANTIGA"]

# ---------------------------------------------------------------- estilo
NAVY = "1F3864"
LARANJA = "C55A11"
CINZA = "F2F2F2"
AMARELO = "FFF2CC"

f_hdr_navy = Font(name="Calibri", sz=11, bold=True, color="FFFFFF")
f_hdr_lar = Font(name="Calibri", sz=11, bold=True, color="FFFFFF")
f_norm = Font(name="Calibri", sz=11)
f_bold = Font(name="Calibri", sz=11, bold=True)
f_nota = Font(name="Calibri", sz=11, color="555555")
f_link = Font(name="Calibri", sz=11, color="0000FF")
f_h1 = Font(name="Calibri", sz=16, bold=True, color=NAVY)
f_h2 = Font(name="Calibri", sz=13, bold=True, color=NAVY)
f_kpi = Font(name="Calibri", sz=14, bold=True)

fill_navy = PatternFill("solid", fgColor=NAVY)
fill_lar = PatternFill("solid", fgColor=LARANJA)
fill_cinza = PatternFill("solid", fgColor=CINZA)
fill_amar = PatternFill("solid", fgColor=AMARELO)

center = Alignment(horizontal="center", vertical="center", wrap_text=True)
borda_fina = Border(*[Side(style="thin", color="D9D9D9")] * 4)

FMT_DATA = "dd/mm/yyyy"
FMT_HORA = "hh:mm"
FMT_DTHORA = "dd/mm/yyyy hh:mm"
FMT_BRL = "R$ #,##0.00"
FMT_BRL0 = "R$ #,##0"
FMT_PCT = "0.0%"

wb = openpyxl.Workbook()
wb.remove(wb.active)


def q(nome):
    """Nome de aba pronto para referencia (aspas quando tem espaco)."""
    return f"'{nome}'" if " " in nome or "-" in nome else nome


def header(ws, linha, titulos, fill):
    for i, t in enumerate(titulos, start=1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font = f_hdr_navy
        c.fill = fill
        c.alignment = center
    ws.row_dimensions[linha].height = 30


# ================================================================= LEIA-ME
ws = wb.create_sheet("LEIA-ME")
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 150
linhas = [
    ("Controle de reunioes -- SDR Educacao -- como usar", f_h1),
    ("", None),
    ("1) SDR -- a aba com o seu nome", f_bold),
    ("Uma linha por agendamento, sempre acrescentando embaixo: data, hora, nome do lead, telefone, link da conversa, "
     "PRODUTO, ORIGEM e o Closer (todas listas suspensas). Produto e Origem sao obrigatorios -- e por eles que o "
     "Dashboard mostra o que cada canal e cada produto esta gerando.", f_norm),
    ("EXEMPLO de linha: 15/09/2026 | 14:30 | Maria Souza | 11 98888 7777 | https://app.useclint.com/chat/xxxx | "
     "PRODUTO 1 | INBOUND | Closer 01 | lead ja assistiu a aula 2", f_nota),
    ("", None),
    ("2) Closer -- aba 'Agendamentos', colunas LARANJA", f_bold),
    ("Suas reunioes estao na aba 'Agendamentos'. Pra ver so as suas: Dados > Visualizacoes de filtro > Criar nova "
     "visualizacao de filtro; no funil da coluna 'Closer' deixe so o seu nome. Isso e por pessoa -- nao muda o que os "
     "outros veem.", f_norm),
    ("PRA ORDENAR POR DATA E HORARIO: dentro da SUA visualizacao de filtro, clique no funil da coluna "
     "'Quando (data e hora)' > Classificar de A a Z. Essa coluna junta data + horario num valor so, entao um clique "
     "ja deixa tudo em ordem crescente -- primeiro a reuniao mais proxima. Ordenar dentro de uma visualizacao de "
     "filtro muda so a SUA tela: nao mexe na ordem real das linhas e nao quebra nada.", f_norm),
    ("Dica: no mesmo funil de 'Quando', em 'Filtrar por condicao' escolha 'A data e posterior a' > 'hoje' pra esconder "
     "o que ja passou. As linhas em branco somem sozinhas quando voce ordena.", f_nota),
    ("Marque na MESMA LINHA da reuniao: Compareceu?, Nova data, Resultado, Valor e Observacao. Como a marcacao mora na "
     "linha da reuniao, ela nunca se solta dela -- mesmo com a tela ordenada.", f_norm),
    ("", None),
    ("3) Gestao -- aba 'Dashboard'", f_bold),
    ("Ajuste o periodo em B2 (inicial) e B3 (final). KPIs gerais e quebra por SDR, por Closer, por PRODUTO, por ORIGEM "
     "e por dia -- tudo respeita o periodo.", f_norm),
    ("FILTRO POR DIA: escreva uma data em B4 e o Dashboard inteiro passa a mostrar so aquele dia (KPIs, SDR, Closer, "
     "produto e origem). Pra voltar ao periodo cheio, apague B4 com a tecla DELETE. B5/C5 mostram o periodo que esta "
     "valendo. A tabela 'Por dia' tem funil proprio: da pra ordenar os dias ou esconder os dias zerados.", f_norm),
    ("", None),
    ("4) Config -- listas suspensas", f_bold),
    ("Produtos (coluna E) e Origens (coluna F) entram na Config com valores de EXEMPLO. Troque pelos nomes reais antes "
     "de soltar pro time: as listas suspensas e o Dashboard seguem sozinhos. Closer novo: acrescente na coluna B. "
     "SDR novo: renomeie uma aba vaga E o nome na coluna A (os dois iguais).", f_norm),
    ("", None),
    ("REGRAS QUE NAO PODEM SER QUEBRADAS", Font(name="Calibri", sz=11, bold=True, color="C00000")),
    ("Pra limpar uma celula use so a tecla DELETE. Nunca 'excluir celula', nunca 'excluir linha', nunca ordenar a aba "
     "'Agendamentos' pela barra de menu (Dados > Classificar intervalo) -- ordene SEMPRE dentro da sua visualizacao de "
     "filtro. Nunca arraste o quadradinho azul sobre area cinza. Nao digite nas colunas cinza nem na aba 'Dashboard'.",
     f_norm),
]
for i, (txt, fnt) in enumerate(linhas, start=1):
    c = ws.cell(row=i, column=1, value=txt or None)
    if fnt:
        c.font = fnt
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[i].height = 30 if txt and len(txt) > 120 else 16

# ================================================================= abas SDR
COLS_SDR = ["Data da reuniao", "Hora", "Nome do lead", "Telefone / WhatsApp",
            "Link da conversa", "Produto", "Origem", "Closer", "Observacao"]
LARG_SDR = [15.7, 9.7, 28.7, 20.7, 46.7, 18.7, 16.7, 16.7, 34.7]
ULT_LINHA_SDR = PRIMEIRA_LINHA_SDR + LINHAS_POR_SDR - 1

for idx, sdr in enumerate(SDRS, start=1):
    ws = wb.create_sheet(sdr)
    ws["A1"] = "SDR:"
    ws["A1"].font = f_bold
    ws["B1"] = f"=Config!$A${idx + 1}"
    ws["B1"].font = f_bold
    ws["D1"] = ("Uma linha por agendamento, sempre acrescentando embaixo. Produto e Origem sao obrigatorios. "
                "Pra limpar uma celula use so a tecla DELETE -- nunca 'excluir celula' nem 'excluir linha'.")
    ws["D1"].font = f_nota
    header(ws, 3, COLS_SDR, fill_navy)
    for i, w in enumerate(LARG_SDR, start=1):
        ws.column_dimensions[gcl(i)].width = w
    for r in range(PRIMEIRA_LINHA_SDR, ULT_LINHA_SDR + 1):
        ws.cell(row=r, column=1).number_format = FMT_DATA
        ws.cell(row=r, column=2).number_format = FMT_HORA
        ws.cell(row=r, column=2).alignment = Alignment(horizontal="center")
        ws.cell(row=r, column=5).font = f_link
    ws.freeze_panes = "A4"

    dv_prod = DataValidation(type="list", formula1=f"Config!$E$2:$E${N_PRODUTOS + 1}", allow_blank=True)
    dv_orig = DataValidation(type="list", formula1=f"Config!$F$2:$F${N_ORIGENS + 1}", allow_blank=True)
    dv_clos = DataValidation(type="list", formula1=f"Config!$B$2:$B${N_CLOSERS + 1}", allow_blank=True)
    for dv, col in ((dv_prod, "F"), (dv_orig, "G"), (dv_clos, "H")):
        ws.add_data_validation(dv)
        dv.add(f"{col}{PRIMEIRA_LINHA_SDR}:{col}{ULT_LINHA_SDR}")

# ================================================================= Agendamentos
COLS_AG = [
    ("ID", 11.7, None, "mirror"),
    ("SDR", 16.7, None, "mirror"),
    ("Quando (data e hora)", 19.0, FMT_DTHORA, "mirror"),
    ("Data da reuniao", 13.5, FMT_DATA, "mirror"),
    ("Hora", 9.7, FMT_HORA, "mirror"),
    ("Nome do lead", 28.7, None, "mirror"),
    ("Telefone / WhatsApp", 20.7, None, "mirror"),
    ("Link da conversa", 50.0, None, "mirror"),
    ("Produto", 18.7, None, "mirror"),
    ("Origem", 16.7, None, "mirror"),
    ("Closer", 14.7, None, "mirror"),
    ("Observacao do SDR", 26.7, None, "mirror"),
    ("Compareceu?", 16.7, None, "closer"),
    ("Nova data (se reagendou)", 20.0, FMT_DATA, "closer"),
    ("Resultado", 17.7, None, "closer"),
    ("Valor da venda", 14.0, FMT_BRL, "closer"),
    ("Observacao do Closer", 44.9, None, "closer"),
]
C_ID, C_SDR, C_QUANDO, C_DATA, C_HORA = 1, 2, 3, 4, 5
C_LEAD, C_TEL, C_LINK, C_PROD, C_ORIG, C_CLOSER, C_OBS = 6, 7, 8, 9, 10, 11, 12
C_COMP, C_NOVA, C_RES, C_VALOR, C_OBSC = 13, 14, 15, 16, 17
L = {i: gcl(i) for i in range(1, 18)}

ws = wb.create_sheet("Agendamentos")
for i, (titulo, larg, fmt, tipo) in enumerate(COLS_AG, start=1):
    c = ws.cell(row=1, column=i, value=titulo)
    c.font = f_hdr_navy if tipo == "mirror" else f_hdr_lar
    c.fill = fill_navy if tipo == "mirror" else fill_lar
    c.alignment = center
    ws.column_dimensions[gcl(i)].width = larg
ws.row_dimensions[1].height = 30

linha = 2
for idx, sdr in enumerate(SDRS, start=1):
    ref = q(sdr)
    for j in range(LINHAS_POR_SDR):
        rs = PRIMEIRA_LINHA_SDR + j                      # linha na aba do SDR
        vazio = f'{ref}!$C{rs}=""'
        def mir(expr):
            return f'=IF({vazio},"",{expr})'
        ws.cell(row=linha, column=C_ID, value=mir(f'"S{idx:02d}-{j + 1:04d}"'))
        ws.cell(row=linha, column=C_SDR, value=mir(f"{ref}!$B$1"))
        ws.cell(row=linha, column=C_QUANDO, value=mir(f"{ref}!$A{rs}+{ref}!$B{rs}"))
        ws.cell(row=linha, column=C_DATA, value=mir(f"{ref}!$A{rs}"))
        ws.cell(row=linha, column=C_HORA, value=mir(f"{ref}!$B{rs}"))
        ws.cell(row=linha, column=C_LEAD, value=mir(f"{ref}!$C{rs}"))
        ws.cell(row=linha, column=C_TEL, value=mir(f"{ref}!$D{rs}"))
        ws.cell(row=linha, column=C_LINK, value=mir(f"{ref}!$E{rs}"))
        ws.cell(row=linha, column=C_PROD, value=mir(f"{ref}!$F{rs}"))
        ws.cell(row=linha, column=C_ORIG, value=mir(f"{ref}!$G{rs}"))
        ws.cell(row=linha, column=C_CLOSER, value=mir(f"{ref}!$H{rs}"))
        ws.cell(row=linha, column=C_OBS, value=mir(f"{ref}!$I{rs}"))
        for i in range(1, 18):
            c = ws.cell(row=linha, column=i)
            c.font = f_norm
            if i <= C_OBS:
                c.fill = fill_cinza
            fmt = COLS_AG[i - 1][2]
            if fmt:
                c.number_format = fmt
            if i in (C_HORA, C_QUANDO):
                c.alignment = Alignment(horizontal="center")
        linha += 1

ULT_AG = linha - 1
ws.freeze_panes = "G2"
ws.auto_filter.ref = f"A1:{L[17]}{ULT_AG}"
dv_comp = DataValidation(type="list", formula1=f"Config!$C$2:$C${len(COMPARECEU) + 1}", allow_blank=True)
dv_res = DataValidation(type="list", formula1=f"Config!$D$2:$D${len(RESULTADO) + 1}", allow_blank=True)
ws.add_data_validation(dv_comp)
dv_comp.add(f"{L[C_COMP]}2:{L[C_COMP]}{ULT_AG}")
ws.add_data_validation(dv_res)
dv_res.add(f"{L[C_RES]}2:{L[C_RES]}{ULT_AG}")

AG = "Agendamentos!"
R_DATA = f"{AG}${L[C_DATA]}$2:${L[C_DATA]}${ULT_AG}"
R_SDR = f"{AG}${L[C_SDR]}$2:${L[C_SDR]}${ULT_AG}"
R_CLOSER = f"{AG}${L[C_CLOSER]}$2:${L[C_CLOSER]}${ULT_AG}"
R_PROD = f"{AG}${L[C_PROD]}$2:${L[C_PROD]}${ULT_AG}"
R_ORIG = f"{AG}${L[C_ORIG]}$2:${L[C_ORIG]}${ULT_AG}"
R_COMP = f"{AG}${L[C_COMP]}$2:${L[C_COMP]}${ULT_AG}"
R_RES = f"{AG}${L[C_RES]}$2:${L[C_RES]}${ULT_AG}"
R_VAL = f"{AG}${L[C_VALOR]}$2:${L[C_VALOR]}${ULT_AG}"
# Periodo aplicado do Dashboard: B5 = inicio, C5 = fim (B4 preenchido = dia unico).
PER = f'{R_DATA},">="&$B$5,{R_DATA},"<="&$C$5'

# ================================================================= Dashboard
ws = wb.create_sheet("Dashboard")
ws.sheet_view.showGridLines = False
ws["A1"] = "Dashboard -- Funil SDR x Closer (Educacao)"
ws["A1"].font = f_h1
ws["A2"] = "Data inicial"
ws["A3"] = "Data final"
ws["A4"] = "Ver um unico dia"
ws["A5"] = "Periodo aplicado"
for cell in ("A2", "A3", "A4", "A5"):
    ws[cell].font = f_bold
ws["B2"] = "=TODAY()-30"
ws["B3"] = "=TODAY()+60"
for cell in ("B2", "B3", "B4"):
    ws[cell].number_format = FMT_DATA
    ws[cell].fill = fill_amar
    ws[cell].font = f_bold
# B5/C5 = periodo que vale de fato: o dia unico de B4 tem prioridade sobre B2/B3.
ws["B5"] = '=IF($B$4="",$B$2,$B$4)'
ws["C5"] = '=IF($B$4="",$B$3,$B$4)'
for cell in ("B5", "C5"):
    ws[cell].number_format = FMT_DATA
    ws[cell].font = f_bold
ws["D2"] = "Tudo aqui respeita este periodo (filtra pela DATA DA REUNIAO). So B2, B3 e B4 sao editaveis."
ws["D4"] = ("FILTRO POR DIA: coloque uma data aqui em B4 e o Dashboard inteiro passa a mostrar so aquele dia. "
            "Deixe B4 vazio (tecla DELETE) para voltar ao periodo de B2/B3.")
ws["D2"].font = f_nota
ws["D4"].font = f_nota
for col, w in zip("ABCDEFGH", [26, 16, 14, 12, 22, 12, 24, 16]):
    ws.column_dimensions[col].width = w

ws["A7"] = "Geral"
ws["A7"].font = f_h2
G0 = 8  # primeira linha do bloco Geral
geral = [
    ("Agendamentos", f"=COUNTIFS({PER})", "0"),
    ("Reunioes realizadas", f'=COUNTIFS({PER},{R_COMP},"REALIZADA")', "0"),
    ("No-show", f'=COUNTIFS({PER},{R_COMP},"NO-SHOW")', "0"),
    ("Reagendadas", f'=COUNTIFS({PER},{R_COMP},"REAGENDADA")', "0"),
    ("Canceladas", f'=COUNTIFS({PER},{R_COMP},"CANCELADA")', "0"),
    ("Pendentes (sem marcacao)",
     f"=$B${G0}-$B${G0+1}-$B${G0+2}-$B${G0+3}-$B${G0+4}", "0"),
    ("Taxa de comparecimento", f"=IFERROR($B${G0+1}/($B${G0}-$B${G0+5}),0)", FMT_PCT),
    ("Vendas", f'=COUNTIFS({PER},{R_RES},"VENDA")', "0"),
    ("Conversao reuniao -> venda", f"=IFERROR($B${G0+7}/$B${G0+1},0)", FMT_PCT),
    ("GMV", f'=SUMIFS({R_VAL},{PER},{R_RES},"VENDA")', FMT_BRL0),
    ("Ticket medio", f"=IFERROR($B${G0+9}/$B${G0+7},0)", FMT_BRL0),
]
for i, (rot, f, fmt) in enumerate(geral):
    r = G0 + i
    ws.cell(row=r, column=1, value=rot).font = f_norm
    c = ws.cell(row=r, column=2, value=f)
    c.number_format = fmt
    c.font = f_kpi if fmt in (FMT_PCT, FMT_BRL0) else f_bold

CAB_BLOCO = ["Nome", "Agendamentos", "Realizadas", "No-show", "Taxa de comparecimento",
             "Vendas", "Conversao reuniao -> venda", "GMV"]


def bloco(titulo, linha_titulo, n, rotulo_formula, criterio_range):
    """Bloco de quebra: rotulos vindos da Config, metricas por COUNTIFS/SUMIFS."""
    ws.cell(row=linha_titulo, column=1, value=titulo).font = f_h2
    hl = linha_titulo + 1
    for i, t in enumerate(CAB_BLOCO, start=1):
        c = ws.cell(row=hl, column=i, value=t)
        c.font = f_hdr_navy
        c.fill = fill_navy
        c.alignment = center
    ws.row_dimensions[hl].height = 30
    for j in range(n):
        r = hl + 1 + j
        ws.cell(row=r, column=1, value=rotulo_formula(j)).font = f_norm
        alvo = f"$A{r}"
        base = f"{PER},{criterio_range},{alvo}"
        cells = [
            (2, f"=IF({alvo}=\"\",\"\",COUNTIFS({base}))", "0"),
            (3, f'=IF({alvo}="","",COUNTIFS({base},{R_COMP},"REALIZADA"))', "0"),
            (4, f'=IF({alvo}="","",COUNTIFS({base},{R_COMP},"NO-SHOW"))', "0"),
            (5, f'=IF({alvo}="","",IFERROR($C{r}/($C{r}+$D{r}),0))', FMT_PCT),
            (6, f'=IF({alvo}="","",COUNTIFS({base},{R_RES},"VENDA"))', "0"),
            (7, f'=IF({alvo}="","",IFERROR($F{r}/$C{r},0))', FMT_PCT),
            (8, f'=IF({alvo}="","",SUMIFS({R_VAL},{base},{R_RES},"VENDA"))', FMT_BRL0),
        ]
        for col, f, fmt in cells:
            c = ws.cell(row=r, column=col, value=f)
            c.number_format = fmt
            c.font = f_norm
            c.border = borda_fina
    return hl + n + 1


prox = bloco("Por SDR", G0 + len(geral) + 2, N_SDR,
             lambda j: f'=IF(Config!$A{j + 2}="","",Config!$A{j + 2})', R_SDR)
prox = bloco("Por Closer", prox + 2, N_CLOSERS,
             lambda j: f'=IF(Config!$B{j + 2}="","",Config!$B{j + 2})', R_CLOSER)
prox = bloco("Por Produto", prox + 2, N_PRODUTOS,
             lambda j: f'=IF(Config!$E{j + 2}="","",Config!$E{j + 2})', R_PROD)
prox = bloco("Por Origem", prox + 2, N_ORIGENS,
             lambda j: f'=IF(Config!$F{j + 2}="","",Config!$F{j + 2})', R_ORIG)

# --- por dia
lt = prox + 2
ws.cell(row=lt, column=1, value="Por dia (data da reuniao)").font = f_h2
ws.cell(row=lt, column=3,
        value="Use o funil desta tabela para ordenar os dias ou esconder os dias sem reuniao.").font = f_nota
hl = lt + 1
cab_dia = ["Dia", "Agendamentos", "Realizadas", "No-show", "Taxa de comparecimento",
           "Vendas", "Conversao reuniao -> venda", "GMV"]
for i, t in enumerate(cab_dia, start=1):
    c = ws.cell(row=hl, column=i, value=t)
    c.font = f_hdr_navy
    c.fill = fill_navy
    c.alignment = center
ws.row_dimensions[hl].height = 30
for j in range(DIAS_DASH):
    r = hl + 1 + j
    c = ws.cell(row=r, column=1, value=f"=$B$5+{j}")
    c.number_format = FMT_DATA
    c.font = f_norm
    dia = f"{R_DATA},$A{r}"
    guard = f'IF($A{r}>$C$5,""'
    cells = [
        (2, f'={guard},COUNTIFS({dia}))', "0"),
        (3, f'={guard},COUNTIFS({dia},{R_COMP},"REALIZADA"))', "0"),
        (4, f'={guard},COUNTIFS({dia},{R_COMP},"NO-SHOW"))', "0"),
        (5, f'={guard},IFERROR($C{r}/($C{r}+$D{r}),0))', FMT_PCT),
        (6, f'={guard},COUNTIFS({dia},{R_RES},"VENDA"))', "0"),
        (7, f'={guard},IFERROR($F{r}/$C{r},0))', FMT_PCT),
        (8, f'={guard},SUMIFS({R_VAL},{dia},{R_RES},"VENDA"))', FMT_BRL0),
    ]
    for col, f, fmt in cells:
        cc = ws.cell(row=r, column=col, value=f)
        cc.number_format = fmt
        cc.font = f_norm
        cc.border = borda_fina
ws.auto_filter.ref = f"A{hl}:H{hl + DIAS_DASH}"
ws.freeze_panes = "A6"

# ================================================================= Config
ws = wb.create_sheet("Config")
cols = [("SDRs", SDRS, N_SDR), ("Closers", CLOSERS, N_CLOSERS),
        ("Compareceu?", COMPARECEU, len(COMPARECEU)), ("Resultado", RESULTADO, len(RESULTADO)),
        ("Produtos", PRODUTOS, N_PRODUTOS), ("Origens", ORIGENS, N_ORIGENS)]
for i, (titulo, valores, _) in enumerate(cols, start=1):
    c = ws.cell(row=1, column=i, value=titulo)
    c.font = f_hdr_navy
    c.fill = fill_navy
    c.alignment = center
    ws.column_dimensions[gcl(i)].width = 18
    for j, v in enumerate(valores, start=2):
        cc = ws.cell(row=j, column=i, value=v)
        cc.font = f_norm
        if i in (5, 6):
            cc.fill = fill_amar
ws.column_dimensions["H"].width = 110
ws["H1"] = ("Closer novo: acrescente o nome na coluna B -- a lista suspensa e o Dashboard seguem sozinhos, sem aba nova. "
            "SDR novo: renomeie uma aba vaga E o nome aqui na coluna A (os dois iguais).")
ws["H2"] = ("PRODUTOS (coluna E) e ORIGENS (coluna F) estao com valores de EXEMPLO -- celulas amarelas. Troque pelos "
            "nomes reais de Educacao antes de soltar pro time; as listas suspensas das abas de SDR e os blocos "
            "'Por Produto' / 'Por Origem' do Dashboard seguem sozinhos.")
ws["H3"] = (f"Limites desta versao: {N_SDR} SDRs, {LINHAS_POR_SDR} agendamentos por SDR, {N_CLOSERS} closers, "
            f"{N_PRODUTOS} produtos, {N_ORIGENS} origens. Passar disso exige refazer o espelho da aba 'Agendamentos'.")
for r in (1, 2, 3):
    ws.cell(row=r, column=8).font = f_nota
    ws.cell(row=r, column=8).alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 32

wb.save("Controle_Reunioes_SDR_Educacao.xlsx")
print("ok - linhas em Agendamentos:", ULT_AG)
