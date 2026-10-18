# Contributing

Help improve a reusable writing system, not a particular fictional universe. Contributions can be documentation corrections, clearer templates, accessibility improvements, better workflows, or tested tools.

Open an issue describing the problem and intended user benefit. For substantial changes, discuss scope before implementation. Fork the public repository, create a focused branch, and submit a pull request. Keep creative projects in separate workspaces; never submit private manuscripts, interview transcripts, credentials, or third-party material without redistribution rights.

Use neutral fixtures and preserve author-control boundaries. Disclose AI assistance in the pull request when material was generated with it, and verify the result yourself. No assistant can approve the author's canon or claim a human review that did not happen.

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_framework.py
```

Document behavior changes and limitations. New utility behavior should have a regression test. Avoid network dependencies or external AI requirements unless the proposal explicitly justifies them. Do not add automatic ingestion, canon promotion, manuscript generation, merging, or publication.

Submit only contributions you have the right to distribute under the [MIT License](LICENSE). Maintainers review contributions before accepting them. Follow the [community expectations](CODE_OF_CONDUCT.md).
