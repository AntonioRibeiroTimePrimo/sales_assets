#!/usr/bin/env python3
"""Salva em disco uma imagem colada na conversa do Claude Code.

Imagens coladas no chat não existem como arquivo no filesystem — elas chegam
como base64 dentro do transcript JSONL da sessão. Este script lê esse
transcript e grava a imagem escolhida no caminho de destino, convertendo para
JPEG quando o original vem em outro formato (WebP, PNG...).

Uso:
    python3 scripts/save_pasted_image.py fotos/ABC.jpg          # última imagem
    python3 scripts/save_pasted_image.py fotos/ABC.jpg --index 0  # a primeira
    python3 scripts/save_pasted_image.py --list                   # só listar

O transcript é localizado automaticamente em
~/.claude/projects/<projeto-slug>/<session-id>.jsonl (o mais recente).
Use --transcript para apontar outro arquivo.
"""

import argparse
import base64
import json
import sys
from pathlib import Path


def find_transcript() -> Path:
    root = Path.home() / ".claude" / "projects"
    candidates = sorted(
        root.glob("*/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if not candidates:
        sys.exit(f"nenhum transcript encontrado em {root}")
    return candidates[0]


def collect_images(transcript: Path) -> list[dict]:
    images = []
    with transcript.open() as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            content = entry.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if isinstance(block, dict) and block.get("type") == "image":
                    source = block.get("source", {})
                    if source.get("type") == "base64":
                        images.append(source)
    return images


def write_jpeg(data: bytes, dest: Path) -> tuple[int, int]:
    from PIL import Image  # pip install Pillow
    from io import BytesIO

    image = Image.open(BytesIO(data)).convert("RGB")
    image.save(dest, "JPEG", quality=92, progressive=True)
    return image.size


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dest", nargs="?", help="caminho de saída, ex: fotos/ABC.jpg")
    parser.add_argument("--index", type=int, default=-1, help="qual imagem (default: a última)")
    parser.add_argument("--transcript", type=Path, help="transcript JSONL específico")
    parser.add_argument("--list", action="store_true", help="listar as imagens e sair")
    args = parser.parse_args()

    transcript = args.transcript or find_transcript()
    images = collect_images(transcript)
    if not images:
        sys.exit(f"nenhuma imagem colada encontrada em {transcript}")

    if args.list:
        for i, source in enumerate(images):
            size = len(base64.b64decode(source["data"]))
            print(f"[{i}] {source.get('media_type')} — {size / 1024:.0f} KB")
        return

    if not args.dest:
        parser.error("informe o caminho de saída (ou use --list)")

    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    source = images[args.index]
    data = base64.b64decode(source["data"])

    if source.get("media_type") == "image/jpeg" and dest.suffix.lower() in (".jpg", ".jpeg"):
        dest.write_bytes(data)
    else:
        write_jpeg(data, dest)

    print(f"{dest} gravado a partir de {source.get('media_type')} ({dest.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
