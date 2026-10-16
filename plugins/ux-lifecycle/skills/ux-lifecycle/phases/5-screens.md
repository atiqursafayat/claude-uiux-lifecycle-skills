# Phase 5: Screens

Goal: screens that carry the approved flow, follow the project's design system, and look deliberate, not templated.

## 1. Pick one visual engine for the surface

| Surface | Specialist (load with `uxl toc` / `uxl section`) |
|---|---|
| Logged-in app screens: dashboards, forms, tables, settings, admin, charts | `ui-ux-pro-max`. Use the stack from PRODUCT.md, e.g. `--stack html-tailwind`, `react` or `shadcn`. |
| Public, persuasive pages: home, landing, marketing, storytelling | `design-taste-frontend` |
| Anything without an established direction | `frontend-design` to plan the direction first |

Don't stack engines on one surface. Whatever you pick, the design system recorded in PRODUCT.md wins: specialists inform it, they don't replace it.

## 2. Plan, then ask

1. Write a compact design plan for the screen:
   - the content hierarchy: what the user must see first, second and third
   - layout at 375 px and at desktop width (an ASCII sketch is enough)
   - components reused from the design system, and new ones needed
   - every state from the flow spec's state inventory
2. Check the plan against the generic patterns in `uxl section frontend-design "Process"` and revise anything that's a default rather than a choice.
3. Follow the ask-first protocol, `uxl section bencium-controlled-ux-designer "Core Philosophy"` (about 90 tokens): present the plan with options and trade-offs, and get the user's approval before changing visual tokens, layout patterns or behaviour. Building to an already-approved design or system needs no new approval.

## 3. Build in the project's stack

- Reuse existing components and tokens; extend the design system rather than one-off styling. Record new tokens or components in PRODUCT.md.
- Use semantic HTML first and ARIA only where needed. Labels and errors are wired to their inputs.
- Design every state, not just the full happy state: empty, loading, error, success and permission-denied.
- Copy comes from `articulate` patterns: action-named buttons, and errors that say what to do.
- Mobile-first, and inside the performance budget from PRODUCT.md.

## 4. Look at it

Run `uxl shots <url>` (375 and 1280 px; add `--widths 375,768,1280` for layout work; pass `--storage-state` for logged-in pages). Fix anything it reports as text first, such as horizontal scroll or console errors, then look at the images. Check them against the plan, fix everything one look reveals, then look again. A screen isn't done until you've seen it.

## Exit check

- Approved plan built.
- All states present.
- Screenshots reviewed at three widths.
- Design-system changes recorded.
- Ready for phase 6.
