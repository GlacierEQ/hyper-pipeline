#!/usr/bin/env python3
"""
Tests for Test Forge, Doc Forge, and Deploy Forge.
"""

import json
import sys
import tempfile
import pytest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from test_forge import TestForge, CodeScanner, TestGenerator, TestValidator
from doc_forge import DocForge, DocLayer, CodeAnalyzer, DocGenerator
from deploy_forge import DeployForge, ProjectAnalyzer, ConfigGenerator, ConfigValidator, PLATFORMS


# ─── Test Forge Tests ────────────────────────────────────────────────────────

class TestCodeScanner:
    def test_scan_python_module(self, tmp_path):
        """Test scanning a Python module."""
        module = tmp_path / "mymodule.py"
        module.write_text('"""My module."""\ndef hello(): return "world"')

        scanner = CodeScanner()
        result = scanner.scan_module(module)

        assert result is not None
        assert result.name == "mymodule"
        assert len(result.functions) == 1
        assert result.functions[0]["name"] == "hello"

    def test_scan_directory(self, tmp_path):
        """Test scanning a directory."""
        (tmp_path / "a.py").write_text("def a(): pass")
        (tmp_path / "b.py").write_text("def b(): pass")
        (tmp_path / "test_c.py").write_text("def c(): pass")  # Should skip

        scanner = CodeScanner()
        results = scanner.scan_directory(tmp_path)

        assert len(results) == 2

    def test_scan_non_python(self, tmp_path):
        """Test scanning non-Python files returns None."""
        js = tmp_path / "app.js"
        js.write_text("function hello() {}")

        scanner = CodeScanner()
        result = scanner.scan_module(js)
        assert result is None


class TestTestGenerator:
    def test_generate_unit_tests(self, tmp_path):
        """Test unit test generation."""
        from test_forge import CodeModule

        module = CodeModule(
            path=tmp_path / "mymod.py",
            name="mymod",
            language="python",
            functions=[{"name": "add", "args": ["a", "b"], "decorators": [], "is_async": False, "line": 1}],
        )

        gen = TestGenerator()
        tests = gen.generate_unit_tests(module)

        assert "def test_add" in tests
        assert "assert" in tests

    def test_generate_property_tests(self, tmp_path):
        """Test property-based test generation."""
        from test_forge import CodeModule

        module = CodeModule(
            path=tmp_path / "mymod.py",
            name="mymod",
            language="python",
            functions=[{"name": "parse", "args": ["data"], "decorators": [], "is_async": False, "line": 1}],
        )

        gen = TestGenerator()
        tests = gen.generate_property_tests(module)

        assert "@given" in tests
        assert "st.integers()" in tests


class TestTestValidator:
    def test_validate_syntax(self):
        """Test syntax validation."""
        validator = TestValidator()
        valid, msg = validator.validate_syntax("def test_ok(): pass")
        assert valid

    def test_validate_invalid_syntax(self):
        """Test invalid syntax detection."""
        validator = TestValidator()
        valid, msg = validator.validate_syntax("def test_ok(: pass")
        assert not valid

    def test_validate_structure(self):
        """Test structure validation."""
        validator = TestValidator()
        valid, issues = validator.validate_structure("def test_ok(): assert True")
        assert valid
        assert len(issues) == 0


