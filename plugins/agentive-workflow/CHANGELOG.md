# Changelog — agentive-workflow

All notable changes to the `agentive-workflow` plugin. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions are semver.
The upgrader agent fetches this file to compute the reconcile diff for
consuming projects — keep Added/Removed/Renamed explicit per release.

## [2.0.2] — 2026-08-11

Patch sync. Six components refreshed from the upstream kit
(agentive-starter-kit, KIT-0100), carrying the advisory defects that the
2.0.1 release review surfaced — fixed in kit canon first, then released,
per KIT-ADR-0028.

### Added

- Nothing. No new components in this release.

### Removed

- Nothing. No components retired in this release.

### Renamed

- Nothing. No component renames in this release; no reference reconcile
  is required in consuming projects.

### Fixed

- **Unenforceable CI watch timeout (`ci-checker`)** — the agent
  documented a 10-minute watch limit while calling `gh run watch`, which
  has no duration flag at all (only `--interval`), so nothing bounded the
  call and a hung run could block indefinitely. Watch commands are now
  wrapped in a resolved supervisor, with three exit codes kept distinct:
  **124** timeout, **127** supervisor not installed (nothing was
  watched — never report it as a CI result), anything else a genuine
  failure. Resolve `timeout` vs `gtimeout` once (macOS ships the latter)
  and substitute it everywhere, alongside the existing repo-routing
  placeholder. Where no supervisor exists at all, the fallback is a
  **bounded poll loop** on the same 10-minute budget — a single
  `gh run view` is a snapshot, not a wait, and stopping after one would
  report a still-running workflow as the final verdict.
- **CI retrigger could ship unrelated staged work (`check-ci`)** —
  `git commit --allow-empty` *permits* an empty commit; it does not
  *make* one, so a retrigger run against a dirty index silently
  committed whatever happened to be staged under the message "chore:
  retrigger CI". Now uses `--allow-empty --only`, which commits exactly
  the named paths and therefore, with none named, nothing at all: the
  retrigger commit is structurally incapable of carrying staged work.
  Split-mode paths are quoted so a path containing spaces cannot split
  into multiple arguments.
- **Evaluator fallback could escalate past its tier
  (`code-review-evaluator`)** — "if the required API key is missing,
  fall back to another evaluator" allowed a prose-shaped review to reach
  the expensive deep tier through the degraded path, by accident rather
  than by decision. Fallback is now sideways-within-tier only; upward is
  a blocked gate.
- **Evaluator trio read as unconditional (`feature-developer`,
  `feature-developer-f5`)** — the three commands were listed with no
  visible branch, several paragraphs below the rule that selects among
  them, so the tier rule was easy to miss. The block now branches
  explicitly, and a mixed diff (any hunk changing behavior) resolves to
  logic-shaped.
- **Stale phase cross-references (`feature-developer`,
  `feature-developer-f5`)** — two "see Phase 6" references still pointed
  at the pre-2.0.1 numbering, where CI polling is now Phase 7.
- **`wrap-up` printed an unverified path** — the summary always printed
  a task-specific review-starter path, while the check behind it was a
  repo-wide glob that could match a *different* task's file. The check is
  now task-specific and the line reports `NOT FOUND` when absent, the
  same treatment the command already applied to its retro line.

## [2.0.1] — 2026-08-10

Patch sync. Content-only refresh of 17 components from the upstream kit
(agentive-starter-kit, KIT-0099), carrying the fixes that the 2.0.0
review itself produced: the 21 findings from movito/agentive-skills#4
were fixed in the kit's canonical tree (KIT-0097), then given a
fresh-eyes coherence repair (KIT-0098), per the fix-here-then-release
contract in KIT-ADR-0028.

No roster membership changes, no renames, no removals — every component
that shipped in 2.0.0 ships in 2.0.1. Consuming projects need no
reference reconcile; `claude plugin update` is sufficient.

### Added

- Nothing. No new components in this release.

### Removed

- Nothing. No components retired in this release.

### Renamed

- Nothing. No component renames in this release; no reference reconcile
  is required in consuming projects.

### Fixed

- **Evaluator ordering contradiction (`feature-developer`,
  `feature-developer-f5`)** — the Workflow Overview table and task-flow
  line placed the Evaluator gate *after* CI+Bots, contradicting the
  pre-PR-open trio rule the same body mandates. Phases renumbered
  (Evaluator 5, Ship 6, CI+Bots 7) and the section physically moved.
- **Instructions that contradicted an agent's own tool grant
  (`document-reviewer`, `security-reviewer`)** — both declare
  themselves read-only and are granted no Bash or Write, while the body
  mandated push-and-verify-CI. The CI block is now "not yours to run",
  with the delegation route named.
- **Stale and unsafe command recipes (`feature-developer` pair)** — the
  evaluator step probed for helper scripts removed in KIT-0091 and used
  a raw `git diff`; it now uses the canonical `agentive review-input`,
  requires a committed tree first (uncommitted work is invisible to the
  diff), and picks `--format` by change shape.
