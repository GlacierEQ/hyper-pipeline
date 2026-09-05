#!/usr/bin/env python3
"""
Doc Forge — 4-Layer Documentation System
Generates comprehensive documentation for humans, experts, machines, and the mesh.

Layers:
  L1: HUMAN    — What and why (normal people)
  L2: EXPERT   — Technical why and how (masters of the trade)
  L3: MACHINE  — API specs, schemas, configs (for machines)
  L4: MESH     — Linking all to all (the connective tissue)

Pipeline:
  SCAN → ANALYZE → GENERATE → LINK → PUBLISH

Usage:
    python3 doc_forge.py --target /path/to/project
    python3 doc_forge.py --target /path/to/project --layers all
    python3 doc_forge.py --target /path/to/project --layers human,expert
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


VERSION = "1.0.0"


# ─── Data Models ─────────────────────────────────────────────────────────────

class DocLayer(Enum):
    HUMAN = "human"        # L1: What and why
    EXPERT = "expert"      # L2: Technical why and how
    MACHINE = "machine"    # L3: API specs, schemas
    MESH = "mesh"          # L4: Linking all to all


@dataclass
class CodeElement:
    """A code element to document."""
    name: str
    type: str  # function, class, method, module
    path: Path
    signature: str = ""
    docstring: str = ""
    params: List[Dict[str, str]] = field(default_factory=list)
    returns: str = ""
    raises: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    line: int = 0


@dataclass
class DocSection:
    """A documentation section."""
    layer: DocLayer
    title: str
    content: str
    elements: List[CodeElement] = field(default_factory=list)


@dataclass
class DocForgeResult:
    """Result of documentation generation."""
    target_path: Path
    layers_generated: List[str] = field(default_factory=list)
    elements_documented: int = 0
    links_created: int = 0
    output_files: List[Path] = field(default_factory=list)
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": str(self.target_path),
            "layers": self.layers_generated,
            "elements": self.elements_documented,
            "links": self.links_created,
            "files": [str(f) for f in self.output_files],
            "duration_ms": round(self.duration_ms, 1),
        }

    def to_markdown(self) -> str:
        lines = [
            "# Doc Forge Result",
            "",
            "## Summary",
            f"- **Layers:** {', '.join(self.layers_generated)}",
            f"- **Elements Documented:** {self.elements_documented}",
            f"- **Links Created:** {self.links_created}",
            f"- **Output Files:** {len(self.output_files)}",
            "",
            "## Generated Files",
        ]
        for f in self.output_files:
            lines.append(f"  ✓ {f.name}")
        return "\n".join(lines)


# ─── Code Analyzer ───────────────────────────────────────────────────────────

class CodeAnalyzer:
    """Analyzes code and extracts documentation-relevant info."""

    def analyze_module(self, path: Path) -> List[CodeElement]:
        """Analyze a Python module."""
        elements = []

        try:
            content = path.read_text(encoding="utf-8")
            tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError):
            return elements

        # Module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            elements.append(CodeElement(
                name=path.stem,
                type="module",
                path=path,
                docstring=module_doc,
            ))

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                elem = self._analyze_function(node, path)
                if elem:
                    elements.append(elem)

            elif isinstance(node, ast.ClassDef):
                elem = self._analyze_class(node, path)
                if elem:
                    elements.append(elem)

        return elements

    def _analyze_function(self, node: ast.FunctionDef, path: Path) -> Optional[CodeElement]:
        """Analyze a function."""
        if node.name.startswith("_") and not node.name.startswith("__"):
            return None

        # Get signature
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        signature = f"{node.name}({', '.join(args)})"

        # Get docstring
        docstring = ast.get_docstring(node) or ""

        # Parse docstring for params/returns
        params = self._parse_params(docstring)
        returns = self._parse_returns(docstring)
        raises = self._parse_raises(docstring)

        return CodeElement(
            name=node.name,
            type="function",
            path=path,
            signature=signature,
            docstring=docstring,
            params=params,
            returns=returns,
            raises=raises,
            line=node.lineno,
        )

    def _analyze_class(self, node: ast.ClassDef, path: Path) -> Optional[CodeElement]:
        """Analyze a class."""
        docstring = ast.get_docstring(node) or ""

        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)

        return CodeElement(
            name=node.name,
            type="class",
            path=path,
            docstring=docstring,
            dependencies=[self._get_name(b) for b in node.bases],
            line=node.lineno,
        )

    def _parse_params(self, docstring: str) -> List[Dict[str, str]]:
        """Parse parameters from docstring."""
        params = []
        lines = docstring.split("\n")
        in_params = False

        for line in lines:
            if "Args:" in line or "Parameters:" in line:
                in_params = True
                continue
            if in_params:
                if line.strip() and ":" in line:
                    parts = line.split(":", 1)
                    params.append({
                        "name": parts[0].strip(),
                        "type": "",
                        "description": parts[1].strip(),
                    })
                elif line.strip() and not line.startswith(" "):
                    in_params = False

        return params

    def _parse_returns(self, docstring: str) -> str:
        """Parse return value from docstring."""
        lines = docstring.split("\n")
        in_returns = False

        for line in lines:
            if "Returns:" in line:
                in_returns = True
                continue
            if in_returns and line.strip():
                return line.strip()

        return ""

    def _parse_raises(self, docstring: str) -> List[str]:
        """Parse exceptions from docstring."""
        raises = []
        lines = docstring.split("\n")
        in_raises = False

        for line in lines:
            if "Raises:" in line:
                in_raises = True
                continue
            if in_raises and line.strip():
                if ":" in line:
                    exc = line.split(":")[0].strip()
                    raises.append(exc)

        return raises

    def _get_name(self, node: ast.expr) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return "unknown"


# ─── Doc Generator ───────────────────────────────────────────────────────────

class DocGenerator:
    """Generates documentation for each layer."""

    def generate_human_layer(self, elements: List[CodeElement], project_name: str) -> str:
        """L1: What and why — for normal people."""
        lines = [
            f"# {project_name}",
            "",
            "## What is this?",
            "",
            f"This project provides {self._summarize_purpose(elements)}.",
            "",
            "## Why does it exist?",
            "",
            self._explain_value(elements),
            "",
            "## How do I use it?",
            "",
        ]

        # Simple usage examples
        for elem in elements:
            if elem.type == "function" and not elem.name.startswith("_"):
                lines.append(f"### {elem.name}")
                lines.append("")
                if elem.docstring:
                    lines.append(elem.docstring.split("\n")[0])
                else:
                    lines.append(f"Use `{elem.name}` to {elem.name.replace('_', ' ')}.")
                lines.append("")

        return "\n".join(lines)

    def generate_expert_layer(self, elements: List[CodeElement], project_name: str) -> str:
        """L2: Technical why and how — for masters of the trade."""
        lines = [
            f"# {project_name} — Technical Documentation",
            "",
            "## Architecture",
            "",
            self._describe_architecture(elements),
            "",
            "## API Reference",
            "",
        ]

        for elem in elements:
            if elem.type in ("function", "class"):
                lines.append(f"### `{elem.signature}`" if elem.signature else f"### `{elem.name}`")
                lines.append("")

                if elem.docstring:
                    lines.append(elem.docstring)
                    lines.append("")

                if elem.params:
                    lines.append("**Parameters:**")
                    lines.append("")
                    for param in elem.params:
                        lines.append(f"- `{param['name']}`: {param['description']}")
                    lines.append("")

                if elem.returns:
                    lines.append(f"**Returns:** {elem.returns}")
                    lines.append("")

                if elem.raises:
                    lines.append("**Raises:**")
                    lines.append("")
                    for exc in elem.raises:
                        lines.append(f"- `{exc}`")
                    lines.append("")

        return "\n".join(lines)

    def generate_machine_layer(self, elements: List[CodeElement], project_name: str) -> str:
        """L3: API specs, schemas — for machines."""
        schema = {
            "openapi": "3.0.0",
            "info": {
                "title": project_name,
                "version": "1.0.0",
            },
            "paths": {},
            "components": {
                "schemas": {},
            },
        }

        for elem in elements:
            if elem.type == "function":
                path = f"/{elem.name}"
                schema["paths"][path] = {
                    "post": {
                        "operationId": elem.name,
                        "summary": elem.docstring.split("\n")[0] if elem.docstring else elem.name,
                        "parameters": [
                            {
                                "name": p["name"],
                                "in": "query",
                                "schema": {"type": "string"},
                            }
                            for p in elem.params
                        ],
                        "responses": {
                            "200": {
                                "description": "Success",
                            }
                        },
                    }
                }

            elif elem.type == "class":
                schema["components"]["schemas"][elem.name] = {
                    "type": "object",
                    "properties": {},
                }

        return json.dumps(schema, indent=2)

    def generate_mesh_layer(
        self, elements: List[CodeElement], human_doc: str, expert_doc: str, machine_doc: str
    ) -> str:
        """L4: Linking all to all — the connective tissue."""
        lines = [
            "# Documentation Mesh",
            "",
            "## Cross-References",
            "",
            "This document links all documentation layers together.",
            "",
            "## Element Index",
            "",
            "| Element | Type | Human | Expert | Machine |",
            "|---------|------|-------|--------|---------|",
        ]

        for elem in elements:
            human_link = f"[What/Why](#human-{elem.name})"
            expert_link = f"[Technical](#expert-{elem.name})"
            machine_link = f"[Schema](#machine-{elem.name})"
            lines.append(
                f"| `{elem.name}` | {elem.type} | {human_link} | {expert_link} | {machine_link} |"
            )

        lines.extend([
            "",
            "## Dependency Graph",
            "",
            "```",
        ])

        # Build dependency graph
        for elem in elements:
            if elem.dependencies:
                for dep in elem.dependencies:
                    lines.append(f"{elem.name} -> {dep}")

        lines.extend([
            "```",
            "",
            "## Layer Connections",
            "",
            "- **L1 (Human)** explains *what* and *why*",
            "- **L2 (Expert)** explains *how* and *technical why*",
            "- **L3 (Machine)** provides *schemas* and *API specs*",
            "- **L4 (Mesh)** *links* everything together",
            "",
            "## Navigation",
            "",
            "- Start with L1 if you're new to the project",
            "- Jump to L2 if you need implementation details",
            "- Use L3 for API integration",
            "- Reference L4 to understand connections",
        ])

        return "\n".join(lines)

    def _summarize_purpose(self, elements: List[CodeElement]) -> str:
        """Summarize project purpose."""
        funcs = [e for e in elements if e.type == "function"]
        classes = [e for e in elements if e.type == "class"]

        parts = []
        if funcs:
            parts.append(f"{len(funcs)} functions")
        if classes:
            parts.append(f"{len(classes)} classes")

        return ", ".join(parts) if parts else "functionality"

    def _explain_value(self, elements: List[CodeElement]) -> str:
        """Explain project value."""
        docstrings = [e.docstring for e in elements if e.docstring]
        if docstrings:
            return docstrings[0].split("\n")[0]
        return "This project solves a specific problem in a clean, efficient way."

    def _describe_architecture(self, elements: List[CodeElement]) -> str:
        """Describe architecture."""
        modules = set(e.path.stem for e in elements)
        funcs = [e for e in elements if e.type == "function"]
        classes = [e for e in elements if e.type == "class"]

        lines = [
            f"**Modules:** {', '.join(modules)}",
            "",
            f"**Public Functions:** {len(funcs)}",
            "",
            f"**Classes:** {len(classes)}",
        ]
        return "\n".join(lines)


# ─── Doc Forge Pipeline ─────────────────────────────────────────────────────

class DocForge:
    """Complete documentation generation pipeline."""

    def __init__(self) -> None:
        self.analyzer = CodeAnalyzer()
        self.generator = DocGenerator()

    def _phase_scan(self, target: Path) -> List[CodeElement]:
        """Phase 1: Scan and analyze code."""
        elements = []
        for py_file in target.rglob("*.py"):
            if "__pycache__" in str(py_file) or py_file.name.startswith("."):
                continue
            elements.extend(self.analyzer.analyze_module(py_file))
        return elements

    def _phase_analyze(self, elements: List[CodeElement]) -> Dict[str, Any]:
        """Phase 2: Analyze codebase structure."""
        return {
            "total_elements": len(elements),
            "functions": len([e for e in elements if e.type == "function"]),
            "classes": len([e for e in elements if e.type == "class"]),
            "modules": len(set(e.path.stem for e in elements)),
        }

    def _phase_generate(
        self,
        elements: List[CodeElement],
        layers: List[DocLayer],
        project_name: str,
        output_dir: Path,
    ) -> List[Path]:
        """Phase 3: Generate documentation layers."""
        files = []

        human_doc = ""
        expert_doc = ""
        machine_doc = ""

        if DocLayer.HUMAN in layers:
            human_doc = self.generator.generate_human_layer(elements, project_name)
            human_path = output_dir / "L1_HUMAN.md"
            human_path.write_text(human_doc)
            files.append(human_path)

        if DocLayer.EXPERT in layers:
            expert_doc = self.generator.generate_expert_layer(elements, project_name)
            expert_path = output_dir / "L2_EXPERT.md"
            expert_path.write_text(expert_doc)
            files.append(expert_path)

        if DocLayer.MACHINE in layers:
            machine_doc = self.generator.generate_machine_layer(elements, project_name)
            machine_path = output_dir / "L3_MACHINE.json"
            machine_path.write_text(machine_doc)
            files.append(machine_path)

        if DocLayer.MESH in layers:
            mesh_doc = self.generator.generate_mesh_layer(elements, human_doc, expert_doc, machine_doc)
            mesh_path = output_dir / "L4_MESH.md"
            mesh_path.write_text(mesh_doc)
            files.append(mesh_path)

        return files

    def _phase_link(self, files: List[Path]) -> int:
        """Phase 4: Create cross-references."""
        links = 0
        for f in files:
            content = f.read_text()
            # Count cross-references
            links += content.count("[")  # Markdown links
        return links

    def forge(
        self,
        target: Path,
        layers: Optional[List[DocLayer]] = None,
        project_name: Optional[str] = None,
        output_dir: Optional[Path] = None,
    ) -> DocForgeResult:
        """Run the complete documentation generation pipeline."""
        start = time.monotonic()

        if layers is None:
            layers = list(DocLayer)

        if project_name is None:
            project_name = target.name

        if output_dir is None:
            output_dir = target / "docs_generated"

        output_dir.mkdir(parents=True, exist_ok=True)

        # Run phases
        elements = self._phase_scan(target)
        analysis = self._phase_analyze(elements)
        files = self._phase_generate(elements, layers, project_name, output_dir)
        links = self._phase_link(files)

        duration = (time.monotonic() - start) * 1000

        return DocForgeResult(
            target_path=target,
            layers_generated=[l.value for l in layers],
            elements_documented=analysis["total_elements"],
            links_created=links,
            output_files=files,
            duration_ms=duration,
        )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Doc Forge v{VERSION} — 4-Layer Documentation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Layers:
  L1 HUMAN    — What and why (normal people)
  L2 EXPERT   — Technical why and how (masters of the trade)
  L3 MACHINE  — API specs, schemas, configs (for machines)
  L4 MESH     — Linking all to all (the connective tissue)
        """,
    )

    parser.add_argument("--target", required=True, help="Target directory")
    parser.add_argument("--layers", default="all", help="Layers to generate (comma-separated or 'all')")
    parser.add_argument("--name", default=None, help="Project name")
    parser.add_argument("--output", default=None, help="Output directory")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")

    args = parser.parse_args()

    if args.layers == "all":
        layers = list(DocLayer)
    else:
        layers = [DocLayer(l.strip()) for l in args.layers.split(",")]

    output_dir = Path(args.output) if args.output else None

    forge = DocForge()
    result = forge.forge(Path(args.target), layers, args.name, output_dir)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.to_markdown())

    return 0


if __name__ == "__main__":
    import argparse
    sys.exit(main())
