# Metadata and identifiers

Use UTF-8 Markdown for working records. Preserve received sources in their original format and name. A cataloged record has one stable ID, one home, source links, scope, status, and known dependencies. Never reuse an ID. Root READMEs and blank trackers are not cataloged records.

| Prefix | Record |
| --- | --- |
| SRC-0001 | Source register entry |
| INT-0001 | Creator interview |
| CLM-0001 | Staged claim |
| DEC-0001 | Author decision |
| CAN-0001 | Approved canon |
| CHR-0001 / LOC-0001 | Development character / location |
| EVT-0001 / REL-0001 | Event / relationship |
| THR-0001 / SCN-0001 | Plot thread / scene |
| Q-0001 / REV-0001 | Question / revision |
| BOOK-001 | Book folder |

Templates use `ID: TEMPLATE`, `Status: Template`, and `Canonical: false`. Copy a template into its working collection, assign an unused ID, and change its status to Draft or Proposed. Never start a proposed record as approved.

The optional validator supports **flat scalar frontmatter only**, not general YAML structures. Use exact field names, one value per line, and no multiline values. Put complex lists in the document body. For an actual approved canon record:

```yaml
---
ID: CAN-0001
Status: Canon
Canonical: true
Scope: series
Source: ../01_Artifacts/source-record.md
Decision: ../00_Project/Decisions/DEC-0001.md
Approved_By: author name
Approved_On: YYYY-MM-DD
---
```

This is a schema example, not an approval. Replace references and date with real evidence. An approved decision uses `Status: Approved`, `Approved_By`, and `Approved_On`. Source and Decision paths are relative to the record containing them; preserve precise message or passage anchors in the body. Do not copy private source contents into public records.

Statuses mean different things: Draft/Proposed are development, Approved is a human decision or accepted story plan, Canon is an approved fictional fact, and Deprecated/Rejected preserve retired material. Interview labels (`Established`, `Working idea`, `Unknown`, `Intentional mystery`, `Not relevant`) describe testimony and are not canon status.

The scene registry is CSV with one unique `SCN-` ID per row. Supported statuses are Planned, Drafting, Drafted, Reviewed, Approved, and Released. Separate scene dependencies with semicolons. Quote CSV fields containing commas. Scene approval is not canon approval.
