<!--
Sync Impact Report:
- Version: 1.0.0 (initial constitution creation)
- Modified Principles: N/A (new constitution)
- Added Sections: All core sections for AI-native Todo SaaS platform
- Removed Sections: N/A
- Templates Requiring Updates:
  ✅ spec-template.md - aligned with phase-driven approach
  ✅ plan-template.md - constitution check gates included
  ✅ tasks-template.md - testing and deployment phases supported
- Follow-up TODOs: None
-->

# AI-Native Todo SaaS Platform Constitution

## Core Principles

### I. Phase-Driven Evolution (NON-NEGOTIABLE)

The system MUST evolve through five distinct phases, each building on the previous:

1. **Phase 1 - Console Todo App**: Python CLI establishing core task logic (add, update, delete, list, mark complete)
2. **Phase 2 - Full Web App**: Production Next.js + FastAPI + Neon PostgreSQL with JWT auth and CRUD UI
3. **Phase 3 - AI Todo Chatbot**: OpenAI Agents SDK + MCP tools for natural language task automation
4. **Phase 4 - Kubernetes Deployment**: Dockerized containers, Helm charts, Minikube orchestration
5. **Phase 5 - Cloud + Kafka + Dapr**: Enterprise architecture with event pipelines, Dapr pub/sub, DigitalOcean deployment

**Rationale**: Each phase delivers independently testable value while building foundational capabilities for subsequent phases. No phase can be skipped; each validates architectural decisions before adding complexity.

**Rules**:
- Phase N+1 MUST NOT start until Phase N is complete and tested
- Each phase MUST have clear acceptance criteria
- Phase transitions MUST be documented with migration steps
- Regression tests from Phase N MUST pass in Phase N+1

---

### II. Cloud-Native Architecture

All components MUST be designed as cloud-native, containerized microservices from Phase 2 onward.

**Requirements**:
- Docker containers for all services (frontend, backend, AI agents)
- Kubernetes-ready deployment manifests
- 12-factor app principles (config via environment, stateless processes, port binding)
- Health checks and readiness probes for all services
- Horizontal scalability support

**Rationale**: Cloud-native design from the start prevents costly refactoring and enables seamless transition from Minikube (Phase 4) to production cloud (Phase 5).

---

### III. AI-First Integration

AI capabilities MUST be core architectural components, not bolt-on features.

**Requirements**:
- OpenAI Agents SDK integration with typed tool definitions
- MCP (Model Context Protocol) tools: `add_task`, `list_tasks`, `update_task`, `delete_task`
- Natural language processing for task creation and understanding
- AI agent state management and conversation persistence
- Structured outputs for task entities

**Rationale**: AI-native design ensures the chatbot (Phase 3) is not a wrapper but a first-class interface with deep system integration.

---

### IV. Event-Driven Communication

From Phase 5 onward, inter-service communication MUST use event-driven patterns via Kafka.

**Requirements**:
- Kafka topics for task lifecycle events (created, updated, completed, deleted)
- Event schemas with versioning
- Idempotent event consumers
- Dead letter queues for failed event processing
- Event sourcing for audit trails

**Rationale**: Event-driven architecture decouples services, enables async workflows (reminders, notifications), and scales horizontally.

---

### V. Dapr Service Mesh Integration

Phase 5 MUST leverage Dapr for cross-cutting concerns.

**Requirements**:
- Dapr pub/sub for event distribution
- Dapr state management for task persistence
- Dapr bindings for scheduled reminders and recurring tasks
- Dapr service invocation for inter-microservice calls
- Secrets management via Dapr secret stores

**Rationale**: Dapr provides infrastructure abstraction, making the system portable across cloud providers and simplifying operations.

---

### VI. Database-Backed Persistence

From Phase 2 onward, Neon PostgreSQL MUST be the single source of truth.

**Requirements**:
- Schema migrations via Alembic (Python) or Prisma (TypeScript)
- Connection pooling for performance
- Prepared statements to prevent SQL injection
- Database indexes on query-heavy fields (user_id, status, created_at)
- Foreign key constraints for referential integrity

**Rationale**: PostgreSQL ensures ACID compliance, supports complex queries, and integrates well with cloud platforms.

---

### VII. Authentication & Authorization

Phase 2+ MUST implement secure JWT-based authentication.

**Requirements**:
- JWT tokens with expiration and refresh mechanisms
- Password hashing using bcrypt or Argon2
- Role-based access control (RBAC) for future multi-tenancy
- Secure cookie handling (HttpOnly, Secure flags)
- Rate limiting on auth endpoints

**Rationale**: Security cannot be retrofitted; JWT provides stateless auth suitable for distributed systems.

---

### VIII. Test-First Development (NON-NEGOTIABLE)

Every phase MUST follow TDD: Write tests → Get user approval → Tests fail → Implement → Tests pass.

**Test Categories**:
- **Unit Tests**: Pure functions, business logic (pytest for Python, Jest for TypeScript)
- **Integration Tests**: API endpoints, database interactions
- **Contract Tests**: OpenAI agent tool interfaces, API contracts
- **End-to-End Tests**: Full user workflows (Playwright for web UI)

**Rationale**: TDD ensures requirements are testable, reduces regressions, and validates each phase before progression.

---

### IX. Observability & Monitoring

