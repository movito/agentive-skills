# Changelog — agentive-workflow

All notable changes to the `agentive-workflow` plugin. Format follows
[Keep a Changelog](https://keepachangelog.com/); versions are semver.
The upgrader agent fetches this file to compute the reconcile diff for
consuming projects — keep Added/Removed/Renamed explicit per release.

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
