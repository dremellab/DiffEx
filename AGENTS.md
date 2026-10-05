## Superpowers usage policy

Superpowers is an optional workflow framework, not the default way to perform tasks.

Optimize for **correctness, speed, and token efficiency**. For routine work, prefer direct repository inspection, implementation, and targeted validation using the normal available tools.

### Default: do not invoke Superpowers

Do NOT invoke a Superpowers skill merely because it appears relevant to the task.

For small, routine, low-risk, or well-understood tasks, work directly without Superpowers.

Examples that normally should NOT use Superpowers include:

- Documentation, README, comments, spelling, formatting, or other prose-only changes.
- Minor configuration changes.
- Small bug fixes with an obvious cause and solution.
- Small or mechanical refactors.
- Adding or modifying a few lines/functions where the implementation is clear.
- Routine dependency/version updates.
- Simple test changes.
- Code explanation or repository exploration.
- Other inconsequential changes where an elaborate workflow would add more overhead than value.

### When Superpowers is appropriate

Consider Superpowers only when the task is sufficiently **large, non-routine, ambiguous, or risky** that a structured workflow is likely to materially improve the result.

Good candidates include:

- Large or non-routine feature additions.
- Significant architectural or design changes.
- Changes spanning multiple components or subsystems.
- Complex bugs whose root cause is unclear.
- Refactors with substantial regression risk.
- Changes to core infrastructure, pipelines, APIs, schemas, or shared interfaces where mistakes could break existing functionality.
- Work where requirements are ambiguous enough that structured brainstorming or planning would materially reduce risk.
- Tasks where the user explicitly requests a Superpowers workflow.

Use the smallest subset of Superpowers necessary for the task. Do not automatically chain brainstorming, planning, TDD, review, and verification workflows.

## TDD policy

**Do NOT use the Superpowers TDD workflow by default.**

The TDD workflow is intentionally reserved for substantial implementation work where its additional tests, validation steps, and token/latency cost are justified by the risk or complexity of the change.

### Use TDD when

Consider the Superpowers TDD workflow for:

- Large or non-routine feature additions.
- Significant behavioral changes.
- Complex business or scientific logic.
- Changes to critical shared code.
- Refactors where preserving existing behavior is difficult or especially important.
- Bugs where a regression test is important to prevent recurrence.
- Work where the user explicitly requests TDD.

### Do NOT use TDD when

Do not invoke the Superpowers TDD workflow for:

- Documentation, README, comments, or prose changes.
- Formatting or lint-only changes.
- Simple configuration changes.
- Small and obvious bug fixes.
- Minor refactors with low regression risk.
- Mechanical code changes.
- Routine maintenance.
- Changes where existing tests already provide adequate coverage and only targeted validation is necessary.
- Any task where generating substantial new test scaffolding would be disproportionate to the size or risk of the change.

For these tasks, perform only the **minimum targeted validation appropriate to the change**.

For example, a small code fix may warrant running an existing relevant test or a focused command. A documentation-only edit generally does not warrant adding tests or invoking a TDD workflow.

### Decision rule

Before invoking any Superpowers workflow, ask:

1. Is this task large, non-routine, ambiguous, or potentially code-breaking?
2. Will the structured workflow materially improve correctness or reduce meaningful risk?
3. Is that benefit proportional to the additional latency, context usage, tests, and validation work?

If not, do the task directly.

When uncertain, prefer the simpler workflow.

**Do not turn a small task into a large task merely to satisfy a Superpowers process.**