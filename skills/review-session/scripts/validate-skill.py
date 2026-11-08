#!/usr/bin/env python3
"""
Skill Quality Validator — enforces standards before shipping.

Usage:
    validate-skill.py <skill-dir>           # validate one skill
    validate-skill.py --all <skills-root>   # validate all active skills

Exit codes: 0 = pass, 1 = failures found

Run this:
- In review-session Step 4 (before shipping)
- In skill-creator Step 5 (after creating required files)
- In setup-skills.sh (on install)
"""

import json
import sys
from pathlib import Path


class SkillValidator:
    def __init__(self, skill_dir: Path):
        self.dir = skill_dir
        # Strip bundled__ prefix for name matching (bundled skills
        # use bundled__name as dir but just name in frontmatter).
        raw_name = skill_dir.name
        self.name = (
            raw_name.removeprefix("bundled__") if raw_name.startswith("bundled__") else raw_name
        )
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(f"❌ {self.name}: {msg}")

    def warn(self, msg):
        self.warnings.append(f"⚠️  {self.name}: {msg}")

    def validate(self):
        self._check_required_files()
        self._check_frontmatter()
        self._check_evals_quality()
        self._check_triggers_quality()
        self._check_skill_md_quality()
        return len(self.errors) == 0

    def _check_required_files(self):
        required = ["SKILL.md", "evals/evals.json", "evals/triggers.json"]
        for f in required:
            if not (self.dir / f).exists():
                self.error(f"missing required file: {f}")

    def _check_frontmatter(self):
        skill_md = self.dir / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()
        if not content.startswith("---"):
            self.error("SKILL.md missing YAML frontmatter (must start with ---)")
            return

        try:
            end = content.index("---", 3)
            frontmatter = content[3:end].strip()
        except ValueError:
            self.error("SKILL.md frontmatter not closed (missing second ---)")
            return

        lines = {
            l.split(":")[0].strip(): l.split(":", 1)[1].strip()
            for l in frontmatter.split("\n")
            if ":" in l
        }

        # Required fields
        if "name" not in lines:
            self.error("frontmatter missing 'name' field")
        elif lines["name"] != self.name:
            self.error(f"name mismatch: frontmatter='{lines['name']}' dir='{self.name}'")

        if "description" not in lines:
            self.error("frontmatter missing 'description' field")
        else:
            desc = lines["description"]
            if not desc.startswith('"') or not desc.endswith('"'):
                self.error('description must be quoted: description: "..."')
            if desc.count('"') > 2:
                self.error("description has unescaped inner quotes — use single quotes inside")
            if "TODO" in desc:
                self.error("description still has TODO placeholder")

        if "type" not in lines:
            self.error("frontmatter missing 'type' field")
        elif lines["type"] not in ("knowledge", "workflow", "orchestrator", "tool"):
            self.error(
                f"invalid type: '{lines['type']}' (must be knowledge|workflow|orchestrator|tool)"
            )

        if "lifecycle" not in lines:
            self.error("frontmatter missing 'lifecycle' field")

    def _check_evals_quality(self):
        evals_path = self.dir / "evals" / "evals.json"
        if not evals_path.exists():
            return

        try:
            data = json.loads(evals_path.read_text())
        except json.JSONDecodeError as e:
            self.error(f"evals.json is invalid JSON: {e}")
            return

        # Check format
        if "skill" not in data:
            self.error("evals.json missing 'skill' field (old format uses 'skill_name')")
        elif data["skill"] != self.name:
            self.warn(f"evals.json skill='{data['skill']}' doesn't match dir='{self.name}'")

        if "test_cases" not in data:
            self.error("evals.json missing 'test_cases' field (old format uses 'evals')")
            return

        cases = data["test_cases"]

        # Minimum 3 test cases
        if len(cases) < 3:
            self.error(f"evals.json has {len(cases)} test cases (minimum 3)")

        for i, tc in enumerate(cases):
            if "name" not in tc:
                self.error(f"evals.json test_cases[{i}] missing 'name'")
            if "input" not in tc:
                self.error(f"evals.json test_cases[{i}] missing 'input'")
            elif "TODO" in tc["input"]:
                self.error(f"evals.json test_cases[{i}] input is still TODO")
            if "assertions" not in tc:
                self.error(f"evals.json test_cases[{i}] missing 'assertions'")
            elif isinstance(tc.get("assertions"), list):
                for a in tc["assertions"]:
                    if "TODO" in a:
                        self.error(f"evals.json test_cases[{i}] assertion is still TODO")
                    if a.lower() in ("works correctly", "correct output", "expected behavior"):
                        self.warn(f"evals.json test_cases[{i}] assertion too vague: '{a}'")

    def _check_triggers_quality(self):
        trig_path = self.dir / "evals" / "triggers.json"
        if not trig_path.exists():
            return

        try:
            data = json.loads(trig_path.read_text())
        except json.JSONDecodeError as e:
            self.error(f"triggers.json is invalid JSON: {e}")
            return

        # Handle both old (array) and new (object) formats
        if isinstance(data, list):
            self.warn("triggers.json uses old array format — should be {skill, test_cases}")
            cases = data
        elif isinstance(data, dict):
            cases = data.get("test_cases", [])
        else:
            self.error("triggers.json has unexpected format")
            return

        if len(cases) < 3:
            self.error(f"triggers.json has {len(cases)} cases (minimum 3 positive + 1 negative)")

        positives = sum(1 for c in cases if c.get("should_trigger", True))
        negatives = sum(1 for c in cases if not c.get("should_trigger", True))

        if positives < 2:
            self.error(f"triggers.json has only {positives} positive triggers (need ≥2)")
        if negatives < 1:
            self.warn("triggers.json has no negative triggers (should_trigger: false)")

        for c in cases:
            inp = c.get("input", c.get("query", ""))
            if "TODO" in inp:
                self.error(f"triggers.json has TODO placeholder: '{inp}'")

    def _check_skill_md_quality(self):
        skill_md = self.dir / "SKILL.md"
        if not skill_md.exists():
            return

        content = skill_md.read_text()
        content.split("\n")

        # Check for closing frontmatter
        try:
            end_idx = content.index("---", 3)
            body = content[end_idx + 3 :].strip()
        except ValueError:
            return

        body_lines = body.split("\n")

        if len(body_lines) < 5:
            self.warn(f"SKILL.md body is very short ({len(body_lines)} lines)")

        if len(body_lines) > 500:
            self.warn(
                f"SKILL.md body is {len(body_lines)} lines (target: <500, split into references/)"
            )

        # Check for nested skill dir (common bug)
        nested = self.dir / self.name
        if nested.is_dir():
            self.error(f"nested directory found: {self.name}/{self.name}/ — remove the duplicate")


