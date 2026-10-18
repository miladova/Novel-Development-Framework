#!/usr/bin/env python3
"""Print a local status report. Reading active chapter prose requires --words."""
import argparse
from collections import Counter
from pathlib import Path
import re
import sys
from validate_framework import read_scenes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--words', action='store_true', help='authorize reading active .md/.txt chapters for approximate counts')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        scenes = read_scenes(root)
        books = sorted(p for p in (root / '05_Books').iterdir()
                       if p.is_dir() and not p.is_symlink() and re.fullmatch(r'BOOK-\d{3,}', p.name))
        print('# Project status\n')
        print(f'Books: {len(books)} | Scenes: {len(scenes)}')
        for status, total in sorted(Counter(row['status'] for row in scenes).items()):
            print(f'- {status}: {total}')
        if not args.words:
            print('\nWord counts not requested. Active manuscripts were not read.')
            return 0
        print('\n| Book | Approximate words |\n| --- | ---: |')
        for book in books:
            words = 0
            chapters = book / 'Chapters'
            if chapters.is_symlink():
                raise ValueError('symlink chapter directory is not allowed')
            for path in chapters.rglob('*'):
                if path.is_symlink():
                    raise ValueError('symlink manuscript is not allowed')
                if path.is_file() and path.suffix.lower() in {'.md', '.txt'} and path.name != 'README.md':
                    words += len(path.read_text(encoding='utf-8').split())
            print(f'| {book.name} | {words} |')
        print('\nWhitespace-token estimate, including headings and markup; DOCX/PDF and archived revisions are excluded.')
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
