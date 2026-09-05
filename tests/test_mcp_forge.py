"""
MCP Forge — Test Suite
Tests for the durable remote MCP server creation pipeline.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from mcp_forge import (
    MCPConcept,
    MCPSchema,
    MCPForge,
    MCPServerResult,
    MCPSchemaBuilder,
    MCPValidator,
    MCP_SERVER_TYPES,
)


# ─── MCPConcept Tests ────────────────────────────────────────────────────────

class TestMCPConcept:
    """Tests for MCP concept dataclass."""

    def test_create_concept(self):
        concept = MCPConcept(
            name="test-server",
            purpose="Test MCP server",
            server_type="api",
        )
        assert concept.name == "test-server"
        assert concept.purpose == "Test MCP server"
        assert concept.server_type == "api"

    def test_concept_with_tools(self):
        concept = MCPConcept(
            name="test",
            purpose="Test",
            tools=["custom1", "custom2"],
        )
        assert len(concept.tools) == 2

    def test_concept_defaults(self):
        concept = MCPConcept(name="t", purpose="p")
        assert concept.auth_required is True
        assert concept.persistence_required is True
        assert concept.monitoring_required is True
        assert concept.complexity == 5


# ─── MCPSchemaBuilder Tests ──────────────────────────────────────────────────

class TestMCPSchemaBuilder:
    """Tests for MCP schema builder."""

    def test_build_tool(self):
        builder = MCPSchemaBuilder()
        tool = builder.build_tool("test_tool", "A test tool")
        assert tool.name == "test_tool"
        assert tool.description == "A test tool"
        assert tool.input_schema["type"] == "object"

    def test_build_resource(self):
        builder = MCPSchemaBuilder()
        resource = builder.build_resource("test_res", "/test", "A test resource")
        assert resource.name == "test_res"
        assert resource.uri == "/test"

    def test_build_prompt(self):
        builder = MCPSchemaBuilder()
        prompt = builder.build_prompt("test_prompt", "A test prompt")
        assert prompt.name == "test_prompt"
        assert prompt.description == "A test prompt"

    def test_build_api_tools(self):
        builder = MCPSchemaBuilder()
        tools = builder.build_api_tools()
        assert len(tools) == 4
        names = [t.name for t in tools]
        assert "fetch" in names
        assert "post" in names

    def test_build_database_tools(self):
        builder = MCPSchemaBuilder()
        tools = builder.build_database_tools()
        assert len(tools) == 4
        names = [t.name for t in tools]
        assert "query" in names
        assert "list_tables" in names

    def test_build_filesystem_tools(self):
        builder = MCPSchemaBuilder()
        tools = builder.build_filesystem_tools()
        assert len(tools) == 6
        names = [t.name for t in tools]
        assert "read" in names
        assert "write" in names


# ─── MCPValidator Tests ──────────────────────────────────────────────────────

class TestMCPValidator:
    """Tests for MCP validator."""

    def test_validate_valid_server(self, tmp_path):
        server_path = tmp_path / "valid-server"
        server_path.mkdir()
        (server_path / "server.py").write_text(
            "from mcp.server import Server\n"
            "async def list_tools(): pass\n"
            "async def call_tool(): pass\n"
            "async def list_resources(): pass\n"
        )
        (server_path / "requirements.txt").write_text("mcp>=1.0.0")
        tests_dir = server_path / "tests"
        tests_dir.mkdir()

        validator = MCPValidator()
        result = validator.validate_structure(server_path)
        assert result["valid"] is True

    def test_validate_missing_server(self, tmp_path):
        server_path = tmp_path / "incomplete"
        server_path.mkdir()

        validator = MCPValidator()
        result = validator.validate_structure(server_path)
        assert result["valid"] is False
        assert any("server.py" in i for i in result["issues"])

    def test_validate_protocol(self, tmp_path):
        server_path = tmp_path / "protocol-server"
        server_path.mkdir()
        (server_path / "server.py").write_text(
            "from mcp.server import Server\n"
            "async def list_tools(): pass\n"
            "async def call_tool(): pass\n"
            "async def list_resources(): pass\n"
        )

        validator = MCPValidator()
        result = validator.validate_protocol(server_path)
        assert result["valid"] is True

    def test_validate_all(self, tmp_path):
        server_path = tmp_path / "full-server"
        server_path.mkdir()
        (server_path / "server.py").write_text(
            "from mcp.server import Server\n"
            "async def list_tools(): pass\n"
            "async def call_tool(): pass\n"
            "async def list_resources(): pass\n"
        )
        (server_path / "requirements.txt").write_text("mcp>=1.0.0")
        (server_path / "tests").mkdir()

        validator = MCPValidator()
        result = validator.validate_all(server_path)
        assert result["valid"] is True
        assert result["total_issues"] == 0


# ─── MCPForge Tests ──────────────────────────────────────────────────────────

class TestMCPForge:
    """Tests for MCP forge pipeline."""

    def test_forge_api_server(self, tmp_path):
        concept = MCPConcept(
            name="api-server",
            purpose="Test API server",
            server_type="api",
        )
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert result.concept.name == "api-server"
        assert result.server_path.exists()
        assert (result.server_path / "server.py").exists()
        assert result.tools_implemented == 4

    def test_forge_database_server(self, tmp_path):
        concept = MCPConcept(
            name="db-server",
            purpose="Test DB server",
            server_type="database",
        )
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert result.server_path.exists()
        assert result.tools_implemented == 4

    def test_forge_filesystem_server(self, tmp_path):
        concept = MCPConcept(
            name="fs-server",
            purpose="Test FS server",
            server_type="filesystem",
        )
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert result.server_path.exists()
        assert result.tools_implemented == 6

    def test_forge_with_custom_tools(self, tmp_path):
        concept = MCPConcept(
            name="custom-server",
            purpose="Test custom server",
            server_type="api",
            tools=["custom_tool1", "custom_tool2"],
        )
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert result.tools_implemented == 6  # 4 standard + 2 custom

    def test_forge_creates_deploy_script(self, tmp_path):
        concept = MCPConcept(name="deploy-test", purpose="Test deploy")
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert (result.server_path / "deploy.sh").exists()

    def test_forge_creates_monitor_config(self, tmp_path):
        concept = MCPConcept(name="monitor-test", purpose="Test monitor")
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        assert (result.server_path / "monitor.json").exists()

    def test_forge_result_dict(self, tmp_path):
        concept = MCPConcept(name="dict-test", purpose="Dict test")
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        d = result.to_dict()
        assert d["name"] == "dict-test"
        assert "quality_score" in d
        assert "tools_implemented" in d

    def test_forge_result_markdown(self, tmp_path):
        concept = MCPConcept(name="md-test", purpose="Markdown test")
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        md = result.to_markdown()
        assert "# MCP Forge Result" in md
        assert "md-test" in md

    def test_forge_all_types(self, tmp_path):
        for server_type in MCP_SERVER_TYPES:
            concept = MCPConcept(
                name=f"{server_type}-server",
                purpose=f"Test {server_type} server",
                server_type=server_type,
            )
            forge = MCPForge()
            result = forge.forge(concept, tmp_path)
            assert result.server_path.exists()

    def test_validate_existing(self, tmp_path):
        concept = MCPConcept(name="validate-me", purpose="Validate test")
        forge = MCPForge()
        result = forge.forge(concept, tmp_path)

        validation = forge.validate_existing(result.server_path)
        assert validation["valid"] is True


# ─── Integration Tests ───────────────────────────────────────────────────────

class TestIntegration:
    """Integration tests for full MCP server creation flow."""

    def test_full_development_cycle(self, tmp_path):
        """Test complete MCP server development from concept to deployed."""
        concept = MCPConcept(
            name="full-cycle-mcp",
            purpose="Full cycle MCP test",
            server_type="api",
            tools=["custom_tool"],
            auth_required=True,
            persistence_required=True,
            monitoring_required=True,
        )
        forge = MCPForge(quality_target=9.0)
        result = forge.forge(concept, tmp_path)

        # Verify all components exist
        assert (result.server_path / "server.py").exists()
        assert (result.server_path / "requirements.txt").exists()
        assert (result.server_path / "Dockerfile").exists()
        assert (result.server_path / "config.json").exists()
        assert (result.server_path / "tests").exists()
        assert (result.server_path / "deploy.sh").exists()
        assert (result.server_path / "monitor.json").exists()

        # Verify content
        server_py = (result.server_path / "server.py").read_text()
        assert "full-cycle-mcp" in server_py
        assert "list_tools" in server_py
        assert "call_tool" in server_py

        # Verify validation
        validation = forge.validate_existing(result.server_path)
        assert validation["valid"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
