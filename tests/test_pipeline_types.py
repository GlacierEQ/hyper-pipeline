#!/usr/bin/env python3
"""
Tests for Pipeline Types.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from pipeline_types import (
    ResearchPipeline, MigrationPipeline, DocumentationPipeline, SecurityPipeline,
    PipelineType, PIPELINE_REGISTRY, get_pipeline, list_pipelines,
)


class TestResearchPipeline:
    def test_execute(self):
        pipeline = ResearchPipeline()
        result = pipeline.execute("AI safety")
        assert result.status == "passed"
        assert len(result.phases) == 5

    def test_execute_with_sources(self):
        pipeline = ResearchPipeline()
        result = pipeline.execute("AI safety", sources=["source1", "source2"])
        assert "2 sources" in result.evidence or "2" in result.phases[1]["evidence"]


class TestMigrationPipeline:
    def test_execute(self):
        pipeline = MigrationPipeline()
        result = pipeline.execute("Python 3.8", "Python 3.12")
        assert result.status == "passed"
        assert len(result.phases) == 5


class TestDocumentationPipeline:
    def test_execute(self):
        pipeline = DocumentationPipeline()
        result = pipeline.execute("/path/to/repo")
        assert result.status == "passed"
        assert len(result.phases) == 5


class TestSecurityPipeline:
    def test_execute(self):
        pipeline = SecurityPipeline()
        result = pipeline.execute("/path/to/repo")
        assert result.status == "passed"
        assert len(result.phases) == 5


class TestPipelineRegistry:
    def test_list_pipelines(self):
        pipelines = list_pipelines()
        assert len(pipelines) == 4

    def test_get_pipeline(self):
        for pt in PipelineType:
            pipeline = get_pipeline(pt)
            assert pipeline is not None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
