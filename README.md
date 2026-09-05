# Hyper-Pipeline

The unified pipeline system — build, compose, and run production-grade pipelines.

## Quick Start

```bash
# Build a new pipeline from concept
python3 hyper.py architect --name my-pipeline --purpose "What it does" --domain engineering

# Compose and run a pipeline
python3 hyper.py forge --template production --target /path/to/project

# Run the 10-phase production pipeline
python3 hyper.py run --template production --target /path/to/project

# Forge a new skill
python3 hyper.py skill --name my-skill --purpose "What it does" --domain engineering

# Forge a new MCP server
python3 hyper.py mcp --name my-server --purpose "What it does" --type api

# Generate test suites
python3 hyper.py test --target /path/to/project --types unit,integration

# Generate 4-layer documentation
python3 hyper.py doc --target /path/to/project --layers all

# Generate CI/CD configuration
python3 hyper.py deploy --target /path/to/project --platform github,docker

# List available options
python3 hyper.py list templates
python3 hyper.py list blocks
python3 hyper.py list skills
python3 hyper.py list connectors
python3 hyper.py list domains
python3 hyper.py list types
python3 hyper.py list platforms
```

## Eight Engines

| Engine | Purpose | Command |
|--------|---------|---------|
| **Architect** | Build new pipelines from concepts | `python3 hyper.py architect` |
| **Forge** | Compose pipelines from blocks/templates | `python3 hyper.py forge` |
| **Runner** | Execute pipelines against targets | `python3 hyper.py run` |
| **Skill Forge** | Create production-grade skills | `python3 hyper.py skill` |
| **MCP Forge** | Create durable remote MCP servers | `python3 hyper.py mcp` |
| **Test Forge** | Auto-generate test suites | `python3 hyper.py test` |
| **Doc Forge** | Generate 4-layer documentation | `python3 hyper.py doc` |
| **Deploy Forge** | Create CI/CD configurations | `python3 hyper.py deploy` |

## Templates

| Template | Phases | Use Case |
|----------|--------|----------|
| `production` | 10 phases | Full-cycle engineering |
| `security` | 6 phases | Security audit |
| `research` | 8 phases | Deep research |
| `perf` | 6 phases | Performance engineering |
| `quick` | 4 phases | Fast iteration |
| `full` | 12 phases | Everything |

## Phase Blocks

### Primitives
- `orient` — Inspect environment
- `grill` — Resolve decisions
- `spec` — Create specification
- `workspace` — Prepare environment
- `implement` — Write code
- `verify` — Run tests
- `review` — Code review
- `finalize` — Update docs
- `finish` — Report

### Power-ups
- `gate-7d` — 7-dimension production audit
- `security-scan` — Threat model + CVE scan
- `perf-profile` — Benchmark + optimize
- `research-deep` — Multi-source research
- `compliance-check` — Regulatory compliance
- `deploy-safe` — Staged deployment

## Skill Forge

The Skill Forge creates production-grade skills with 7 phases:

```
CONCEPT → DECOMPOSE → DESIGN → BUILD → VALIDATE → TEST → PUBLISH
```

### Skill Domains

| Domain | Description |
|--------|-------------|
| `engineering` | Code, architecture, systems |
| `research` | Investigation, analysis, synthesis |
| `security` | Audit, threat model, compliance |
| `data` | Analytics, visualization, reporting |
| `design` | UI, UX, visual design |
| `memory` | Persistence, context, state |
| `orchestration` | Workflow, delegation, coordination |

### Skill Output Structure

```
my-skill/
├── SKILL.md                    # Main skill definition
├── README.md                   # Usage documentation
├── tests/
│   └── test_my_skill.py        # Test suite
└── references/
    └── REFERENCE.md            # Quick reference
```

## MCP Forge

The MCP Forge creates durable remote MCP servers with 7 phases:

```
CONCEPT → SCHEMA → IMPLEMENT → VALIDATE → TEST → DEPLOY → MONITOR
```

### MCP Server Types

| Type | Description |
|------|-------------|
| `api` | REST/GraphQL API wrapper |
| `database` | Database query and management |
| `filesystem` | File operations and management |
| `git` | Git repository operations |
| `cloud` | Cloud service integration |
| `monitoring` | System and service monitoring |
| `orchestration` | Workflow and task orchestration |

### MCP Server Output Structure

```
my-server/
├── server.py                   # Main MCP server
├── requirements.txt            # Dependencies
├── Dockerfile                  # Container deployment
├── config.json                 # Server configuration
├── deploy.sh                   # Deployment script
├── monitor.json                # Monitoring config
└── tests/
    └── test_server.py          # Test suite
```

## Test Forge

The Test Forge auto-generates comprehensive test suites:

```
SCAN → CLASSIFY → GENERATE → VALIDATE → REPORT
```

### Test Types

| Type | Description |
|------|-------------|
| `unit` | Isolated function/method tests |
| `integration` | Component interaction tests |
| `e2e` | End-to-end workflow tests |
| `property` | Property-based tests (Hypothesis) |
| `snapshot` | Snapshot/regression tests |

### Usage

