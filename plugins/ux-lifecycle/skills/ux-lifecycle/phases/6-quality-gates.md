# Phase 6: Quality gates (the bar for "user-friendly")

Run these on whatever was built or named for audit. Start with the tools, then judge what they can't:
- `uxl lint <paths>` runs static accessibility and UX checks over templates and components, grouped by rule with `file:line`.
- `uxl contrast <fg> <bg> …` checks the design-system text and background pairs (take them from PRODUCT.md tokens).
- `uxl shots <url>` reports horizontal scroll and console errors at each width.
- For a large area, have `ux-scout` run these and return the summary.

Then report each finding as `file:line` or `screen → element`, with a severity and a concrete fix. Raise the project's own bar from PRODUCT.md wherever it is stricter.

For a full audit, run the method in specialist `evaluate` (heuristic evaluation plus cognitive walkthrough), then use the gates below as the checklist.

## Severity

- **Critical:** blocks a core task, loses data or money, or excludes users who rely on assistive technology. Fix before shipping.
- **Serious:** a major barrier or a likely error; many users get stuck or need help.
- **Moderate:** friction, but the task is still completable.
- **Minor:** polish.

## Gate 1: Usability heuristics (Nielsen's 10, applied)

1. **Visibility of system status:** every action gets feedback within about 100 ms; long operations show progress; statuses are visible and current.
2. **Match with the real world:** the user's vocabulary, no internal IDs or jargon, and a natural order of steps.
3. **User control:** undo or cancel where possible; confirm only destructive or irreversible actions, and name the consequence.
4. **Consistency and standards:** the same words, icons, placement and patterns for the same things, and platform conventions are followed.
5. **Error prevention:** constraints, defaults and formats shown up front; dangerous actions are separated from common ones.
6. **Recognition over recall:** options are visible, previous inputs remembered, and context carried across steps.
7. **Flexibility:** shortcuts, bulk actions and filters for frequent users, without cluttering the screen for new ones.
8. **Minimalist design:** each element earns its place; hierarchy makes the primary action obvious.
9. **Error recovery:** messages say what happened and how to fix it, appear next to the problem, and keep the user's input.
10. **Help:** contextual hints where people get stuck, plus a findable path to human help.

## Gate 2: Accessibility (WCAG 2.2 AA minimum)

- Text contrast of at least 4.5:1 (3:1 for large text and UI components), and colour is never the only signal.
- Everything works by keyboard: logical focus order, visible focus, no traps; modals trap focus and restore it on close.
- Every input has a label; errors are linked to their fields and announced; icon-only buttons have accessible names.
- Semantic structure: one `h1`, ordered headings, landmarks, lists and tables used for what they are.
- Targets at least 24×24 CSS px (44×44 recommended on touch screens); usable at 200% zoom and at 320 px width without horizontal scrolling.
- `prefers-reduced-motion` respected; nothing flashes; no timeouts without warning and a way to extend.
- Images have meaningful alt text, or empty alt if decorative.

Read specialist `include` for the method. If the AccessLint plugin is installed, run `accesslint:accessibility-scan` on the live pages. Automated tools catch only part of the problems, so also do the keyboard and zoom checks by hand.

## Gate 3: States and robustness

Every screen in the flow spec's state inventory exists and is designed (method: specialist `fortify`):
- empty, loading (skeleton or spinner within 1 s), error, success, partial and permission-denied
- long text and long lists
- zero, one and many items
- slow network and double-submit

## Gate 4: Content and UX writing

Read specialist `articulate` for the method. In short:
- Use sentence case and plain words, front-load the meaning, and keep each sentence to one idea.
- Buttons say what happens ("Submit application", not "OK"), and the same action keeps the same name throughout the flow.
- Errors don't blame or apologise; they say what to do.
- Empty states invite the next action.
- Numbers, dates and currency are formatted for the user's locale.

## Gate 5: Performance and context

- Pages are usable quickly on the slowest device and network in PRODUCT.md. Images are sized and lazy-loaded, and the critical path has no heavy scripts.
- Mobile-first: the primary tasks are comfortable at 375 px.
- Internationalisation, if the product is multilingual (method: specialist `localize`):
  - no text baked into images
  - layouts survive longer translations (+30–40%)
  - fonts support every script in use
  - RTL handled if needed

## Gate 6: Trust, privacy and safety

- Users see why personal data is asked for and who will see it.
- Sensitive actions (money, approvals, deletions) are confirmed, recorded in an audit trail, and visible to the people affected.
- Role permissions are enforced on the server and reflected in the UI, which hides or disables what a user can't do and explains why.

## Gate 7: Visual design review

Use the visual engine chosen in `phases/5-screens.md`, and run specialist `web-design-guidelines` on the changed UI code. Check:
- hierarchy, spacing rhythm and alignment
- consistency with the design system
- no generic "AI-made" patterns

## Output

Write a gate report to the feature folder (or `docs/ux/audits/<area>-<date>.md`). It needs:
- a pass/fail line per gate
- findings sorted by severity
- what was not checked and why

Fix critical and serious findings before release unless the user explicitly accepts them.
