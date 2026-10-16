# Phase 1: Discover (understand the problem before designing)

Goal: be clear about whose problem this is, how they cope today, and how we'll know it's solved. Then decide how much research it deserves.

**Specialists:**
- `specialists/strategize/SKILL.md` for problem framing and hypotheses
- `specialists/investigate/SKILL.md` for research methods, guides, surveys and synthesis
- `specialists/personas/persona-methodology.md` before writing personas

## Steps

1. **Frame the problem** in the feature brief (`templates/feature-brief.md`, top half):
   - Job story: *When* \<situation>, *I want to* \<motivation>, *so I can* \<outcome>. Write one per affected role.
   - The current workaround, and what it costs the user.
   - Evidence so far, labelled as data, anecdote or assumption.
   - The riskiest assumptions: ones that, if wrong, mean we build the wrong thing.
2. **Choose a research depth** proportional to risk and cost:

   | Situation | Do |
   |---|---|
   | Low risk; copy or layout | Skip. Rely on heuristics in phase 6. |
   | Known problem, unclear solution | Test the flow or a prototype with about 5 users per role (phase 7) |
   | Unclear problem or a new audience | Interview 5–8 people per role before designing |
   | Need to size or prioritise across many users | Run a short survey (5–10 questions) after the interviews, never instead of them |
   | Existing product with data | Mine analytics, support tickets and logs first. They're free and real. |

3. **Interview guide.** Use `templates/interview-guide.md`. Rules:
   - Ask about past behaviour ("Tell me about the last time you…"), not hypotheticals ("Would you use…").
   - Don't pitch or show the solution.
   - Use open questions, follow up with "why?", and stay quiet long enough for people to keep talking.
   - Include accessibility and low-connectivity users if they're part of the audience.
   - Get consent, minimise personal data, and anonymise notes.
4. **Synthesis.** After the sessions, turn the notes into atomic observations, cluster them (affinity mapping), and write insights in this form: \<user> \<does or needs> \<because>, which means \<implication>. Record them in `docs/ux/research/<topic>.md`. Separate what people said from what they did.
5. **Personas (optional).** Write them only if they'll actually guide decisions. Base them on research, not demographics: goals, context, constraints, frustrations and skills. Mark any that aren't research-backed as *proto-personas*.

## Exit check

- Job stories for each affected role.
- The riskiest assumptions are listed, each with a plan to check it, or an explicit decision to accept the risk.
- Research findings, if any, are linked from the brief.
