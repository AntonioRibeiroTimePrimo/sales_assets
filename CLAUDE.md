# sales_assets

Repositório de mídia usada nos materiais de vendas do Grupo Primo. Só assets —
não há código de aplicação.

## Estrutura

| Pasta | Conteúdo | Convenção de nome |
| --- | --- | --- |
| `fotos/` | Retratos dos vendedores | `<PMP>.jpg` — o PMP em maiúsculas, ex: `JPS.jpg` |
| `produtos/` | Marcas/produtos | nome do produto em minúsculas, ex: `portfel.jpg` |
| `flags/` | Bandeiras de países | país em português, ex: `brasil.svg` |
| `sino/` | Vídeos de celebração | — |

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
