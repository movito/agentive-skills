# agentive-skills

Private Claude Code plugin marketplace for movito repos. **Single source of truth** for the
agentive review/implementation workflow skills that were previously copy-pasted across many repos.

This repo is private. It is not published anywhere public and carries no support obligation to
anyone else — it exists so the skills are maintained in one place and *pulled* into projects
rather than forked into them.

## What's inside

One plugin, `agentive-workflow`, bundling five skills (consolidated from the newest copies,
originally from `dispatch-kit`):

| Skill | Version | Purpose |
|---|---|---|
| `bot-triage` | 1.1.0 | Triage/reply/resolve BugBot & CodeRabbit comments |
| `code-review-evaluator` | 1.2.0 | Adversarial code-review evaluator after bot rounds |
| `pre-implementation` | 1.2.0 | Pre-code checks: pattern reuse, API misuse, spec drift |
| `review-handoff` | 1.0.0 | Hand off a PR for human review after bots pass |
| `self-review` | 1.0.0 | Input-boundary self-review pass before committing |

## Use it in a project

```sh
# add this private marketplace (uses your GitHub credentials)
/plugin marketplace add movito/agentive-skills
# install the plugin
/plugin install agentive-workflow@agentive-skills
```

Updating later pulls the latest from this repo:

```sh
/plugin marketplace update agentive-skills
```

For auto-update of a private marketplace at startup, export a GitHub token in your shell
(e.g. in `~/.zshrc`).

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

- Edit a skill under `plugins/agentive-workflow/skills/<name>/SKILL.md`.
- Bump the skill's `version:` in its frontmatter and the plugin `version` in
  `.claude-plugin/plugin.json` + `marketplace.json` (semver).
- Commit and push. Downstream projects pick it up on `/plugin marketplace update`.

## Provenance

Consolidated 2026-05-21 from `movito/ixda-services-2.0` (the repo carrying the newest variant of
each skill). Historical origin: `dispatch-kit` 0.3.2. See `CONSOLIDATION.md` for the variant
audit this was built from.
