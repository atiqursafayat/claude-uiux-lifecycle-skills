# Phase 4: Define (scope, acceptance criteria, metrics, priority)

Goal: agree on what "done" and "successful" mean before building.

**Specialist:** `specialists/measure/SKILL.md` for choosing metrics (HEART, Goal-Signal-Metric) and designing A/B tests.

## Steps

1. **Complete the feature brief** (`templates/feature-brief.md`, bottom half):
   - **Scope:** what is in this release and what is explicitly out (non-goals).
   - **Acceptance criteria:** written as user-observable outcomes (Given / When / Then). Include UX criteria, not just function: states covered, accessibility level, copy reviewed, works at 375 px, performance budget.
   - **Success metrics:** one primary metric tied to the job story, such as task completion rate, time to complete, drop-off at a named step, or support tickets about it. Add one or two guardrails, such as error rate or opt-outs. Give each a baseline (or "unknown"), a target, and how it will be measured.
   - **Dependencies and risks:** data, permissions, notifications, legal or privacy, migration of existing records.
2. **Prioritise** when there are several candidates. Use RICE (Reach × Impact × Confidence ÷ Effort), or MoSCoW for a fixed release. Show the scores so the user can disagree. Fixes that unblock a core journey come before new features.
3. **Slice thin.** Prefer the smallest release that completes the journey end-to-end over a broad release that leaves gaps between steps.
4. **Get the user's approval** of the brief before phase 5.

## Exit check

- The brief has acceptance criteria, including UX criteria, a primary metric and non-goals.
- The user has approved it.
