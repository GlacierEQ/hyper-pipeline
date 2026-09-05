"""
Pipeline Architect — Test Suite
Tests for the meta-pipeline engine, sequential thinking, quality scoring.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from architect import (
    ArchitectConcept,
    ArchitectResult,
    PipelineArchitect,
    SequentialThinkingEnforcer,
    QualityScorer,
    QualityScore,
    ThinkingChain,
    ThinkingStep,
    SKILL_CATEGORIES,
    CONNECTORS,
)


# ─── Sequential Thinking Tests ───────────────────────────────────────────────

class TestSequentialThinking:
    """Tests for sequential thinking enforcement."""

    def test_enforce_above_threshold(self):
        enforcer = SequentialThinkingEnforcer(threshold=7)
        assert enforcer.should_enforce(7)
        assert enforcer.should_enforce(10)
        assert not enforcer.should_enforce(6)

    def test_create_chain(self):
        enforcer = SequentialThinkingEnforcer()
        chain = enforcer.create_chain("test-unit")
        assert chain.unit == "test-unit"
        assert len(chain.steps) == 5
        assert chain.confidence > 0

    def test_chain_has_all_steps(self):
        enforcer = SequentialThinkingEnforcer()
        chain = enforcer.create_chain("test")
        step_types = [s["step"] for s in chain.steps]
        assert "observe" in step_types
        assert "analyze" in step_types
        assert "hypothesize" in step_types
        assert "verify" in step_types
        assert "synthesize" in step_types

    def test_validate_chain_valid(self):
        enforcer = SequentialThinkingEnforcer()
        chain = enforcer.create_chain("test")
        validation = enforcer.validate_chain(chain)
        assert validation["valid"]
        assert validation["confidence"] >= 0.8

    def test_validate_chain_incomplete(self):
        enforcer = SequentialThinkingEnforcer()
        chain = ThinkingChain(unit="test")
        chain.add_step(ThinkingStep.OBSERVE, "observe", "evidence")
        validation = enforcer.validate_chain(chain)
        assert not validation["valid"]
        assert len(validation["issues"]) > 0

    def test_confidence_calculation(self):
        chain = ThinkingChain(unit="test")
        assert chain.calculate_confidence() == 0.0

        chain.add_step(ThinkingStep.OBSERVE, "step1", "ev1")
        chain.add_step(ThinkingStep.ANALYZE, "step2", "ev2")
        chain.add_step(ThinkingStep.HYPOTHESIZE, "step3", "ev3")
        chain.add_step(ThinkingStep.VERIFY, "step4", "ev4")
        chain.add_step(ThinkingStep.SYNTHESIZE, "step5", "ev5")
        confidence = chain.calculate_confidence()
        assert confidence > 0.8


# ─── Quality Scoring Tests ───────────────────────────────────────────────────

class TestQualityScoring:
    """Tests for quality scoring system."""

    def test_score_phase_complete(self):
        scorer = QualityScorer()
        phase = {
            "name": "implement",
            "type": "primitive",
            "inputs": ["spec"],
            "outputs": ["code"],
            "evidence": ["tests passing", "code written"],
            "skills": ["helix-pro-code"],
            "quality_gate": {"min_score": 9},
        }
        score = scorer.score_phase(phase)
        assert score.total >= 7.0

    def test_score_phase_minimal(self):
        scorer = QualityScorer()
        phase = {"name": "x"}
        score = scorer.score_phase(phase)
        assert score.total < 8.0

    def test_score_pipeline(self):
        scorer = QualityScorer()
        pipeline = {
            "phases": [
                {"name": "orient", "inputs": ["a"], "outputs": ["b"], "evidence": ["e1"], "skills": ["s1"]},
                {"name": "implement", "inputs": ["b"], "outputs": ["c"], "evidence": ["e2"], "skills": ["s2"]},
            ]
        }
        score = scorer.score_pipeline(pipeline)
        assert score.total > 0
        assert score.grade in ["S", "A+", "A", "B+", "B", "C"]

    def test_validate_passed(self):
        scorer = QualityScorer(target=8.0)
        score = QualityScore(
            completeness=9.0, correctness=9.0, clarity=9.0,
            confidence=9.0, coherence=9.0,
        )
        result = scorer.validate(score)
        assert result["passed"]

    def test_validate_failed(self):
        scorer = QualityScorer(target=9.5)
        score = QualityScore(
            completeness=7.0, correctness=7.0, clarity=7.0,
            confidence=7.0, coherence=7.0,
        )
        result = scorer.validate(score)
        assert not result["passed"]

    def test_grade_s(self):
        score = QualityScore(
            completeness=10.0, correctness=10.0, clarity=10.0,
            confidence=10.0, coherence=10.0,
        )
        assert score.grade == "S"

    def test_grade_c(self):
        score = QualityScore(
            completeness=5.0, correctness=5.0, clarity=5.0,
            confidence=5.0, coherence=5.0,
        )
        assert score.grade == "C"


# ─── Architect Engine Tests ──────────────────────────────────────────────────

class TestArchitectEngine:
    """Tests for the pipeline architect engine."""

    def test_architect_basic(self):
        architect = PipelineArchitect(quality_target=8.0)
        concept = ArchitectConcept(
            name="test-pipeline",
            purpose="Test pipeline",
            domain="engineering",
            complexity=5,
        )
        result = architect.architect(concept)
        assert result.concept.name == "test-pipeline"
        assert result.pipeline["name"] == "test-pipeline"
        assert len(result.pipeline["phases"]) > 0

    def test_architect_with_skills(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(
            name="skilled-pipeline",
            purpose="Pipeline with skills",
            required_skills=["semgrep", "data-analytics"],
        )
        result = architect.architect(concept)
        assert "requested" in result.skill_map
        assert "semgrep" in result.skill_map["requested"]

    def test_architect_with_connectors(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(
            name="connected-pipeline",
            purpose="Pipeline with connectors",
            required_connectors=["github", "notion"],
        )
        result = architect.architect(concept)
        assert "github" in result.connector_map
        assert "notion" in result.connector_map

    def test_architect_high_complexity(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(
            name="complex-pipeline",
            purpose="Complex pipeline",
            complexity=9,
        )
        result = architect.architect(concept)
        assert len(result.thinking_chains) > 0

    def test_architect_output_yaml(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(name="yaml-test", purpose="Test")
        result = architect.architect(concept)
        yaml_output = result.to_yaml()
        assert "name: yaml-test" in yaml_output
        assert "phases:" in yaml_output

    def test_architect_output_markdown(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(name="md-test", purpose="Test")
        result = architect.architect(concept)
        md_output = result.to_markdown()
        assert "# Pipeline Architect Report" in md_output
        assert "md-test" in md_output

    def test_architect_output_json(self):
        architect = PipelineArchitect()
        concept = ArchitectConcept(name="json-test", purpose="Test")
        result = architect.architect(concept)
        json_output = json.dumps(result.to_dict())
        assert "json-test" in json_output
        assert "quality_score" in json_output


# ─── Registry Tests ──────────────────────────────────────────────────────────

class TestRegistries:
    """Tests for skill and connector registries."""

    def test_skill_categories_exist(self):
        assert "engineering" in SKILL_CATEGORIES
        assert "research" in SKILL_CATEGORIES
        assert "security" in SKILL_CATEGORIES

    def test_skill_structure(self):
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                assert "name" in skill
                assert "purpose" in skill
                assert "integration" in skill

    def test_connectors_exist(self):
        assert "github" in CONNECTORS
        assert "notion" in CONNECTORS
        assert "supabase" in CONNECTORS

    def test_connector_structure(self):
        for name, connector in CONNECTORS.items():
            assert "type" in connector
            assert "purpose" in connector
            assert "auth" in connector


# ─── Integration Tests ───────────────────────────────────────────────────────

class TestIntegration:
    """Integration tests for full pipeline creation."""

    def test_full_pipeline_creation(self):
        """Test complete pipeline creation flow."""
        architect = PipelineArchitect(quality_target=8.5)
        concept = ArchitectConcept(
            name="full-test",
            purpose="Full integration test",
            domain="engineering",
            complexity=8,
            required_skills=["helix-pro-code", "quality-gate"],
            required_connectors=["github"],
        )
        result = architect.architect(concept)

        # Verify all components
        assert result.pipeline["name"] == "full-test"
        assert len(result.pipeline["phases"]) >= 7
        assert len(result.thinking_chains) > 0
        assert "engineering" in result.skill_map
        assert "github" in result.connector_map
        assert result.quality_score.total > 0

        # Verify outputs
        json_out = json.dumps(result.to_dict())
        yaml_out = result.to_yaml()
        md_out = result.to_markdown()
        assert len(json_out) > 100
        assert len(yaml_out) > 100
        assert len(md_out) > 100

    def test_domain_research(self):
        """Test research domain pipeline."""
        architect = PipelineArchitect()
        concept = ArchitectConcept(
            name="research-test",
            purpose="Research pipeline",
            domain="research",
            complexity=6,
        )
        result = architect.architect(concept)
        assert "research" in result.skill_map

    def test_domain_security(self):
        """Test security domain pipeline."""
        architect = PipelineArchitect()
        concept = ArchitectConcept(
            name="security-test",
            purpose="Security pipeline",
            domain="security",
            complexity=9,
        )
        result = architect.architect(concept)
        assert "security" in result.skill_map


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
