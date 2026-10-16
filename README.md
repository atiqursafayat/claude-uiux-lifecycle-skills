# claude-ux-skills

A Claude Code plugin marketplace with one plugin, **`ux-lifecycle`**. It gives Claude a complete, project-independent UX process:

**research → journeys and status lifecycles → flows and IA → feature brief and metrics → screens → quality gates → browser and user validation → release and learning**

It works in any stack. Project knowledge lives in each project's `docs/ux/PRODUCT.md`. The skill drafts that file from the codebase on first use and asks you only about the gaps.

## Install in a project

From the project's root:

```bash
claude plugin marketplace add atiqursafayat/claude-ux-skills --scope project
claude plugin install ux-lifecycle@ux-skills --scope project
```

Commit the resulting `.claude/settings.json` so everyone working on the project, including cloud sessions, gets the plugin. Use `--scope user` instead to enable it for all of your projects on one machine.

For automated accessibility scans, also install AccessLint:

```bash
claude plugin marketplace add accesslint/claude-marketplace --scope project
claude plugin install accesslint@accesslint --scope project
```

## Use

```
/ux-lifecycle init                      # create docs/ux/PRODUCT.md for this project
/ux-lifecycle feature <name>            # full lifecycle for a new feature
/ux-lifecycle journey <role or process> # map a journey and its status lifecycle, find gaps
/ux-lifecycle audit <area>              # heuristic and accessibility audit with severities
/ux-lifecycle screen <page>             # design or redesign one screen
/ux-lifecycle test <journey>            # browser-test a journey end to end
/ux-lifecycle release <feature>         # pre-release gates and checklist
```

It also triggers on its own for UX, journey, flow and usability requests.

## What's inside

```
plugins/ux-lifecycle/skills/ux-lifecycle/
  SKILL.md        orchestrator: picks the mode and phases, sets the rules
  phases/         0-context … 8-release: method, outputs, exit checks
  templates/      PRODUCT.md, feature brief, interview guide, journey map,
                  lifecycle (state machine), flow spec, usability test, release checklist
  specialists/    vetted third-party skills, loaded only by the phase that needs them
```

Specialists stay outside `skills/`, so they never auto-trigger, compete or add to every session's context. `specialists/README.md` lists each one with its purpose, source, pinned commit and license:
- research, journeys, IA, service blueprints, edge cases, metrics, heuristic evaluation, accessibility, UX writing and localisation from [ghaida/intent](https://github.com/ghaida/intent) (CC0)
- browser testing and visual direction from [anthropics/skills](https://github.com/anthropics/skills)
- `ui-ux-pro-max`, `design-taste-frontend`, `bencium-controlled-ux-designer` and Vercel's `web-design-guidelines` (MIT)

## License

The original content (orchestrator, phases, templates) is MIT; see `LICENSE`. Each bundled specialist keeps its own license file.
