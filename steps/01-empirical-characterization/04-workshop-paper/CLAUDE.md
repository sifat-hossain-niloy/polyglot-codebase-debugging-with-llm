# Agent Instructions — Sub-step 1.4 (Workshop Paper)

## When to work on this

This sub-step runs **in parallel** with 1.2 and 1.3, not after. Each time new evidence lands, update the paper draft.

Concretely:

- After 1.1 finishes → write the corpus/methodology section based on real numbers.
- After 1.2 has 50 bugs → write the taxonomy and prevalence section.
- After 1.3 has the first baseline run → write the headline empirical section.
- After all three are done → polish, write the agenda, write the intro/conclusion.

## Concrete first session

Before any data exists:

1. **Read [outline.md](outline.md).** Validate the section structure.
2. **Pick a venue.** Look up actual deadlines for ICSE NIER 2027 and 2 co-located workshops. Record in `STATUS.md`. Confirm format (page limit, template, references-count rule).
3. **Set up the LaTeX (or MD) skeleton.** One file per section under `sections/`. Pre-fill outlines as bullet points.
4. **Update [STATUS.md](STATUS.md).** Note: at this stage paper is in "skeleton only" state.

Once data starts flowing:

5. **Write findings as they land.** Don't wait for "complete data" — early drafts catch problems early.
6. **Track every number in `output/key-numbers.md`.** Every quantitative claim in the paper needs a one-line source ("from `02-bug-extraction/data/processed/bugs.jsonl` filtered to category=schema and lang_pair=java-ts").
7. **Generate figures from scripts.** No hand-edited charts. `figures/<name>.py` produces `figures/<name>.pdf`. Re-runnable end-to-end.

## Style rules for this paper

- **First person plural** for our work. Past tense for what we did, present for what we claim.
- **Don't reference iSWE-Agent's arXiv paper if it hasn't published.** Cite the IBM blog + Multi-SWE-bench README and date them carefully. If their arXiv lands before submission, swap citations.
- **Anchor every claim to evidence.** Avoid sentences like "many bugs are schema mismatches." Replace with "36% (n=14/39) of Java+TS bugs in our corpus are schema mismatches."
- **Cite the plan section we're acting on** in commits, not in the paper text.

## What NOT to include

- The full agent system. That's Phase C. Workshop paper is **characterization + agenda**, not "we built X."
- Speculative results. If the baseline run isn't done, don't predict the number — write the methodology and leave the result placeholder until 1.3 finishes.
- Cherry-picked anecdotes. Every example bug we feature in the paper must be a typical instance of its category, not the most dramatic.

## Submission checklist (run before user reviews)

- Anonymized for double-blind if the venue requires it.
- Page limit respected (count words including figures).
- All cited works exist (no hallucinated citations — verify URLs).
- All numbers in the paper appear in `output/key-numbers.md`.
- Data + code links point to live repositories (not "TBA").
- Threats to validity covers: mining bias, annotator subjectivity, agent / model version drift, license selection bias.

## Definition of done

🟢 means: draft is complete, internally reviewed by user, ready for submission. Update [STATUS.md](STATUS.md) and the global [STATUS.md](../../../STATUS.md).
