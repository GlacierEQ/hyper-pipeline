#!/usr/bin/env python3
"""
Deploy Forge — CI/CD Pipeline Creation
Generates deployment configurations for multiple platforms.

Pipeline:
  ANALYZE → SELECT → CONFIGURE → VALIDATE → PUBLISH

Platforms:
  - GitHub Actions
  - Vercel
  - Docker
  - Kubernetes
  - AWS Lambda

Usage:
    python3 deploy_forge.py --target /path/to/project --platform github
    python3 deploy_forge.py --target /path/to/project --platform docker,k8s
    python3 deploy_forge.py --target /path/to/project --platform all
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


VERSION = "1.0.0"


# ─── Platform Definitions ────────────────────────────────────────────────────

PLATFORMS = {
    "github": {
        "description": "GitHub Actions CI/CD",
        "files": [".github/workflows/ci.yml", ".github/workflows/deploy.yml"],
        "detect": [".git", ".github"],
    },
    "vercel": {
        "description": "Vercel deployment",
        "files": ["vercel.json"],
        "detect": ["package.json", "next.config.js", "next.config.ts"],
    },
    "docker": {
        "description": "Docker containerization",
        "files": ["Dockerfile", "docker-compose.yml", ".dockerignore"],
        "detect": ["package.json", "requirements.txt", "go.mod"],
    },
    "k8s": {
        "description": "Kubernetes deployment",
        "files": ["k8s/deployment.yml", "k8s/service.yml", "k8s/ingress.yml"],
        "detect": ["Dockerfile", "docker-compose.yml"],
    },
    "aws": {
        "description": "AWS Lambda deployment",
        "files": ["template.yml", "samconfig.toml"],
        "detect": ["requirements.txt", "package.json"],
    },
    "railway": {
        "description": "Railway.app deployment",
        "files": ["railway.json", "Procfile"],
        "detect": ["package.json", "requirements.txt"],
    },
}


# ─── Data Models ─────────────────────────────────────────────────────────────

class DeployPhase(Enum):
    ANALYZE = "analyze"
    SELECT = "select"
    CONFIGURE = "configure"
    VALIDATE = "validate"
    PUBLISH = "publish"


@dataclass
class ProjectInfo:
    """Detected project information."""
    name: str
    language: str
    framework: str
    has_tests: bool = False
    has_docker: bool = False
    has_ci: bool = False
    dependencies: List[str] = field(default_factory=list)
    scripts: Dict[str, str] = field(default_factory=dict)


@dataclass
class DeployConfig:
    """Generated deployment configuration."""
    platform: str
    files: Dict[str, str] = field(default_factory=dict)
    validated: bool = False
    issues: List[str] = field(default_factory=list)


@dataclass
class DeployForgeResult:
    """Result of deployment generation."""
    target_path: Path
    platforms: List[str] = field(default_factory=list)
    configs_generated: int = 0
    files_created: List[Path] = field(default_factory=list)
    validated: bool = False
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": str(self.target_path),
            "platforms": self.platforms,
            "configs": self.configs_generated,
            "files": [str(f) for f in self.files_created],
            "validated": self.validated,
            "duration_ms": round(self.duration_ms, 1),
        }

    def to_markdown(self) -> str:
        lines = [
            "# Deploy Forge Result",
            "",
            "## Summary",
            f"- **Platforms:** {', '.join(self.platforms)}",
            f"- **Configs Generated:** {self.configs_generated}",
            f"- **Files Created:** {len(self.files_created)}",
            f"- **Validated:** {'✓' if self.validated else '✗'}",
            "",
            "## Generated Files",
        ]
        for f in self.files_created:
            lines.append(f"  ✓ {f}")
        return "\n".join(lines)


# ─── Project Analyzer ────────────────────────────────────────────────────────

class ProjectAnalyzer:
    """Analyzes project structure."""

    def analyze(self, target: Path) -> ProjectInfo:
        """Analyze project at target path."""
        info = ProjectInfo(name=target.name, language="unknown", framework="unknown")

        # Detect language
        if (target / "requirements.txt").exists() or (target / "pyproject.toml").exists():
            info.language = "python"
        elif (target / "package.json").exists():
            info.language = "javascript"
        elif (target / "go.mod").exists():
            info.language = "go"
        elif (target / "Cargo.toml").exists():
            info.language = "rust"

        # Detect framework
        if (target / "next.config.js").exists() or (target / "next.config.ts").exists():
            info.framework = "nextjs"
        elif (target / "manage.py").exists():
            info.framework = "django"
        elif (target / "app.py").exists() or (target / "main.py").exists():
            info.framework = "fastapi"

        # Detect tests
        info.has_tests = any(target.rglob("test_*.py")) or any(target.rglob("*.test.js"))

        # Detect existing CI/Docker
        info.has_ci = (target / ".github" / "workflows").exists()
        info.has_docker = (target / "Dockerfile").exists()

        # Read package.json if exists
        pkg_json = target / "package.json"
        if pkg_json.exists():
            try:
                pkg = json.loads(pkg_json.read_text())
                info.scripts = pkg.get("scripts", {})
                info.dependencies = list(pkg.get("dependencies", {}).keys())
            except json.JSONDecodeError:
                pass

        # Read requirements.txt
        req_txt = target / "requirements.txt"
        if req_txt.exists():
            info.dependencies = [
                line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                for line in req_txt.read_text().splitlines()
                if line.strip() and not line.startswith("#")
            ]

        return info


# ─── Config Generator ───────────────────────────────────────────────────────

class ConfigGenerator:
    """Generates deployment configurations."""

    def generate_github_actions(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate GitHub Actions CI/CD."""
        configs = {}

        # CI workflow
        ci_yaml = """name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest tests/ -v

      - name: Run linter
        run: |
          ruff check .
"""
        configs[".github/workflows/ci.yml"] = ci_yaml

        # Deploy workflow
        deploy_yaml = """name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: |
          echo "Add your deployment steps here"
"""
        configs[".github/workflows/deploy.yml"] = deploy_yaml

        return configs

    def generate_vercel(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate Vercel configuration."""
        configs = {}

        vercel_json = """{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/"
    }
  ]
}
"""
        configs["vercel.json"] = vercel_json

        return configs

    def generate_docker(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate Docker configuration."""
        configs = {}

        if info.language == "python":
            dockerfile = """FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
"""
        elif info.language == "javascript":
            dockerfile = """FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
"""
        else:
            dockerfile = """FROM ubuntu:22.04

WORKDIR /app

COPY . .

CMD ["./start.sh"]
"""

        configs["Dockerfile"] = dockerfile

        # docker-compose.yml
        compose = f"""version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
"""
        configs["docker-compose.yml"] = compose

        # .dockerignore
        dockerignore = """node_modules
.git
.env
__pycache__
*.pyc
.pytest_cache
coverage
"""
        configs[".dockerignore"] = dockerignore

        return configs

    def generate_k8s(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate Kubernetes manifests."""
        configs = {}

        deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
        - name: app
          image: app:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "128Mi"
              cpu: "250m"
            limits:
              memory: "256Mi"
              cpu: "500m"
"""
        configs["k8s/deployment.yml"] = deployment

        service = """apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
"""
        configs["k8s/service.yml"] = service

        ingress = """apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 80
"""
        configs["k8s/ingress.yml"] = ingress

        return configs

    def generate_aws(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate AWS SAM configuration."""
        configs = {}

        template = """AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    MemorySize: 128

Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.12
      Events:
        Api:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
"""
        configs["template.yml"] = template

        return configs

    def generate_railway(self, info: ProjectInfo) -> Dict[str, str]:
        """Generate Railway configuration."""
        configs = {}

        railway_json = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm start",
    "healthcheckPath": "/",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 3
  }
}
"""
        configs["railway.json"] = railway_json

        return configs


# ─── Config Validator ────────────────────────────────────────────────────────

class ConfigValidator:
    """Validates deployment configurations."""

    def validate(self, configs: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Validate all configurations."""
        issues = []

        for filename, content in configs.items():
            # Check YAML syntax
            if filename.endswith((".yml", ".yaml")):
                if not self._validate_yaml(content):
                    issues.append(f"{filename}: Invalid YAML")

            # Check JSON syntax
            if filename.endswith(".json"):
                if not self._validate_json(content):
                    issues.append(f"{filename}: Invalid JSON")

            # Check Dockerfile
            if filename == "Dockerfile":
                if "FROM" not in content:
                    issues.append("Dockerfile: Missing FROM instruction")

        return len(issues) == 0, issues

    def _validate_yaml(self, content: str) -> bool:
        """Validate YAML syntax."""
        try:
            import yaml
            yaml.safe_load(content)
            return True
        except ImportError:
            # If yaml not installed, basic validation
            return "---" in content or "name:" in content or "apiVersion:" in content
        except Exception:
            return False

    def _validate_json(self, content: str) -> bool:
        """Validate JSON syntax."""
        try:
            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False


# Type alias
from typing import Tuple


# ─── Deploy Forge Pipeline ───────────────────────────────────────────────────

class DeployForge:
    """Complete deployment configuration pipeline."""

    def __init__(self) -> None:
        self.analyzer = ProjectAnalyzer()
        self.generator = ConfigGenerator()
        self.validator = ConfigValidator()

    def _phase_analyze(self, target: Path) -> ProjectInfo:
        """Phase 1: Analyze project."""
        return self.analyzer.analyze(target)

    def _phase_select(self, info: ProjectInfo, platforms: List[str]) -> List[str]:
        """Phase 2: Select appropriate platforms."""
        selected = []
        for platform in platforms:
            if platform in PLATFORMS:
                selected.append(platform)
        return selected

    def _phase_configure(
        self, info: ProjectInfo, platforms: List[str], output_dir: Path
    ) -> List[DeployConfig]:
        """Phase 3: Generate configurations."""
        configs = []

        for platform in platforms:
            config = DeployConfig(platform=platform)

            if platform == "github":
                config.files = self.generator.generate_github_actions(info)
            elif platform == "vercel":
                config.files = self.generator.generate_vercel(info)
            elif platform == "docker":
                config.files = self.generator.generate_docker(info)
            elif platform == "k8s":
                config.files = self.generator.generate_k8s(info)
            elif platform == "aws":
                config.files = self.generator.generate_aws(info)
            elif platform == "railway":
                config.files = self.generator.generate_railway(info)

            configs.append(config)

        return configs

    def _phase_validate(self, configs: List[DeployConfig]) -> bool:
        """Phase 4: Validate all configurations."""
        all_valid = True
        for config in configs:
            valid, issues = self.validator.validate(config.files)
            config.validated = valid
            config.issues = issues
            if not valid:
                all_valid = False
        return all_valid

    def _phase_publish(
        self, configs: List[DeployConfig], output_dir: Path
    ) -> List[Path]:
        """Phase 5: Write configuration files."""
        files = []

        for config in configs:
            for filename, content in config.files.items():
                filepath = output_dir / filename
                filepath.parent.mkdir(parents=True, exist_ok=True)
                filepath.write_text(content)
                files.append(filepath)

        return files

    def forge(
        self,
        target: Path,
        platforms: Optional[List[str]] = None,
        output_dir: Optional[Path] = None,
    ) -> DeployForgeResult:
        """Run the complete deployment configuration pipeline."""
        start = time.monotonic()

        if platforms is None:
            platforms = ["github", "docker"]

        if output_dir is None:
            output_dir = target / "deploy_generated"

        output_dir.mkdir(parents=True, exist_ok=True)

        # Run phases
        info = self._phase_analyze(target)
        selected = self._phase_select(info, platforms)
        configs = self._phase_configure(info, selected, output_dir)
        valid = self._phase_validate(configs)
        files = self._phase_publish(configs, output_dir)

        duration = (time.monotonic() - start) * 1000

        return DeployForgeResult(
            target_path=target,
            platforms=selected,
            configs_generated=len(configs),
            files_created=files,
            validated=valid,
            duration_ms=duration,
        )


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Deploy Forge v{VERSION} — CI/CD Pipeline Creation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Platforms:
  github   — GitHub Actions CI/CD
  vercel   — Vercel deployment
  docker   — Docker containerization
  k8s      — Kubernetes deployment
  aws      — AWS Lambda (SAM)
  railway  — Railway.app deployment
        """,
    )

    parser.add_argument("--target", required=True, help="Target directory")
    parser.add_argument("--platform", default="github,docker", help="Platforms (comma-separated or 'all')")
    parser.add_argument("--output", default=None, help="Output directory")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")

    args = parser.parse_args()

    if args.platform == "all":
        platforms = list(PLATFORMS.keys())
    else:
        platforms = [p.strip() for p in args.platform.split(",")]

    output_dir = Path(args.output) if args.output else None

    forge = DeployForge()
    result = forge.forge(Path(args.target), platforms, output_dir)

    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.to_markdown())

    return 0


if __name__ == "__main__":
    import argparse
    sys.exit(main())
