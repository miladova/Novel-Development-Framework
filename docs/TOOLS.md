# Optional offline tools

Python 3.10+; standard library only. Run commands from the repository root. These tools do not call AI services, approve canon, import conversations, render DOCX/PDF, or publish a book.

## Structural validation

`python scripts/validate_framework.py`

Checks required files, UTF-8 Markdown outside excluded source areas, simple relative-link destinations, duplicate cataloged IDs, canonical approval fields and local evidence references, scene IDs, book references, scene statuses, and named scene dependencies. `--root PATH` checks another copied workspace.

It skips `_inbox/`, `archive/`, `_private/`, active `Chapters/`, Git internals, and symlink directories. It does not parse general YAML; follow the [flat metadata standard](../00_Project/Metadata_Standard.md). Supported links are ordinary inline Markdown destinations without optional title syntax. External URLs and `#fragment` existence are not checked.

A passing result does not prove actual author approval, completeness, continuity, chronology, acyclic plot dependencies, privacy, literary quality, or copyright clearance. Human review remains necessary. Do not run checks against sources outside the task's authorization.

## Book scaffolding

```bash
python scripts/create_book.py --id BOOK-001 --title "My Novel"
python scripts/create_book.py --id BOOK-001 --title "My Novel" --apply
```

The first command lists planned files without writing. `--apply` copies the blank book template and substitutes its ID and title placeholders. Existing destinations and template symlinks are rejected. If a filesystem error interrupts creation, inspect the partial new folder before retrying; existing sources are not removed.

## Status and word counts

`python scripts/project_status.py` reports book and scene counts without reading active prose.

`python scripts/project_status.py --words` explicitly reads active `.md` and `.txt` files under each numbered book's `Chapters/` folder. Counts are approximate whitespace tokens, including headings and markup; `README.md`, DOCX, PDF, templates, and archived revisions are excluded. This is not a publishing-industry word-count standard. The report goes to stdout and does not modify records.

## Named-source checksum

`python scripts/source_manifest.py "path/to/source.docx"`

Hashes exactly one named file and prints JSON containing original filename, size, format, and SHA-256. It changes no files and does not parse the source. Completeness remains unknown. Save that output separately only as part of an authorized preservation task; do not redirect it over the original. Comparing a later checksum can reveal byte changes, not whether a conversation capture was complete.

## Tests and continuous integration

`python -m unittest discover -s tests -v`

Tests create temporary copies and use neutral fixture text. The GitHub Actions workflow runs tests and validation with read-only repository permissions. It does not auto-commit, merge, deploy, or upload manuscript artifacts. Maintainers should review dependency-update pull requests rather than automatically accepting them.