All services MUST emit structured logs, metrics, and traces.

**Requirements**:
- Structured JSON logging with correlation IDs
- Prometheus metrics for request rates, latencies, errors
- OpenTelemetry tracing for distributed requests
- Kubernetes liveness and readiness probes
- Centralized log aggregation (e.g., Loki, CloudWatch)

**Rationale**: Observability is essential for debugging distributed systems and maintaining SLAs in production.

---

### X. Simplicity & Incremental Complexity

Start simple; add complexity only when justified by phase requirements.

**Rules**:
- Phase 1: No frameworks, pure Python CLI
- Phase 2: Minimal frontend (React/Next.js), REST API
- Phase 3: Add AI only after stable CRUD operations
- Phase 4: Kubernetes only after containerization proven locally
- Phase 5: Kafka/Dapr only for event-driven use cases (reminders, notifications)

**Rationale**: YAGNI (You Aren't Gonna Need It) prevents over-engineering. Each phase validates whether added complexity delivers value.

---

## Technology Stack

### Phase 1: Console App
- **Language**: Python 3.11+
- **Dependencies**: None (stdlib only)
- **Storage**: In-memory or JSON file

### Phase 2: Web App
- **Frontend**: Next.js 14+ (React, TypeScript)
- **Backend**: FastAPI (Python 3.11+)
- **Database**: Neon PostgreSQL
- **Auth**: JWT (PyJWT library)
- **ORM**: SQLAlchemy or Prisma

### Phase 3: AI Chatbot
- **AI Framework**: OpenAI Agents SDK
- **Tools**: MCP protocol implementations
- **Models**: GPT-4 or GPT-4 Turbo
- **State**: Persistent conversation storage in PostgreSQL

### Phase 4: Kubernetes
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube for local, production for cloud)
- **Package Manager**: Helm
- **Ingress**: NGINX Ingress Controller

### Phase 5: Cloud-Native
- **Cloud Provider**: DigitalOcean Kubernetes (DOKS)
- **Messaging**: Kafka (managed or self-hosted)
- **Service Mesh**: Dapr 1.12+
- **Event Streaming**: Kafka topics with Avro schemas

---

## Development Workflow

### Phase Acceptance Criteria

Each phase MUST meet these criteria before proceeding:

1. **All tests pass** (unit, integration, contract, e2e as applicable)
2. **Documentation complete** (quickstart.md, API contracts, deployment guide)
3. **User validation** (manual testing of core workflows)
4. **Performance benchmarks met** (defined per phase)
5. **Security review** (auth, input validation, secrets management)

### Git Workflow

- **Main Branch**: `master` - always deployable, reflects latest completed phase
- **Feature Branches**: `feature/<phase>-<feature-name>` (e.g., `feature/phase2-jwt-auth`)
- **Commits**: Atomic, with descriptive messages following Conventional Commits
- **Pull Requests**: Required for all merges; include tests and documentation

### Code Review Standards

- All code MUST be reviewed before merging
- PRs MUST include tests covering new functionality
- Breaking changes MUST be flagged and documented
- AI-generated code MUST be reviewed for correctness and security

---

## Security Requirements

### Data Protection
- All passwords MUST be hashed (bcrypt min cost 12)
- Secrets MUST be stored in environment variables or Dapr secret stores
- Database connections MUST use TLS in production
- API endpoints MUST validate and sanitize all inputs

### API Security
- Rate limiting: 100 requests/minute per user
- CORS policies explicitly defined
- JWT tokens expire after 1 hour; refresh tokens after 7 days
- SQL injection prevention via parameterized queries

### Kubernetes Security
- Non-root container users
- Read-only root filesystems where possible
- Network policies restricting pod-to-pod communication
- Secrets mounted as volumes, not environment variables

---

## Performance Standards

### Phase 2 (Web App)
- API response time: p95 < 200ms
- Database query time: p95 < 50ms
- Frontend initial load: < 2 seconds
- Support: 100 concurrent users

### Phase 4 (Kubernetes)
- Horizontal pod autoscaling: CPU > 70%
- Zero-downtime deployments
- Pod startup time: < 30 seconds

### Phase 5 (Cloud + Kafka)
- Event processing latency: p95 < 500ms
- Kafka throughput: 10,000 events/second
- Support: 10,000 concurrent users
- Availability: 99.9% uptime SLA

---

## Governance

### Amendment Process

1. Propose change via GitHub issue or ADR
2. Team review and discussion (minimum 3 business days)
3. Approval requires consensus or maintainer sign-off
4. Update constitution with version bump
5. Update dependent templates and documentation
6. Communicate changes to all contributors

### Version Semantics

- **MAJOR**: Backward-incompatible principle changes (e.g., removing TDD requirement)
- **MINOR**: New principles or sections added (e.g., adding security principle)
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance

- All PRs MUST verify adherence to phase-appropriate principles
- Quarterly constitution reviews to ensure relevance
- Violations MUST be documented in `plan.md` Complexity Tracking table with justification

### Architectural Decision Records (ADRs)

Significant architectural decisions MUST be documented in `history/adr/` using the ADR template. Examples:
- Choosing Neon PostgreSQL over AWS RDS
- Selecting Kafka vs RabbitMQ for event streaming
- Dapr adoption rationale

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
