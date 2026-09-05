#!/usr/bin/env python3
"""
Pipeline Architect — Meta-pipeline that builds production-grade pipelines
with skill integration, connector wiring, and sequential thinking enforcement.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# ─── Constants ───────────────────────────────────────────────────────────────

VERSION = "1.0.0"

# ─── Skill Registry ──────────────────────────────────────────────────────────

SKILL_CATEGORIES = {
    "engineering": [
        {"name": "helix-pro-code", "purpose": "Pro-code engineering", "integration": "inline"},
        {"name": "compose-next", "purpose": "Multi-step feature work", "integration": "inline"},
        {"name": "quality-gate", "purpose": "Phase acceptance", "integration": "inline"},
        {"name": "production-readiness-gate", "purpose": "7-dimension audit", "integration": "inline"},
        {"name": "verification-before-completion", "purpose": "No claims without evidence", "integration": "inline"},
    ],
    "research": [
        {"name": "deep-research", "purpose": "Multi-source investigation", "integration": "subagent"},
        {"name": "super-research", "purpose": "Autonomous research loops", "integration": "subagent"},
        {"name": "arxiv", "purpose": "Academic papers", "integration": "reference"},
    ],
    "security": [
        {"name": "semgrep", "purpose": "Static analysis", "integration": "inline"},
        {"name": "differential-review", "purpose": "PR security review", "integration": "inline"},
        {"name": "supply-chain-risk-auditor", "purpose": "Dependency audit", "integration": "inline"},
    ],
    "data": [
        {"name": "data-analytics", "purpose": "Quantitative analysis", "integration": "subagent"},
        {"name": "build-report", "purpose": "Analytical reports", "integration": "subagent"},
        {"name": "visualize-data", "purpose": "Charts and figures", "integration": "subagent"},
    ],
    "design": [
        {"name": "frontend-design", "purpose": "Visual design", "integration": "subagent"},
        {"name": "mega-web", "purpose": "Elite web engineering", "integration": "inline"},
        {"name": "design-blueprint", "purpose": "Structured design specs", "integration": "inline"},
    ],
    "memory": [
        {"name": "memory-unified", "purpose": "Persistent memory", "integration": "inline"},
        {"name": "context-capsule", "purpose": "State protection", "integration": "inline"},
        {"name": "handoff-record", "purpose": "Recovery fidelity", "integration": "inline"},
    ],
    "orchestration": [
        {"name": "swarm-orchestrator", "purpose": "Multi-agent delegation", "integration": "inline"},
        {"name": "skill-connector-router", "purpose": "Dynamic skill dispatch", "integration": "inline"},
        {"name": "make-it-heavy", "purpose": "High-intensity execution", "integration": "inline"},
    ],
}

# ─── Connector Registry ──────────────────────────────────────────────────────

CONNECTORS = {
    "github": {"type": "api", "purpose": "Repos, issues, PRs", "auth": "token"},
    "notion": {"type": "api", "purpose": "Docs, databases", "auth": "token"},
    "supabase": {"type": "database", "purpose": "Postgres, auth", "auth": "key"},
    "vercel": {"type": "service", "purpose": "Deploy, edge", "auth": "token"},
    "openrouter": {"type": "api", "purpose": "LLM routing", "auth": "key"},
    "dropbox": {"type": "storage", "purpose": "Files", "auth": "token"},
    "gmail": {"type": "api", "purpose": "Email", "auth": "oauth"},
}


# ─── Sequential Thinking Engine ──────────────────────────────────────────────

class ThinkingStep(Enum):
    OBSERVE = "observe"
    ANALYZE = "analyze"
    HYPOTHESIZE = "hypothesize"
    VERIFY = "verify"
    SYNTHESIZE = "synthesize"


@dataclass
class ThinkingChain:
    """A sequential thinking chain for a work unit."""
    unit: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0

    def add_step(self, step: ThinkingStep, description: str, evidence: str) -> None:
        self.steps.append({
            "step": step.value,
            "description": description,
            "evidence": evidence,
        })
        self.evidence.append(evidence)

    def calculate_confidence(self) -> float:
        """Calculate confidence based on evidence quality."""
        if not self.steps:
            return 0.0
        evidence_score = len(self.evidence) / 5.0  # 5 steps = 1.0
        completeness = len(self.steps) / 5.0
        self.confidence = min(1.0, (evidence_score + completeness) / 2.0)
        return self.confidence


class SequentialThinkingEnforcer:
    """Enforces sequential thinking on complex work units."""

    def __init__(self, threshold: int = 7) -> None:
        self.threshold = threshold
        self.chains: List[ThinkingChain] = []

    def should_enforce(self, complexity: int) -> bool:
        return complexity >= self.threshold

    def create_chain(self, unit: str) -> ThinkingChain:
        chain = ThinkingChain(unit=unit)

        # Add standard 5-step chain
        chain.add_step(
            ThinkingStep.OBSERVE,
            "What do I see?",
            "Raw observations and data points",
        )
        chain.add_step(
            ThinkingStep.ANALYZE,
            "What does it mean?",
            "Interpretation and pattern recognition",
        )
        chain.add_step(
            ThinkingStep.HYPOTHESIZE,
            "What might be true?",
            "Proposed explanations and theories",
        )
        chain.add_step(
            ThinkingStep.VERIFY,
            "How can I confirm?",
            "Verification methods and evidence",
        )
        chain.add_step(
            ThinkingStep.SYNTHESIZE,
            "What's my conclusion?",
            "Final synthesis and decision",
        )

        chain.calculate_confidence()
        self.chains.append(chain)
        return chain

    def validate_chain(self, chain: ThinkingChain) -> Dict[str, Any]:
        """Validate a thinking chain meets quality standards."""
        issues = []

        if len(chain.steps) < 5:
            issues.append("Incomplete thinking chain (< 5 steps)")

        if chain.confidence < 0.8:
            issues.append(f"Low confidence ({chain.confidence:.2f} < 0.80)")

        step_types = [s["step"] for s in chain.steps]
        required = ["observe", "analyze", "hypothesize", "verify", "synthesize"]
        for r in required:
            if r not in step_types:
                issues.append(f"Missing step: {r}")

        return {
            "valid": len(issues) == 0,
            "confidence": chain.confidence,
            "issues": issues,
        }


# ─── Quality Scorer ──────────────────────────────────────────────────────────

@dataclass
class QualityScore:
    """Quality score for a pipeline or phase."""
    completeness: float = 0.0
    correctness: float = 0.0
    clarity: float = 0.0
    confidence: float = 0.0
    coherence: float = 0.0

    @property
    def total(self) -> float:
        return (
            self.completeness * 0.20 +
            self.correctness * 0.25 +
            self.clarity * 0.20 +
            self.confidence * 0.20 +
            self.coherence * 0.15
        )

    @property
    def grade(self) -> str:
        score = self.total
        if score >= 9.5:
            return "S"
        elif score >= 9.0:
            return "A+"
        elif score >= 8.5:
            return "A"
        elif score >= 8.0:
            return "B+"
        elif score >= 7.0:
            return "B"
        else:
            return "C"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "completeness": round(self.completeness, 2),
            "correctness": round(self.correctness, 2),
            "clarity": round(self.clarity, 2),
            "confidence": round(self.confidence, 2),
            "coherence": round(self.coherence, 2),
            "total": round(self.total, 2),
            "grade": self.grade,
        }


class QualityScorer:
    """Scores pipeline designs for quality."""

    def __init__(self, target: float = 9.0) -> None:
        self.target = target

    def score_phase(self, phase: Dict[str, Any]) -> QualityScore:
        """Score a single phase."""
        score = QualityScore()

        # Completeness: has all required fields
        required = ["name", "inputs", "outputs", "evidence", "skills"]
        present = sum(1 for r in required if r in phase)
        score.completeness = min(10, (present / len(required)) * 10 + 2)

        # Correctness: evidence is specific and sufficient
        evidence = phase.get("evidence", [])
        score.correctness = min(10, 4 + len(evidence) * 1.5) if evidence else 2

        # Clarity: name is descriptive, type specified
        name = phase.get("name", "")
        has_type = "type" in phase
        score.clarity = min(10, 5 + (2 if len(name) > 5 else 0) + (3 if has_type else 0))

        # Confidence: has quality gate
        has_gate = "quality_gate" in phase
        has_skills = len(phase.get("skills", [])) > 0
        score.confidence = min(10, 5 + (3 if has_gate else 0) + (2 if has_skills else 0))

        # Coherence: connects to other phases
        has_inputs = bool(phase.get("inputs"))
        has_outputs = bool(phase.get("outputs"))
        score.coherence = min(10, 6 + (2 if has_inputs else 0) + (2 if has_outputs else 0))

        return score

    def score_pipeline(self, pipeline: Dict[str, Any]) -> QualityScore:
        """Score a full pipeline."""
        phases = pipeline.get("phases", [])
        if not phases:
            return QualityScore()

        phase_scores = [self.score_phase(p) for p in phases]

        avg = QualityScore()
        avg.completeness = sum(s.completeness for s in phase_scores) / len(phase_scores)
        avg.correctness = sum(s.correctness for s in phase_scores) / len(phase_scores)
        avg.clarity = sum(s.clarity for s in phase_scores) / len(phase_scores)
        avg.confidence = sum(s.confidence for s in phase_scores) / len(phase_scores)
        avg.coherence = sum(s.coherence for s in phase_scores) / len(phase_scores)

        return avg

    def validate(self, score: QualityScore) -> Dict[str, Any]:
        """Validate score meets target."""
        return {
            "passed": score.total >= self.target,
            "score": score.total,
            "target": self.target,
            "grade": score.grade,
            "gap": max(0, self.target - score.total),
        }


# ─── Pipeline Architect Engine ───────────────────────────────────────────────

@dataclass
class ArchitectConcept:
    """Input concept for pipeline creation."""
    name: str
    purpose: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    domain: str = "engineering"
    quality_target: float = 9.0
    complexity: int = 5
    required_skills: List[str] = field(default_factory=list)
    required_connectors: List[str] = field(default_factory=list)


@dataclass
class ArchitectResult:
    """Result of pipeline architecture."""
    concept: ArchitectConcept
    pipeline: Dict[str, Any]
    thinking_chains: List[Dict[str, Any]]
    skill_map: Dict[str, List[str]]
    connector_map: Dict[str, List[str]]
    quality_score: QualityScore
    validation: Dict[str, Any]
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept": {
                "name": self.concept.name,
                "purpose": self.concept.purpose,
                "domain": self.concept.domain,
                "quality_target": self.concept.quality_target,
            },
            "pipeline": self.pipeline,
            "thinking_chains": self.thinking_chains,
            "skill_map": self.skill_map,
            "connector_map": self.connector_map,
            "quality_score": self.quality_score.to_dict(),
            "validation": self.validation,
        }

    def to_yaml(self) -> str:
        """Generate YAML pipeline config."""
        lines = [
            f"# Pipeline: {self.concept.name}",
            f"# Generated by Pipeline Architect v{VERSION}",
            f"# Quality Score: {self.quality_score.total:.2f} ({self.quality_score.grade})",
            "",
            f"name: {self.concept.name}",
            f'description: "{self.concept.purpose}"',
            f"version: \"1.0\"",
            "",
            "phases:",
        ]

        for phase in self.pipeline.get("phases", []):
            lines.append(f"  - name: {phase['name']}")
            lines.append(f"    type: {phase.get('type', 'primitive')}")
            if phase.get("skills"):
                lines.append(f"    skills:")
                for s in phase["skills"]:
                    lines.append(f"      - {s}")
            if phase.get("evidence"):
                lines.append(f"    evidence:")
                for e in phase["evidence"]:
                    lines.append(f"      - {e}")
            lines.append("")

        lines.extend([
            "quality:",
            f"  target: {self.concept.quality_target}",
            "  dimensions:",
            "    - completeness",
            "    - correctness",
            "    - clarity",
            "    - confidence",
            "    - coherence",
            "",
            "skills:",
        ])
        for category, skills in self.skill_map.items():
            lines.append(f"  {category}:")
            for s in skills:
                lines.append(f"    - {s}")

        return "\n".join(lines)

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            f"# Pipeline Architect Report",
            "",
            "## Concept",
            f"- **Name:** {self.concept.name}",
            f"- **Purpose:** {self.concept.purpose}",
            f"- **Domain:** {self.concept.domain}",
            f"- **Quality Target:** {self.concept.quality_target}+",
            "",
            "## Quality Score",
            f"- **Total:** {self.quality_score.total:.2f} ({self.quality_score.grade})",
            f"- **Completeness:** {self.quality_score.completeness:.2f}",
            f"- **Correctness:** {self.quality_score.correctness:.2f}",
            f"- **Clarity:** {self.quality_score.clarity:.2f}",
            f"- **Confidence:** {self.quality_score.confidence:.2f}",
            f"- **Coherence:** {self.quality_score.coherence:.2f}",
            "",
            "## Validation",
            f"- **Passed:** {'✓' if self.validation['passed'] else '✗'}",
            f"- **Target:** {self.validation['target']}",
            f"- **Gap:** {self.validation['gap']:.2f}",
            "",
            "## Phases",
            "| # | Phase | Type | Skills | Evidence |",
            "|---|-------|------|--------|----------|",
        ]

        for i, phase in enumerate(self.pipeline.get("phases", []), 1):
            skills = ", ".join(phase.get("skills", []))
            evidence = ", ".join(phase.get("evidence", []))
            lines.append(
                f"| {i} | {phase['name']} | {phase.get('type', 'primitive')} | {skills} | {evidence} |"
            )

        lines.extend([
            "",
            "## Skill Map",
        ])
        for category, skills in self.skill_map.items():
            lines.append(f"### {category.title()}")
            for s in skills:
                lines.append(f"- `{s}`")

        lines.extend([
            "",
            "## Connector Map",
        ])
        for connector, phases in self.connector_map.items():
            lines.append(f"- **{connector}**: {', '.join(phases)}")

        return "\n".join(lines)


class PipelineArchitect:
    """Meta-pipeline that builds production-grade pipelines."""

    def __init__(self, quality_target: float = 9.0) -> None:
        self.quality_target = quality_target
        self.thinking_enforcer = SequentialThinkingEnforcer(threshold=7)
        self.scorer = QualityScorer(target=quality_target)

    def _map_skills(self, concept: ArchitectConcept) -> Dict[str, List[str]]:
        """Map required skills to pipeline phases."""
        skill_map: Dict[str, List[str]] = {}

        # Always include core skills
        skill_map["core"] = [
            "quality-gate",
            "verification-before-completion",
            "context-capsule",
        ]

        # Domain-specific skills
        domain = concept.domain
        if domain in SKILL_CATEGORIES:
            skill_map[domain] = [s["name"] for s in SKILL_CATEGORIES[domain][:3]]

        # Add requested skills
        if concept.required_skills:
            skill_map["requested"] = concept.required_skills

        return skill_map

    def _map_connectors(self, concept: ArchitectConcept) -> Dict[str, List[str]]:
        """Map required connectors to pipeline phases."""
        connector_map: Dict[str, List[str]] = {}

        for connector in concept.required_connectors:
            if connector in CONNECTORS:
                connector_map[connector] = ["implement", "verify"]

        return connector_map

    def _design_thinking_chains(self, concept: ArchitectConcept) -> List[Dict[str, Any]]:
        """Design sequential thinking chains for complex units."""
        chains = []

        if concept.complexity >= 7:
            chain = self.thinking_enforcer.create_chain(concept.name)
            validation = self.thinking_enforcer.validate_chain(chain)
            chains.append({
                "unit": concept.name,
                "steps": chain.steps,
                "confidence": chain.confidence,
                "validation": validation,
            })

        return chains

    def _design_phases(self, concept: ArchitectConcept, skill_map: Dict, connector_map: Dict) -> List[Dict[str, Any]]:
        """Design pipeline phases."""
        phases = []

        # Phase 1: Orient
        phases.append({
            "name": "orient",
            "type": "primitive",
            "inputs": ["concept"],
            "outputs": ["understanding"],
            "evidence": ["repository mapped", "requirements understood", "constraints identified"],
            "skills": ["quality-gate", "context-capsule"],
        })

        # Phase 2: Grill (if complex)
        if concept.complexity >= 5:
            phases.append({
                "name": "grill",
                "type": "primitive",
                "inputs": ["understanding"],
                "outputs": ["decisions"],
                "evidence": ["decisions resolved", "trade-offs documented", "alternatives evaluated"],
                "skills": ["context-capsule", "sequential-thinking"],
            })

        # Phase 3: Spec
        phases.append({
            "name": "spec",
            "type": "primitive",
            "inputs": ["decisions", "understanding"],
            "outputs": ["specification"],
            "evidence": ["spec written", "tasks defined", "acceptance criteria set"],
            "skills": skill_map.get("core", []),
        })

        # Phase 4: Implement
        phases.append({
            "name": "implement",
            "type": "primitive",
            "inputs": ["specification"],
            "outputs": ["implementation"],
            "evidence": ["code written", "tests passing", "type hints complete"],
            "skills": skill_map.get(concept.domain, []),
            "connectors": list(connector_map.keys()),
        })

        # Phase 5: Gate (if quality target high)
        if concept.quality_target >= 8.0:
            phases.append({
                "name": "gate",
                "type": "power-up",
                "inputs": ["implementation"],
                "outputs": ["validated"],
                "evidence": ["7-dimension audit passed", "all gates green", "quality score documented"],
                "skills": ["production-readiness-gate"],
                "quality_gate": {"min_score": concept.quality_target},
            })

        # Phase 6: Verify
        phases.append({
            "name": "verify",
            "type": "primitive",
            "inputs": ["validated", "implementation"],
            "outputs": ["verified"],
            "evidence": ["all tests passed", "no regressions", "coverage verified"],
            "skills": ["verification-before-completion"],
        })

        # Phase 7: Review
        phases.append({
            "name": "review",
            "type": "primitive",
            "inputs": ["verified"],
            "outputs": ["reviewed"],
            "evidence": ["code review complete", "standards compliance verified"],
            "skills": ["quality-gate"],
        })

        # Phase 8: Finalize
        phases.append({
            "name": "finalize",
            "type": "primitive",
            "inputs": ["reviewed"],
            "outputs": ["delivered"],
            "evidence": ["docs updated", "status marked", "changelog written"],
            "skills": [],
        })

        # Phase 9: Finish
        phases.append({
            "name": "finish",
            "type": "primitive",
            "inputs": ["delivered"],
            "outputs": ["result"],
            "evidence": ["pipeline complete", "report generated", "artifacts packaged"],
            "skills": [],
        })

        return phases

    def architect(self, concept: ArchitectConcept) -> ArchitectResult:
        """Build a production-grade pipeline from a concept."""
        start = time.monotonic()

        # Step 1: Map skills
        skill_map = self._map_skills(concept)

        # Step 2: Map connectors
        connector_map = self._map_connectors(concept)

        # Step 3: Design thinking chains
        thinking_chains = self._design_thinking_chains(concept)

        # Step 4: Design phases
        phases = self._design_phases(concept, skill_map, connector_map)

        # Step 5: Assemble pipeline
        pipeline = {
            "name": concept.name,
            "description": concept.purpose,
            "version": "1.0",
            "phases": phases,
            "quality": {
                "target": concept.quality_target,
                "dimensions": ["completeness", "correctness", "clarity", "confidence", "coherence"],
            },
        }

        # Step 6: Score quality
        quality_score = self.scorer.score_pipeline(pipeline)

        # Step 7: Validate
        validation = self.scorer.validate(quality_score)

        duration = (time.monotonic() - start) * 1000

        return ArchitectResult(
            concept=concept,
            pipeline=pipeline,
            thinking_chains=thinking_chains,
            skill_map=skill_map,
            connector_map=connector_map,
            quality_score=quality_score,
            validation=validation,
            duration_ms=duration,
        )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description=f"Pipeline Architect v{VERSION}")
    parser.add_argument("--name", type=str, required=True, help="Pipeline name")
    parser.add_argument("--purpose", type=str, required=True, help="Pipeline purpose")
    parser.add_argument("--domain", type=str, default="engineering",
                        choices=["engineering", "research", "security", "data", "design"],
                        help="Pipeline domain")
    parser.add_argument("--complexity", type=int, default=5, help="Complexity 1-10")
    parser.add_argument("--quality", type=float, default=9.0, help="Quality target")
    parser.add_argument("--skills", type=str, default="", help="Required skills (comma-separated)")
    parser.add_argument("--connectors", type=str, default="", help="Required connectors (comma-separated)")
    parser.add_argument("--output", type=str, default=None, help="Output file")
    parser.add_argument("--format", choices=["json", "yaml", "markdown", "all"], default="all")

    args = parser.parse_args()

    concept = ArchitectConcept(
        name=args.name,
        purpose=args.purpose,
        inputs=["input"],
        outputs=["output"],
        domain=args.domain,
        quality_target=args.quality,
        complexity=args.complexity,
        required_skills=[s.strip() for s in args.skills.split(",") if s.strip()],
        required_connectors=[c.strip() for c in args.connectors.split(",") if c.strip()],
    )

    architect = PipelineArchitect(quality_target=args.quality)
    result = architect.architect(concept)

    # Output
    if args.format in ("json", "all"):
        output = json.dumps(result.to_dict(), indent=2)
        if args.format == "all":
            print(output)
        elif args.output:
            Path(args.output).write_text(output)
        else:
            print(output)

    if args.format in ("yaml", "all"):
        yaml_output = result.to_yaml()
        if args.format == "all":
            print("\n" + "=" * 60 + "\n")
            print(yaml_output)
        elif args.output:
            Path(args.output + ".yaml").write_text(yaml_output)
        else:
            print("\n" + "=" * 60 + "\n")
            print(yaml_output)

    if args.format in ("markdown", "all"):
        md_output = result.to_markdown()
        if args.format == "all":
            print("\n" + "=" * 60 + "\n")
            print(md_output)
        elif args.output:
            Path(args.output + ".md").write_text(md_output)
        else:
            print("\n" + "=" * 60 + "\n")
            print(md_output)

    # Summary
    print(f"\n{'='*60}")
    print(f"PIPELINE ARCHITECT: {concept.name}")
    print(f"Quality Score: {result.quality_score.total:.2f} ({result.quality_score.grade})")
    print(f"Validation: {'PASS' if result.validation['passed'] else 'FAIL'}")
    print(f"Duration: {result.duration_ms:.0f}ms")
    print(f"{'='*60}")

    return 0 if result.validation["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
