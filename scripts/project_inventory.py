#!/usr/bin/env python3
"""Create a read-only, content-free inventory of an unfamiliar repository."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".cache",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
    "node_modules",
    "bower_components",
    "vendor",
    "target",
    "dist",
    "build",
    "coverage",
    ".terraform",
    ".venv",
    "venv",
}

MANIFEST_NAMES = {
    "package.json",
    "pnpm-workspace.yaml",
    "yarn.lock",
    "pnpm-lock.yaml",
    "package-lock.json",
    "turbo.json",
    "nx.json",
    "Cargo.toml",
    "Cargo.lock",
    "go.mod",
    "go.work",
    "pyproject.toml",
    "poetry.lock",
    "requirements.txt",
    "Pipfile",
    "Gemfile",
    "composer.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "gradlew",
    "Makefile",
    "Taskfile.yml",
    "justfile",
}

SERVICE_MANIFESTS = {
    "package.json",
    "Cargo.toml",
    "go.mod",
    "pyproject.toml",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Gemfile",
    "composer.json",
}

DOC_PREFIXES = ("readme", "contributing", "architecture", "design", "adr", "runbook")
API_SUFFIXES = (".proto", ".graphql", ".gql", ".wsdl", ".avsc", ".avdl")
DEPLOY_SUFFIXES = (".tf", ".tfvars")
TEST_DIRS = {"test", "tests", "spec", "specs", "e2e", "integration", "integration-tests"}
MIGRATION_DIRS = {"migration", "migrations", "schema", "schemas", "ddl"}
OBSERVABILITY_TERMS = {"observability", "telemetry", "metrics", "tracing", "prometheus", "grafana", "opentelemetry", "otel"}
ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "server.py",
    "manage.py",
    "main.go",
    "main.rs",
    "main.ts",
    "main.js",
    "server.ts",
    "server.js",
    "Program.cs",
    "Application.java",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan file names and paths without reading source contents."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    parser.add_argument(
        "--max-depth",
        type=int,
        default=5,
        help="Maximum directory depth to scan (default: 5)",
    )
    parser.add_argument(
        "--max-files",
        type=int,
        default=100_000,
        help="Stop after this many files (default: 100000)",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--focus-path",
        help="Scan only this repository-relative directory while preserving a bounded scope",
    )
    return parser.parse_args()


def relative_depth(root: Path, directory: Path) -> int:
    try:
        return len(directory.relative_to(root).parts)
    except ValueError:
        return 0


def classify(path: Path) -> set[str]:
    name = path.name
    lower = name.lower()
    parts = {part.lower() for part in path.parts}
    categories: set[str] = set()

    if name in MANIFEST_NAMES or lower.endswith((".sln", ".csproj", ".fsproj")):
        categories.add("build_and_dependency")
    if lower.startswith(DOC_PREFIXES) or "docs" in parts:
        if path.suffix.lower() in {"", ".md", ".mdx", ".rst", ".txt", ".adoc"}:
            categories.add("documentation")
    if (
        lower.startswith(("openapi", "swagger", "asyncapi"))
        or lower.endswith(API_SUFFIXES)
        or lower in {"schema.graphql", "schema.gql"}
    ):
        categories.add("api_contract")
    if (
        lower.startswith("dockerfile")
        or lower.startswith(("docker-compose", "compose."))
        or lower.endswith(DEPLOY_SUFFIXES)
        or any(part.lower() in {"k8s", "kubernetes", "helm", "deploy", "deployment"} for part in path.parts)
    ):
        categories.add("deployment_and_infrastructure")
    if name in ENTRYPOINT_NAMES or (
        len(path.parts) >= 2 and path.parts[-2].lower() == "cmd" and name.startswith("main.")
    ):
        categories.add("entrypoint_hint")
    if lower.startswith((".env.example", ".env.sample")) or lower in {
        "application.yml",
        "application.yaml",
        "application.properties",
        "config.example.yml",
        "config.example.yaml",
    }:
        categories.add("configuration_example")
    if (
        parts & TEST_DIRS
        or lower.startswith(("test_", "spec_"))
        or lower.endswith(("_test.py", "_test.go", ".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.rb"))
    ):
        categories.add("tests_and_quality")
    if parts & MIGRATION_DIRS or lower.startswith(("schema.", "migration.")):
        categories.add("data_schema_and_migrations")
    if (
        ".github" in parts and "workflows" in parts
        or lower in {".gitlab-ci.yml", "jenkinsfile", "buildkite.yml", "azure-pipelines.yml", "circle.yml"}
        or ".circleci" in parts
    ):
        categories.add("ci_and_automation")
    if lower in {"codeowners", "owners", "maintainers", "maintainers.md"} or "ownership" in lower:
        categories.add("ownership")
    if parts & OBSERVABILITY_TERMS or any(term in lower for term in OBSERVABILITY_TERMS):
        categories.add("observability")
    if any(
        token in lower
        for token in ("route", "router", "handler", "controller", "consumer", "subscriber", "listener", "worker", "scheduler", "cron", "job")
    ):
        categories.add("route_event_and_job_hints")
    if lower in {".envrc", "devcontainer.json", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"} or ".devcontainer" in parts:
        categories.add("local_development")
    return categories


def scan(root: Path, max_depth: int, max_files: int) -> dict[str, object]:
    extensions: Counter[str] = Counter()
    categories: dict[str, list[str]] = defaultdict(list)
    module_manifests: dict[str, list[str]] = defaultdict(list)
    top_level: set[str] = set()
    scanned_files = 0
    truncated = False

    for current, dirnames, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        depth = relative_depth(root, current_path)
        dirnames[:] = sorted(
            directory
            for directory in dirnames
            if directory not in IGNORED_DIRS
            and not (current_path / directory).is_symlink()
            and depth < max_depth
        )

        if depth == 0:
            top_level.update(dirnames)
            top_level.update(filenames)

        for filename in sorted(filenames):
            path = current_path / filename
            if path.is_symlink():
                continue
            scanned_files += 1
            if scanned_files > max_files:
                truncated = True
                break

            relative = path.relative_to(root)
            extension = path.suffix.lower() or "[no extension]"
            extensions[extension] += 1

            for category in classify(relative):
                if len(categories[category]) < 250:
                    categories[category].append(relative.as_posix())

            if filename in SERVICE_MANIFESTS:
                module = relative.parent.as_posix() or "."
                module_manifests[module].append(filename)

        if truncated:
            break

    return {
        "root": str(root),
        "scanned_files": min(scanned_files, max_files),
        "truncated": truncated,
        "max_depth": max_depth,
        "ignored_directories": sorted(IGNORED_DIRS),
        "top_level": sorted(top_level),
        "extensions": dict(extensions.most_common()),
        "categories": {key: sorted(value) for key, value in sorted(categories.items())},
        "module_candidates": {
            key: sorted(value) for key, value in sorted(module_manifests.items())
        },
    }


def markdown_list(items: Iterable[str], empty: str = "_None found within scan depth._") -> str:
    values = list(items)
    if not values:
        return empty
    return "\n".join(f"- `{value}`" for value in values)


def to_markdown(result: dict[str, object]) -> str:
    extensions = result["extensions"]
    categories = result["categories"]
    modules = result["module_candidates"]

    lines = [
        "# Project inventory",
        "",
        f"- Repository root: `{result.get('repository_root', result['root'])}`",
        f"- Scanned root: `{result['root']}`",
        f"- Focus path: `{result.get('focus_path') or '.'}`",
        f"- Files scanned: {result['scanned_files']}",
        f"- Maximum depth: {result['max_depth']}",
        f"- Truncated at file limit: {'yes' if result['truncated'] else 'no'}",
        "",
        "## Top-level entries",
        "",
        markdown_list(result["top_level"]),
        "",
        "## Candidate modules",
        "",
    ]

    if modules:
        lines.extend(["| Directory | Manifests |", "|---|---|"])
        for directory, manifests in modules.items():
            rendered = ", ".join(f"`{manifest}`" for manifest in manifests)
            lines.append(f"| `{directory}` | {rendered} |")
    else:
        lines.append("_No service/package manifests found within scan depth._")

    lines.extend(["", "## File types", "", "| Extension | Count |", "|---|---:|"])
    for extension, count in list(extensions.items())[:40]:
        lines.append(f"| `{extension}` | {count} |")

    headings = {
        "build_and_dependency": "Build and dependency files",
        "documentation": "Documentation",
        "api_contract": "API and message contracts",
        "deployment_and_infrastructure": "Deployment and infrastructure",
        "entrypoint_hint": "Entrypoint hints",
        "configuration_example": "Configuration examples",
        "local_development": "Local development hints",
        "tests_and_quality": "Tests and quality",
        "data_schema_and_migrations": "Data schemas and migrations",
        "route_event_and_job_hints": "Route, event, and job hints",
        "ci_and_automation": "CI and automation",
        "ownership": "Ownership hints",
        "observability": "Observability hints",
    }
    for key, heading in headings.items():
        lines.extend(["", f"## {heading}", "", markdown_list(categories.get(key, []))])

    lines.extend(
        [
            "",
            "## Interpretation note",
            "",
            "This inventory uses file names and paths only. Confirm architecture through active wiring, implementation, schemas, tests, and runtime configuration.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    if args.max_depth < 0:
        raise SystemExit("--max-depth must be non-negative")
    if args.max_files < 1:
        raise SystemExit("--max-files must be positive")

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Repository root is not a directory: {root}")

    scan_root = root
    focus_path = None
    if args.focus_path:
        requested = Path(args.focus_path)
        if requested.is_absolute():
            raise SystemExit("--focus-path must be repository-relative")
        scan_root = (root / requested).resolve()
        try:
            focus_path = scan_root.relative_to(root).as_posix()
        except ValueError as exc:
            raise SystemExit("--focus-path must stay inside the repository root") from exc
        if not scan_root.is_dir():
            raise SystemExit(f"Focus path is not a directory: {scan_root}")

    result = scan(scan_root, args.max_depth, args.max_files)
    result["repository_root"] = str(root)
    result["focus_path"] = focus_path
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
