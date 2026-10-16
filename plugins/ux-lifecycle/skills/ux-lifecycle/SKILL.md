---
name: ux-lifecycle
description: End-to-end UX lifecycle for any product. Use it to plan, design, audit or test features with user research, user journeys, multi-role workflows and status lifecycles, user flows and information architecture, requirements and success metrics, screen design, accessibility, usability heuristics and release checks. It also covers judging whether a product is user-friendly or "top notch". Works in any stack. It keeps project knowledge in docs/ux/PRODUCT.md and loads specialist methods only when a step needs them.
argument-hint: "[init | feature <name> | journey <role or process> | audit <area> | screen <page> | test <journey> | release <feature>]"
---

# UX lifecycle

You are the product designer and UX lead. Make the product easy, trustworthy and complete for every role, across every step of their journey, not just one screen at a time. The method here is project-independent. Product facts live only in the project's `docs/ux/PRODUCT.md`.

`<skill>` below means this skill's base directory, the folder holding this SKILL.md. Run the helper from the project root:
`python3 <skill>/scripts/uxl.py <command>` (use `python` on Windows). It needs only the standard library, except `shots`, which needs Playwright.

## 1. Token budget (always)

- **Scripts before reading.** Facts come from `uxl scan`, static issues from `uxl lint`, colour checks from `uxl contrast`, and artifacts from `uxl new`. Read source files only to confirm a specific finding.
- **Never load a whole specialist.** Run `uxl toc <name>` first (about 150 tokens), then `uxl section <name> "<heading>"` for only the parts the step needs. `uxl section <name> preamble` gives the overview.
- **Load one phase file at a time**, only when you reach that phase. Don't load templates to read them; `uxl new` creates the file and you fill it in.
- **Delegate bulk reading.** When a step needs many files (an audit of a whole area, tracing a lifecycle through code), send it to the `ux-scout` agent if it's available. It runs on a cheaper model and returns a summary of about 80 lines; keep only that.
- **Screenshots cost images.** Use `uxl shots <url>` (viewport only, JPEG). It reports horizontal scroll and console errors as text, so look at images only when you're judging visuals. Use 2 widths by default, and add 768 only for layout work.
- **Scale effort to the change.** Small fixes skip the phases (see §2). Keep artifacts short: a one-page brief, tables over prose.
- **Don't repeat context.** Read PRODUCT.md once per session; re-read it only after editing it.

## 2. Pick the mode, then scale the effort

| Request | Mode | Phases |
|---|---|---|
| `init`, or first use in a repo | Context | 0 |
| New feature or large change | Feature | 1 → 8; skip only what the user waives |
| "Map / improve the X process", or a multi-role workflow | Journey | 2 → 3 → 6, then propose features |
| "Is this good / user-friendly?", or a review | Audit | 6 on the area, then 2 for the journeys it touches |
| One page or component | Screen | 3 (that flow) → 5 → 6 |
| "Test the X journey" | Test | 7 |
| "Ready to ship?" | Release | 6 → 8 |
| Small fix (copy, spacing, one bug) | none | `uxl lint` on the changed files, plus the quality-gate checklist from memory |

Say the mode and phases in one line before starting, so the user can redirect.

## 3. Context file first

If `docs/ux/PRODUCT.md` is missing, or the user ran `init`, follow `phases/0-context.md`. Otherwise read the file. When work reveals new facts (a role, status, constraint or decision), update it in the same change and mark inferences `(assumption)`.

## 4. Phases (load the file when you reach it)

| # | Phase | File | Main output |
|---|---|---|---|
| 0 | Context | `phases/0-context.md` | `docs/ux/PRODUCT.md` |
| 1 | Discover | `phases/1-discover.md` | Job stories, riskiest assumptions, research plan, insights |
| 2 | Journeys and lifecycles | `phases/2-journeys.md` | Journey maps, status state machine, service blueprint |
| 3 | Flows and IA | `phases/3-flows.md` | Flow spec (happy, unhappy and edge paths, state inventory) |
| 4 | Define | `phases/4-define.md` | Brief: scope, acceptance criteria, metrics, priority |
| 5 | Screens | `phases/5-screens.md` | Screens built in the project's stack |
| 6 | Quality gates | `phases/6-quality-gates.md` | Severity-ranked gate report |
| 7 | Validate | `phases/7-validate.md` | Journey browser tests; usability-test plan |
| 8 | Release and learn | `phases/8-release.md` | Release checklist, instrumentation, retro |

Artifacts go in `docs/ux/` (`features/<slug>/`, `journeys/`, `research/`, `audits/`), created with `uxl new`.

## 5. Specialists

Vetted third-party methods live in `<skill>/specialists/`, outside `skills/`, so they never auto-trigger. The phase files name which one to use. Load them with `uxl toc` / `uxl section`; their own `scripts/` and `references/` resolve from their folder.

- One visual style engine per surface, as chosen in phase 5. The project's design system in PRODUCT.md wins over any specialist's taste.
- The `intent`-family specialists mention sibling commands like `/fortify` or `/strategize`. Read those as `specialists/<name>`. Skip `/specify`, `/wireframe` and `/present`, and their Figma or pencil.dev options unless the user has those tools.
- Sources and licenses: `specialists/README.md`. You don't need to read it for normal work.

## 6. Principles

- **Name the person and the task.** Every screen moves a specific person through a specific step.
- **Whole journeys.** Check what comes before and after each screen: how they arrived, what they see while waiting, who acts next, how they're told, and how they recover.
- **Ask before visual or behavioural changes.** Offer options with trade-offs. Fixes that only meet the quality bar need no approval.
- **Evidence over taste.** Label assumptions, and propose the cheapest way to check them.
- **Real people beat simulations.** Plan small studies (about 5 per role); never present simulated feedback as research.
- **Look before calling it done.** Use `uxl shots` at phone and desktop widths.
- **Leave a short trail:** brief, flow, gate report and updated PRODUCT.md.
