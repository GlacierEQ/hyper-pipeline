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

# List available options
python3 hyper.py list templates
python3 hyper.py list blocks
python3 hyper.py list skills
python3 hyper.py list connectors
```

## Three Engines

| Engine | Purpose | Command |
|--------|---------|---------|
| **Architect** | Build new pipelines from concepts | `python3 hyper.py architect` |
| **Forge** | Compose pipelines from blocks/templates | `python3 hyper.py forge` |
| **Runner** | Execute pipelines against targets | `python3 hyper.py run` |

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
├── hyper.py                    # Unified CLI
├── run_tests.py                # Test runner
├── scripts/
│   ├── architect.py            # Pipeline builder
│   ├── forge.py                # Pipeline composer
│   ├── pipeline_runner.py      # Pipeline executor
│   └── production_auditor.py   # 7-dimension auditor
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
│   └── test_pipeline.py        # 21 tests
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
```

## License

APEX Estate — GlacierEQ
