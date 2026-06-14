# agentive-skills

Private Claude Code plugin marketplace for movito repos. **Single source of truth** for the
agentive review/implementation workflow — skills, commands, and agents — previously copy-pasted
across many repos.

This repo is private. It is not published anywhere public and carries no support obligation to
anyone else — it exists so the workflow is maintained in one place and *pulled* into projects
rather than forked into them.

## What's inside

One plugin, `agentive-workflow`. Every component is namespaced `agentive-workflow:<name>` when
the plugin is enabled (e.g. `/agentive-workflow:preflight`,
`Agent(subagent_type="agentive-workflow:feature-developer-v7")`).

### Skills

| Skill | Version | Purpose |
|---|---|---|
| `bot-triage` | 1.1.0 | Triage/reply/resolve BugBot & CodeRabbit comments |
| `code-review-evaluator` | 1.2.0 | Adversarial code-review evaluator after bot rounds |
| `pre-implementation` | 1.2.0 | Pre-code checks: pattern reuse, API misuse, spec drift |
| `review-handoff` | 1.0.0 | Hand off a PR for human review after bots pass |
| `self-review` | 1.0.0 | Input-boundary self-review pass before committing |

### Commands

`check-ci`, `check-bots`, `wait-for-bots`, `babysit-pr`, `triage-threads`, `preflight`,
`retro`, `wrap-up`, `start-task`, `status`, `commit-push-pr`, `check-spec`. These are the
cross-repo-aware generation: each auto-detects a `## Target Repository` section in the
consuming project's `CLAUDE.md` and routes `git`/`gh` to the target repo, falling back to
single-repo mode when no such section exists.

### Agents

| Agent | Model | Notes |
|---|---|---|
| `feature-developer-v7` | claude-fable-5 | Gated implementation workflow, inline CI/bot polling |
| `feature-developer-v6` | claude-opus-4-8 | Opus-class copy of v7 (content-identical) |
| `code-reviewer` | — | Post-implementation quality review |
| `ci-checker` | — | Interactive CI status verification |

> The two `feature-developer` agents ship as **unfilled templates**: their
> `## Project Context` and `### Stack Notes` carry `ACME-NNNN` / EXTENSION POINT
> placeholders. Each consuming project fills them in locally (or via its bootstrap),
> because the right tech stack, task prefix, and layout differ per project.

### Depends on: helper scripts via the manifest channel (not the plugin)

Several components delegate to helper scripts that live in a project's `scripts/core/`:

- the cross-repo **commands** call `verify-ci.sh` (`check-ci`), `check-bots.sh`
  (`check-bots`), `preflight-check.sh` (`preflight`), and `gh-review-helper.sh`
  (`triage-threads`);
- the **`code-review-evaluator` skill** calls `prepare-review-input.sh`;
- those `.sh` scripts in turn source `lib/target_repo.sh` for cross-repo detection.

None of these scripts are shipped by this plugin; they are distributed through the
agentive-starter-kit manifest sync (`scripts/.core-manifest.json`, `core_version` ≥ 2.1.0).
A project consuming this plugin's commands/skills needs that script generation present.
The two channels are deliberate:

- **plugin** (this repo) → skills, commands, agents, to planning/consumer projects
- **manifest** (agentive-starter-kit) → scripts + kit-internal artifact copies, kit-to-kit

See agentive-starter-kit KIT-ADR-0024 §3 for the channel split.

## Use it in a project

```sh
# add this private marketplace (uses your GitHub credentials)
/plugin marketplace add movito/agentive-skills
# install the plugin
/plugin install agentive-workflow@agentive-skills
```

## Pin and upgrade

The plugin carries an explicit semver `version` in `.claude-plugin/plugin.json`, so it acts as
a **pin**: a consuming project receives changes only when that version is bumped, not on every
commit to this repo. To make the pin explicit per project, record it in the project's
`CLAUDE.md` `## Provenance` section, e.g. `agentive-workflow@1.1.0`.

Upgrading a project is a deliberate action:

```sh
/plugin marketplace update agentive-skills   # refresh marketplace metadata
/plugin update agentive-workflow@agentive-skills
```

After upgrading, update the project's `## Provenance` pin and run one real task end-to-end
before relying on the new version. Because the version is the cache key, **re-publishing the
same version number does not propagate** — always bump `version` for changes to reach
consumers.

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

- Edit a component under `plugins/agentive-workflow/{skills,commands,agents}/`.
- Plugin-internal cross-references use the namespaced form (`/agentive-workflow:preflight`),
  because consuming projects delete their flat local copies on migration. When syncing a
  command/skill/agent from the kit's canonical copy, apply the namespacing transform
  (`/preflight` → `/agentive-workflow:preflight`, etc.) — but never namespace script paths
  (`scripts/core/check-bots.sh`) or `adversarial` evaluator names (`code-reviewer-fast`).
- Bump the component's `version:` frontmatter and the plugin `version` in
  `.claude-plugin/plugin.json` + `marketplace.json` (semver).
- Commit and push. Downstream projects pick it up on a deliberate `/plugin update`.

## Provenance

Skills consolidated 2026-05-21 from `movito/ixda-services-2.0`. Commands and agents added
2026-06-13 (KIT-0030) from the agentive-starter-kit canonical generation. Historical origin:
`dispatch-kit` 0.3.2. See `CONSOLIDATION.md` for the original skill variant audit.
