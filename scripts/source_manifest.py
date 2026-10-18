#!/usr/bin/env python3
"""Hash one explicitly named source, writing JSON to stdout and changing no files."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    try:
        source = args.source
        if source.is_symlink() or not source.is_file():
            raise ValueError('source must be an existing regular file, not a symlink')
        before = source.stat()
        digest = hashlib.sha256()
        size = 0
        with source.open('rb') as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b''):
                size += len(block)
                digest.update(block)
        after = source.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns) or size != before.st_size:
            raise ValueError('source changed while hashing; no manifest is reliable')
        print(json.dumps({'original_filename': source.name, 'format': source.suffix.lower(),
                          'bytes': size, 'sha256': digest.hexdigest(),
                          'capture_status': 'unknown', 'transcript_complete': None,
                          'note': 'Byte integrity only; no parsing, preservation, extraction or approval performed.'}, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
