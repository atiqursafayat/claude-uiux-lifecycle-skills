# Phase 2: Journeys and lifecycles

Goal: see the whole experience across time and roles, so gaps between screens and between people become visible. Most "unfriendly" products fail here, not on individual screens.

**Specialists:**
- `specialists/journey/SKILL.md` for journey maps and multi-step workflows
- `specialists/blueprint/SKILL.md` for multi-role, back-office processes and failure modes

## A. Journey map (one per role and goal)

Use `templates/journey-map.md`. Columns are stages, such as discover → sign up → do the main task → wait → get the outcome → come back. For each stage, record:
- **What the user is doing** and their goal at that moment
- **Touchpoints**: the screen, email, SMS, notification or offline contact
- **What they need to know**, and whether the product actually tells them
- **Pain points and risks**: confusion, waiting without feedback, re-entering data, fear of mistakes
- **Emotion**: a rough high, neutral or low, drawn from evidence where possible
- **Opportunities**: ideas, not commitments

Build the map from the real product: walk the routes in code, or click through the running app. Don't work only from intentions.

## B. Lifecycle state machine (for anything with a status)

Applications, orders, tickets, payments and approvals all need one. Use `templates/lifecycle.md`. Document:
- Every status, with the user-facing name for each one (not the database enum)
- Every transition: who or what triggers it, conditions, side effects
- **Who acts next** in each status, and whether they know it. A notification, task list or badge must exist.
- Time limits, reminders and escalations for statuses that can stall
- Exits: cancel, withdraw, reject, expire, reopen and appeal. Each needs a reason and a message the user can see.
- Reversibility: what can be undone, by whom, and with an audit trail

Then check it: every status needs an owner, a way out and a visible explanation, and every money or decision transition needs an audit record. Missing ones are findings.

## C. Service blueprint (when several roles or back-office steps are involved)

Use these lanes, top to bottom:
1. User actions
2. Front-stage: what the user sees
3. Back-stage staff actions
4. Support systems: jobs, emails, integrations, payments

It exposes:
- handoffs nobody owns
- invisible waiting
- manual steps that need tooling
- places where the user isn't told what's happening

## D. Cross-journey checks

- The same object has the same name and status everywhere: list, detail, email and report.
- Each role's home or dashboard answers three questions: what needs my attention, what is in progress, and what happened recently.
- A first-time user can reach their first success without help. Onboarding and empty states lead them there.
- The returning user resumes where they left off.

## Exit check

Journey maps and the state machine are saved in `docs/ux/journeys/`. Every gap found is listed with a severity (see `phases/6-quality-gates.md`) and fed into feature briefs or the backlog.
