# sales_assets

Repositório de mídia usada nos materiais de vendas do Grupo Primo. Só assets —
não há código de aplicação.

## Estrutura

| Pasta | Conteúdo | Convenção de nome |
| --- | --- | --- |
| `fotos/` | Retratos dos vendedores | `<PMP>.jpg` — o PMP em maiúsculas, ex: `JPS.jpg` |
| `produtos/` | Marcas/produtos | nome do produto em minúsculas, ex: `portfel.jpg` |
| `flags/` | Bandeiras de países | país em português, ex: `brasil.svg` |
| `sino/` | Vídeos de celebração, o áudio do sino (`sino.mp3` + `sino_base64.txt`) e os prompts de IA que geraram cada vídeo (`PROMPTS.md`) | — |
| `scripts_venda/` | Imagens enviadas dentro de um script de venda (extensao `script_personalizado`, mensagem `[imagem]<url>`) | `<produto>_<assunto>.jpg`, ex: `l2x_pilares.jpg` |

Fotos de vendedor são sempre `.jpg`. Se o original vier em WebP/PNG, converta
antes de commitar (o script abaixo faz isso).

## Adicionar uma imagem colada no chat

Imagem colada na conversa **não existe como arquivo** no filesystem — ela chega
como base64 dentro do transcript JSONL da sessão, em
`~/.claude/projects/<projeto-slug>/<session-id>.jsonl`. Não adianta procurar com
`find`; é preciso extrair do transcript:

```bash
python3 scripts/save_pasted_image.py --list          # ver as imagens da sessão
python3 scripts/save_pasted_image.py fotos/ABC.jpg   # gravar a última
```

O script converte para JPEG progressivo (qualidade 92) quando o original não é
JPEG. Depois de gravar, abra o arquivo com a ferramenta Read para conferir
visualmente que é a imagem certa antes de commitar.

## PMP dos vendedores — vem do BigQuery

O PMP **nunca** deve ser inventado nem deduzido do nome (os códigos são
atribuídos, não derivados: Camila Silva = `CCL`, Bruna Palmieri = `BPS`). A fonte
é a tabela de vendedores, e a chave de junção é o **e-mail**, não o nome
(usada aqui para nomear os arquivos de `fotos/` e `competicao_ufc/`):

```
grupo-primo-prd.staging_google_sheets.stg_google_sheets__map_sellers_tvd
  seller_name | seller_email | seller_pmp | seller_contract | is_active
```

Cuidados: um mesmo vendedor pode ter duas linhas (CLT e PJ) com o mesmo PMP e
`is_active` diferente — considere ativo quem tem *pelo menos uma* linha ativa. E
e-mails com sufixo `+algo` são alias da conta base (`guilherme.fracasso+gp@` é o
mesmo GPF que `guilherme.fracasso@`).

Não há `bq` CLI no ambiente. Acesso pela REST API, autenticando com o
`GCP_CREDENTIALS_JSON` (base64 de um authorized_user com refresh_token):

```python
import os, base64, json, requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

d = json.loads(base64.b64decode(os.environ["GCP_CREDENTIALS_JSON"]))
c = Credentials(None, refresh_token=d["refresh_token"], client_id=d["client_id"],
                client_secret=d["client_secret"],
                token_uri="https://oauth2.googleapis.com/token")
c.refresh(Request())
requests.post(
    "https://bigquery.googleapis.com/bigquery/v2/projects/grupo-primo-prd/queries",
    headers={"Authorization": "Bearer " + c.token},
    json={"query": SQL, "useLegacySql": False, "timeoutMs": 120000})
```

Os datasets ficam em `grupo-primo-prd` (região `us`). Para achar tabela por nome:
`SELECT table_schema, table_name FROM \`grupo-primo-prd.region-us.INFORMATION_SCHEMA.TABLES\``.
