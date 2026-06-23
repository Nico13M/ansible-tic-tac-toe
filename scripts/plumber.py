from __future__ import annotations

import sys
from pathlib import Path

import yaml


REQUIRED_STAGES = [
    "plumber",
    "precommit",
    "test",
    "sonar",
    "build",
    "scan",
    "deploy",
    "release",
    "docs",
]

REQUIRED_JOBS = [
    "plumber:conformity",
    "precommit:hooks",
    "unit:test",
    "sonar:analysis",
    "build:image",
    "scan:trivy",
    "deploy:staging",
    "deploy:production",
    "release:sentry:staging",
    "release:sentry:production",
    "mkdocs:build",
    "pages",
]


def main() -> int:
    ci_file = Path(sys.argv[1] if len(sys.argv) > 1 else ".gitlab-ci.yml")
    report = Path("plumber-report.txt")
    issues: list[str] = []

    if not ci_file.exists():
        issues.append(f"Missing file: {ci_file}")
    else:
        config = yaml.safe_load(ci_file.read_text(encoding="utf-8")) or {}
        stages = config.get("stages", [])
        missing_stages = [stage for stage in REQUIRED_STAGES if stage not in stages]
        missing_jobs = [job for job in REQUIRED_JOBS if job not in config]
        if missing_stages:
            issues.append(f"Missing stages: {', '.join(missing_stages)}")
        if missing_jobs:
            issues.append(f"Missing jobs: {', '.join(missing_jobs)}")
        plumber_job = config.get("plumber:conformity", {})
        if plumber_job.get("allow_failure") is not True:
            issues.append("Plumber job should be allow_failure: true")

    if not issues:
        issues.append("Plumber compliance check passed")

    report.write_text("\n".join(issues) + "\n", encoding="utf-8")
    print("\n".join(issues))
    return 0 if issues == ["Plumber compliance check passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
