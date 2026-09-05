#!/usr/bin/env python3
"""
Session Renamer — Intelligent Session Naming Engine
Generates meaningful names for sessions based on content and context.

Usage:
    python3 session_renamer.py --name "new session" --context "working on MCP forge"
    python3 session_renamer.py --auto --context "building test suite for hyper-pipeline"
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "1.0.0"


# ─── Name Patterns ───────────────────────────────────────────────────────────

ACTION_VERBS = [
    "build", "create", "design", "implement", "fix", "update", "refactor",
    "optimize", "test", "deploy", "debug", "analyze", "review", "audit",
    "migrate", "upgrade", "integrate", "configure", "setup", "initialize",
    "compose", "orchestrate", "synthesize", "generate", "validate", "verify",
]

DOMAINS = {
    "pipeline": ["architect", "forge", "runner", "compose", "template", "block"],
    "mcp": ["server", "tool", "resource", "protocol", "handler", "schema"],
    "test": ["unit", "integration", "e2e", "property", "suite", "coverage"],
    "doc": ["readme", "api", "guide", "tutorial", "reference", "changelog"],
    "deploy": ["ci", "cd", "docker", "k8s", "vercel", "github", "actions"],
    "skill": ["skill", "forge", "trigger", "domain", "connector"],
    "security": ["audit", "scan", "vulnerability", "fix", "harden"],
    "data": ["etl", "pipeline", "analytics", "report", "dashboard"],
    "ml": ["model", "train", "inference", "deploy", "monitor"],
    "systems": ["kernel", "memory", "io", "network", "process"],
}

CONTEXT_KEYWORDS = {
    "fix": ["bug", "error", "issue", "broken", "fail", "crash"],
    "build": ["create", "new", "add", "implement", "generate"],
    "update": ["modify", "change", "edit", "improve", "enhance"],
    "test": ["test", "verify", "validate", "check", "assert"],
    "deploy": ["deploy", "ship", "push", "release", "publish"],
    "refactor": ["clean", "organize", "restructure", "simplify"],
}


# ─── Data Models ─────────────────────────────────────────────────────────────

@dataclass
class SessionName:
    """A generated session name."""
    name: str
    description: str
    confidence: float
    tags: List[str]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "confidence": self.confidence,
            "tags": self.tags,
            "timestamp": self.timestamp,
        }


# ─── Name Generator ──────────────────────────────────────────────────────────

class SessionRenamer:
    """Generates meaningful session names."""

    def __init__(self) -> None:
        self.history: List[SessionName] = []

    def generate(self, context: str, current_name: Optional[str] = None) -> SessionName:
        """Generate a session name from context."""
        # Analyze context
        action = self._detect_action(context)
        domain = self._detect_domain(context)
        specificity = self._calculate_specificity(context)
        tags = self._extract_tags(context)

        # Build name
        if domain and action:
            name = f"{action}-{domain}"
        elif domain:
            name = domain
        elif action:
            name = action
        else:
            name = self._generate_generic_name(context)

        # Add specificity if needed
        if specificity > 0.5:
            name = f"{name}-{int(specificity * 10)}"

        # Clean name
        name = self._clean_name(name)

        # Generate description
        description = self._generate_description(action, domain, context)

        # Calculate confidence
        confidence = self._calculate_confidence(action, domain, context)

        session = SessionName(
            name=name,
            description=description,
            confidence=confidence,
            tags=tags,
            timestamp=time.strftime("%Y-%m-%d %H:%M"),
        )

        self.history.append(session)
        return session

    def _detect_action(self, context: str) -> Optional[str]:
        """Detect the primary action from context."""
        context_lower = context.lower()

        for verb in ACTION_VERBS:
            if verb in context_lower:
                return verb

        # Check context keywords
        for action, keywords in CONTEXT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in context_lower:
                    return action

        return None

    def _detect_domain(self, context: str) -> Optional[str]:
        """Detect the domain from context."""
        context_lower = context.lower()

        for domain, keywords in DOMAINS.items():
            for keyword in keywords:
                if keyword in context_lower:
                    return domain

        return None

    def _calculate_specificity(self, context: str) -> float:
        """Calculate how specific the context is (0-1)."""
        words = context.split()
        length_score = min(1.0, len(words) / 10)
        unique_words = len(set(w.lower() for w in words))
        diversity_score = min(1.0, unique_words / 8)
        return (length_score + diversity_score) / 2

    def _extract_tags(self, context: str) -> List[str]:
        """Extract relevant tags from context."""
        tags = []
        context_lower = context.lower()

        for domain, keywords in DOMAINS.items():
            for keyword in keywords:
                if keyword in context_lower:
                    tags.append(domain)
                    break

        return list(set(tags))

    def _generate_generic_name(self, context: str) -> str:
        """Generate a generic name when no specific action/domain found."""
        words = context.split()
        if len(words) >= 2:
            return "-".join(w.lower() for w in words[:2])
        return "session"

    def _clean_name(self, name: str) -> str:
        """Clean and normalize the name."""
        # Remove special characters
        name = re.sub(r'[^a-z0-9-]', '-', name.lower())
        # Remove consecutive hyphens
        name = re.sub(r'-+', '-', name)
        # Remove leading/trailing hyphens
        name = name.strip('-')
        return name

    def _generate_description(self, action: Optional[str], domain: Optional[str], context: str) -> str:
        """Generate a human-readable description."""
        parts = []
        if action:
            parts.append(f"Action: {action}")
        if domain:
            parts.append(f"Domain: {domain}")
        parts.append(f"Context: {context[:100]}")
        return " | ".join(parts)

    def _calculate_confidence(self, action: Optional[str], domain: Optional[str], context: str) -> float:
        """Calculate confidence in the generated name."""
        score = 0.0
        if action:
            score += 0.4
        if domain:
            score += 0.4
        if len(context.split()) >= 3:
            score += 0.2
        return min(1.0, score)


# ─── Batch Renamer ───────────────────────────────────────────────────────────

class BatchRenamer:
    """Rename multiple sessions at once."""

    def __init__(self) -> None:
        self.renamer = SessionRenamer()

    def rename_batch(self, sessions: List[Dict[str, str]]) -> List[SessionName]:
        """Rename a batch of sessions."""
        results = []
        for session in sessions:
            name = self.renamer.generate(
                context=session.get("context", ""),
                current_name=session.get("name"),
            )
            results.append(name)
        return results

    def rename_from_file(self, filepath: Path) -> List[SessionName]:
        """Rename sessions from a JSON file."""
        data = json.loads(filepath.read_text())
        sessions = data if isinstance(data, list) else data.get("sessions", [])
        return self.rename_batch(sessions)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=f"Session Renamer v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--name", help="Current session name")
    parser.add_argument("--context", help="Session context/description")
    parser.add_argument("--auto", action="store_true", help="Auto-generate from context")
    parser.add_argument("--file", help="Batch rename from JSON file")
    parser.add_argument("--format", choices=["json", "text"], default="text")

    args = parser.parse_args()

    renamer = SessionRenamer()

    if args.file:
        batch = BatchRenamer()
        results = batch.rename_from_file(Path(args.file))
        for r in results:
            print(f"  {r.name}: {r.description}")
    elif args.context:
        result = renamer.generate(args.context, args.name)
        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2))
        else:
            print(f"\nSession Name: {result.name}")
            print(f"Description: {result.description}")
            print(f"Confidence: {result.confidence:.0%}")
            print(f"Tags: {', '.join(result.tags)}")
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
