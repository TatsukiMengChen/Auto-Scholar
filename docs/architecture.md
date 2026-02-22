# Auto-Scholar Architecture

## System Overview

Auto-Scholar is a 5-node LangGraph workflow with human-in-the-loop approval for academic literature review generation.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LangGraph Workflow                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐                                                            │
│   │   START     │                                                            │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐     ┌─────────────────────────────────────────────────┐   │
│   │ Entry Router│────▶│ is_continuation?                                │   │
│   └──────┬──────┘     │   YES → draft_node (update existing review)     │   │
│          │            │   NO  → plan_node (new research)                │   │
│          │            └─────────────────────────────────────────────────┘   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │ plan_node   │  Generate 3-5 search keywords from user query              │
│   │             │  Output: search_keywords[]                                 │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │ search_node │  Parallel search: Semantic Scholar + arXiv + PubMed        │
│   │             │  Deduplication by normalized title                         │
│   │             │  Output: candidate_papers[]                                │
│   └──────┬──────┘                                                            │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    ⏸️  HUMAN APPROVAL INTERRUPT                      │   │
│   │                                                                      │   │
│   │   User reviews candidate_papers and selects which to include         │   │
│   │   POST /api/research/approve { paper_ids: [...] }                    │   │
│   └──────────────────────────────┬──────────────────────────────────────┘   │
│                                  │                                           │
│                                  ▼                                           │
│   ┌─────────────────────┐                                                    │
│   │ read_and_extract_   │  Extract core contributions from approved papers   │
│   │ node                │  Enrich with PDF URLs (Unpaywall/OpenAlex)         │
│   │                     │  Output: approved_papers[] with contributions      │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐                                                    │
│   │ draft_node          │  Generate structured literature review             │
│   │                     │  Uses {cite:N} placeholders for citations          │
│   │                     │  Output: final_draft with sections                 │
│   └──────────┬──────────┘                                                    │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────────────┐     ┌─────────────────────────────────────────┐   │
│   │ qa_evaluator_node   │────▶│ QA Checks:                              │   │
│   │                     │     │   1. Citation bounds (no [N] > papers)  │   │
│   │                     │     │   2. No hallucinated paper_ids          │   │
│   │                     │     │   3. All approved papers cited          │   │
│   └──────────┬──────────┘     └─────────────────────────────────────────┘   │
│              │                                                               │
│              ▼                                                               │
│   ┌─────────────┐     ┌─────────────────────────────────────────────────┐   │
│   │  QA Router  │────▶│ has_errors AND retry_count < 3?                 │   │
│   └──────┬──────┘     │   YES → draft_node (retry with error feedback)  │   │
│          │            │   NO  → END                                     │   │
│          │            └─────────────────────────────────────────────────┘   │
│          ▼                                                                   │
│   ┌─────────────┐                                                            │
│   │    END      │  Final draft ready for export                              │
│   └─────────────┘                                                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Frontend (Next.js 16)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐    ┌──────────────────────────────────────────┐   │
│  │    Agent Console     │    │              Workspace                    │   │
│  │  ┌────────────────┐  │    │  ┌────────────────────────────────────┐  │   │
│  │  │  QueryInput    │  │    │  │  ReviewRenderer                    │  │   │
│  │  │  LogStream     │  │    │  │  • Markdown rendering              │  │   │
│  │  │  StatusIndicator│ │    │  │  • CitationTooltip on hover        │  │   │
│  │  │  ChatThread    │  │    │  │  • Edit mode support               │  │   │
│  │  │  HistoryPanel  │  │    │  └────────────────────────────────────┘  │   │
│  │  └────────────────┘  │    │  ┌────────────────────────────────────┐  │   │
│  │                      │    │  │  ChartsView                        │  │   │
│  │  ┌────────────────┐  │    │  │  • Year trend                      │  │   │
│  │  │ ApprovalModal  │  │    │  │  • Source distribution             │  │   │
│  │  │ PaperTable     │  │    │  │  • Author frequency                │  │   │
│  │  └────────────────┘  │    │  └────────────────────────────────────┘  │   │
│  └──────────────────────┘    └──────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Zustand Store                                 │   │
│  │  • threadId, status, logs, candidatePapers, approvedPapers, draft    │   │
│  │  • Actions: startResearch, approveResearch, continueResearch         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                              REST API + SSE
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Backend (FastAPI + LangGraph)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                           API Endpoints                               │   │
│  │  POST /api/research/start     - Initialize research                   │   │
│  │  GET  /api/research/stream    - SSE log streaming                     │   │
│  │  POST /api/research/approve   - Approve papers, generate review       │   │
│  │  POST /api/research/continue  - Multi-turn conversation               │   │
│  │  GET  /api/research/status    - Check workflow status                 │   │
│  │  GET  /api/research/sessions  - List/get session history              │   │
│  │  POST /api/research/export    - Export to Markdown/DOCX               │   │
│  │  POST /api/research/charts    - Generate analytics charts             │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                           Utilities                                   │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ llm_client  │  │ scholar_api │  │ event_queue │  │  exporter   │  │   │
│  │  │ OpenAI +    │  │ Semantic    │  │ SSE debounce│  │ MD/DOCX     │  │   │
│  │  │ structured  │  │ Scholar +   │  │ 92% network │  │ APA/MLA/    │  │   │
│  │  │ outputs     │  │ arXiv +     │  │ reduction   │  │ IEEE/GB     │  │   │
│  │  │             │  │ PubMed      │  │             │  │             │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │   │
│  │  │ http_pool   │  │fulltext_api │  │source_tracker│ │   charts    │  │   │
│  │  │ TCP reuse   │  │ Unpaywall + │  │ Failure skip│  │ matplotlib  │  │   │
│  │  │ 50 conns    │  │ OpenAlex    │  │ 3 fails/2min│  │ base64 PNG  │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      State Persistence                                │   │
│  │  AsyncSqliteSaver → checkpoints.db                                    │   │
│  │  • Workflow state checkpointing                                       │   │
│  │  • Resume via ainvoke(None, config)                                   │   │
│  │  • Session history via checkpoint metadata                            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Query
    │
    ▼
┌─────────────────┐
│ plan_node       │ → LLM generates 3-5 keywords
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ search_node     │ → Parallel API calls to 3 sources
│                 │ → Deduplication by normalized title
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ HUMAN APPROVAL  │ → User selects papers via UI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ extract_node    │ → LLM extracts contributions (2 concurrent)
│                 │ → Unpaywall/OpenAlex for PDF URLs
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ draft_node      │ → LLM generates review with {cite:N}
│                 │ → Backend converts to [N] format
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ qa_node         │ → Validate citations (no hallucination)
│                 │ → Retry up to 3x if errors
└────────┬────────┘
         │
         ▼
Final Review (exportable to MD/DOCX)
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| LangGraph over simple chains | Need conditional routing (QA retry) and human interrupt |
| SQLite checkpointing | Simple persistence, no external DB dependency |
| SSE debouncing (200ms) | Balance between latency and network efficiency |
| Citation placeholder system | LLM uses {cite:N}, backend validates and converts |
| Multi-source search | Semantic Scholar (best metadata) + arXiv + PubMed for coverage |
| Source failure tracking | Skip source after 3 failures in 2 minutes |
| HTTP connection pooling | TCP reuse reduces latency, 50 connection limit |
