# Phase 3: Flows and information architecture

Goal: specify, step by step, how a user completes one task, including everything that can go wrong, before drawing screens.

**Specialists:**
- specialist `journey` for task flows and decision points
- specialist `fortify` for unhappy paths and state inventories
- specialist `organize` for information architecture

## A. Flow spec (one per task)

Create it with `uxl new flow-spec --name <feature>`.

1. **Entry points:** every way a user can arrive, such as the nav, a dashboard card, an email link, search or a deep link. Each must land in the right context, with login and return-to working.
2. **Happy path:** numbered steps showing screen → user action → system response.
3. **Unhappy paths:** at each step, ask:
   - What if the input is invalid?
   - What if the server fails or is slow?
   - What if the user lacks permission, or their session expires?
   - What if there's a duplicate, a conflict, or someone else changed it meanwhile?
   - What if the user abandons midway? Is the draft saved, and can they resume?
   - What if they go back, refresh or double-submit?
4. **State inventory** for each screen: empty (first use), loading, partial, full, error, success, disabled and read-only, plus each relevant permission or role.
5. **Exit:** what the user sees on completion, what happens next, who is notified, and where the user goes from there.
6. **Effort check:** count the steps and fields. Remove anything the system already knows, defer what isn't needed now, and set smart defaults.

## B. Information architecture (for navigation or multi-page work)

- **Inventory** the existing pages and group them by user task, not by database table or org chart.
- **Navigation per role:** show only what that role uses; put the top 3–5 tasks one click from home.
- **Labels:** use the user's words. Check them against research, support tickets or the user's own vocabulary. Keep them consistent with the copy in `phases/6-quality-gates.md`.
- **Wayfinding:** page titles match the nav labels, breadcrumbs appear in deep hierarchies, the current location is shown, and search exists where lists grow large.
- **Validate** when the IA changes significantly: run a quick tree test or card sort with 5+ users, or at least walk through each role's top tasks.

## Exit check

- The flow spec covers entry points, the happy path, unhappy paths and the state inventory.
- The user has approved the flow before screens are built for new or changed behaviour.
