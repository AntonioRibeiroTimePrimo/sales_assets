# sino/ — videos de celebracao e o som do sino

Cada video daqui foi gerado por IA. O prompt que gerou (ou que gera o proximo) mora
neste arquivo, para nao ter de reinventar o estilo a cada versao.

| Arquivo | O que e | Gerado em | Duracao / formato |
| --- | --- | --- | --- |
| `intro.mp4` | Voxel estilo Minecraft de camisa da selecao, num estadio, puxando o badalo de um sino dourado. E o sino default de todos os produtos (`sino_video`) | Kling AI 3.0 Omni (marca d'agua no canto) | 5,04 s / 1920x1080 / h264+aac |
| `intro_ufc.mp4` | Voxel lutador de MMA acertando um gongo dourado num octogono. So toca na venda do produto de `sino_comp_lancamento` (Lucro2X) | Google Flow | 4,01 s / 1280x720 |
| `sino.mp3` | So o **audio** do sino, extraido do `intro.mp4`, cortado no ataque, normalizado a -16 LUFS e com fade-out | ffmpeg, a partir do `intro.mp4` | 2,95 s / mono 44,1 kHz / 96 kbps |
| `sino_base64.txt` | O mesmo `sino.mp3` como **data URI** (`data:audio/mpeg;base64,...`), 48.287 caracteres, pronto pra colar em HTML/Apps Script | — | — |
| `referencia_estilo.jpg` | Frame limpo do `intro.mp4` (marca d'agua cortada), pra usar como referencia de estilo no Flow | — | 1920x1010 |
| `prompt_sino_terno.txt` | O prompt da versao de terno em texto puro, pronto pra abrir e copiar (mesmo conteudo das secoes abaixo) | — | — |
| `ref_terno_personagem.jpg` | Recorte do homem de terno da 1a tentativa, **sem o sino junto** — referencia de personagem (Ingredients) pro Flow | frame de 6,3 s da v1 | 560x720 |
| `ref_terno_sino.jpg` | Recorte do sino da 1a tentativa, solto — referencia de objeto pro Flow | frame de 1,0 s da v1 | 430x560 |

---

## Prompt para o Flow — versao "vendedor de terno"

Mesmo formato voxel do `intro.mp4`, mesmos movimentos, trocando o jogador de
camisa da selecao por um homem de terno e gravata vermelha.

### Duas coisas que NAO se pede no prompt, porque o Flow nao entrega

**1. O AUDIO.** Nao obedece. Medido em 11/09/2026: a v1 deste prompt pedia
`complete silence` e o video voltou com **4 badaladas**. O `intro_ufc.mp4`, o outro
video do Flow desta pasta, tem audio com pico em -0,7 dB — ou seja, o modelo tambem
nao entrega mudo quando se pede. O som certo entra depois, por cima, com o `ffmpeg`
da secao "Trocar o audio", que e deterministico. O que ele gerar de audio se descarta.

**2. A MAO AGARRANDO O BADALO.** Contato de mao com objeto pequeno ele nao resolve.
Na v1 a mao passava perto do badalo e voltava sem nunca fechar, enquanto o sino
ficava **parado** — lia como tapa no ar. Por isso a acao virou **golpe**: punho
fechado na lateral do sino, que e a mesma acao do `intro_ufc.mp4`, o unico video
desta pasta que o Flow gerou bem.

**Cole isto no Flow (texto -> video, 16:9).** Em ingles porque o Veo segue
descricao de camera com muito mais fidelidade em ingles do que em portugues —
o video nao tem fala, entao o idioma do prompt nao aparece na tela.

**Versao em `.txt`, pronta pra abrir e copiar: [`prompt_sino_terno.txt`](prompt_sino_terno.txt)**
(com a tabela defeito -> correcao da v1 para a v2).

```
Minecraft-style low-poly voxel 3D animation. Chunky blocky characters, flat
pixel-art textures, thick dark outlines, soft cartoon lighting, shallow depth
of field with a heavily blurred background. Medium shot. The camera is
completely locked off and never moves or zooms.

A blocky voxel businessman stands on the right side of the frame, facing
camera: short dark blocky hair, dark navy business suit jacket, crisp white
shirt, bright red tie. Directly beside him, at chest height and within easy
arm's reach, a large golden brass bell hangs from a short black bracket.

He pulls his right arm back and swings it forward, striking the side of the
bell hard with his closed fist. The bell rocks violently back and forth on its
bracket, a burst of golden sparks flies off the impact point, and the bell
keeps swinging until the end of the shot. He strikes it once more, then holds
his fist up and smiles at camera.

Background: a modern open-plan sales floor, completely out of focus.

Audio: none.

No text, no captions, no subtitles, no logos, no watermark, no on-screen UI,
no camera movement, no zoom, no cuts.
```

### Os 6 defeitos da v1, e o que mudou na v2

Vale pra qualquer video voxel gerado aqui, nao so pra este.

| Defeito | Correcao |
| --- | --- |
| Mao nunca agarrava o badalo; lia como tapa no ar | Golpe com punho fechado — sem contato fino pra resolver |
| Sino ficava parado enquanto o braco se mexia | `rocks violently back and forth` + faisca no impacto: o movimento do sino virou a acao principal |
| Sino longe e acima da cabeca, gesto impossivel | `at chest height and within easy arm's reach`, em suporte curto ao lado. Sino pendurado no alto traz o problema do badalo de volta |
| Personagem e sino mudavam de tamanho no plano | O push-in lento saiu. Camera travada, declarado duas vezes |
| Cabelo e rosto morfavam entre frames | Plano de 5 s — a instabilidade do Veo cresce com a duracao |
| Ultimos 2 s parados, sem o aceno pedido | Termina com o sino balancando e o punho erguido: um fim que se ve |

**Gere 3 ou 4 do mesmo prompt e escolha.** A variacao entre execucoes e grande; a
primeira saida nao e o teto do prompt.

### Reaproveitar um video que nao ficou bom

O personagem da v1 ficou BOM (terno azul-marinho, gravata vermelha, cabelo blocado,
escritorio desfocado); o que falhou foi a acao e a posicao do sino. Da pra manter a
aparencia e jogar fora o movimento — **mas so por um dos tres caminhos**:

| Caminho | Vale? | Por que |
| --- | --- | --- |
| **Ingredients / referencia de personagem** | **Sim** | Mantem a identidade ja aprovada e monta uma cena NOVA a partir do texto — e a cena e justamente o que precisa mudar. Recortes prontos: `ref_terno_personagem.jpg` e `ref_terno_sino.jpg` |
| Extend / Jump to | Nao | So acrescenta segundos DEPOIS do clipe. O gesto errado e o sino fora de alcance continuam la, agora com mais tempo em cima |
| Frames to Video (frame inicial) | Nao | O frame inicial trava a composicao, e a composicao e o defeito. Nenhum frame da v1 tem o sino ao alcance do braco |

**Os recortes sao dois arquivos separados de proposito.** Numa imagem so, a distancia
errada entre o homem e o sino viaja junto com a referencia.

### Trocar so o cenario

Uma linha do prompt, o resto igual. Substitua a linha do `Background:`:

| Clima | Linha |
| --- | --- |
| Chao de vendas (default acima) | `Background: a modern open-plan sales floor, completely out of focus.` |
| Palco/transmissao (identidade do gerencial: preto + dourado) | `Background: a dark broadcast stage with warm gold spotlights and drifting haze, completely out of focus.` |
| Estadio (mantem o clima do `intro.mp4` atual) | `Background: a sunny football stadium with a blurred crowd in the stands.` |

### Versao em portugues

Se preferir rodar em portugues, e este — mas prefira o de cima:

```
Animacao 3D voxel estilo Minecraft. Personagens blocados, textura de pixel art
chapada, contorno escuro grosso, luz de desenho suave, pouca profundidade de
campo com o fundo bem desfocado. Plano medio. A camera fica totalmente travada
e nunca se move nem da zoom.

Um homem voxel de terno esta do lado direito do quadro, de frente pra camera:
cabelo curto escuro blocado, palito azul-marinho, camisa branca e gravata
vermelha viva. Bem ao lado dele, na altura do peito e ao alcance do braco, um
grande sino de latao dourado preso num suporte preto curto.

Ele puxa o braco direito pra tras e o lanca pra frente, acertando a lateral do
sino com o punho fechado. O sino balanca com violencia pra frente e pra tras no
suporte, uma explosao de faiscas douradas sai do ponto do impacto, e o sino
continua balancando ate o fim do plano. Ele acerta mais uma vez, depois ergue o
punho e sorri pra camera.

Fundo: um escritorio moderno de time de vendas, totalmente desfocado.

Audio: nenhum.

Sem texto, sem legenda, sem logo, sem marca d'agua, sem interface na tela, sem
movimento de camera, sem zoom, sem corte.
```

### Ajustes no Flow

- **Referencia de estilo:** o `referencia_estilo.jpg` desta pasta e um frame limpo do
  video atual. Da pra jogar como ingrediente/imagem de referencia pra amarrar o look —
  mas ele carrega a camisa amarela junto, entao se o terno nao pegar, tire a referencia
  e va so de texto.
- **Duracao:** o Flow entrega 8 s. **Corte pra ~5 s**, no maximo 6. Na v1 os ultimos
  2 s eram o personagem parado olhando pra camera. E o overlay do dashboard so revela
  o card da venda quando o video termina (evento `ended`), entao video longo e tela
  travada durante a comemoracao.
- **Formato de saida:** 16:9, 1080p, mp4/h264. A v1 saiu em 1280x720 — peca 1080p pra
  TV. O `intro.mp4` tem 4,8 MB e passa; acima de ~8 MB o carregamento pela URL raw
  comeca a atrasar a primeira badalada nas TVs.

### Trocar o audio pelo sino de verdade (passo obrigatorio)

O `sino.mp3` desta pasta e o som do video de hoje, isolado e normalizado. Isto joga
fora o audio que o Flow gerou e poe o sino no lugar, sem recomprimir a imagem:

```bash
ffmpeg -i video_do_flow.mp4 -i sino.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest \
  intro_social.mp4
```

Para a badalada cair no frame em que ele puxa o badalo, atrase o som com `-itsoffset`
antes do segundo arquivo (exemplo com 1,5 s):

```bash
ffmpeg -i video_do_flow.mp4 -itsoffset 1.5 -i sino.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k \
  intro_social.mp4
```

O `sino.mp3` tem ~6 badaladas em 2,95 s. Com um video de 2 golpes, corte o mp3 na 2a
pra nao soar mais sino do que se ve na tela:

```bash
ffmpeg -i sino.mp3 -t 1.4 -af "afade=t=out:st=1.1:d=0.3" sino_2x.mp3
```

---

## Onde o video entra em producao

Nao ha deploy envolvido em trocar o video — e chave de planilha:

- **Dashboard gerencial:** aba `Config`, chave `sino_video` (default no `Code.gs`,
  `DEFAULTS.SINO_VIDEO`). `sino_video_lancamento` + `sino_comp_lancamento` roteiam um
  video diferente pra um `product_id` especifico.
- **Arena Lucro2X:** `SINO_VIDEO_OUTROS` / `SINO_VIDEO_URL_LDX`, em
  `Dashboards/lucro2x/04_competicao_externa/Dados.gs` (esse sim exige colar e
  redeployar o Apps Script).

Commite o mp4 novo aqui com nome proprio (`intro_social.mp4`, por exemplo) em vez de
sobrescrever o `intro.mp4` — assim da pra voltar atras mudando so a chave da Config.

---

## Como o `sino.mp3` e o base64 foram feitos

```bash
# audio do sino, cortado no ataque (2,05 s do intro.mp4), normalizado, com fade-out
ffmpeg -ss 2.05 -i intro.mp4 -vn \
  -af "afade=t=in:st=0:d=0.02,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=2.75:d=0.20" \
  -t 2.95 -ac 1 -ar 44100 -c:a libmp3lame -b:a 96k sino.mp3

# data URI pronto pra colar
python3 -c "import base64;print('data:audio/mpeg;base64,'+base64.b64encode(open('sino.mp3','rb').read()).decode())" > sino_base64.txt
```

Uso do base64 em HTML/Apps Script — cole o conteudo de `sino_base64.txt` no `src`:

```html
<audio id="sino-som" preload="auto" src="data:audio/mpeg;base64,...."></audio>
```

**Autoplay:** navegador nao toca audio sem interacao previa do usuario. O padrao ja
usado no sino do gerencial vale aqui: o botao 🔔/🔕 arma o som, a preferencia fica no
`localStorage`, e o `play()` roda dentro do `catch` que cai pra mudo se o browser
bloquear. Nao coloque o data URI dentro do video do overlay — o video vem por URL raw
justamente pra nao inchar o load da pagina em 4 MB de base64.
