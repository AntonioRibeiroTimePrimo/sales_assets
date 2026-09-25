# Controle de Reuniões — SDR Educação

Versão do "Controle de Reuniões LDX" adaptada para o fluxo geral de SDR de
Educação. `gerar_planilha.py` regenera o `.xlsx` do zero — é a fonte da verdade;
edite o script, não o arquivo, quando precisar mudar limites ou estrutura.

## Arquitetura (igual à do LDX)

```
aba por SDR (SDR 01..10)  →  Agendamentos (espelho por fórmula)  →  Dashboard
                                                                    Config (listas)
```

O SDR só escreve na aba dele. A aba `Agendamentos` espelha as 10 abas por
fórmula (colunas cinza) e é onde o Closer marca o desfecho (colunas laranja).
Como a marcação mora na mesma linha da reunião, ela nunca se solta do
agendamento.

## O que mudou em relação ao LDX

| Mudança | Onde |
| --- | --- |
| Coluna `Quando (data e hora)` — data + hora num valor só, para o Closer ordenar em ordem crescente com um clique dentro da visualização de filtro | `Agendamentos!C` |
| Colunas `Produto` e `Origem` preenchidas pelo SDR, com lista suspensa | abas de SDR (`F`/`G`) → `Agendamentos!I`/`J` |
| Blocos `Por Produto` e `Por Origem` | `Dashboard` |
| Filtro de dia único (`B4`) que refiltra o Dashboard inteiro; `B5`/`C5` mostram o período aplicado | `Dashboard` |
| Filtro/ordenação na tabela `Por dia` | `Dashboard` |
| Rótulos do Dashboard vêm da `Config` — closer/produto/origem novo aparece sozinho | `Dashboard` |
| 10 abas de SDR (era 6) | — |

## Limites

10 SDRs · 500 agendamentos por SDR (5.000 linhas em `Agendamentos`) · 15 closers ·
12 produtos · 12 origens · 45 dias no bloco "Por dia". Passar disso exige
regenerar pelo script (ajustar as constantes no topo e rodar
`python3 gerar_planilha.py`).

## Antes de soltar para o time

Produtos e origens entram com valores de **exemplo** (células amarelas na
`Config`, colunas E e F). Troque pelos nomes reais de Educação — as listas
suspensas e os blocos do Dashboard seguem sozinhos.

## Validação

Sem LibreOffice no ambiente, as fórmulas foram validadas com o motor `formulas`
(Python) sobre uma cópia reduzida com dados sintéticos: Geral, quebras por SDR /
Closer / Produto / Origem, bloco Por dia, a chave de ordenação `Quando` e o
filtro de dia único — todos batendo com o esperado calculado em Python puro.
Só funções Excel-2007 (`IF`, `IFERROR`, `COUNTIFS`, `SUMIFS`, `TODAY`), nativas
no Google Sheets.
