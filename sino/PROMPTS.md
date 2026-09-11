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

---

## Prompt para o Flow — versao "vendedor de terno"

Mesmo formato voxel do `intro.mp4`, mesmos movimentos, trocando o jogador de
camisa da selecao por um homem de terno e gravata vermelha.

**Cole isto no Flow (texto -> video, 16:9).** Em ingles porque o Veo segue
descricao de camera e de audio com muito mais fidelidade em ingles do que em
portugues — o video nao tem fala, entao o idioma do prompt nao aparece na tela.

```
Minecraft-style low-poly voxel 3D animation. Chunky blocky characters, flat
pixel-art textures, thick dark outlines, soft sunny cartoon lighting, shallow
depth of field with a heavily blurred background. Medium shot, camera locked
off, very slow push-in over the whole shot.

A blocky voxel businessman stands on the right third of the frame, facing
camera: short dark blocky hair, dark navy business suit jacket, crisp white
shirt, bright red tie. On the left third of the frame a large golden brass
bell hangs from above at head height, with a heavy hanging clapper below it.

He starts perfectly still with his arms down. He raises his right arm into
frame, grabs the bell's clapper, and yanks it down three times in a row,
swinging the bell hard from side to side. He keeps holding the clapper and
gives one small proud nod to camera. The bell is still swinging when the shot
ends.

Background: a modern open-plan sales floor, completely out of focus.

Audio: three loud, bright, resonant brass bell strikes with a long metallic
decay, over faint distant office cheering. No music, no dialogue, no narration.

No text, no captions, no subtitles, no logos, no watermark, no on-screen UI,
no camera shake, no cuts.
```

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
chapada, contorno escuro grosso, luz de desenho suave e ensolarada, pouca
profundidade de campo com o fundo bem desfocado. Plano medio, camera fixa, com
um leve avanco lento durante todo o plano.

Um homem voxel de terno esta no terco direito do quadro, de frente pra camera:
cabelo curto escuro blocado, palito azul-marinho, camisa branca e gravata
vermelha viva. No terco esquerdo do quadro, um grande sino de latao dourado
pendurado na altura da cabeca, com um badalo pesado embaixo.

Ele comeca parado, bracos ao lado do corpo. Levanta o braco direito, agarra o
badalo do sino e puxa tres vezes seguidas, fazendo o sino balancar forte de um
lado pro outro. Continua segurando o badalo e da um leve aceno de cabeca,
orgulhoso, pra camera. O sino ainda esta balancando quando o plano termina.

Fundo: um escritorio moderno de time de vendas, totalmente desfocado.

Audio: tres badaladas de latao altas, brilhantes e ressonantes, com cauda
metalica longa, sobre uma comemoracao distante e abafada de escritorio. Sem
musica, sem fala, sem narracao.

Sem texto, sem legenda, sem logo, sem marca d'agua, sem interface na tela, sem
tremida de camera, sem corte.
```

### Ajustes no Flow

- **Referencia de estilo:** o `referencia_estilo.jpg` desta pasta e um frame limpo do
  video atual. Da pra jogar como ingrediente/imagem de referencia pra amarrar o look —
  mas ele carrega a camisa amarela junto, entao se o terno nao pegar, tire a referencia
  e va so de texto.
- **Duracao:** o Flow entrega 8 s. **Corte pra ~5 s**, no maximo 6. O overlay do
  dashboard so revela o card da venda quando o video termina (evento `ended`), entao
  video longo e tela travada durante a comemoracao.
- **Formato de saida:** 16:9, 1080p, mp4/h264. O `intro.mp4` tem 4,8 MB e passa; acima
  de ~8 MB o carregamento pela URL raw comeca a atrasar a primeira badalada nas TVs.
- **O audio do Veo costuma sair fraco.** Se a badalada vier abafada, troque a trilha
  pelo `sino.mp3` desta pasta (o sino do video atual, ja normalizado).

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
