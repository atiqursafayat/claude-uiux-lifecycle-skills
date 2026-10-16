# Phase 8: Release and learn

Goal: ship safely, then find out whether it worked, and feed what you learn back in.

**Specialist:** `measure` for instrumentation and reading results.

## Release checklist (`uxl new release-checklist --name <feature>`)

- The quality gate report has no open critical or serious findings, or the user has accepted them in writing.
- Acceptance criteria verified, including the browser test of the main journey (phase 7).
- Existing data and in-flight records work with the change: migrations, records already part-way through a lifecycle, old links and emails.
- Every notification, email and SMS that the flow sends has been reviewed, both content and trigger.
- Help content, FAQs and admin or staff guidance are updated, and support knows what changed.
- A rollback plan, or a feature flag for risky changes.
- Instrumentation is live for the primary metric and the guardrails.
- Changelog or release note written in user language.

## Measure

- Track the funnel of the journey, step by step, to find where people drop off.
- Track task success, time on task, error and validation-failure rates, and support contacts about the feature.
- Prefer privacy-respecting, aggregate analytics; never log sensitive personal data.
- Review the metrics against the targets in the feature brief at an agreed date, such as 2–4 weeks after release.

## Learn

- Collect qualitative feedback: an in-product prompt at the end of the journey, support tickets, and a few follow-up conversations.
- Write a short retro in the feature folder: target vs. actual, what surprised us, and what's next.
- Update `docs/ux/PRODUCT.md` with new facts and decisions, and add follow-up items to the backlog with priorities (phase 4).