```bash
# Generate unit tests only
python3 hyper.py test --target /path --types unit

# Generate unit + integration tests
python3 hyper.py test --target /path --types unit,integration

# Generate all test types with 95% coverage target
python3 hyper.py test --target /path --types unit,integration,property --coverage 95
```

## Doc Forge

The Doc Forge generates 4-layer documentation:

```
SCAN → ANALYZE → GENERATE → LINK → PUBLISH
```

### Documentation Layers

| Layer | Audience | Content |
|-------|----------|---------|
| **L1 HUMAN** | Normal people | What and why |
| **L2 EXPERT** | Masters of the trade | Technical why and how |
| **L3 MACHINE** | Machines | API specs, schemas, configs |
| **L4 MESH** | Everyone | Links all layers together |

### Usage

```bash
# Generate all layers
python3 hyper.py doc --target /path --layers all

# Generate human + expert layers only
python3 hyper.py doc --target /path --layers human,expert

# Generate machine layer (OpenAPI schema)
python3 hyper.py doc --target /path --layers machine
```

### Output Structure

```
docs_generated/
├── L1_HUMAN.md      # What/why for normal people
├── L2_EXPERT.md     # Technical docs for experts
├── L3_MACHINE.json  # OpenAPI schema for machines
└── L4_MESH.md       # Cross-reference index
```

## Deploy Forge

The Deploy Forge creates CI/CD configurations:

```
ANALYZE → SELECT → CONFIGURE → VALIDATE → PUBLISH
```

### Supported Platforms

| Platform | Description |
|----------|-------------|
| `github` | GitHub Actions CI/CD |
| `vercel` | Vercel deployment |
| `docker` | Docker containerization |
| `k8s` | Kubernetes deployment |
| `aws` | AWS Lambda (SAM) |
| `railway` | Railway.app deployment |

### Usage

```bash
# Generate GitHub Actions + Docker
python3 hyper.py deploy --target /path --platform github,docker

# Generate all platforms
python3 hyper.py deploy --target /path --platform all

# Generate Kubernetes only
python3 hyper.py deploy --target /path --platform k8s
```

## Skills (35+)

| Category | Skills |
|----------|--------|
| Engineering | helix-pro-code, compose-next, quality-gate, production-readiness-gate |
| Research | deep-research, super-research, arxiv |
| Security | semgrep, differential-review, supply-chain-risk-auditor |
| Data | data-analytics, build-report, visualize-data |
| Design | frontend-design, mega-web, design-blueprint |
| Memory | memory-unified, context-capsule, handoff-record |
| Orchestration | swarm-orchestrator, skill-connector-router, make-it-heavy |

## Connectors

| Connector | Type | Purpose |
|-----------|------|---------|
| GitHub | API | Repos, issues, PRs |
| Notion | API | Docs, databases |
| Supabase | Database | Postgres, auth |
| Vercel | Service | Deploy, edge |
| OpenRouter | API | LLM routing |
| Dropbox | Storage | Files |
| Gmail | API | Email |

## Sequential Thinking

For complexity ≥ 7, enforces 5-step thinking chain:

```
1. OBSERVE → What do I see?
2. ANALYZE → What does it mean?
3. HYPOTHESIZE → What might be true?
4. VERIFY → How can I confirm?
5. SYNTHESIZE → What's my conclusion?
```

## Quality Scoring

5 dimensions, weighted:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 20% | All aspects covered |
| Correctness | 25% | No errors, verifiable |
| Clarity | 20% | Unambiguous |
| Confidence | 20% | Evidence-backed |
| Coherence | 15% | Logically consistent |

**Target: 9.0+**

## Structure

```
hyper-pipeline/
├── hyper.py                    # Unified CLI (8 commands)
├── run_tests.py                # Test runner
├── scripts/
│   ├── architect.py            # Pipeline builder
│   ├── forge.py                # Pipeline composer
│   ├── pipeline_runner.py      # Pipeline executor
│   ├── production_auditor.py   # 7-dimension auditor
│   ├── skill_forge.py          # Skill development pipeline
│   ├── mcp_forge.py            # MCP server creation pipeline
│   ├── test_forge.py           # Test suite generation
│   ├── doc_forge.py            # 4-layer documentation
│   └── deploy_forge.py         # CI/CD configuration
├── templates/
│   ├── security.yaml
│   ├── research.yaml
│   └── perf.yaml
├── skills/
│   ├── architect/SKILL.md
│   ├── forge/SKILL.md
│   └── production/SKILL.md
├── tests/
│   ├── test_architect.py       # 27 tests
│   ├── test_forge.py           # 30 tests
│   ├── test_pipeline.py        # 21 tests
│   ├── test_skill_forge.py     # 22 tests
│   ├── test_mcp_forge.py       # 24 tests
│   └── test_three_forges.py    # 30 tests
└── references/
    └── remediation.md
```

## Tests

```bash
# Run all tests
python3 run_tests.py

# Run specific suite
python3 -m pytest tests/test_architect.py -v
python3 -m pytest tests/test_forge.py -v
python3 -m pytest tests/test_pipeline.py -v
python3 -m pytest tests/test_skill_forge.py -v
python3 -m pytest tests/test_mcp_forge.py -v
python3 -m pytest tests/test_three_forges.py -v
```

## License

APEX Estate — GlacierEQ
