# Getting started

## Choose a workspace

For unpublished writing, use a new private repository generated from this template, or download the ZIP and keep it locally. Confirm visibility before uploading anything. Public forks remain public; fork the framework to contribute improvements, not to hide a manuscript. See [privacy](PRIVACY.md).

On GitHub, use **Use this template -> Create a new repository** when that setting is enabled. Select only the default branch. Alternatively use **Code -> Download ZIP**, extract it, and create your own repository. No Python, Git command line, or AI account is needed to read and edit the Markdown documents.

Official instructions: [creating from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

## Define the project

Complete [Vision](../00_Project/Vision.md), [Author Intent](../00_Project/Author_Intent.md), and [Voice Guide](../00_Project/Voice_Guide.md). Decide whether this is an original novel, a rewrite, or a series. Record the active phase in the [dashboard](../00_Project/Dashboard.md).

Do not populate every folder just to make the repository look complete. Start with the questions and records your book actually needs.

## Create one book

Copy `05_Books/BOOK_TEMPLATE/` to `05_Books/BOOK-001/` and replace the title and ID placeholders. The optional utility previews this without writing:

```bash
python scripts/create_book.py --id BOOK-001 --title "My Novel"
python scripts/create_book.py --id BOOK-001 --title "My Novel" --apply
```

Keep the blank template for future books. New book folders are scaffolding, not generated stories. The utility refuses an existing destination.

## Start a new story

Use the [initialization interview](../09_Tools/Templates/Project_Initialization.md). Record settled positions and uncertainties separately. Develop enough story architecture to support the next writing task, rather than attempting to decide every detail of the universe first.

## Reconstruct an existing manuscript

Place an unchanged source in `_inbox/manuscripts/`. Explicitly identify which file may be inspected and for what purpose. Establish the comparison baseline with the author. Preserve the source separately before any extraction or rewriting. See [the manuscript workflow](MANUSCRIPT_WORKFLOW.md).

## Give an assistant a bounded first task

```text
Read AGENTS.md and the relevant policies. Identify this repository's branch
and commit. Review my Vision, Author Intent, and Open Questions, then prepare
a Writing Context Brief and a focused initialization interview. Do not inspect
manuscript inbox files, invent story facts, approve canon, or generate prose.
```

An assistant needs actual access to the files. Naming a repository does not guarantee access or persistent memory. Ask it to disclose what it could and could not read.

## End each session with a handoff

Update the dashboard, question tracker, and [session handoff](../09_Tools/Templates/Session_Handoff.md). Record approvals exactly and link their evidence. Before committing, review the changed files and repository visibility. Commit framework improvements separately from private creative work.

## Use optional checks

```bash
python scripts/validate_framework.py
python scripts/project_status.py
python -m unittest discover -s tests -v
```

Use Python 3.10 or newer. Some systems call the executable `python3`; on Windows, `py -3` may be the available launcher. The scripts run locally without installing packages. Read [tool limits](TOOLS.md) before interpreting a passing check as anything more than structural validation.
