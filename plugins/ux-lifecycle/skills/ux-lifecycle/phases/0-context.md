# Phase 0: Context (create or refresh `docs/ux/PRODUCT.md`)

Goal: a short, accurate file that tells any later session who the product is for, what they're trying to do, and the standards the product is held to.

## Steps

1. **Read before asking.** Run `uxl scan`. It reports the stack, UI folders, roles, every status enum, routes, notification call sites (including commented-out ones), i18n and analytics in about 1,000 tokens. Confirm or extend those facts by reading only the specific files it points to, or ask the `ux-scout` agent. Look for:
   - README and docs
   - the routes or URL config, which show the screens
   - models or schema, especially status and state fields, which show the lifecycles
   - user and role or permission code, which shows the roles
   - templates and components, along with CSS tokens and theme config, which show the design system
   - locale files, which show the languages
   - notification and email code, which shows the handoffs
   - analytics, if any
2. **Draft** `docs/ux/PRODUCT.md` by running `uxl new PRODUCT`, then filling it in. Fill every section you can from the code, and mark inferred items `(assumption)`.
3. **Ask the user only about the gaps**, and at most about 6 questions in one message. Prioritise:
   - Who are the primary users, and which one matters most?
   - What is the single most important job of the product?
   - Which journeys hurt today? Ask for support complaints and drop-offs.
   - What are the constraints: devices, connectivity, languages, literacy, accessibility, regulation?
   - What does "top notch" mean here, and which competitors or references do they admire?
   - Is there real usage data or research?
4. Update the file with the answers, removing `(assumption)` where confirmed.
5. Keep it under about 200 lines. Link out to longer documents instead of copying them in.

## Exit check

- Every role is named with its main goal.
- The core lifecycles are listed with their statuses.
- Constraints and the quality bar are explicit.
- The design-system source is identified.
- The user has seen the file.
