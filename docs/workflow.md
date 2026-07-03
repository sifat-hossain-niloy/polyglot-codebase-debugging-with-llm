# Session Workflow

How to start, work through, and end a Claude session in this repo.

## Starting a session

1. **Open the repo root in Claude Code.** [CLAUDE.md](../CLAUDE.md) auto-loads.
2. **Read [STATUS.md](../STATUS.md).** Find the active step.
3. **Open the active step's `STATUS.md`** (e.g., `steps/01-empirical-characterization/STATUS.md`). Find the active sub-step.
4. **Read the sub-step's `CLAUDE.md` and `STATUS.md`.** That's your starting brief.
5. **Don't re-summarize the plan to the user.** They wrote it. Just confirm what you're about to do.

## During a session

- Work on **one sub-step at a time**. If a thought belongs to a different sub-step, jot it as an open question in the current `STATUS.md` and continue.
- **Schema-validate** any JSONL output before claiming a task is done. See [shared/schemas/](../shared/schemas/).
- **Cite the plan section** in commits and prompts: `§3.3 Step 1.1`. Keeps work traceable.
- If a script is non-trivial, add a `scripts/README.md` in the sub-step explaining how to run each script.

## Ending a session

Before stopping, **always**:

1. Update the sub-step's `STATUS.md`:
   - Move items from "What's next" → "What's done."
   - Add anything you found surprising or any unanswered question to "Open questions."
   - Update the **Last updated** date and the **State** indicator.
2. If you finished a sub-step (state = 🟢), update the parent step's `STATUS.md` to mark the next sub-step as active.
3. If you finished a step entirely, update the global [STATUS.md](../STATUS.md) and bump the active step.

Failure to do this is the #1 cause of duplicated or lost work in multi-session research repos. Don't skip it.

## Handing off mid-task

If you have to stop mid-task (e.g., a script is running long, a question needs the user's input):

1. In the sub-step's `STATUS.md`, write a "🟡 in progress" block under **What's done** describing:
   - What you've done.
   - What state files are in (paths + line numbers).
   - What the next session needs to do to resume.
2. Don't commit partial scripts that don't run. Either finish the script or stash it as a comment in `STATUS.md`.

## Spawning sub-agents

When using the `Agent` tool inside a session:

- For broad GitHub search ("find Java+TS monorepos with active CI"), use `general-purpose`.
- For code-base questions inside this repo, use `Explore`.
- Always state in the prompt which sub-step you're in (e.g., "I'm working in `steps/01-empirical-characterization/01-github-mining/`") so the agent can read the local CLAUDE.md.

## When to ask the user

Ask, don't guess, when:

- The taxonomy or annotation protocol needs a decision the plan doesn't specify.
- A baseline agent run will cost over ~$10 in API tokens.
- You'd be deleting or replacing data that another session produced.
- A scope or scheduling question affects the publication target (e.g., "should we include Rust in the workshop paper?").

Otherwise, document the assumption in `STATUS.md` and proceed.

## When to push back

Push back on the user (politely) if:

- A request would skip Step 1's empirical work and jump to Step 3's tool building. The plan and the publication strategy depend on the empirical foundation existing first.
- A request would publicly release data without checking license/PII on GitHub-mined content.
- A request would commit raw mined data >10MB to git.