class TestTestForge:
    def test_forge_creates_test_files(self, tmp_path):
        """Test that forge creates test files."""
        # Create a simple module
        src = tmp_path / "src"
        src.mkdir()
        (src / "utils.py").write_text('"""Utilities."""\ndef add(a, b): return a + b')

        forge = TestForge()
        result = forge.forge(src, ["unit"], tmp_path / "tests_out")

        assert result.tests_generated > 0
        assert len(result.test_files) > 0

    def test_forge_result_dict(self, tmp_path):
        """Test result dict output."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "utils.py").write_text("def add(a, b): return a + b")

        forge = TestForge()
        result = forge.forge(src, ["unit"], tmp_path / "tests_out")

        d = result.to_dict()
        assert "modules_scanned" in d
        assert "tests_generated" in d

    def test_forge_result_markdown(self, tmp_path):
        """Test result markdown output."""
        src = tmp_path / "src"
        src.mkdir()
        (src / "utils.py").write_text("def add(a, b): return a + b")

        forge = TestForge()
        result = forge.forge(src, ["unit"], tmp_path / "tests_out")

        md = result.to_markdown()
        assert "# Test Forge Result" in md


# ─── Doc Forge Tests ─────────────────────────────────────────────────────────

class TestCodeAnalyzer:
    def test_analyze_module(self, tmp_path):
        """Test module analysis."""
        module = tmp_path / "mymod.py"
        module.write_text('"""My module."""\n\ndef hello():\n    """Say hello."""\n    return "world"')

        analyzer = CodeAnalyzer()
        elements = analyzer.analyze_module(module)

        # Filter out module-level docstring element
        func_elements = [e for e in elements if e.type == "function"]
        assert len(func_elements) >= 1
        assert any(e.name == "hello" for e in func_elements)

    def test_analyze_class(self, tmp_path):
        """Test class analysis."""
        module = tmp_path / "mymod.py"
        module.write_text('class MyClass:\n    """A class."""\n    def method(self): pass')

        analyzer = CodeAnalyzer()
        elements = analyzer.analyze_module(module)

        classes = [e for e in elements if e.type == "class"]
        assert len(classes) == 1
        assert classes[0].name == "MyClass"


class TestDocGenerator:
    def test_generate_human_layer(self):
        """Test human layer generation."""
        from doc_forge import CodeElement

        elements = [
            CodeElement(name="process", type="function", path=Path("x.py"), docstring="Process data."),
        ]

        gen = DocGenerator()
        doc = gen.generate_human_layer(elements, "MyProject")

        assert "MyProject" in doc
        assert "process" in doc

    def test_generate_expert_layer(self):
        """Test expert layer generation."""
        from doc_forge import CodeElement

        elements = [
            CodeElement(
                name="fetch",
                type="function",
                path=Path("x.py"),
                signature="fetch(url, timeout)",
                docstring="Fetch data from URL.",
                params=[{"name": "url", "type": "str", "description": "The URL"}],
                returns="Response",
            ),
        ]

        gen = DocGenerator()
        doc = gen.generate_expert_layer(elements, "MyProject")

        assert "fetch(url, timeout)" in doc
        assert "Parameters:" in doc

    def test_generate_machine_layer(self):
        """Test machine layer generation."""
        from doc_forge import CodeElement

        elements = [
            CodeElement(name="query", type="function", path=Path("x.py")),
        ]

        gen = DocGenerator()
        doc = gen.generate_machine_layer(elements, "MyProject")

        schema = json.loads(doc)
        assert schema["openapi"] == "3.0.0"
        assert "/query" in schema["paths"]

    def test_generate_mesh_layer(self):
        """Test mesh layer generation."""
        from doc_forge import CodeElement

        elements = [
            CodeElement(name="func_a", type="function", path=Path("x.py"), dependencies=["func_b"]),
            CodeElement(name="func_b", type="function", path=Path("x.py")),
        ]

        gen = DocGenerator()
        doc = gen.generate_mesh_layer(elements, "human", "expert", "machine")

        assert "func_a -> func_b" in doc
        assert "L1 (Human)" in doc


class TestDocForge:
    def test_forge_all_layers(self, tmp_path):
        """Test generating all layers."""
        (tmp_path / "utils.py").write_text('"""Utilities."""\ndef add(a, b): """Add two numbers.""" return a + b')

        forge = DocForge()
        result = forge.forge(tmp_path, output_dir=tmp_path / "docs")

        assert len(result.layers_generated) == 4
        assert len(result.output_files) == 4

    def test_forge_human_only(self, tmp_path):
        """Test generating human layer only."""
        (tmp_path / "utils.py").write_text("def add(a, b): return a + b")

        forge = DocForge()
        result = forge.forge(tmp_path, [DocLayer.HUMAN], output_dir=tmp_path / "docs")

        assert result.layers_generated == ["human"]
        assert len(result.output_files) == 1

    def test_forge_mesh_layer(self, tmp_path):
        """Test mesh layer links all elements."""
        (tmp_path / "core.py").write_text("def process(): pass\ndef validate(): pass")

        forge = DocForge()
        result = forge.forge(
            tmp_path,
            [DocLayer.MESH],
            output_dir=tmp_path / "docs",
        )

        mesh_file = result.output_files[0]
        content = mesh_file.read_text()
        assert "process" in content
        assert "validate" in content


# ─── Deploy Forge Tests ──────────────────────────────────────────────────────

class TestProjectAnalyzer:
    def test_analyze_python_project(self, tmp_path):
        """Test Python project detection."""
        (tmp_path / "requirements.txt").write_text("flask==3.0.0\npytest==8.0.0")
        (tmp_path / "tests").mkdir()

        analyzer = ProjectAnalyzer()
        info = analyzer.analyze(tmp_path)

        assert info.language == "python"
        assert "flask" in info.dependencies

    def test_analyze_javascript_project(self, tmp_path):
        """Test JavaScript project detection."""
        pkg = {"name": "my-app", "dependencies": {"next": "14.0.0"}, "scripts": {"dev": "next dev"}}
        (tmp_path / "package.json").write_text(json.dumps(pkg))
        (tmp_path / "next.config.js").write_text("module.exports = {}")

        analyzer = ProjectAnalyzer()
        info = analyzer.analyze(tmp_path)

        assert info.language == "javascript"
        assert info.framework == "nextjs"


class TestConfigGenerator:
    def test_generate_github_actions(self):
        """Test GitHub Actions generation."""
        from deploy_forge import ProjectInfo

        info = ProjectInfo(name="test", language="python", framework="fastapi")
        gen = ConfigGenerator()
        configs = gen.generate_github_actions(info)

        assert ".github/workflows/ci.yml" in configs
        assert "pytest" in configs[".github/workflows/ci.yml"]

    def test_generate_docker(self):
        """Test Docker generation."""
        from deploy_forge import ProjectInfo

        info = ProjectInfo(name="test", language="python", framework="fastapi")
        gen = ConfigGenerator()
        configs = gen.generate_docker(info)

        assert "Dockerfile" in configs
        assert "FROM python:" in configs["Dockerfile"]
        assert "docker-compose.yml" in configs


class TestConfigValidator:
    def test_validate_valid_yaml(self):
        """Test valid YAML validation."""
        validator = ConfigValidator()
        valid, issues = validator.validate({"test.yml": "name: test\nversion: 1"})
        assert valid

    def test_validate_valid_json(self):
        """Test valid JSON validation."""
        validator = ConfigValidator()
        valid, issues = validator.validate({"test.json": '{"key": "value"}'})
        assert valid


class TestDeployForge:
    def test_forge_github(self, tmp_path):
        """Test GitHub deployment generation."""
        (tmp_path / "requirements.txt").write_text("flask")

        forge = DeployForge()
        result = forge.forge(tmp_path, ["github"], tmp_path / "deploy")

        assert "github" in result.platforms
        assert result.configs_generated == 1
        assert len(result.files_created) == 2

    def test_forge_docker(self, tmp_path):
        """Test Docker deployment generation."""
        (tmp_path / "requirements.txt").write_text("flask")

        forge = DeployForge()
        result = forge.forge(tmp_path, ["docker"], tmp_path / "deploy")

        assert "docker" in result.platforms
        assert result.validated

    def test_forge_multiple_platforms(self, tmp_path):
        """Test multiple platform generation."""
        (tmp_path / "requirements.txt").write_text("flask")

        forge = DeployForge()
        result = forge.forge(tmp_path, ["github", "docker"], tmp_path / "deploy")

        assert len(result.platforms) == 2
        assert result.configs_generated == 2

    def test_forge_result_dict(self, tmp_path):
        """Test result dict output."""
        (tmp_path / "requirements.txt").write_text("flask")

        forge = DeployForge()
        result = forge.forge(tmp_path, ["github"], tmp_path / "deploy")

        d = result.to_dict()
        assert "platforms" in d
        assert "files" in d


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
