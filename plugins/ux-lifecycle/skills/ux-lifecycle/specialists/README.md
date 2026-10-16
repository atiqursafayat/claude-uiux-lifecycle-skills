# Specialists

These are vetted third-party skills, kept outside `skills/` so they never trigger by themselves. The `ux-lifecycle` phases tell you when to read one: `specialists/<name>/SKILL.md`. Each specialist's own relative paths, such as `references/` or `scripts/`, resolve from its own folder.

## When to use each

| Specialist | Use it for | Phase |
|---|---|---|
| `strategize` | Problem framing, hypotheses, opportunity sizing, scoping | 1 |
| `investigate` | Research planning, interviews, usability-test protocols, surveys, synthesis | 1, 7 |
| `personas` | Research-backed personas, validity thresholds, anti-patterns (`persona-methodology.md`) | 1 |
| `journey` | Journey maps, task flows, multi-step workflows, decision points | 2, 3 |
| `blueprint` | Service blueprints, multi-role and back-office processes, failure-mode analysis | 2 |
| `organize` | Information architecture, navigation, taxonomy, labels, card sorts, tree tests | 3 |
| `fortify` | Unhappy paths, state inventories, errors, empty, loading and first-run states | 3, 6 |
| `measure` | Success metrics (HEART, Goal-Signal-Metric), A/B test design | 4, 8 |
| `frontend-design` | Planning a distinctive visual direction before building | 5 |
| `bencium-controlled-ux-designer` | Ask-before-deciding protocol; accessibility, responsive and motion references | 5 |
| `ui-ux-pro-max` | App screens: style and palette data, UX rules, chart choice, stack-specific guidance | 5, 6 |
| `design-taste-frontend` | Public, marketing and landing pages only (not dashboards or app screens) | 5 |
| `evaluate` | Heuristic evaluation, cognitive walkthrough, severity-ranked UX audit | 6 |
| `include` | Accessibility as a design discipline: WCAG 2.2, screen readers, keyboard, cognitive and motor | 6 |
| `articulate` | UX writing: voice and tone, labels, errors, empty states, CTAs | 6 |
| `localize` | Languages, scripts, cultural adaptation, formats | 6 |
| `web-design-guidelines` | Rule-by-rule review of UI code (fetches Vercel's current rules) | 6 |
| `webapp-testing` | Driving the running app with Playwright: screenshots, console logs, scripted journeys | 7 |

## Reading the `intent` specialists

The `intent` skills were written as one suite of slash commands and refer to each other by command name. Inside this plugin, read those references as follows:

- **Commands bundled here:** `/strategize`, `/investigate`, `/journey`, `/organize`, `/blueprint`, `/fortify`, `/evaluate`, `/articulate`, `/measure`, `/include` and `/localize` each mean `specialists/<name>/SKILL.md`.
- **Commands not bundled:**
  - `/specify`: use phase 4 and the flow spec.
  - `/wireframe`, `/present`, `/storytelling`, `/transpose`, `/philosopher`: skip those steps.
- **Diagram output:** use the default self-contained HTML or Mermaid output. The Figma and pencil.dev options need their own MCP servers; use them only if the user has those connected and asks for them.

Their "routing" advice is a suggestion only. The `ux-lifecycle` phase order decides what runs next.

## Sources

| Specialist | Source | Commit | License | Local changes |
|---|---|---|---|---|
| strategize, investigate, journey, blueprint, organize, fortify, measure, evaluate, include, articulate, localize | [ghaida/intent](https://github.com/ghaida/intent) `skills/<name>` (v1.7.1) | `3fc38df` (2026-10-10) | CC0-1.0 | none |
| personas | [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) `product-team/skills/ux-researcher-designer/references/persona-methodology.md` | `19392f7` (2026-08-26) | MIT | only that reference file; the random-name persona generator script was left out |
| frontend-design, webapp-testing | [anthropics/skills](https://github.com/anthropics/skills) `skills/<name>` | `dbd4588` (2026-10-09) | Apache-2.0 | none |
| web-design-guidelines | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | `063bee9` (2026-08-28) | MIT (per the README) | none |
| ui-ux-pro-max | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) `.claude/skills/ui-ux-pro-max` (v2.15.0) | `56ea9cf` (2026-10-15) | MIT | `scripts/tests/` removed; script paths written as `<ui-ux-pro-max-dir>/scripts/search.py`, where the dir is this specialist's folder |
| design-taste-frontend | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) `skills/taste-skill` | `f624f37` (2026-10-14) | MIT | `evals/` removed |
| bencium-controlled-ux-designer | [bencium/bencium-claude-code-design-skill](https://github.com/bencium/bencium-claude-code-design-skill) | `5de46a3` (2026-10-04) | MIT | none |

## Runtime notes

- `ui-ux-pro-max`: Python 3 standard library over bundled CSV files. No network.
- `webapp-testing`: needs Python `playwright` and a Chromium browser. `scripts/with_server.py` starts the server commands you pass it.
- `design-taste-frontend`:
  - Node scripts.
  - `assets.mjs` fetches openly licensed images from public APIs.
  - `inspect.mjs` drives a local Chrome.
- `web-design-guidelines`: fetches its rules from raw.githubusercontent.com on each run.
- All others are markdown only.

## Updating

Re-copy a specialist from upstream, re-apply the local changes above, review the diff, and update the commit.