- **Split-mode path correctness (`feature-developer` pair,
  `ci-checker`)** — planning-repo commands used relative paths that
  resolve against the *target* worktree in a cross-repo session;
  the planning root is now derived once and routed through explicitly.
  `ci-checker` detects topology before the origin/default-repo check,
  which is legitimately skipped in split mode.
- **Upgrade/rollback correctness (`upgrader`)** — version resolution no
  longer fetches `ref=main` for a target version's CHANGELOG or
  blind-prefixes `v` on 404; and rollback no longer assumes
  `claude plugin update` can move backwards (it resolves
  marketplace-latest), restoring from cache and verifying via
  `claude plugin list` instead.
- **Hardcodes that leak one project into every project
  (`code-reviewer`, `test-runner`, `document-reviewer`,
  `security-reviewer`)** — `/check-ci main` verified the base branch
  rather than the change; Serena activation and example task IDs named
  a specific downstream project. Now de-hardcoded upstream, so the kit
  and the distributed copies finally agree.
- **Lifecycle discipline (`code-reviewer` and peers)** — `project
  start` was an unconditional first action; it is now conditional on
  task status and session topology, mirroring the feature-developer
  verify-never-create contract.

### Changed

- **Handoff conventions (`planner`, `planner-f5`)** — bot presence or
  absence on a repo is an environmental claim: cite the query or write
  UNVERIFIED. (The 2.0.0 handoff asserted "no bots" on the marketplace
  repo unverified; 23 review threads arrived on a PR planned around
  having none.)
- **`roster.yaml`** — `plugin_version` 2.0.1 and refreshed
  `kit_version`/`kit_sha256` for the 17 resynced components. Membership
  is byte-identical to 2.0.0. This turns the kit's CI drift guard green.

## [2.0.0] — 2026-08-09

Content refresh from the upstream kit's canonical `.claude/` tree
(agentive-starter-kit, KIT-0096). The 1.x plugin had drifted two agent
generations behind the kit (last content push 2026-06-18); this release
makes the plugin the current agent channel per KIT-ADR-0028 and adds a
machine-readable roster (`roster.yaml`) so the kit's CI can detect the
next drift automatically.

### Removed (BREAKING)

- **`feature-developer-v6`** — superseded. Migration: local references
  `agentive-workflow:feature-developer-v6` →
  `agentive-workflow:feature-developer` (Opus-class canonical).
- **`feature-developer-v7`** — superseded. Migration: local references
  `agentive-workflow:feature-developer-v7` →
  `agentive-workflow:feature-developer-f5` (Fable-class variant).

The upgrader agent's PREVIEW → ACK flow (docs/PLUGIN-UPGRADE-GUIDE.md
in consuming projects) handles the reference reconcile for both renames.

- **`wrap-up` no longer emits `phase_complete`**: its dispatch-kit
  event step was removed upstream (KIT-0077 retired the dispatch
  integration). Projects with automation listening for `phase_complete`
  must adapt. (Other commands' optional `dispatch emit` steps remain,
  marked fire-and-forget.)

### Added

- **Agents**: `feature-developer` (2.1.1), `feature-developer-f5`
  (1.1.0), `planner` (2.0.0), `planner-f5` (1.0.0) — the plugin
  previously shipped NO planner — plus `test-runner` (1.0.0),
  `document-reviewer` (1.0.0), `security-reviewer` (1.0.0), and
  `upgrader` (1.1.0).
- **`roster.yaml`** — the deliberate ships/kit-side decision per kit
  component, with the kit-source version + sha256 each shipped copy was
  derived from. Input for the kit repo's CI drift guard.
- **This CHANGELOG**, at the path the upgrader agent fetches
  (`plugins/agentive-workflow/CHANGELOG.md`).

### Changed

- **All 12 commands and 5 skills refreshed** to the kit's current
  canonical bodies (June → August generation): the verify-never-create
  Phase 1 contract, Session-topology handoffs, the oscillation
  protocol, format-by-change-shape evaluator guidance, review-body
  triage, `agentive` CLI adoption where the kit has migrated.
- **`ci-checker`** and **`code-reviewer`** refreshed to current kit
  bodies (with the 1.x distribution genericizations re-applied).
- **Generalization per KIT-ADR-0025**: distributed bodies no longer
  carry KIT-LOCAL extension-point regions or unfilled templates —
  each agent reads project specifics at runtime from the consuming
  repo's own files (`CLAUDE.md`, task spec, `.kit/context/`).

## [1.1.0] — 2026-06-18

Cross-repo-aware command generation; `feature-developer-v6`/`-v7`,
`code-reviewer`, `ci-checker`; 5 skills. (Pre-roster era.)

## [1.0.0] — 2026-06-13

Initial plugin release (KIT-0030): skills consolidated from
`movito/ixda-services-2.0`, commands and agents from the
agentive-starter-kit canonical generation.
