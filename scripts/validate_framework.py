#!/usr/bin/env python3
"""Offline structural checks. This does not verify story truth or human consent."""
import argparse
import csv
from datetime import date
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REQUIRED = (
    'AGENTS.md', 'README.md', 'LICENSE', '00_Project/Constitution.md',
    '00_Project/Metadata_Standard.md', '02_Canon/Canon_Index.md',
    'docs/GETTING_STARTED.md', 'docs/WORKFLOW.md', 'docs/PRIVACY.md',
    'docs/CANON_APPROVAL_PROCESS.md', 'docs/MANUSCRIPT_WORKFLOW.md',
    'docs/INTERVIEW_PROTOCOL.md', 'docs/REWRITE_PROTOCOL.md',
    '09_Tools/Templates/Canon_Record.md', '04_Story/Scene_Registry.csv',
)
SCENE_FIELDS = ['scene_id', 'book_id', 'chapter', 'pov', 'purpose', 'change',
                'status', 'depends_on', 'source_refs']
SCENE_STATES = {'Planned', 'Drafting', 'Drafted', 'Reviewed', 'Approved', 'Released'}
SKIP_DIRS = {'.git', '.worktrees', '__pycache__', '_private', '_inbox', 'archive', 'Chapters'}
UNKNOWN = {'', 'unknown', 'none', 'null', '[]', 'pending'}


def metadata(text):
    """Read the documented flat scalar header, not arbitrary YAML."""
    if not text.startswith('---\n'):
        return {}
    header, marker, _ = text[4:].partition('\n---')
    if not marker:
        return {}
    return {key.strip(): value.strip().strip('\"\'')
            for line in header.splitlines() if ':' in line
            for key, value in [line.split(':', 1)]}


def local_target(root, source, target):
    parts = urlsplit(target.strip().strip('<>'))
    if parts.scheme or parts.netloc or not parts.path:
        return None
    path = (source.parent / unquote(parts.path)).resolve()
    if not path.is_relative_to(root):
        raise ValueError('link escapes repository: ' + target)
    return path


def markdown_files(root):
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not (Path(parent) / d).is_symlink()]
        for name in sorted(files):
            if name.endswith('.md'):
                yield Path(parent) / name


def read_scenes(root):
    path = root / '04_Story/Scene_Registry.csv'
    if path.is_symlink():
        raise ValueError('scene registry must not be a symlink')
    with path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != SCENE_FIELDS:
            raise ValueError('scene registry has incorrect columns')
        rows = list(reader)
    errors, ids = [], set()
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            errors.append('scene registry has a malformed row')
            continue
        sid = row['scene_id']
        if not re.fullmatch(r'SCN-\d{4,}', sid):
            errors.append('invalid scene ID: ' + sid)
        if sid in ids:
            errors.append('duplicate scene ID: ' + sid)
        ids.add(sid)
        bid = row['book_id']
        if not re.fullmatch(r'BOOK-\d{3,}', bid) or not (root / '05_Books' / bid).is_dir():
            errors.append('unknown book for scene: ' + sid)
        if row['status'] not in SCENE_STATES:
            errors.append('invalid scene status: ' + sid)
    for row in rows:
        for dependency in (row.get('depends_on') or '').split(';'):
            if dependency and dependency.strip() not in ids:
                errors.append('unknown scene dependency: ' + dependency.strip())
    if errors:
        raise ValueError('; '.join(errors))
    return rows


def validate(root):
    root = root.resolve()
    errors, seen, count = [], {}, 0
    if not root.is_dir():
        return ['repository root does not exist'], 0
    for name in REQUIRED:
        p = root / name
        if not p.is_file() or p.is_symlink():
            errors.append('missing or unsafe required file: ' + name)
    for path in markdown_files(root):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append('symlink document is not inspected: ' + rel)
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError):
            errors.append('unreadable UTF-8 document: ' + rel)
            continue
        count += 1
        if not text.strip():
            errors.append('empty Markdown: ' + rel)
        outside_code = re.sub(r'(?ms)^```[^\n]*\n.*?^```[^\n]*$', '', text)
        outside_code = re.sub(r'(?ms)^~~~[^\n]*\n.*?^~~~[^\n]*$', '', outside_code)
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', outside_code):
            try:
                linked = local_target(root, path, target)
                if linked is not None and not linked.exists():
                    errors.append(rel + ': missing link target ' + target)
            except ValueError as exc:
                errors.append(rel + ': ' + str(exc))
        meta = metadata(text)
        record_id = meta.get('ID', '')
        if record_id and record_id != 'TEMPLATE':
            if record_id in seen:
                errors.append('duplicate record ID: ' + record_id)
            seen[record_id] = rel
        if rel.startswith('02_Canon/') and path.name not in {'README.md', 'Canon_Index.md'}:
            if not re.fullmatch(r'CAN-\d{4,}', record_id):
                errors.append(rel + ': missing canonical record ID')
            if meta.get('Status') not in {'Canon', 'Deprecated'}:
                errors.append(rel + ': unapproved material belongs outside canon')
            if meta.get('Canonical') != 'true':
                errors.append(rel + ': canonical metadata must be true')
            for field in ('Approved_By', 'Approved_On', 'Source', 'Decision'):
                if meta.get(field, '').lower() in UNKNOWN:
                    errors.append(rel + ': missing approval evidence field ' + field)
            try:
                date.fromisoformat(meta.get('Approved_On', ''))
            except ValueError:
                errors.append(rel + ': invalid approval date')
            for field in ('Source', 'Decision'):
                if meta.get(field, '').lower() in UNKNOWN:
                    continue
                try:
                    linked = local_target(root, path, meta[field])
                    if linked is None or not linked.is_file():
                        raise ValueError('approval evidence must reference a local file')
                    if field == 'Decision':
                        if not linked.is_relative_to(root / '00_Project') or linked.suffix != '.md':
                            raise ValueError('approval decision must be a Markdown governance record in 00_Project')
                        approval = metadata(linked.read_text(encoding='utf-8'))
                        if approval.get('Status') != 'Approved' or approval.get('Approved_By', '').lower() in UNKNOWN:
                            raise ValueError('decision lacks explicit approval metadata')
                        if not re.fullmatch(r'DEC-\d{4,}', approval.get('ID', '')):
                            raise ValueError('decision requires a stable DEC ID')
                        try:
                            date.fromisoformat(approval.get('Approved_On', ''))
                        except ValueError:
                            raise ValueError('decision requires a valid approval date')
                except (ValueError, OSError, UnicodeError) as exc:
                    errors.append(rel + ': ' + str(exc))
    try:
        read_scenes(root)
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        errors.append(str(exc))
    return errors, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, count = validate(args.root)
    if errors:
        print('FAIL\n' + '\n'.join(errors))
        return 1
    print(f'PASS: {count} Markdown documents; required files, local links, canon metadata and scene registry checked.')
    print('Not checked: prose quality, story truth, actual consent, external URLs, or link fragments.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