def validate_one(skill_dir: Path) -> bool:
    v = SkillValidator(skill_dir)
    passed = v.validate()

    for e in v.errors:
        print(e)
    for w in v.warnings:
        print(w)

    if passed and not v.warnings:
        print(f"✅ {v.name}: PASS")
    elif passed:
        print(f"✅ {v.name}: PASS ({len(v.warnings)} warnings)")
    else:
        print(f"❌ {v.name}: FAIL ({len(v.errors)} errors, {len(v.warnings)} warnings)")

    return passed


def validate_all(skills_root: Path) -> bool:
    total = 0
    passed = 0
    failed = 0
    errors_total = 0
    warnings_total = 0

    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith("_") or skill_dir.name.startswith("."):
            continue
        if not (skill_dir / "SKILL.md").exists():
            continue

        total += 1
        v = SkillValidator(skill_dir)
        if v.validate():
            passed += 1
        else:
            failed += 1

        errors_total += len(v.errors)
        warnings_total += len(v.warnings)

        for e in v.errors:
            print(e)
        for w in v.warnings:
            print(w)

    print(f"\n{'═' * 50}")
    print(f"Total: {total} skills | ✅ {passed} pass | ❌ {failed} fail")
    print(f"Errors: {errors_total} | Warnings: {warnings_total}")

    return failed == 0


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  validate-skill.py <skill-dir>           # validate one skill")
        print("  validate-skill.py --all <skills-root>   # validate all active skills")
        sys.exit(1)

    if args[0] == "--all":
        root = Path(args[1]) if len(args) > 1 else Path(".")
        ok = validate_all(root)
    else:
        skill_dir = Path(args[0])
        if not skill_dir.exists():
            print(f"❌ Directory not found: {skill_dir}")
            sys.exit(1)
        ok = validate_one(skill_dir)

    sys.exit(0 if ok else 1)
