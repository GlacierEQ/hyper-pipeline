#!/usr/bin/env python3
"""
Tests for Session Renamer.
"""

import json
import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from session_renamer import SessionRenamer, BatchRenamer, SessionName


class TestSessionRenamer:
    def test_generate_basic(self):
        renamer = SessionRenamer()
        result = renamer.generate("working on MCP forge")
        assert result.name != ""
        assert result.confidence > 0

    def test_generate_with_action(self):
        renamer = SessionRenamer()
        result = renamer.generate("building test suite for hyper-pipeline")
        assert "build" in result.name or "test" in result.name

    def test_generate_with_domain(self):
        renamer = SessionRenamer()
        result = renamer.generate("creating MCP server tools")
        assert "mcp" in result.name

    def test_tags_extracted(self):
        renamer = SessionRenamer()
        result = renamer.generate("deploying to docker and kubernetes")
        assert "deploy" in result.tags or "docker" in result.tags

    def test_confidence_score(self):
        renamer = SessionRenamer()
        result = renamer.generate("a")
        assert result.confidence < 0.5

        result2 = renamer.generate("building MCP server tools for deployment")
        assert result2.confidence > 0.5

    def test_clean_name(self):
        renamer = SessionRenamer()
        result = renamer.generate("Build  MCP   Server!!!")
        assert " " not in result.name
        assert "!" not in result.name

    def test_history_tracked(self):
        renamer = SessionRenamer()
        renamer.generate("first session")
        renamer.generate("second session")
        assert len(renamer.history) == 2


class TestBatchRenamer:
    def test_rename_batch(self):
        batch = BatchRenamer()
        sessions = [
            {"name": "new session", "context": "building test suite"},
            {"name": "new session", "context": "deploying to docker"},
        ]
        results = batch.rename_batch(sessions)
        assert len(results) == 2
        assert results[0].name != results[1].name

    def test_rename_from_file(self, tmp_path):
        data = {"sessions": [
            {"context": "MCP server implementation"},
            {"context": "CI/CD pipeline setup"},
        ]}
        filepath = tmp_path / "sessions.json"
        filepath.write_text(json.dumps(data))

        batch = BatchRenamer()
        results = batch.rename_from_file(filepath)
        assert len(results) == 2


class TestSessionName:
    def test_to_dict(self):
        name = SessionName(
            name="build-mcp",
            description="Building MCP server",
            confidence=0.8,
            tags=["mcp", "build"],
            timestamp="2026-09-05 12:00",
        )
        d = name.to_dict()
        assert d["name"] == "build-mcp"
        assert d["confidence"] == 0.8
        assert len(d["tags"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
