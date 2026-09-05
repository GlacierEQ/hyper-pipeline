---
name: pipeline-architect
description: >
  Meta-pipeline that builds other pipelines. Takes a concept and produces a
  production-grade pipeline with skills, connectors, sequential thinking enforcement,
  and quality gates. For building pipelines that deliver 9+ quality outputs.
  Triggers: "build pipeline", "create workflow", "design pipeline", "architect",
  "pipeline for X", "sequential thinking", "9+ quality", "skill integration".
---

# Pipeline Architect

## Purpose

Build production-grade pipelines that incorporate skills, connectors, and sequential
thinking enforcement. The meta-system that creates pipelines worthy of the name.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE ARCHITECT                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐         │
│  │  CONCEPT      │     │  DESIGN       │     │  BUILD        │         │
│  │  INTAKE       │ ──► │  ENGINE       │ ──► │  ENGINE       │         │
│  └───────────────┘     └───────────────┘     └───────────────┘         │
│         │                     │                     │                   │
│         ▼                     ▼                     ▼                   │
│  ┌───────────────┐     ┌───────────────┐     ┌───────────────┐         │
│  │  SKILL        │     │  SEQUENTIAL   │     │  QUALITY      │         │
│  │  CONNECTOR    │     │  THINKING     │     │  GATE         │         │
│  │  MAPPER       │     │  ENFORCER     │     │  (9+ SCORE)   │         │
│  └───────────────┘     └───────────────┘     └───────────────┘         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Pipeline Creation Flow

```
CONCEPT ──► DECOMPOSE ──► MAP SKILLS ──► MAP CONNECTORS ──► DESIGN PHASES
   │              │              │               │               │
   ▼              ▼              ▼               ▼               ▼
 INTAKE      BREAK DOWN    SELECT SKILLS   WIRE APIS       SEQUENCE
                         + CONNECTORS                    + GATE
   │                                                            │
   ▼                                                            ▼
BUILD PIPELINE ──► VALIDATE ──► SCORE (9+) ──► DELIVER
```

## The 12-Phase Architect Pipeline

### Phase 1: CONCEPT INTAKE
Capture the pipeline concept in structured form:

```yaml
concept:
  name: <pipeline-name>
  purpose: <what it does>
  inputs: <what it takes>
  outputs: <what it produces>
  quality_target: <9+ expected>
  domain: <engineering|research|security|data|creative>
```

### Phase 2: PROBLEM DECOMPOSITION
Break the concept into atomic work units:

```yaml
decomposition:
  - unit: <work-unit-1>
    type: <thinking|doing|verifying>
    complexity: <1-10>
    dependencies: []
  - unit: <work-unit-2>
    type: <thinking|doing|verifying>
    complexity: <1-10>
    dependencies: [<unit-1>]
```

### Phase 3: SEQUENTIAL THINKING DESIGN
Design the thinking chain for each unit:

```yaml
sequential_thinking:
  - unit: <work-unit>
    chain:
      - step: <observation>
        type: perceive
        evidence: <what to look for>
      - step: <analysis>
        type: reason
        evidence: <how to interpret>
      - step: <hypothesis>
        type: hypothesize
        evidence: <what to propose>
      - step: <verification>
        type: verify
        evidence: <how to confirm>
      - step: <synthesis>
        type: conclude
        evidence: <what to deliver>
    quality_gate:
      min_score: 9
      checks: [completeness, correctness, clarity, confidence]
```

### Phase 4: SKILL MAPPING
Map required skills to each phase:

```yaml
skill_map:
  - phase: <phase-name>
    skills:
      - name: <skill-name>
        purpose: <what it does>
        integration: <inline|subagent|reference>
        fallback: <alternative if unavailable>
```

**Available Skill Categories:**
| Category | Skills |
|----------|--------|
| Engineering | `helix-pro-code`, `compose-next`, `quality-gate` |
| Research | `deep-research`, `super-research`, `arxiv` |
| Security | `semgrep`, `differential-review`, `supply-chain-risk-auditor` |
| Data | `data-analytics`, `build-report`, `visualize-data` |
| Design | `frontend-design`, `mega-web`, `design-blueprint` |
| Memory | `memory-unified`, `context-capsule`, `handoff-record` |
| Orchestration | `swarm-orchestrator`, `skill-connector-router`, `make-it-heavy` |

### Phase 5: CONNECTOR WIRING
Wire external APIs and services:

```yaml
connectors:
  - name: <connector-name>
    type: <api|database|file|service>
    config:
      endpoint: <url>
      auth: <method>
      rate_limit: <requests/sec>
    phases: [<phase-1>, <phase-2>]
    fallback: <what to do if unavailable>
```

**Available Connectors:**
| Connector | Type | Purpose |
|-----------|------|---------|
| GitHub | API | Repos, issues, PRs |
| Notion | API | Docs, databases |
| Supabase | Database | Postgres, auth |
| Vercel | Service | Deploy, edge |
| OpenRouter | API | LLM routing |
| Dropbox | Storage | Files |
| Gmail | API | Email |

