# Canon approval process

1. Stage a claim with its exact source, speaker, context, and uncertainty. Keep it outside `02_Canon/`.
2. Review conflicts, alternatives, scope, exceptions, and downstream effects. Intentional mysteries remain intentional mysteries.
3. Ask the author for a distinct approval decision. `Established` in an interview is not sufficient by itself. Record the author's actual wording or an exact evidence reference.
4. Create a decision in `00_Project/Decisions/` using an unused DEC ID. Only after approval set Status to Approved and record Approved_By and Approved_On.
5. Promote the reviewed claim to one authoritative CAN record in `02_Canon/`. Complete Source, Decision, Approved_By, Approved_On, Scope, Status: Canon, and Canonical: true using the [metadata standard](../00_Project/Metadata_Standard.md).
6. Update the [canon index](../02_Canon/Canon_Index.md), [decision log](../00_Project/Decision_Log.md), and links from affected development records.
7. Review the diff and commit this bounded promotion separately from unrelated drafting.

Changes to existing canon require the same process and a dependency review. Preserve superseded content through history and a Deprecated successor link. An assistant may prepare records but may not supply its own consent or approve its own suggestion.

A validator checks documentation structure, not whether a real human gave approval. The author remains responsible for the decision.
