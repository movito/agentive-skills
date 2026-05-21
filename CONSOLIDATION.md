# Rollout runbook — agentive-skills private marketplace

Generated 2026-05-21. Canonical source: `movito/ixda-services-2.0`. Token used for the audit is
read-only, so the steps below that create/modify repos need a token (or `gh auth login`) with
**Contents: write** and, for the PR approach, **Pull requests: write**.

## Phase 1 — Publish the marketplace repo (once)

The scaffolded repo is in `agentive-skills/`. Create the private GitHub repo and push it:

```sh
cd agentive-skills
git init -b main
git add .
git commit -m "agentive-workflow plugin v1.0.0 (consolidated from ixda-services-2.0)"

# create the PRIVATE repo and push (gh CLI):
gh repo create movito/agentive-skills --private --source=. --remote=origin --push
# …or with an empty repo already created on github.com:
# git remote add origin https://github.com/movito/agentive-skills.git
# git push -u origin main
```

Verify it resolves as a marketplace:

```sh
/plugin marketplace add movito/agentive-skills
/plugin install agentive-workflow@agentive-skills
```

## Phase 2 — Adopt in each downstream repo

For every repo below: enable the plugin via `.claude/settings.json`, then delete the vendored
skill copies so there is exactly one source of truth.

Add to the repo's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "agentive-skills": { "source": { "source": "github", "repo": "movito/agentive-skills" } }
  },
  "enabledPlugins": ["agentive-workflow@agentive-skills"]
}
```

Then remove the copied skill folders (paths below are per repo). Recommended as a branch + PR
per repo so each change is reviewable.

> Note: `dispatch-kit` is the historical origin and holds **two** internal copies
> (`.claude/skills` and `.agent-context/starter-kit-export/skills`). Decide whether it should
> consume the marketplace like everyone else, or remain the upstream authoring repo. If it stays
> upstream, fold its authoring into `agentive-skills` instead and retire `dispatch-kit`'s exports.

### Vendored copies to delete (by repo)

### adversarial-workflow
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/code-review-evaluator/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.claude/skills/review-handoff/SKILL.md`
- `.claude/skills/self-review/SKILL.md`

### agentive-starter-kit
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.kit/skills/code-review-evaluator/SKILL.md`
- `.kit/skills/review-handoff/SKILL.md`
- `.kit/skills/self-review/SKILL.md`

### design-theory-timeline
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.kit/skills/code-review-evaluator/SKILL.md`
- `.kit/skills/review-handoff/SKILL.md`
- `.kit/skills/self-review/SKILL.md`

### dispatch-kit
- `.agent-context/starter-kit-export/skills/bot-triage/SKILL.md`
- `.agent-context/starter-kit-export/skills/code-review-evaluator/SKILL.md`
- `.agent-context/starter-kit-export/skills/pre-implementation/SKILL.md`
- `.agent-context/starter-kit-export/skills/review-handoff/SKILL.md`
- `.agent-context/starter-kit-export/skills/self-review/SKILL.md`
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/code-review-evaluator/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.claude/skills/review-handoff/SKILL.md`
- `.claude/skills/self-review/SKILL.md`

### epistemic-drift
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/code-review-evaluator/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.claude/skills/review-handoff/SKILL.md`
- `.claude/skills/self-review/SKILL.md`

### ixda-services-2.0
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.kit/skills/code-review-evaluator/SKILL.md`
- `.kit/skills/review-handoff/SKILL.md`
- `.kit/skills/self-review/SKILL.md`

### moss-skolemusikkorps
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/code-review-evaluator/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.claude/skills/review-handoff/SKILL.md`
- `.claude/skills/self-review/SKILL.md`

### research-method-matrix
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/code-review-evaluator/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.claude/skills/review-handoff/SKILL.md`
- `.claude/skills/self-review/SKILL.md`

### suwinex-planning
- `.claude/skills/bot-triage/SKILL.md`
- `.claude/skills/pre-implementation/SKILL.md`
- `.kit/skills/code-review-evaluator/SKILL.md`
- `.kit/skills/review-handoff/SKILL.md`
- `.kit/skills/self-review/SKILL.md`

## Phase 3 — Going forward

- Make all skill edits in `agentive-skills`, bump semver, push.
- Downstream: `/plugin marketplace update agentive-skills`.
- No more copying. The audit spreadsheet can be re-run any time to confirm zero drift remains.