### Phase 6: PHASE DESIGN
Design each pipeline phase with evidence requirements:

```yaml
phases:
  - name: <phase-name>
    type: <primitive|power-up|custom>
    inputs:
      - <what this phase needs>
    outputs:
      - <what this phase produces>
    evidence:
      - <what proves this phase worked>
    quality_gate:
      min_score: 9
      checks:
        - <completeness: all aspects covered>
        - <correctness: no errors>
        - <clarity: unambiguous>
        - <confidence: verifiable>
    skills:
      - <skill-1>
      - <skill-2>
    connectors:
      - <connector-1>
```

### Phase 7: QUALITY ARCHITECTURE
Design the quality enforcement system:

```yaml
quality:
  scoring:
    scale: 1-10
    dimensions:
      - completeness: <0-10>
      - correctness: <0-10>
      - clarity: <0-10>
      - confidence: <0-10>
      - coherence: <0-10>
    formula: "avg(completeness, correctness, clarity, confidence, coherence)"
    target: 9

  gates:
    - name: <gate-name>
      phase: <phase-name>
      min_score: 9
      blocking: true
      remediation: <what to do if failed>

  evidence:
    - type: <test|review|audit|metric>
      phase: <phase-name>
      requirement: <what must exist>
```

### Phase 8: ERROR RECOVERY
Design fallbacks and recovery:

```yaml
recovery:
  - failure: <what can fail>
    detection: <how to detect>
    recovery: <what to do>
    max_retries: <number>
    backoff: <strategy>

  - failure: skill_unavailable
    detection: import_error
    recovery: use_fallback_skill
    fallback_skills:
      - <alternative-1>
      - <alternative-2>
```

### Phase 9: STATE MANAGEMENT
Design durable state:

```yaml
state:
  files:
    - name: MISSION.md
      purpose: Current objective
      update: every_phase
    - name: EVIDENCE.md
      purpose: Verification receipts
      update: every_gate
    - name: CONTEXT.md
      purpose: Compacted state
      update: every_3_phases
    - name: HANDOFF.md
      purpose: Recovery point
      update: on_interrupt

  persistence:
    type: jsonl
    location: .pipeline/
    backup: true
```

### Phase 10: PIPELINE ASSEMBLY
Assemble the final pipeline config:

```yaml
# Generated by Pipeline Architect
name: <pipeline-name>
version: "1.0"
description: <description>

phases:
  <all phases from Phase 6>

quality:
  <quality config from Phase 7>

recovery:
  <recovery config from Phase 8>

state:
  <state config from Phase 9>

skills:
  <all skills from Phase 4>

connectors:
  <all connectors from Phase 5>
```

### Phase 11: VALIDATION
Validate the pipeline design:

```yaml
validation:
  checks:
    - all_phases_have_skills: true
    - all_phases_have_evidence: true
    - quality_gates_on_critical: true
    - error_recovery_defined: true
    - state_persistence: true
    - sequential_thinking_on_complex: true
  score: <0-10>
  pass_threshold: 9
```

### Phase 12: DELIVERY
Package and deliver:

```yaml
delivery:
  - name: <pipeline-name>.yaml
    location: templates/
  - name: SKILL.md
    location: skills/<pipeline-name>/
  - name: README.md
    location: skills/<pipeline-name>/
  - name: scripts/runner.py
    location: skills/<pipeline-name>/
```

## Sequential Thinking Enforcement

For any phase with complexity > 7, enforce sequential thinking:

```yaml
sequential_thinking_enforcement:
  enabled: true
  threshold: 7  # complexity score

  chain:
    1. OBSERVE: What do I see?
    2. ANALYZE: What does it mean?
    3. HYPOTHESIZE: What might be true?
    4. VERIFY: How can I confirm?
    5. SYNTHESIZE: What's my conclusion?

  quality_checks:
    - each_step_has_evidence: true
    - no_step_skipped: true
    - confidence_scored: true
    - ambiguity_flagged: true
```

## Quality Scoring (9+ Target)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 20% | All aspects covered |
| Correctness | 25% | No errors, verifiable |
| Clarity | 20% | Unambiguous, well-structured |
| Confidence | 20% | Evidence-backed |
| Coherence | 15% | Logically consistent |

**Formula:**
```
score = (completeness * 0.20) + (correctness * 0.25) + 
        (clarity * 0.20) + (confidence * 0.20) + (coherence * 0.15)
```

**Target: score >= 9.0**

## Output Contract

The Pipeline Architect produces:

```
skills/pipeline-architect/
├── SKILL.md                    # This file
├── templates/
│   └── <pipeline-name>.yaml    # Generated pipeline config
├── skills/<pipeline-name>/
│   ├── SKILL.md                # Pipeline skill definition
│   └── scripts/runner.py       # Automated runner
└── references/
    └── design-doc.md           # Design documentation
```

## Non-goals

- Does not produce low-quality pipelines
- Does not skip sequential thinking on complex tasks
- Does not allow quality scores below 9

**We. Architect. Excellence.**
