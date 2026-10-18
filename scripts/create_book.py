#!/usr/bin/env python3
"""Preview a new book folder; use --apply to create it without overwriting."""
import argparse
from pathlib import Path
import re
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--id', required=True, help='BOOK-001 or another unused numeric ID')
    parser.add_argument('--title', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        if not re.fullmatch(r'BOOK-\d{3,}', args.id):
            raise ValueError('book ID must have the form BOOK-001')
        if not args.title.strip() or any(ord(c) < 32 for c in args.title):
            raise ValueError('title must be nonempty and on one line')
        root = args.root.resolve()
        books = root / '05_Books'
        source = books / 'BOOK_TEMPLATE'
        target = books / args.id
        if books.is_symlink() or source.is_symlink() or not source.is_dir():
            raise ValueError('missing or unsafe book template directory')
        if target.exists() or target.is_symlink():
            raise ValueError('destination already exists; nothing was overwritten')
        files = []
        for path in sorted(source.rglob('*')):
            if path.is_symlink():
                raise ValueError('template symlinks are not allowed')
            if path.is_file():
                content = path.read_text(encoding='utf-8')
                content = content.replace('{{BOOK_ID}}', args.id).replace('{{BOOK_TITLE}}', args.title.strip())
                files.append((path.relative_to(source), content))
        if not files:
            raise ValueError('book template is empty')
        print(('CREATE' if args.apply else 'DRY RUN') + ': ' + args.id)
        for rel, _ in files:
            print('  ' + (Path('05_Books') / args.id / rel).as_posix())
        if not args.apply:
            print('No files changed. Review the preview, then repeat with --apply.')
            return 0
        target.mkdir(exist_ok=False)
        for rel, content in files:
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(content)
        print('Book scaffold created; no story, canon approval, or publication was generated.')
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
