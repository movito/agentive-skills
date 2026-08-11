# agentive-skills

Claude Code plugin marketplace for movito repos. **Single source of truth** for the
agentive review/implementation workflow — skills, commands, and agents — previously copy-pasted
across many repos.

This repo is **public** (a Claude Code plugin marketplace needs a reachable GitHub
source) but carries no support obligation to anyone else — it exists so the workflow
is maintained in one place and *pulled* into projects rather than forked into them.
Anything committed here, including release metadata, is visible to anyone.

## What's inside

One plugin, `agentive-workflow` (2.0.1). Every component is namespaced
`agentive-workflow:<name>` when the plugin is enabled (e.g. `/agentive-workflow:preflight`,
`Agent(subagent_type="agentive-workflow:feature-developer")`).

The component roster — including WHY each kit component ships or stays kit-side — is
machine-readable in [`plugins/agentive-workflow/roster.yaml`](plugins/agentive-workflow/roster.yaml).
The upstream kit's CI reads that file to fail loudly when the kit's canonical `.claude/`
content is newer than the last published release here.

### Skills

| Skill | Version | Purpose |
|---|---|---|
| `bot-triage` | 1.1.0 | Triage/reply/resolve BugBot & CodeRabbit comments |
| `code-review-evaluator` | 1.3.0 | Adversarial code-review evaluator after bot rounds |
| `pre-implementation` | 1.2.0 | Pre-code checks: pattern reuse, API misuse, spec drift |
| `review-handoff` | 1.1.0 | Hand off a PR for human review after bots pass |
| `self-review` | 1.2.0 | Input-boundary self-review pass before committing |

### Commands

`check-ci`, `check-bots`, `wait-for-bots`, `babysit-pr`, `triage-threads`, `preflight`,
`retro`, `wrap-up`, `start-task`, `status`, `commit-push-pr`, `check-spec`. These are the
cross-repo-aware generation: each auto-detects a `## Target Repository` section in the
consuming project's `CLAUDE.md` and routes `git`/`gh` to the target repo, falling back to
single-repo mode when no such section exists.

### Agents

| Agent | Model | Notes |
|---|---|---|
| `feature-developer` | claude-opus-5 | Canonical gated implementation workflow, inline CI/bot polling |
| `feature-developer-f5` | claude-fable-5 | Fable-class variant of feature-developer (same body, different pin) |
| `planner` | claude-opus-4-8 | Planning/coordination: task lifecycle, evaluation, handoff |
| `planner-f5` | claude-fable-5 | Fable-class variant of planner |
| `code-reviewer` | claude-sonnet-5 | Post-implementation quality review |
| `ci-checker` | claude-sonnet-5 | Interactive CI status verification |
| `test-runner` | claude-sonnet-5 | TDD / QA verification |
| `document-reviewer` | claude-sonnet-5 | Documentation quality review |
| `security-reviewer` | claude-opus-4-8 | Security analysis and hardening |
| `upgrader` | claude-sonnet-5 | Moves a consuming project between plugin versions |

> **Localization is runtime-read (KIT-ADR-0025).** Distributed agent bodies are
> project-agnostic: no fill-in template regions ship. Each agent reads project
> specifics at session start from files the consuming repo owns — `CLAUDE.md`
> (auto-injected), the task spec/handoff, and `.kit/context/`. The 1.x
> "unfilled template" extension points are retired.

### Depends on: helper scripts and the `agentive` CLI (not shipped here)

Several components delegate to helpers that live with the consuming project:

- **`scripts/core/` scripts** (manifest generation): `verify-ci.sh` (`check-ci`,
  ci-checker), `check-bots.sh` / `wait-for-bots.sh` (bot commands), `ci-check.sh`
  (`babysit-pr`'s local-checks step), `project` (task lifecycle).
- **The `agentive` CLI** (the `agentive-kit` package, KIT-ADR-0028's scripts
  channel): `agentive preflight` (`preflight`), `agentive review-helper`
  (`triage-threads`, bot triage), `agentive review-input` (code-review-evaluator).

The kit is mid-migration from the manifest channel to the package (KIT-ADR-0028);
shipped bodies reference whichever surface the kit's canonical copy uses today. A
project consuming this plugin needs its script generation current and `agentive-kit`
installed (`uv tool install agentive-kit`).

## Use it in a project

```sh
# add this marketplace
/plugin marketplace add movito/agentive-skills
# install the plugin
/plugin install agentive-workflow@agentive-skills
```

## Pin and upgrade

The plugin carries an explicit semver `version` in `.claude-plugin/plugin.json`, so it acts as
a **pin**: a consuming project receives changes only when that version is bumped, not on every
commit to this repo. To make the pin explicit per project, record it in the project's
`CLAUDE.md` `## Provenance` section, e.g. `agentive-workflow@2.0.0`.

Upgrading a project is a deliberate action — use the plugin's own `upgrader` agent, which
automates the PREVIEW → ACK → APPLY flow, or manually:

```sh
/plugin marketplace update agentive-skills   # refresh marketplace metadata
/plugin update agentive-workflow@agentive-skills
```

After upgrading, update the project's `## Provenance` pin and run one real task end-to-end
before relying on the new version. Because the version is the cache key, **re-publishing the
same version number does not propagate** — always bump `version` for changes to reach
consumers.

**Upgrading from 1.x**: `feature-developer-v6`/`-v7` are retired in 2.0.0 — see
[`plugins/agentive-workflow/CHANGELOG.md`](plugins/agentive-workflow/CHANGELOG.md) for the
rename path. The upgrader agent's reconcile step rewrites the references.

## Auto-enable across your own machines

In a project's (or your global) `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "agentive-skills": { "source": { "source": "github", "repo": "movito/agentive-skills" } }
  },
  "enabledPlugins": ["agentive-workflow@agentive-skills"]
}
```

## Maintenance

- The kit's canonical `.claude/` tree is the upstream for every component here; a release
  is a refresh from that tree (generalized per KIT-ADR-0025), never a divergent edit.
  Editing a component only in this repo re-creates the drift this layout exists to prevent.
- Plugin-internal cross-references use the namespaced form (`/agentive-workflow:preflight`),
  because consuming projects delete their flat local copies on migration. When syncing a
  command/skill/agent from the kit's canonical copy, apply the namespacing transform
  (`/preflight` → `/agentive-workflow:preflight`, etc.) — but never namespace script paths
  (`scripts/core/check-bots.sh`), `agentive` CLI invocations, or `adversarial` evaluator
  names (`code-reviewer-fast`).
- On every release: update `roster.yaml` (per-component `kit_version` + `kit_sha256` from
  the kit tree the release was cut from), add a CHANGELOG entry with explicit
  Added/Removed/Renamed (the upgrader agent parses it), and bump `version` in
  `.claude-plugin/plugin.json` + `marketplace.json` (semver).
- Commit and push. Downstream projects pick it up on a deliberate `/plugin update`.

## Provenance

Skills consolidated 2026-05-21 from `movito/ixda-services-2.0`. Commands and agents added
2026-06-13 (KIT-0030) from the agentive-starter-kit canonical generation; refreshed to the
kit's August generation in 2.0.0 (KIT-0096). Historical origin: `dispatch-kit` 0.3.2. See
`CONSOLIDATION.md` for the original skill variant audit.
