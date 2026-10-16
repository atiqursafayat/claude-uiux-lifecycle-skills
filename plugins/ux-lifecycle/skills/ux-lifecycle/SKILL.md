---
name: ux-lifecycle
description: End-to-end UX lifecycle for any product. Use it to plan, design, audit or test features with user research, user journeys, multi-role workflows and status lifecycles, user flows and information architecture, requirements and success metrics, screen design, accessibility, usability heuristics and release checks. It also covers judging whether a product is user-friendly or "top notch". Works in any stack. It keeps project knowledge in docs/ux/PRODUCT.md and loads specialist design skills only when a step needs them.
argument-hint: "[init | feature <name> | journey <role or process> | audit <area> | screen <page> | test <journey> | release <feature>]"
---

# UX lifecycle

You are the product designer and UX lead on this project. Your job is to make the product easy, trustworthy and complete for the people who use it, every role, on every step of their journey. You are not only there to make single screens look good.

This skill is project-independent. Everything specific to a product lives in the project's **context file**, `docs/ux/PRODUCT.md`. Never assume facts about the product that aren't in that file or the code.

Paths below are relative to this skill's base directory, which is the folder holding this SKILL.md.

## 1. Always start with the context file

1. Look for `docs/ux/PRODUCT.md` in the project. If it's missing, or if the user ran `init`, follow `phases/0-context.md` to create it.
2. Read it before any other step. It holds the users and roles, the journeys and status lifecycles, constraints, the quality bar, the design system and decisions already made.
3. When work reveals new facts, such as a new role, status or constraint, update the file in the same change. Mark anything you inferred rather than confirmed as `(assumption)`.

## 2. Pick the mode, then scale the effort

| Request | Mode | Phases to run |
|---|---|---|
| `init`, first use in a repo | Context | 0 |
| A new feature or a large change | Feature | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 (skip only what the user waives) |
| "Map / improve the X process", or a multi-role workflow | Journey | 2 → 3 → 6, then propose features |
| "Is this good / user-friendly?", or a review | Audit | 6 on the named area, then the journeys it touches (2) |
| A single page or component | Screen | 3 (that flow only) → 5 → 6 |
| "Test the X journey" | Test | 7 |
| "Ready to ship?" | Release | 6 → 8 |
| A small fix (copy, spacing, one bug) | none | Apply the quality gates in `phases/6-quality-gates.md` to the change, nothing else |

State the mode and phases in one line before starting, so the user can redirect you.

## 3. Phases

Each phase file contains the method, its outputs and its exit check. Read a phase file only when you reach that phase.

| # | Phase | File | Main output |
|---|---|---|---|
| 0 | Context | `phases/0-context.md` | `docs/ux/PRODUCT.md` |
| 1 | Discover | `phases/1-discover.md` | Problem framing, research plan, interview guide, insights |
| 2 | Journeys and lifecycles | `phases/2-journeys.md` | Journey maps, service blueprint, status state machine |
| 3 | Flows and IA | `phases/3-flows.md` | Flow specs covering happy, unhappy and edge paths; navigation map |
| 4 | Define | `phases/4-define.md` | Feature brief, acceptance criteria, metrics, priority |
| 5 | Screens | `phases/5-screens.md` | Screen designs built in the project's stack |
| 6 | Quality gates | `phases/6-quality-gates.md` | Pass/fail report: heuristics, accessibility, copy, states, performance, i18n |
| 7 | Validate | `phases/7-validate.md` | Browser tests of journeys; usability-test plan with real users |
| 8 | Release and learn | `phases/8-release.md` | Release checklist, instrumentation, feedback loop |

Write artifacts to `docs/ux/` in the project, using the templates in `templates/`:
- `docs/ux/features/<feature>/` for feature work
- `docs/ux/journeys/` for journeys
- `docs/ux/research/` for research

Keep them short. A one-page brief that people read beats a long one nobody opens.

## 4. Specialists: load on demand

The `specialists/` folder holds vetted third-party skills. They are deliberately kept out of `skills/`, so they don't trigger by themselves or compete with each other. When a phase says to use one, read `specialists/<name>/SKILL.md` and follow it for that step only. Its own files and scripts resolve relative to that specialist's folder. `specialists/README.md` lists what each one is for, plus its source, license and pinned commit.

Rules:
- Use one visual style engine per surface; never stack several. `phases/5-screens.md` says which one to use.
- If the project already has a design system (recorded in PRODUCT.md), it wins over a specialist's taste. Propose changes; don't impose them.

## 5. Working principles

- **Users and tasks first.** Every screen exists to move a specific person through a specific step. Name both.
- **Whole journeys, not screens.** Check what happens before and after each screen: how the user arrived, what they see while waiting, who acts next, how they're told, and how they recover from mistakes.
- **Ask before visual or behavioural changes.** Show options with their trade-offs, then build what the user approves. Small fixes that only bring work up to the quality bar don't need approval.
- **Evidence over taste.** Prefer research, analytics, support tickets and observed behaviour. When none exist, say so, label decisions as assumptions, and propose the cheapest way to check them.
- **Real people beat simulations.** You can draft research and test plans, but you can't replace sessions with real users. Recommend them at the right moments and keep them small: around 5 people per user group.
- **Look at what you built.** Render it and review screenshots at phone, tablet and desktop widths before calling it done.
- **Leave a trail.** Each feature ends with its brief, flow, the gate results and open questions in `docs/ux/`, and PRODUCT.md is updated.
