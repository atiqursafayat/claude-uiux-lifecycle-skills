# Phase 7: Validate

Goal: prove that real tasks can be completed end to end, first by machine, then by people.

## A. Journey tests in a real browser (every feature)

Read `specialists/webapp-testing/SKILL.md` for the Playwright mechanics. Then turn the flow spec into test scenarios. The scenarios are what make these UX tests rather than plain clicking.

1. **One scenario per flow**, written as the user's goal. For example: "A new applicant submits an application from a phone." Use a test account for each role.
2. **Happy path:** drive every step from the real entry point (the email link, the dashboard card), not a deep link to the middle. Assert that each step's system response appears.
3. **Unhappy paths:** for each row in the flow spec's unhappy-path table, cause the condition and assert what the user should see and how they recover:
   - invalid input
   - a duplicate submission
   - abandoning and resuming
   - a forbidden role
4. **State coverage:** visit each screen with empty, partial and full data. Assert that empty states show a next action and that nothing renders raw, like `None`, `undefined`, `NaN` or an error trace.
5. **Viewports:** run at 375×812 and 1280×800. Take a screenshot at each step and review the images yourself.
6. **Hygiene:** fail the test on console errors and failed network requests.
7. **Handoffs:** for multi-role lifecycles, continue as the next role. Check that the item appears in their queue with the right status, and that the notification or email was produced, either in the test mail outbox or in logs.

Keep the scenarios in the project's test suite if it has browser tests, so they guard against regressions. Otherwise save them in `docs/ux/features/<feature>/journey-tests/`. Report pass/fail per scenario, with screenshots of any failures.

## B. Accessibility checks on the running pages

- If the AccessLint plugin is installed, run `accesslint:accessibility-scan` on each screen in the journey.
- Otherwise use the checks in `specialists/include/SKILL.md` and Gate 2 of phase 6.
- Always do the keyboard-only walk-through and the 200%-zoom check by hand.

## C. Usability test with real people (new or changed core journeys)

- Read `specialists/investigate/SKILL.md` (its usability-testing section) and fill `templates/usability-test-plan.md`.
- Recommend about 5 participants per role, in their real context and on their real devices.
- Prepare the plan, the tasks, test data and the note-taking sheet. The user or their team runs the sessions; you help synthesise the results afterwards.
- Never present simulated "user feedback" as research. If no sessions are run, record that the change has not been validated with users, and why.

## Exit check

- All journey scenarios pass, or failures are logged as findings with a severity.
- The accessibility scan is clean of critical and serious issues.
- A usability test is planned or done for core-journey changes.
