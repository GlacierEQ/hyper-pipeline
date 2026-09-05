#!/usr/bin/env python3
"""
Hyper-Pipeline — Unified Pipeline System
The meta-pipeline that builds, composes, and runs pipelines.

Usage:
    python3 hyper.py architect --name my-pipeline --purpose "Build X"
    python3 hyper.py forge --template production --target /path
    python3 hyper.py run --template production --target /path
    python3 hyper.py list [templates|blocks|skills]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))


def cmd_architect(args: argparse.Namespace) -> int:
    """Run the pipeline architect."""
    from architect import ArchitectConcept, PipelineArchitect

    concept = ArchitectConcept(
        name=args.name,
        purpose=args.purpose,
        domain=args.domain,
        complexity=args.complexity,
        quality_target=args.quality,
        required_skills=[s.strip() for s in args.skills.split(",") if s.strip()],
        required_connectors=[c.strip() for c in args.connectors.split(",") if c.strip()],
    )

    architect = PipelineArchitect(quality_target=args.quality)
    result = architect.architect(concept)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    elif args.format == "yaml":
        print(result.to_yaml())
    elif args.format == "markdown":
        print(result.to_markdown())
    else:
        print(result.to_markdown())
        print("\n" + "=" * 60 + "\n")
        print(result.to_yaml())

    print(f"\nQuality: {result.quality_score.total:.2f} ({result.quality_score.grade})")
    return 0 if result.validation["passed"] else 1


def cmd_forge(args: argparse.Namespace) -> int:
    """Run the pipeline forge."""
    from forge import PipelineComposer

    composer = PipelineComposer()

    if args.config:
        config = composer.compose_from_yaml(args.config)
    else:
        config = composer.compose_from_template(args.template)

    result = composer.run(config, Path(args.target))

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.to_markdown())

    return 0 if result.all_passed else 1


def cmd_run(args: argparse.Namespace) -> int:
    """Run a pipeline directly."""
    from pipeline_runner import PipelineRunner

    runner = PipelineRunner(args.target, skip_phases=args.skip.split(",") if args.skip else [])
    result = runner.run()

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.to_markdown())

    return 0 if result.all_passed else 1


def cmd_list(args: argparse.Namespace) -> int:
    """List available templates, blocks, or skills."""
    if args.what == "templates":
        from forge import PipelineComposer
        composer = PipelineComposer()
        for t in composer.list_templates():
            print(f"  {t}")

    elif args.what == "blocks":
        from forge import PipelineComposer
        composer = PipelineComposer()
        for b in composer.list_blocks():
            print(f"  {b}")

    elif args.what == "skills":
        from architect import SKILL_CATEGORIES
        for category, skills in SKILL_CATEGORIES.items():
            print(f"\n  {category}:")
            for s in skills:
                print(f"    - {s['name']}: {s['purpose']}")

    elif args.what == "connectors":
        from architect import CONNECTORS
        for name, info in CONNECTORS.items():
            print(f"  {name}: {info['purpose']} ({info['type']})")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Hyper-Pipeline — Unified Pipeline System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build a new pipeline
  python3 hyper.py architect --name security-audit --purpose "Full security audit" --domain security

  # Run a pipeline on a project
  python3 hyper.py forge --template production --target /path/to/project

  # Run the 10-phase production pipeline
  python3 hyper.py run --template production --target /path/to/project

  # List available options
  python3 hyper.py list templates
  python3 hyper.py list blocks
  python3 hyper.py list skills
        """,
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # Architect command
    arch = sub.add_parser("architect", help="Build a new pipeline from concept")
    arch.add_argument("--name", required=True, help="Pipeline name")
    arch.add_argument("--purpose", required=True, help="Pipeline purpose")
    arch.add_argument("--domain", default="engineering", choices=["engineering", "research", "security", "data", "design"])
    arch.add_argument("--complexity", type=int, default=5, help="Complexity 1-10")
    arch.add_argument("--quality", type=float, default=9.0, help="Quality target")
    arch.add_argument("--skills", default="", help="Required skills (comma-separated)")
    arch.add_argument("--connectors", default="", help="Required connectors (comma-separated)")
    arch.add_argument("--format", choices=["json", "yaml", "markdown", "all"], default="all")

    # Forge command
    forge = sub.add_parser("forge", help="Compose and run a pipeline")
    forge.add_argument("--template", help="Template name")
    forge.add_argument("--config", help="YAML config file")
    forge.add_argument("--target", required=True, help="Target directory")
    forge.add_argument("--format", choices=["json", "markdown"], default="markdown")

    # Run command
    run = sub.add_parser("run", help="Run a pipeline directly")
    run.add_argument("--template", default="production", help="Template name")
    run.add_argument("--target", required=True, help="Target directory")
    run.add_argument("--skip", default="", help="Skip phases (comma-separated)")
    run.add_argument("--format", choices=["json", "markdown"], default="markdown")

    # List command
    ls = sub.add_parser("list", help="List available options")
    ls.add_argument("what", choices=["templates", "blocks", "skills", "connectors"])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "architect": cmd_architect,
        "forge": cmd_forge,
        "run": cmd_run,
        "list": cmd_list,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
