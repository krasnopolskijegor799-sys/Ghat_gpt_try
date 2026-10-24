"""Make a block of text easier to read by spacing out its sentences.

Usage:
    python commit.py article.txt
    cat article.txt | python commit.py
    python commit.py --max-chars 160 article.txt
"""

import argparse
import re
import sys
from pathlib import Path


SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")


def format_text(text: str, max_chars: int) -> str:
    """Split text into readable paragraphs and flag especially long sentences."""
    formatted_paragraphs = []

    for paragraph in re.split(r"\n\s*\n", text.strip()):
        paragraph = re.sub(r"\s+", " ", paragraph).strip()
        if not paragraph:
            continue

        sentences = [part.strip() for part in SENTENCE_END.split(paragraph) if part.strip()]
        for sentence in sentences:
            if len(sentence) > max_chars:
                formatted_paragraphs.append(f"⚠️ Длинное предложение ({len(sentence)} символов):\n{sentence}")
            else:
                formatted_paragraphs.append(sentence)

    return "\n\n".join(formatted_paragraphs)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Разбивает сплошной текст на короткие абзацы и отмечает длинные предложения."
    )
    parser.add_argument("file", nargs="?", help="путь к текстовому файлу; если не указан, текст читается из stdin")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=240,
        help="сколько символов может быть в предложении без предупреждения (по умолчанию: 240)",
    )
    args = parser.parse_args()

    if args.max_chars < 1:
        parser.error("--max-chars должен быть больше нуля")

    try:
        if args.file:
            source_text = Path(args.file).read_text(encoding="utf-8")
        elif sys.stdin.isatty():
            parser.error("укажите файл или передайте текст через stdin")
        else:
            source_text = sys.stdin.read()
    except (OSError, UnicodeError) as error:
        print(f"Не удалось прочитать текст: {error}", file=sys.stderr)
        return 1

    result = format_text(source_text, args.max_chars)
    if result:
        print(result)
    else:
        print("В тексте пока нет содержимого.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
