"""
Skill Forge — Test Suite
Tests for the complete skill development pipeline.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from skill_forge import (
    SkillConcept,
    SkillDesign,
    SkillForge,
    SkillResult,
    SkillStructureBuilder,
    SkillValidator,
    SKILL_DOMAINS,
)


# ─── SkillConcept Tests ──────────────────────────────────────────────────────

class TestSkillConcept:
    """Tests for skill concept dataclass."""

    def test_create_concept(self):
        concept = SkillConcept(
            name="test-skill",
            purpose="Test purpose",
            domain="engineering",
        )
        assert concept.name == "test-skill"
        assert concept.purpose == "Test purpose"
        assert concept.domain == "engineering"

    def test_concept_with_triggers(self):
        concept = SkillConcept(
            name="test",
            purpose="Test",
            triggers=["trigger1", "trigger2"],
        )
        assert len(concept.triggers) == 2

    def test_concept_defaults(self):
        concept = SkillConcept(name="t", purpose="p")
        assert concept.complexity == 5
        assert concept.quality_target == 9.0


# ─── SkillDesign Tests ───────────────────────────────────────────────────────

class TestSkillDesign:
    """Tests for skill design dataclass."""

    def test_create_design(self):
        concept = SkillConcept(name="test", purpose="Test")
        design = SkillDesign(concept=concept)
        assert design.concept.name == "test"
        assert len(design.phase_chain) == 0

    def test_design_with_phases(self):
        concept = SkillConcept(name="test", purpose="Test")
        design = SkillDesign(
            concept=concept,
            phase_chain=["orient", "build", "verify"],
        )
        assert len(design.phase_chain) == 3


# ─── SkillStructureBuilder Tests ─────────────────────────────────────────────

class TestSkillStructureBuilder:
    """Tests for skill structure builder."""

    def test_build_skill_md(self):
        concept = SkillConcept(
            name="test-skill",
            purpose="Test purpose",
            triggers=["test", "check"],
        )
        design = SkillDesign(concept=concept)
        builder = SkillStructureBuilder()
        comp = builder.build_skill_md(concept, design)

        assert comp.name == "SKILL.md"
        assert "test-skill" in comp.content
        assert "Test purpose" in comp.content
        assert comp.required is True

    def test_build_test_file(self):
        concept = SkillConcept(name="my-skill", purpose="Test")
        builder = SkillStructureBuilder()
        comp = builder.build_test_file(concept)

        assert comp.name == "test"
        assert "test_my_skill" in comp.path
        assert "import pytest" in comp.content
        assert comp.required is True

    def test_build_readme(self):
        concept = SkillConcept(name="my-skill", purpose="Test purpose")
        builder = SkillStructureBuilder()
        comp = builder.build_readme(concept)

        assert comp.name == "README.md"
        assert "My Skill" in comp.content
        assert "Test purpose" in comp.content
        assert comp.required is False

    def test_build_reference(self):
        concept = SkillConcept(name="my-skill", purpose="Test")
        builder = SkillStructureBuilder()
        comp = builder.build_reference(concept)

        assert comp.name == "reference"
        assert comp.path == "references/REFERENCE.md"
        assert comp.required is False

    def test_build_all(self):
        concept = SkillConcept(name="test", purpose="Test")
        design = SkillDesign(concept=concept)
        builder = SkillStructureBuilder()
        components = builder.build_all(concept, design)

        assert len(components) == 4
        names = [c.name for c in components]
        assert "SKILL.md" in names
        assert "test" in names


# ─── SkillValidator Tests ────────────────────────────────────────────────────

class TestSkillValidator:
    """Tests for skill validator."""

    def test_validate_valid_skill(self, tmp_path):
        skill_path = tmp_path / "valid-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text(
            "---\nname: test\ndescription: Test skill purpose\n---\n\n# Purpose\n\nTest purpose with enough content to pass validation checks and ensure quality standards."
        )
        tests_dir = skill_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_pass(): assert True")

        validator = SkillValidator()
        result = validator.validate_structure(skill_path)
        assert result["valid"] is True

    def test_validate_missing_skill_md(self, tmp_path):
        skill_path = tmp_path / "incomplete-skill"
        skill_path.mkdir()

        validator = SkillValidator()
        result = validator.validate_structure(skill_path)
        assert result["valid"] is False
        assert any("SKILL.md" in i for i in result["issues"])

    def test_validate_missing_tests(self, tmp_path):
        skill_path = tmp_path / "no-tests-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("---\nname: test\n---\n\n# Purpose\n\nTest.")

        validator = SkillValidator()
        result = validator.validate_structure(skill_path)
        assert result["valid"] is False
        assert any("tests" in i for i in result["issues"])

    def test_validate_content_quality(self, tmp_path):
        skill_path = tmp_path / "quality-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text(
            "---\nname: test\n---\n\n# Purpose\n\nTest purpose.\n\n# Quality\n\nTarget: 9.0\n\n# Output\n\nExample output."
        )

        validator = SkillValidator()
        result = validator.validate_content(skill_path)
        assert result["score"] >= 8.0

    def test_validate_all(self, tmp_path):
        skill_path = tmp_path / "full-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text(
            "---\nname: test\ndescription: Test skill purpose\n---\n\n# Purpose\n\nTest purpose with enough content.\n\n# Quality\n\nTarget: 9.0.\n\n# Output\n\nExample."
        )
        tests_dir = skill_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_pass(): assert True")

        validator = SkillValidator()
        result = validator.validate_all(skill_path)
        assert result["valid"] is True
        assert result["total_issues"] == 0


# ─── SkillForge Tests ────────────────────────────────────────────────────────

class TestSkillForge:
    """Tests for skill forge pipeline."""

    def test_forge_creates_skill(self, tmp_path):
        concept = SkillConcept(
            name="forge-test",
            purpose="Test forging",
            domain="engineering",
        )
        forge = SkillForge()
        result = forge.forge(concept, tmp_path)

        assert result.concept.name == "forge-test"
        assert result.skill_path.exists()
        assert (result.skill_path / "SKILL.md").exists()

    def test_forge_with_complexity(self, tmp_path):
        concept = SkillConcept(
            name="complex-test",
            purpose="Complex test",
            complexity=8,
        )
        forge = SkillForge()
        result = forge.forge(concept, tmp_path)

        assert result.validation_passed is True
        assert len(result.design.thinking_chain) > 0

    def test_forge_result_dict(self, tmp_path):
        concept = SkillConcept(name="dict-test", purpose="Dict test")
        forge = SkillForge()
        result = forge.forge(concept, tmp_path)

        d = result.to_dict()
        assert d["name"] == "dict-test"
        assert "quality_score" in d
        assert "components_built" in d

    def test_forge_result_markdown(self, tmp_path):
        concept = SkillConcept(name="md-test", purpose="Markdown test")
        forge = SkillForge()
        result = forge.forge(concept, tmp_path)

        md = result.to_markdown()
        assert "# Skill Forge Result" in md
        assert "md-test" in md

    def test_forge_all_domains(self, tmp_path):
        for domain in SKILL_DOMAINS:
            concept = SkillConcept(
                name=f"{domain}-skill",
                purpose=f"Test {domain} skill",
                domain=domain,
            )
            forge = SkillForge()
            result = forge.forge(concept, tmp_path)
            assert result.skill_path.exists()

    def test_validate_existing(self, tmp_path):
        concept = SkillConcept(name="validate-me", purpose="Validate test")
        forge = SkillForge()
        result = forge.forge(concept, tmp_path)

        validation = forge.validate_existing(result.skill_path)
        assert validation["valid"] is True


# ─── Integration Tests ───────────────────────────────────────────────────────

class TestIntegration:
    """Integration tests for full skill development flow."""

    def test_full_development_cycle(self, tmp_path):
        """Test complete skill development from concept to published."""
        # Create
        concept = SkillConcept(
            name="full-cycle",
            purpose="Full cycle test",
            domain="engineering",
            triggers=["test", "check", "verify"],
            tools=["pytest"],
            complexity=7,
        )
        forge = SkillForge(quality_target=9.0)
        result = forge.forge(concept, tmp_path)

        # Verify all components exist
        assert (result.skill_path / "SKILL.md").exists()
        assert (result.skill_path / "tests").exists()
        assert (result.skill_path / "README.md").exists()
        assert (result.skill_path / "references").exists()

        # Verify content
        skill_md = (result.skill_path / "SKILL.md").read_text()
        assert "full-cycle" in skill_md
        assert "Full cycle test" in skill_md

        # Verify validation
        validation = forge.validate_existing(result.skill_path)
        assert validation["valid"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
