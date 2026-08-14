#!/usr/bin/env python3
"""Verify the published plugin bodies against roster.yaml (KIT-0110).

The blind half of the release guard, closed. The KIT repo's drift guard
(``check_plugin_drift.py`` in movito/agentive-starter-kit) verifies
KIT ↔ ROSTER only — it proves "the roster remembers the kit's current
bytes", never "the published plugin reflects them". A release that bumps
the roster hashes but forgets to copy the merged bodies goes green there
with stale content shipping (KIT-0109 retro — verified by reading the
function, then falsified).

THIS check runs marketplace-side, same repo, no network:

1. **Schema validation first** — a malformed roster is its own loud
   failure (exit 4), never a vacuous pass (KIT-0110 evaluator F3).
2. For every ``ships: true`` component, the published body at its
   derived path (``agents/<name>.md``, ``commands/<name>.md``,
   ``skills/<name>/SKILL.md``) must exist and hash to the rostered
   ``plugin_sha256``.
3. Every published body file must be rostered — an unrostered body is a
   ship nobody decided.

The bodies intentionally differ from kit canon (generalization per
KIT-ADR-0025); that is why the comparison lives here, against
``plugin_sha256``, and not kit-side against ``kit_sha256``. The column
is maintained by the kit's ``scripts/local/plugin_resync.py``.

Exit codes: ``0`` verified, ``1`` mismatch/missing/unrostered body,
``2`` usage/environment error, ``4`` roster read/parse/schema error.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins" / "agentive-workflow"
ROSTER = PLUGIN_DIR / "roster.yaml"

KINDS = ("agent", "command", "skill")
_SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")

BODY_GLOBS = (
    "agents/*.md",
    "commands/*.md",
    "skills/*/SKILL.md",
)

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_USAGE = 2
EXIT_ROSTER_IO = 4


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def body_relpath(comp: dict) -> str:
    kind = comp["kind"]
    name = comp["name"]
    if kind == "agent":
        return f"agents/{name}.md"
    if kind == "command":
        return f"commands/{name}.md"
    return f"skills/{name}/SKILL.md"


def load_components(roster_path: Path) -> list[dict]:
    """Parse and schema-validate the roster; loud failure on any defect."""
    try:
        import yaml
    except ImportError:
        print("ERROR: PyYAML is required (pip install pyyaml).")
        raise SystemExit(EXIT_USAGE) from None
    try:
        text = roster_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: cannot read roster {roster_path}: {exc}")
        raise SystemExit(EXIT_ROSTER_IO) from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        print(f"ERROR: roster is not valid YAML: {exc}")
        raise SystemExit(EXIT_ROSTER_IO) from exc
    if not isinstance(data, dict) or not isinstance(data.get("components"), list):
        print("ERROR: roster has no 'components' list.")
        raise SystemExit(EXIT_ROSTER_IO)

    problems: list[str] = []
    seen_names: set[str] = set()
    for i, comp in enumerate(data["components"]):
        if not isinstance(comp, dict):
            problems.append(f"components[{i}]: record is not a mapping")
            continue
        name = comp.get("name")
        label = name if isinstance(name, str) and name else f"components[{i}]"
        if not isinstance(name, str) or not name:
            problems.append(f"{label}: missing or non-string name")
        elif name in seen_names:
            problems.append(f"{label}: duplicate roster entry")
        else:
            seen_names.add(name)
        if not isinstance(comp.get("ships", False), bool):
            problems.append(f"{label}: non-boolean ships")
            continue
        if not comp.get("ships", False):
            continue
        # shipped entries: everything the comparison needs must be present
        # and safe BEFORE any path is derived from it
        if isinstance(name, str) and not _SAFE_NAME.match(name):
            problems.append(f"{label}: unsafe component name for path use")
        # `in` on the KINDS tuple: membership check against the known
        # component kinds, not substring matching.
        if comp.get("kind") not in KINDS:
            problems.append(f"{label}: unknown kind {comp.get('kind')!r}")
        sha = comp.get("plugin_sha256")
        if not isinstance(sha, str) or not _SHA256.match(sha):
            problems.append(
                f"{label}: ships=true but plugin_sha256 is missing or not a "
                "sha256 hex digest — run the kit's plugin_resync.py"
            )
    if problems:
        print("ERROR: roster is malformed — fix it before trusting any check:")
        for p in problems:
            print(f"  - {p}")
        raise SystemExit(EXIT_ROSTER_IO)
    return data["components"]


def check_bodies(components: list[dict]) -> list[str]:
    """Return findings (empty = every published body matches the roster)."""
    findings: list[str] = []
    rostered_bodies: set[str] = set()

    for comp in components:
        if not comp.get("ships", False):
            continue
        name = comp["name"]
        rel = body_relpath(comp)
        rostered_bodies.add(rel)
        body = PLUGIN_DIR / rel
        if not body.is_file():
            findings.append(
                f"{name}: rostered as shipped but no body at {rel} — "
                "the release copied nothing for this component"
            )
            continue
        actual = sha256_of(body)
        if actual != comp["plugin_sha256"]:
            findings.append(
                f"{name}: published body does not match the roster "
                f"({rel}: {actual[:12]}… != rostered "
                f"{comp['plugin_sha256'][:12]}…) — bump-without-copy, or an "
                "edit outside a release; re-run the kit's plugin_resync.py"
            )

    for pattern in BODY_GLOBS:
        for path in sorted(PLUGIN_DIR.glob(pattern)):
            rel = path.relative_to(PLUGIN_DIR).as_posix()
            # `in` on a set: membership check that this published body has
            # a roster entry, not substring matching.
            if rel not in rostered_bodies:
                findings.append(
                    f"unrostered body: {rel} ships with no roster entry — "
                    "a ship nobody decided; roster it or remove it"
                )

    return findings


def main() -> int:
    if not ROSTER.is_file():
        print(f"ERROR: no roster at {ROSTER} — wrong checkout layout?")
        return EXIT_USAGE

    components = load_components(ROSTER)
    findings = check_bodies(components)

    if findings:
        print(
            f"PLUGIN INTEGRITY: {len(findings)} finding(s) — the published "
            "bodies do not match the roster."
        )
        for f in findings:
            print(f"  - {f}")
        return EXIT_FINDINGS

    shipped = sum(1 for c in components if c.get("ships", False))
    print(f"verified: {shipped} published bodies match roster.yaml.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
