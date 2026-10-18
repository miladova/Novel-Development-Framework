# Public framework, private writing

This repository is public. Files, commit history, issues, pull requests, and workflow logs can expose material to others. Public framework development and unpublished book development belong in separate workspaces.

## Choose the right copy

Fork when contributing to the public framework. For a private novel, create a new private repository from the template or a downloaded copy. Public forks are public, and their visibility cannot be changed independently. See GitHub's [fork documentation](https://docs.github.com/en/pull-requests/reference/forks).

## Before any upload or commit

Check the destination repository and its visibility. Review `git status` and `git diff --cached`. Look for manuscripts, interviews, names and contact details, credentials, licensed reference material, hidden attachments, and generated exports. Public CI runs after a push; it cannot undo disclosure.

The `_private/` directory is ignored for optional local scratch material. Environment files, common private keys, temporary files, and local worktrees are also ignored. **`.gitignore` is not access control or a complete privacy scanner.** It does not remove already tracked files or erase Git history. Do not rely on it to keep story directories private. See [GitHub's ignoring-files guide](https://docs.github.com/en/get-started/git-basics/ignoring-files).

Keep unpublished drafts in your private repository, not in a public fork with a renamed folder. Before publishing a writing workspace, review all tracked files and history and explicitly determine the license for creative content.

## Assistants and external services

The included Python scripts do not call external services. A connected AI assistant or editor may still transmit material to its provider. Authorize only the sources needed for the task and review the provider's privacy and retention settings. `AGENTS.md` is guidance, not technical isolation.

## An accidental disclosure

Stop further publishing. Revoke exposed credentials promptly where relevant. Removing a file in a new commit does not remove older copies. Follow the host's current sensitive-data removal guidance and assess who received the material. Do not post more sensitive details in a public issue while seeking help.
