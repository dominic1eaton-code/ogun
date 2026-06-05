# ogun OS — Glossary, Acronym System & Naming Conventions

**Document:** `GLOSSARY.md`
**Project:** Ogún · 2026
**Version:** 0.1.0-beta
**Owner:** The Ogun Foundation

---

## Table of Contents

1. [Naming Philosophy](#1-naming-philosophy)
2. [Naming Conventions](#2-naming-conventions)
3. [Acronym System](#3-acronym-system)
4. [Glossary — Core Concepts](#4-glossary--core-concepts)
5. [Glossary — The OS & Architecture](#5-glossary--the-os--architecture)
6. [Glossary — Apps & Platform Systems](#6-glossary--apps--platform-systems)
7. [Glossary — Agent System (Sambara)](#7-glossary--agent-system-sambara)
8. [Glossary — Protocols & Policies](#8-glossary--protocols--policies)
9. [Glossary — The Enterprise Model](#9-glossary--the-enterprise-model)
10. [Glossary — Data, Metrics & Records](#10-glossary--data-metrics--records)
11. [Glossary — People & Roles](#11-glossary--people--roles)
12. [Glossary — Component Types](#12-glossary--component-types)
13. [Enum & Status Reference](#13-enum--status-reference)
14. [Namespace URI Scheme Reference](#14-namespace-uri-scheme-reference)
15. [App Name Quick-Reference](#15-app-name-quick-reference)
16. [Component Acronym & Naming System](#16-component-acronym--naming-system)
17. [Documents Repository](#17-documents-repository)

---

## 1. Naming Philosophy

ogun OS names its systems, protocols, and apps from **Yoruba and West African cultural heritage** — a deliberate, meaningful attribution rooted in the project's founding values of sovereignty, forging, and intelligence.

- **Ogun** — the Yoruba orisha of iron, technology, and creation. The OS embodies the principle of forging raw platform capabilities into a coherent operating environment.
- **Elegua** — the Yoruba orisha of crossroads, communication, and messages. Names the inter-component communication protocol.
- **Ọpọn** — a sacred divination board in Yoruba tradition; in ogun OS it names the cross-enterprise data isolation protocol, representing boundaries that must not be crossed without ceremony.
- **Sambara** — drawn from Swahili traditions of communal intelligence; names the AI agents operating system.
- **Enzo, Kogi, Dongo, Ume, Heshima, Shango, Igi, Akeel, Moto, Zamani, Apapo, Orun, Shaba, Kanna, Qala, Zuri, Didara, Misimu, Ayo** — Yoruba, Swahili, or West African-derived names for the Tier-4 application suite.

Use of these names carries an ongoing obligation of respectful context and attribution.

---

## 2. Naming Conventions

### 2.1 System & Crate Names

| Pattern | Rule | Examples |
|---|---|---|
| **OS components** | `ogun-<domain>` (kebab-case) | `ogun-kernel-core`, `ogun-desktop`, `ogun-shell` |
| **Kernel apps (Tier 1)** | `ogun-<function>` | `ogun-bootloader`, `ogun-session-manager` |
| **OS apps (Tier 2)** | `ogun-<name>` | `ogun-command-center`, `ogun-settings`, `ogun-security` |
| **Utility apps (Tier 3)** | `ogun-<name>` | `ogun-notes`, `ogun-tasks`, `ogun-focus` |
| **User apps (Tier 4)** | Single Yoruba/Swahili word (lowercase) | `enzo`, `kogi`, `dongo`, `sambara` |
| **Drivers** | `ogun-host-<platform>` or `ogun-display-<target>` | `ogun-host-linux`, `ogun-display-tauri` |
| **SDKs** | `ogun-<layer>-sdk` | `ogun-app-sdk`, `ogun-kernel-sdk`, `ogun-driver-sdk` |
| **Protocols** | Proper name, no prefix | Elegua Protocol, Ọpọn Protocol |
| **Rust structs/enums** | PascalCase | `SambaraAgent`, `AgentAuthorityLevel`, `EleguaMessage` |
| **Rust fields & vars** | snake_case | `agent_id`, `workspace_id`, `operator_id` |
| **Config keys (TOML)** | snake_case | `max_restart_attempts`, `ehr_floor_default` |
| **CLI commands** | `<app>.<verb>` (namespaced dot notation) | `sambara.run`, `enzo.kpis`, `dongo.wallet` |
| **IPC channels** | `ipc://<app>/<event>.<action>` | `ipc://kogi/engagement.renewed`, `ipc://dongo/wallet.query` |
| **Telemetry streams** | `telemetry://<domain>/<scope>/<event>` | `telemetry://agents/[enterprise-id]/actions` |
| **VFS paths** | `<namespace>://<id>/<path>` | `agent://sambara/[agent-id]/book.json` |
| **Agent namespaces** | Reverse-DNS: `com.enzo.<system>.<role>` | `com.enzo.kogi.pricing`, `com.enzo.qala.planner` |
| **System policies** | `SYS-<NNN>` | `SYS-001`, `SYS-004`, `SYS-008` |
| **User policies** | `USP-<NNN>` | `USP-001`, `USP-005`, `USP-007` |
| **Package files** | `<component>-<version>-<platform>.ogun` | `ogun-kernel-linux-x86_64-0.1.0-alpha.img` |

### 2.2 Version Numbering

All components use **semantic versioning** (`major.minor.patch[-channel]`):

| Bump | Meaning |
|---|---|
| **major** | Breaking change to public contract, ABI, or schema |
| **minor** | New capability; backward compatible |
| **patch** | Bug fix, model/config update; no redeployment |
| **channel suffix** | `-alpha`, `-beta`, `-canary`, `-stable` |

Example: `v2.1.0-canary`

### 2.3 File Naming

| File Type | Convention | Example |
|---|---|---|
| Specification docs | `<system>-<topic>.md` (kebab-case) | `ogun-architecture-0_1_0-beta.md` |
| Config files | `ogun.toml`, `ogun-component.toml` | `~/.ogun/config/ogun.toml` |
| Agent specs | `ogun-agent.toml` | `ogun-agent.toml` |
| Package bundles | `<id>-<version>.ogun` (ZIP) | `agent-pricing-v2.1.0.ogun` |
| Kernel images | `ogun-kernel-<platform>-<version>.img` | `ogun-kernel-windows-x64-0.1.0-beta.img` |
| Log files | `<domain>-<type>.log` | `agent-actions.log` |

### 2.4 Identifier Conventions

| Identifier | Format | Example |
|---|---|---|
| `agent_id` | UUID v4 | `"3f4a2b1c-..."` |
| `message_id` | UUID v7 (time-ordered) | `"01936..."` |
| `session_id` | UUID v4 | `"a2f1..."` |
| `trace_id` | UUID v4 | `"b3e2..."` |
| `workspace_id` | Slug: `<name>-<shortid>` | `"design-studio-4f2a"` |
| `enterprise_id` | Slug: `@handle` or UUID | `"accenture-portal"` |
| `operator_id` | UUID or `@handle` | `"@eatondo"` |
| `model_id` | `<provider>-<model>-<version>` | `"claude-sonnet-4-6"` |
| `build_hash` | SHA-256 hex prefix | `"sha256:a3f4b2..."` |

---

## 3. Acronym System

### 3.1 Core Platform Acronyms

| Acronym | Full Form | Context |
|---|---|---|
| **OS** | Operating System | The ogun OS platform itself |
| **IPC** | Inter-Process Communication | The message bus between all components |
| **EMF** | Elegua Message Format | The wire format for all IPC messages |
| **VFS** | Virtual Filesystem | The semantic namespace-based filesystem layer |
| **ABI** | Application Binary Interface | The stable contract between kernel and apps (`OGUN_ABI_VERSION`) |
| **SDK** | Software Development Kit | The layer-specific development libraries (`ogun-app-sdk`, etc.) |
| **JIT** | Just-In-Time | JIT compilation mode for development hot-patching |
| **PID** | Process Identifier | The kernel's unique numeric identifier for every running process |
| **OPM** | ogun Package Manager | The CLI for installing, updating, and removing `.ogun` packages |
| **OBA** | ogun AI Assistant | The bundled conversational AI agent (Tier-3 utility app) |
| **PCC** | Portfolio Control Center | The enterprise switching and management surface in the Command Center |
| **DAG** | Directed Acyclic Graph | Used in agent dependency and build graph management |
| **SLA** | Service Level Agreement | Declared latency/availability targets for agents and services |
| **CLI** | Command Line Interface | The shell-based management surface |
| **API** | Application Programming Interface | External service interfaces (Anthropic, OpenAI, etc.) |
| **WASM** | WebAssembly | The browser compilation target for ogun OS |
| **MDM** | Master Data Management | The canonical, deduplicated record system (for operators, agents) |
| **REPL** | Read-Eval-Print Loop | The interactive shell runtime |
| **PKI** | Public Key Infrastructure | Certificate and key management in `ogun-security` |
| **RBAC** | Role-Based Access Control | Permission model used in Heshima |
| **ABAC** | Attribute-Based Access Control | Fine-grained permission model used in Heshima |
| **SOP** | Standard Operating Procedure | Documented procedures in Ume and Enzo |
| **OKR** | Objectives and Key Results | Goal framework used in Shaba and Enzo |
| **KPI** | Key Performance Indicator | Tracked metrics in the Observatory/Qala |
| **MRR** | Monthly Recurring Revenue | Monthly total income; headline metric in the Command Center |
| **TPV** | Total Portfolio Value | Estimated aggregate value of all portfolio assets |
| **EPV** | Expected Pipeline Value | `Σ(proposal_value × win_probability)` across all active pipelines |
| **EHR** | Effective Hourly Rate | Total income ÷ total invested hours (including non-billable) |
| **FI** | Financial Independence | Target state tracked by Dongo's FI calculator |
| **FIRE** | Financial Independence, Retire Early | FI calculation mode in Dongo |
| **BMC** | Business Model Canvas | Strategic design tool in Shaba |
| **BoM** | Bill of Materials | Component list for complex solutions in Shango |
| **GMV** | Gross Merchandise Value | Total transaction volume in Zuri marketplace |
| **RLHF** | Reinforcement Learning from Human Feedback | Learning mode where agent models update from operator approvals/rejections |
| **LLM** | Large Language Model | The foundation model type used by most Sambara agents |
| **PII** | Personally Identifiable Information | Data requiring special protection in context injection pipelines |
| **FBAR** | Foreign Bank Account Report | Compliance obligation tracked in Dongo digital assets |
| **FATCA** | Foreign Account Tax Compliance Act | International tax compliance tracked in Dongo |
| **HSA** | Health Savings Account | Benefits account tracked in Dongo |
| **FSA** | Flexible Spending Account | Benefits account tracked in Dongo |
| **HRA** | Health Reimbursement Arrangement | Benefits account tracked in Dongo |
| **ICP** | Ideal Client Profile | The target client definition used by the Acquisition Agent |
| **CMM** | Capability Maturity Model | Assessment framework used in Shaba |
| **CMMI** | Capability Maturity Model Integration | Extended CMM framework reference in Shaba |
| **ECE** | Expected Calibration Error | Model evaluation metric in Sambara Learning |
| **HTN** | Hierarchical Task Networks | Planning algorithm used by PLANNER agents |
| **MCTS** | Monte Carlo Tree Search | Planning algorithm used for uncertain environments |
| **PPO** | Proximal Policy Optimization | RL training algorithm used in Sambara Learning |
| **SAC** | Soft Actor-Critic | RL training algorithm used in Sambara Learning |

### 3.2 Agent System Acronyms

| Acronym | Full Form | Context |
|---|---|---|
| **OBSERVE** | Observe (authority level) | Read-only agent mode; no actions taken |
| **RECOMMEND** | Recommend (authority level) | Agent drafts proposals; human decides |
| **EXECUTE_BOUNDED** | Execute Bounded (authority level) | Agent executes within declared parameter ranges |
| **FULL_AUTONOMY** | Full Autonomy (authority level) | Agent operates within policy; humans set goals only |
| **L0–L3** | Autonomy Levels 0–3 | Internal numeric representation of authority levels |
| **AGM** | Agent Group Member | A single agent within a coordination group |

### 3.3 Policy Acronyms

| ID | Full Name | Summary |
|---|---|---|
| **SYS-001** | Ọpọn Cross-Enterprise Data Isolation | Agents/apps cannot access another enterprise's data without logged consent |
| **SYS-003** | Revenue Attribution Integrity | All financial actions must carry valid attribution IDs |
| **SYS-004** | Agent Authority Bounds | Agents cannot exceed their declared authority level |
| **SYS-006** | Capability-Based Process Authorization | Every action is capability-checked before execution |
| **SYS-007** | Identity Profile Isolation | Heshima profiles cannot be cross-contaminated |
| **SYS-008** | Operator Data Boundary | Agent actions are bounded to the owning operator's data scope |
| **USP-001** | Rate/Yield Floor | Pricing Agent cannot recommend rates below EHR floor |
| **USP-003** | Pipeline Health Floor | Acquisition Agent activates when EPV < 1.5× monthly target |
| **USP-005** | Stale Deal Follow-Up | Follow-up Agent activates when deal stage age > 7 days |
| **USP-006** | Attribution Integrity | Bookkeeping Agent dispatched when unattributed transactions exist |
| **USP-007** | Burnout Protection | Acquisition Agent blocked when effort utilization > 90% |

---

## 4. Glossary — Core Concepts

**Personal Enterprise**
The management of one's career and skills as an independent business — a portfolio of freelance projects, contracts, and entrepreneurial ventures, powered by technology and automation to achieve maximum autonomy and financial control. The foundational concept ogun OS is designed to serve.

**Independent Worker**
The primary user persona of ogun OS. Encompasses freelancers, consultants, creators, founders, contractors, investors, and gig workers. Anyone operating a personal enterprise without a traditional employer structure.

**CNO (Chief Navigation Officer)**
A persona type representing an operator who runs multiple enterprises simultaneously as a single optimized system, tracking cross-enterprise synergies in real time.

**Sovereign Personal Enterprise OS**
The product category coined by ogun OS: a locally-installed, cryptographically verified, capability-gated operating environment in which every independent worker can structure their enterprises, engagements, assets, agents, and value production as a first-class system concern — enforced at the kernel boundary.

**Shock Insight**
The first personalized, data-backed intelligence insight delivered to an operator after warm-start onboarding. It reveals the operator's actual EHR, pipeline health, and revenue patterns versus their declared targets. A milestone event in the operator lifecycle (`COLD → ACTIVATED` transition). Generated by the Observatory Agent.

**Compounding**
A design principle throughout the platform: every action should improve the quality of all future actions. Tracked in the Compounding Registry (agent layer) and modeled in the enterprise value formula as `compounding_factor`. Compounding effects are explicitly modeled, measured, and optimized.

**Scaffold Pattern / Scaffold Detection**
The detection of a repeatable service: the same service type delivered ≥ 4 times in 180 days with average EHR ≥ the EHR floor. Triggers the Productization Agent. Identifies the moment a service is repeatable enough to productize.

**Hypergrid**
The distributed, multi-node runtime fabric managed by the `apapo` app. Enables ogun OS instances and enterprises to communicate across a decentralized network. Governed by the Distributed Elegua Message format.

**OgunNet**
The peer-to-peer network layer within ogun OS (v2.0.0). The underlying transport for Hypergrid communication.

**RustyDB**
The Rust-native embedded database used by ogun OS for session state, audit indexes, node identity, and module registry. A core infrastructure component.

**Workspace**
An isolated, persistent, enterprise-aware runtime context that scopes all OS activity — processes, files, agents, telemetry, and layout — to a specific operational domain. Every process in ogun OS carries `workspace_context` as a first-class metadata field, enforced at the kernel level.

**Operator**
The authenticated human user of ogun OS. Synonymous with the independent worker in most contexts. Operators own enterprises, set goals, configure agents, and approve agent actions. An operator has a role: `OWNER`, `ADMIN`, `MEMBER`, or `VIEWER`.

---

## 5. Glossary — The OS & Architecture

**ogun OS**
A programmable operating environment for independent workers. Organizes enterprises, engagements, assets, workflows, agents, intelligence systems, and value production — not merely files, applications, and windows. Written in Rust; runs on Windows, Linux, macOS, Browser (WASM), Android, and iOS.

**ogun-bootloader**
The first ogun program to execute on startup. Bridges the inert host OS and the live ogun runtime. Validates the cryptographic signature of the kernel image and passes control to `ogun-kernel-core`.

**ogun-kernel-core**
The central orchestration kernel. Contains 15 subsystems: Process Manager, Scheduler, IPC Manager, Memory Manager, Storage Manager, File Manager, Security Manager, Services Manager, Session Manager, Modules Manager, Network Manager, Telemetry Manager, and others. The most critical component in the entire system.

**Elegua Protocol**
The unified inter-component communication specification for ogun OS. Named after the Yoruba orisha of crossroads and messages. All communication between components — apps, agents, kernel — uses this protocol via the IPC bus.

**Elegua Message Format (EMF)**
The wire format for all IPC messages. Carries `operator_id`, `workspace_id`, `agent_id`, `trace_id`, and `span_id` on every message. Context is never stripped. See Section 8 for the full protocol entry.

**Virtual UEFI / Boot Chain**
The three-stage boot verification pipeline in ogun OS: (1) image signature validation, (2) manifest integrity check, (3) host key re-derivation. Failure at any stage halts boot. Implemented by `ogun-bootloader` and `ogun-image-builder`.

**Capability-Based Security**
The ogun OS security model. Every process is granted an explicit whitelist of capabilities. Any action not in the whitelist is denied by default by the Security Manager at every IPC boundary. Cannot be bypassed.

**`ogun-component.toml`**
The manifest file for every ogun OS component (.ogun package). Declares the component's `kind` (driver, module, plugin, extension, app), version, dependencies, capabilities, and platform targets.

**`.ogun` Package**
The distribution format for all ogun OS components. A signed ZIP archive containing the component manifest, binary or library, configuration, and metadata. Installed by `opm` (ogun Package Manager).

**CleanShutdownMarker**
The final write performed during an ogun OS shutdown. Its absence on next boot indicates an unclean shutdown and triggers crash recovery by the Session Manager.

**NativeAppManager**
The central registry of all native ogun apps loaded by the kernel. Manages load, tick, deliver, unload, hot-reload, and JIT-reload for all running apps. Native apps start at PID 1000.

**Hot Reload**
The mechanism by which a running app is updated to a new binary without restarting the kernel or losing process state. The app's state is snapshotted, the library is swapped, and state is restored.

**Scheduler**
A kernel subsystem managing cooperative and priority-based execution of all processes. Supports FIFO, priority, fair share, deadline, and adaptive policies.

**IPC Manager**
A kernel subsystem managing typed message channels, event buses, pub/sub streams, and request-response messaging between all processes via the Elegua Protocol.

**File Manager / VFS**
The kernel subsystem managing the Virtual Filesystem and resolving semantic namespace URIs (`enterprise://`, `agent://`, `workspace://`, etc.) to actual storage paths.

**Security Manager**
The kernel subsystem enforcing capability-based permissions. Validates capability grants at every IPC boundary. Holds the `AuditLogAppend` capability exclusively — no agent or app can write to the audit log directly.

**Telemetry Manager**
The kernel subsystem providing integrated tracing, metrics, structured logs, and runtime diagnostics across all components.

---

## 6. Glossary — Apps & Platform Systems

### Tier 1 — Kernel Apps

| App | Full Name |
|---|---|
| `ogun-bootloader` | ogun Bootloader |
| `ogun-kernel-core` | ogun Kernel Core Runtime |
| `ogun-image-builder` | ogun Image Builder |
| `ogun-installer` | ogun Installer |
| `ogun-session-manager` | ogun Session Manager |
| `ogun-system-manager` | ogun System Manager |

### Tier 2 — OS Apps

| App | Full Name |
|---|---|
| `ogun-desktop` | ogun Desktop Environment |
| `ogun-shell` | ogun Shell (REPL) |
| `ogun-explorer` | ogun File Explorer |
| `ogun-command-center` | ogun Command Center |
| `ogun-settings` | ogun Settings Center |
| `ogun-profile` | ogun Profile Center |
| `ogun-security` | ogun Security Center |
| `ogun-command-palette` | ogun Command Palette |
| `ogun-workspaces` | ogun Workspaces |
| `ogun-namespaces` | ogun Namespace Manager |
| `ogun-app-manager` | ogun App Manager |
| `ogun-ui` | ogun UI Design System |
| `ogun-operator` | ogun Operator Center |

### Tier 3 — Utility Apps

| App | Full Name |
|---|---|
| `ogun-notes` | ogun Notes |
| `ogun-tasks` | ogun Tasks |
| `ogun-focus` | ogun Focus |
| `ogun-schedule` | ogun Schedule |
| `ogun-messenger` | ogun Messenger |
| `ogun-search` | ogun Search |
| `ogun-assistant` | ogun AI Assistant (OBA) |
| `ogun-contacts` | ogun Contacts |

### Tier 4 — User Apps (Personal Enterprise Suite)

See [Section 15 — App Name Quick-Reference](#15-app-name-quick-reference) for the full table.

---

## 7. Glossary — Agent System (Sambara)

**Sambara**
The AI agents operating system embedded within ogun OS. Named from the Swahili tradition of communal intelligence. Provides the complete runtime, lifecycle, governance, coordination, learning, and optimization infrastructure for all AI agents. Consists of eight engines: `sambara-kernel`, `sambara-coordinator`, `sambara-registry`, `sambara-data`, `sambara-learning`, `sambara-intelligence`, `sambara-optimizer`, `sambara-governance`.

**SambaraAgent**
The universal abstract root model. Every agent — regardless of domain or purpose — is an instance of `SambaraAgent`. Platform-specific behavior is expressed through configuration, model bindings, and permission grants — not through structural divergence from the root model.

**Agent**
An instance of `SambaraAgent` — a managed AI entity with declared perception, reasoning, action, memory, learning, communication, and governance configurations, operating within operator-declared authority bounds.

**Agent Authority Level**
The permission ceiling for an agent's autonomous action. Four levels, in ascending order:
- **OBSERVE** — read-only; no actions taken; generates MetricSnapshots and learning signals
- **RECOMMEND** — drafts proposals for operator review; humans decide whether to act
- **EXECUTE_BOUNDED** — executes within explicitly declared parameter ranges; exceptions escalate
- **FULL_AUTONOMY** — operates within declared domain without per-action approval; humans set goals

Authority escalation cannot be triggered by agent logic — it requires explicit operator interaction.

**Agent Book**
The complete, versioned, append-only container of all information, metadata, and content pertaining to a specific agent — from design through retirement. Stored at `agent://sambara/[agent-id]/book.json`. Analogous to a personnel file for an AI agent.

**AgentSpec**
The design-time specification of an agent — the complete declaration of its identity, perception, reasoning, action, model binding, memory, learning, communication, and governance requirements.

**AgentConfig**
The compiled, immutable runtime configuration produced by the agent build pipeline from the `AgentSpec`, resolved dependencies, and injected governance policies.

**AgentPackage**
The deployable artifact produced by the agent build pipeline — a signed `.ogun` bundle containing the `AgentConfig`, model references, tool bindings, memory schema, and policy manifest.

**Agent Driver**
The interface layer between the Sambara inference serving system and an external LLM or AI model provider. Translates the platform's canonical `InferenceRequest` into the provider's wire format. Built-in drivers: `anthropic-claude`, `openai-chatgpt`, `deepseek`, `ollama-local`. Custom drivers are registered via the `AiBackend` plugin hook.

**GovernanceConfig**
The governance block injected into every agent at initialization time. Read-only to the agent. Contains: autonomy level, policy bindings, permission grants, data access rules, boundary rules, and audit configuration. Agents cannot inspect, modify, or bypass it.

**Agent Bus**
The dedicated event fabric for agent communication within the Sambara runtime. Accessible only with `AgentBusAccess` capability. All agent-to-agent communication is event-routed through this bus — direct agent-to-agent calls are prohibited.

**Agent Group**
A bounded set of agents working together toward a shared goal under a declared coordination protocol. Eight protocols: Pipeline, Parallel, Loop, Hierarchy, Consensus, Auction, Blackboard, Market.

**Coordination Protocol**
The protocol governing how agents in a group work together:
- **Pipeline** — sequential; A → B → C
- **Parallel** — concurrent; A, B, C simultaneously → Aggregator
- **Loop** — cyclic; Planner → Analyst → Optimizer → Executor → Observer → Learner → [repeat]
- **Hierarchy** — Coordinator decomposes goals; Workers execute; results aggregated
- **Consensus** — all agents must agree before action; ARBITER resolves disagreements
- **Blackboard** — shared state board; agents coordinate through state, not direct messages
- **Auction** — agents bid for tasks based on capability fit
- **Market** — internal market with task pricing and supply/demand dynamics

**Sambara Kernel (`sambara-kernel`)**
The agent OS runtime. Manages agent lifecycle, memory, scheduling, permissions, execution sessions, and health monitoring.

**Sambara Coordinator (`sambara-coordinator`)**
The multi-agent orchestration engine. Manages agent groups, coordination protocols, fleet scheduling, and collective behavior.

**Sambara Registry (`sambara-registry`)**
The authoritative catalog of all agents. Manages versioning, dependency graphs, impact analysis, and fleet view. The single source of truth for all agent identity and configuration data.

**Sambara Learning (`sambara-learning`)**
The ML and learning engine. Seven subsystems: registry, train, evaluate, serve, experiment, update, monitor. Manages model training, serving, continuous learning, drift detection, and experiment tracking.

**Sambara Intelligence (`sambara-intelligence`)**
The higher-order reasoning engine. Manages structured reasoning, goal-directed planning, knowledge graph, and decision modeling.

**Sambara Optimizer (`sambara-optimizer`)**
The optimization engine. Manages goal optimization, resource allocation, sequence planning via A*, and compounding effect modeling.

**Sambara Governance (`sambara-governance`)**
The policy, permissions, autonomy, and audit engine. Enforced at the OS layer. Agents cannot bypass it.

**Compounding Registry**
The platform-maintained mapping of action types to estimated compounding factors. Used by `sambara-optimizer` to prefer high-compounding actions when all else is equal.

**Effectiveness Score**
A 0.0–1.0 rolling score (30-day window) measuring how reliably an agent's actions produce positive enterprise state changes. Computed from `PolicyOutcome` records. Used for authority progression decisions. Required to be > 0.75 over 10+ firings before `FULL_AUTONOMY` can be granted.

**PolicyOutcome**
The recorded result of a policy-triggered agent action. Includes: metric state at fire time, action taken, approval decision, and 30-day post-fire metric delta.

**Agent Session**
An isolated execution context for a single agent activation. Each session has a unique `session_id`. A crash in one session does not affect other sessions. Working memory is session-scoped and cleared on session end.

**GoalWeightVector**
The operator-declared weighting across the four value dimensions: `α` (income), `β` (asset growth), `γ` (passive income ratio), `δ` (network). Used by the Optimizer to score and rank agent action candidates.

**Feature Store**
The bridge between raw enterprise data and ML model training/serving. Provides online (< 10ms p99) and offline serving modes. Managed by `sambara-data.features`.

**Drift Detection**
Continuous monitoring of models for data drift, concept drift, and label drift. Triggers retraining when drift exceeds the configured threshold. Managed by `sambara-learning.monitor`.

**Agent Enterprise Maturity Progression**
The lifecycle stages through which an agent's authority expands as the enterprise matures and effectiveness is demonstrated:
`COLD → ACTIVATED → CALIBRATING → INTELLIGENT → OPTIMIZED → COMPOUNDING`

### Named Domain Agents

| Agent | Namespace | Role | Default Authority |
|---|---|---|---|
| **FOLLOWUP_AGENT** | `com.enzo.kogi.followup` | Stale deal follow-up; proposal re-engagement | RECOMMEND |
| **PRICING_AGENT** | `com.enzo.kogi.pricing` | Rate adjustment within operator floor/ceiling | RECOMMEND → EXECUTE_BOUNDED |
| **EXECUTION_AGENT** | `com.enzo.kogi.execution` | Task scheduling and delivery reminders | EXECUTE_BOUNDED |
| **ACQUISITION_AGENT** | `com.enzo.kogi.acquisition` | Outreach when pipeline falls below health floor | EXECUTE_BOUNDED |
| **BOOKKEEPING_AGENT** | `com.enzo.kogi.bookkeeping` | Transaction reconciliation and attribution | EXECUTE_BOUNDED |
| **OBSERVATORY_AGENT** | `com.enzo.kogi.observatory` | Daily MetricSnapshot generation; insight surfacing | OBSERVE |
| **PRODUCTIZATION_AGENT** | `com.enzo.kogi.productization` | Scaffold detection; packaging initiation | EXECUTE_BOUNDED |
| **QALA_PLANNER** | `com.enzo.qala.planner` | Build graph generation for product construction | EXECUTE_BOUNDED |
| **QALA_EXECUTOR** | `com.enzo.qala.executor` | Execution of builds via the Factory System | EXECUTE_BOUNDED |
| **ESTATE_AGENT** | `com.enzo.zamani.estate` | Estate intelligence, maintenance, monetization | OBSERVE → RECOMMEND |
| **ATTRIBUTION_AGENT** | `com.enzo.ume.attribution` | Revenue attribution in agent-initiated transactions | EXECUTE_BOUNDED |
| **LIFECYCLE_AGENT** | `com.enzo.lifecycle` | State machine transitions across all platform systems | EXECUTE_BOUNDED |
| **ORCHESTRATION_AGENT** | `com.enzo.orchestration` | Cross-system workflow routing | COORDINATOR |
| **PRIVACY_AGENT** | `com.enzo.privacy` | Ọpọn Protocol enforcement in agent-initiated flows | GOVERNANCE |

---

## 8. Glossary — Protocols & Policies

**Elegua Protocol**
The unified inter-component communication specification for ogun OS. Every cross-boundary message carries `operator_id`, `workspace_id`, `agent_id`, and `trace_id`. Context is never stripped. All communication between apps, agents, and the kernel flows through this protocol via the IPC bus.

**Ọpọn Protocol (SYS-001)**
The cross-enterprise data isolation protocol. Named after the sacred Yoruba divination board. Three core rules:
- **`opn-001`** — Operator Data Isolation: an agent/app in enterprise A cannot read/write enterprise B without `CrossEnterpriseRead/Write` capability + a logged, valid, non-expired consent record
- **`opn-002`** — Financial Data Protection: financial records require a separate, financial-specific consent record; a general cross-enterprise consent does not grant financial data access
- **`opn-003`** — Agent Authority Bounds: no agent may execute any action exceeding its declared authority level
- **`opn-004`** — Write-Before-Act Audit: the audit record is written before the action completes; if the write fails, the action is aborted; no action can occur without an audit record
- **`opn-005`** — Plugin Approval Gate: plugins providing AI backends require operator approval before loading

**Policy Engine**
The system component responsible for evaluating the full policy equation `π_total(S) = compose(π_system, π_user, π_agent)` and dispatching policy actions (e.g., activating agents, surfacing insights). Precedence: `SYSTEM > USER > AGENT`.

**System Policy (SYS-NNN)**
Unconditional platform invariants enforced at the kernel level. Cannot be overridden by any operator or agent action. See [Section 3.3](#33-policy-acronyms) for the full list.

**Universal Starter Policy Set (USP-NNN)**
User-layer policies provisioned to all operators by default. Can be modified by operators within the bounds of system policies. See [Section 3.3](#33-policy-acronyms) for the full list.

**Agent Policy Domain**
The seven policy domains governing agent behavior: `AGENT.CAPABILITY`, `AGENT.AUTONOMY`, `AGENT.DATA`, `AGENT.BOUNDARY`, `AGENT.RATE`, `AGENT.FINANCIAL`, `AGENT.GOVERNANCE`.

**Consent Record**
A logged, valid, non-expired record granting an agent or app permission to cross enterprise boundaries. Required for `CrossEnterpriseRead`, `CrossEnterpriseWrite`, and financial data access. Must be explicitly created by an operator.

---

## 9. Glossary — The Enterprise Model

**The Enterprise Value Formula**
The mathematical model of a personal enterprise as a closed-loop value transformation system:
```
Enterprise(t) = f(Identity(I), State(S), Production(P), Allocation(A), Exchange(E), Feedback(F))
```

**Enterprise Lifecycle Stages**
The progression of a personal enterprise as it matures on the platform:

| Stage | Description |
|---|---|
| **COLD** | No data; all agents at OBSERVE only |
| **ACTIVATED** | Onboarding complete; Bookkeeping and Follow-up agents active |
| **CALIBRATING** | 7+ days of data; Pricing Agent at RECOMMEND; Follow-up at EXECUTE_BOUNDED |
| **INTELLIGENT** | 90+ days; Pricing Agent at EXECUTE_BOUNDED; Acquisition and Execution agents active |
| **OPTIMIZED** | Pricing Agent at FULL_AUTONOMY (if effectiveness ≥ 0.75); Productization Agent active |
| **COMPOUNDING** | Long track record; all agents at highest earned authority; passive income growing |

**Engagement**
A state machine representing active client work in the production pipeline. The successor to the word "project" in the ogun OS vocabulary. Engagements have lifecycle states managed by Kogi.

**Artifact**
The produced output of an engagement — the deliverable. Tracked and registered in the system. An Artifact can graduate to become an Asset.

**Asset**
A portfolio item with value and revenue attribution. Artifacts can graduate to Assets when they represent ongoing value (e.g., a productized service, a digital product). Tracked in Igi.

**EHR Floor**
The operator-declared minimum Effective Hourly Rate below which the Pricing Agent will not recommend rates. Enforced by `USP-001`. Prevents underpricing.

**Pipeline Health Floor**
The minimum Expected Pipeline Value (EPV) target, expressed as a multiple of the monthly income target (default: 1.5×). When EPV falls below this threshold, `USP-003` activates the Acquisition Agent.

**MetricSnapshot**
A structured, timestamped snapshot of all enterprise KPIs generated by the Observatory Agent on a scheduled basis (default: daily at 06:00). The primary data output of the OBSERVE authority level.

**InsightRecord**
A structured recommendation generated by an agent — containing the triggering signal, reasoning, evidence, expected impact (confidence-banded), and proposed action. Surfaced in the Observatory/Enzo intelligence feed for operator review.

**Hub**
A multi-operator collaborative enterprise context. Used in cross-enterprise revenue sharing and team engagements. Hub communications honor the Ọpọn Protocol — raw enterprise data never crosses partition boundaries.

**The Four Value Dimensions**
The axes of the operator's `GoalWeightVector`:
- **α (alpha)** — Income: active revenue from engagements
- **β (beta)** — Asset Growth: portfolio appreciation and new asset creation
- **γ (gamma)** — Passive Ratio: proportion of income from non-time-traded sources
- **δ (delta)** — Network: relationship capital and referral value

---

## 10. Glossary — Data, Metrics & Records

**AgentAuditRecord**
The immutable record of every significant agent action. Written before the action completes (write-before-act per `opn-004`). Stored in `~/.ogun/logs/agent-actions.log` (encrypted, append-only). Cannot be deleted by any component.

**AgentChangeRecord**
An immutable record capturing every change to any agent's configuration, authority, or model. Stored in `agent://sambara/[agent-id]/changes/`. Never deleted.

**PerformanceSummary**
A periodic snapshot of an agent's operational metrics: activation count, success rate, mean latency, effectiveness score, compounding contribution, human approval/rejection rates, and policy violation count.

**ModelRegistryEntry**
The complete provenance record for a model artifact: training metadata, evaluation results, SHA-256 integrity hash, serving configuration, lineage, and current status.

**EngagementRecord**
The master data record for a client engagement in Kogi. Includes pipeline stage, value, EHR, renewal dates, and relationship health signals.

**TransactionRecord**
A financial transaction record in Dongo. All agent-initiated transactions must carry valid attribution (`enterprise_id`, `engagement_id`, or `artifact_id`) per `SYS-003`.

**WorkspaceRecord**
The full data record for a workspace, including enterprise linkage, KPIs, agent assignments, member roles, VFS root, and layout state. Versioned.

**OperatorRecord**
The canonical, deduplicated master data record for an operator. The single source of truth for all identity, configuration, and preference data across the platform.

**KnowledgeContribution**
A record of what a specific agent has added to the enterprise knowledge graph — detected patterns, identified relationships, and insights that have proven durable.

**SignalRecord**
An anomaly, trend, or threshold breach detected by an agent in OBSERVE mode. Feeds into the Observatory intelligence system.

---

## 11. Glossary — People & Roles

**Operator**
The authenticated human user of ogun OS. Owner of one or more personal enterprises. Has a role (`OWNER`, `ADMIN`, `MEMBER`, `VIEWER`) that determines what they can do within a workspace or enterprise.

**Executor**
A configured automated agent or delegation entity that acts on behalf of an operator within declared bounds. Registered in Heshima with scope, time limits, and revocation controls.

**Maintainer**
The `operator_id` or "system" identity responsible for a specific agent in the registry.

**Workspace Member**
An operator granted access to a specific workspace. Roles: `OWNER` (full control), `ADMIN` (configure, deploy), `MEMBER` (approve/reject agent proposals, view logs), `VIEWER` (read-only).

**Hub Member**
An operator participating in a multi-operator Hub enterprise context. Hub revenue splits are managed by the Attribution Agent.

---

## 12. Glossary — Component Types

**Driver**
A Rust `rlib` crate statically linked into the kernel binary at compile time. The only component permitted to call native host platform APIs directly. Two types: Host Driver (`OgunHostDriver`) and Display Driver (`OgunDisplayDriver`). Cannot be loaded/unloaded at runtime.

**Module**
A Rust `cdylib` loaded by the Kernel Modules Manager at boot. Extends kernel capabilities with kernel-level access. Cannot call upward into plugins, extensions, or apps. Lives in `~/.ogun/modules/`.

**Plugin**
A Rust `cdylib` loaded by the OS Runtime Loader. Adds a self-contained, isolated feature to the ogun OS runtime without modifying core OS behavior. Attaches to declared `PluginHook` points. Does not require operator approval (unlike extensions).

**Extension**
A Rust `cdylib` loaded by the OS Runtime Loader. Actively modifies or replaces core OS runtime behavior. Requires **explicit operator approval** before loading. Must restore all modified defaults on shutdown.

**Shell Package**
A Plugin subtype that adds commands to the ogun shell REPL. The lightest-weight extensibility mechanism. Commands follow the format `<package-id>.<verb>`. Compiled to `cdylib`, distributed as a `.ogun` bundle.

**Kernel App (Tier 1)**
A core runtime infrastructure component. Runs at kernel privilege. Forms the foundation every other tier depends on. Examples: `ogun-bootloader`, `ogun-kernel-core`.

**OS App (Tier 2)**
An operator-facing platform surface component. Forms the desktop, shell, file system interface, and administrative tools. Managed by the OS Session Manager.

**Utility App (Tier 3)**
A lightweight, always-available productivity tool. Surfaces in the Utility Bar of the desktop. Examples: `ogun-notes`, `ogun-tasks`, `ogun-focus`.

**User App (Tier 4)**
A full software-defined enterprise operating system for a specific domain of independent work. The personal enterprise suite. Examples: `enzo`, `kogi`, `dongo`, `sambara`.

**Service**
A long-running daemon process managed by the Services Manager. Registered in the service registry, addressable via `service://` namespace.

---

## 13. Enum & Status Reference

### Agent Types
`PLANNER` · `ANALYST` · `OPTIMIZER` · `EXECUTOR` · `OBSERVER` · `LEARNER` · `COORDINATOR` · `ROUTER` · `ARBITER` · `AGGREGATOR` · `GOVERNANCE` · `META` · `DOMAIN`

### Agent Status
`DRAFT` · `STAGED` · `ACTIVE` · `IDLE` · `RUNNING` · `LEARNING` · `PAUSED` · `DEGRADED` · `FAILED` · `DEPRECATED` · `RETIRED`

### Agent Authority Levels
`OBSERVE` · `RECOMMEND` · `EXECUTE_BOUNDED` · `FULL_AUTONOMY`

### Autonomy Levels (numeric)
`LEVEL_0` (pure assist) · `LEVEL_1` (assisted) · `LEVEL_2` (supervised) · `LEVEL_3` (autonomous)

### Reasoning Types
`REACTIVE` · `DELIBERATIVE` · `PROBABILISTIC` · `GRAPH` · `HYBRID`

### Learning Modes
`SUPERVISED` · `REINFORCEMENT` · `SELF_SUPERVISED` · `HUMAN_FEEDBACK` · `HYBRID`

### Model Types
`LLM` · `CLASSIFIER` · `REGRESSOR` · `RANKER` · `EMBEDDER` · `GRAPH_NN` · `REINFORCEMENT` · `BAYESIAN` · `ENSEMBLE` · `HYBRID`

### Model Status
`DRAFT` · `STAGING` · `PRODUCTION` · `SHADOW` · `DEPRECATED` · `ARCHIVED`

### Coordination Protocols
`PIPELINE` · `PARALLEL` · `LOOP` · `HIERARCHY` · `CONSENSUS` · `AUCTION` · `BLACKBOARD` · `MARKET`

### Trigger Types
`EVENT` · `SCHEDULE` · `POLLING` · `WEBHOOK`

### Deployment Environments
`SANDBOX` · `STAGING` · `CANARY` · `PRODUCTION` · `DARK`

### Deployment Strategies
`ROLLING` · `BLUE_GREEN` · `CANARY` · `SHADOW`

### Agent Runtime Status
`RUNNING` · `IDLE` · `ERROR` · `SUSPENDED`

### Process Lifecycle
`CREATED` → `INITIALIZED` → `RUNNING` → `SUSPENDED` → `TERMINATED`

### Workspace Status
`DRAFT` · `ACTIVE` · `PAUSED` · `CLOSING` · `ARCHIVED`

### Workspace Priority
`LOW` · `MEDIUM` · `HIGH` · `CRITICAL`

### Health Signal
`HEALTHY` · `WARNING` · `DEGRADED` · `CRITICAL`

### Enterprise Lifecycle
`COLD` · `ACTIVATED` · `CALIBRATING` · `INTELLIGENT` · `OPTIMIZED` · `COMPOUNDING`

### Action Reversibility
`REVERSIBLE` · `IRREVERSIBLE` · `TIME_WINDOWED`

### Agent Driver Providers
`ANTHROPIC` · `OPENAI` · `DEEPSEEK` · `OLLAMA` · `CUSTOM`

### Notification Channels
`IN_APP` · `EMAIL` · `SMS` · `PUSH`

### Process Kind
`NativeApp` · `Service` · `KernelTask` · `SystemAgent`

### Message Kind
`AgentAuthRequest` · `AgentAuthResponse` · `ShutdownRequest` · `Ping` · `Data` · `Notification` · `Custom`

---

## 14. Namespace URI Scheme Reference

| Prefix | Scope | Example |
|---|---|---|
| `enterprise://` | Enterprise-scoped resources and data | `enterprise://accenture-portal/finance/` |
| `asset://` | Portfolio-registered asset objects | `asset://[asset-id]/` |
| `artifact://` | Produced deliverable objects | `artifact://[id]/` |
| `operator://` | Operator-owned identity data | `operator://[id]/profile` |
| `agent://` | Agent state and execution records | `agent://sambara/[agent-id]/book.json` |
| `workspace://` | Workspace runtime context | `workspace://[id]/session/` |
| `service://` | System service registration | `service://sambara-registry/manifest.json` |
| `system://` | OS runtime and kernel state | `system://security/audit/` |
| `ipc://` | IPC channels and message buses | `ipc://kogi/engagement.renewed` |
| `telemetry://` | Telemetry and metric streams | `telemetry://agents/[enterprise-id]/actions` |
| `config://` | Configuration values | `config://ogun/agents/defaults` |
| `temp://` | Transient scratch space (auto-cleaned) | `temp://session/[id]/` |

### Agent VFS Path Structure
```
agent://sambara/[agent-id]/
├── book.json                   — complete Agent Book
├── spec/current.yaml           — current agent specification
├── working/                    — ephemeral session context
├── episodic/                   — past execution records
├── semantic/                   — knowledge contributions
├── shared/                     — signals exposed to other agents
├── log/[YYYY-MM-DD]            — daily action log
├── governance/current.json     — current governance config
└── authority/changes.json      — authority change history
```

---

## 15. App Name Quick-Reference

| App Name | Full Name | Domain |
|---|---|---|
| **enzo** | Personal Enterprise Management System | Enterprise structure, programs, projects, operations |
| **kogi** | Software-Defined Office Management System | Workspace, effort, attention, filtering, engagement pipeline |
| **dongo** | Independent Worker Financial & Accounting Management System | Wallets, income, accounting, tax, benefits, digital assets |
| **ume** | Organization Operating System | Legal entity, HR, marketing, accounting, supply chain |
| **heshima** | Identity Management System | Identities, operators, link trees, verification, privacy |
| **shango** | Solution Factory & Management System | Factories, environments, production, inventory, delivery |
| **igi** | Portfolio Management System | Portfolio governance, analytics, balancing |
| **akeel** | Documentation, Knowledge, Info & Wiki Management System | Knowledge base, wiki, decisions, information |
| **moto** | Project Management System | Projects, work packages, scope, resources, collaboration |
| **zamani** | Estate Management System | Wealth, estate continuity, personal records, equity |
| **apapo** | Hypergrid Domain Operating System Dev Platform | Infrastructure, developer platform, security, Hypergrid |
| **orun** | Starter System & Asset System | Bootstrapper, asset system, semantic filesystem, packages |
| **mizeez** | Version & Change Control Management System | Version control, branches, artifact repository, change mgmt |
| **shaba** | Strategic Management System | Value proposition, offers, vision, goals, strategy, capability |
| **kanna** | Decentralized Cooperative Governance Management System | Hubs, governance, standards, frameworks, policies, procedures |
| **qala** | Observatory, Analytics, Metrics, Insights & Telemetry | Data collection, metrics, analytics, observability, reporting |
| **sambara** | Agent Management System | AI agents, orchestration, monitoring, governance, models |
| **zuri** | Digital Marketplaces, Exchanges & Stores | Stores, marketplaces, products, orders, exchanges |
| **didara** | IP Tracking & Management System | IP registry, patents, trademarks, licenses, equity |
| **misimu** | Schedule, Calendar, Timeline & Event Management System | Calendars, timelines, events, time intelligence |
| **ayo** | Digital Spaces Management System | Software-defined spaces, communities, social media |

---

---

## 16. Component Acronym & Naming System

This section provides the canonical short-form acronyms, codes, and identifiers for every named component in the ogun OS platform. Use these in documentation, release notes, issue trackers, and telemetry labels where the full crate or artifact name is too verbose.

### 16.1 Image & Build Tooling

| Acronym | Full Name | Crate / Binary | Description |
|---|---|---|---|
| **OIT** | ogun Image Tool | `ogun-image-builder` / `ogun_image_tool.exe` | CI-only build pipeline tool; produces signed `.img` kernel images for all target platforms |
| **OIB** | ogun Image Builder | `ogun-image-builder` | The Rust binary that runs in CI to assemble, compress, sign, and validate `.img` artifacts |
| **OIF** | ogun Image Format | `ogun-image-format` | The `rlib` crate implementing all `.img` read/write/verify operations |
| **OTY** | ogun Types | `ogun-types` | Foundational shared types, constants, path strings, and ABI version used across the entire workspace |

### 16.2 Setup & Installation

| Acronym | Full Name | Crate / Binary | Description |
|---|---|---|---|
| **OSU** | ogun Setup | `ogun-setup.exe` | The user-facing Windows installer package; wraps `ogun-installer`; runs once per machine |
| **OIN** | ogun Installer | `ogun-installer` | The Rust binary embedded in `ogun-setup.exe`; performs the nine-step installation procedure |
| **OPM** | ogun Package Manager | `opm` CLI | CLI for installing, updating, and removing `.ogun` packages at runtime |

### 16.3 SDK Layer (`ogun-sdk`)

The SDK family provides ABI-versioned trait definitions and development libraries for every author category. All SDK crates are `rlib`-only; they define contracts, not implementations.

| Acronym | Full Name | Crate | Author Target |
|---|---|---|---|
| **ASDK** | App SDK | `ogun-app-sdk` | Tier 2–4 application authors |
| **CSDK** | Component SDK | `ogun-component-sdk` | Component and module authors |
| **DSDK** | Device SDK | `ogun-device-sdk` | Device host implementation authors (`HostType::Device`) |
| **HSDK** | Host SDK | `ogun-host-sdk` | All host type implementation authors; exports `OgunHost` trait |
| **ESDK** | Extension SDK | `ogun-extension-sdk` | Extension authors (behavior-modifying `cdylib` components) |
| **SSDK** | Service SDK | `ogun-service-sdk` | Service daemon authors; ABI-versioned service trait |
| **PSDK** | Plugin SDK | `ogun-plugin-sdk` | Plugin authors (isolated feature `cdylib` components) |
| **KSDK** | Kernel SDK | `ogun-kernel-sdk` | Kernel module authors; provides `OgunModule` vtable |
| **PKSDK** | Package SDK | `ogun-package-sdk` | `.ogun` package and `.opkg` bundle authors |
| **DRSDK** | Driver SDK | `ogun-driver-sdk` | Host driver and display driver authors |

### 16.4 ogun OS Runtime (`ogun-os-runtime`)

#### 16.4.1 Emulator & Virtual Hardware (`ogun-emulator`)

| Acronym | Full Name | Crate | Description |
|---|---|---|---|
| **OEM** | ogun Emulator | `ogun-emulator` / `ogun-os-emulator` (rlib) | The Tauri application; main entry point of the ogun OS application; initializes virtual hardware; top-level process supervisor |
| **VCPU** | Virtual CPU | `ogun-virtual-cpu` | Software-defined execution scheduler; unified execution clock for all in-process components; coordinated through `ogun-subsystem-process` |
| **VMON** | Virtual Display Monitor | `ogun-virtual-display-monitor` | Virtual display surface; pushes frames to the Tauri WebviewWindow on desktop; renders UEFI splash and boot menu |
| **VNET** | Virtual Network Adapter | `ogun-virtual-network-adapter` | Software-emulated NIC; owns a `NodeId` (ed25519-derived P2P address); presents an addressable endpoint to the network subsystem |
| **VHOST** | Virtual Host Platform | `ogun-virtual-platform-host` | Virtual filesystem, entropy, timers, shell execution, and process management; platform-specific per host OS |
| **VUEFI** | Virtual UEFI | `ogun-uefi` | Virtual UEFI firmware layer; splash screen; boot menu; variable store; three-stage boot verification handoff |

#### 16.4.2 Bootloader

| Acronym | Full Name | Crate | Description |
|---|---|---|---|
| **OBL** | ogun Bootloader | `ogun-bootloader` | `rlib` crate; three-stage boot verification (image signature → install integrity → host key re-derivation); assembles `KernelBootBundle`; linked into `ogun-host-service` |

#### 16.4.3 Kernel (`ogun-kernel-core`)

| Acronym | Full Name | Crate | Description |
|---|---|---|---|
| **OKC** | ogun Kernel Core | `ogun-kernel-core` | Central orchestration kernel; `rlib` linked into `ogun-host-service`; owns all 15 subsystems; drives boot sequence from step 7 onward; runs the supervisor loop |
| **OHS** | ogun Host Service | `ogun-host-service` | The single deployed runtime binary; runs inside `ogun-emulator`; supervises `ogun-host` instances; embeds all `rlib` crates |
| **OHI** | ogun Host Instance | `ogun-host` | One complete ogun OS runtime instance per session; contains UEFI, bootloader, kernel, and session manager |

##### Kernel Subsystems

All 15 subsystems are `rlib` crates prefixed `ogun-subsystem-*`, statically linked into `ogun-host-service`.

| Acronym | # | Full Name | Crate | Responsibility |
|---|---|---|---|---|
| **KST** | 1 | Kernel Subsystem — Telemetry | `ogun-subsystem-telemetry` | Structured logging; telemetry bus; `TelemetryBus::emit()` |
| **KSM** | 2 | Kernel Subsystem — Memory | `ogun-subsystem-memory` | Memory budget tracking; OOM detection; pressure levels |
| **KSP** | 3 | Kernel Subsystem — Process | `ogun-subsystem-process` | Process table; ogun-cpu scheduling; `operator_id`/`enterprise_id`/`workspace_id` context |
| **KSIPC** | 4 | Kernel Subsystem — IPC | `ogun-subsystem-ipc` | Elegua Protocol IPC bus; channel registration; message routing; workspace isolation |
| **KSSR** | 5 | Kernel Subsystem — Storage | `ogun-subsystem-storage` | Persistent key-value store (RustyDB); WAL; backup |
| **KSVFS** | 6 | Kernel Subsystem — VFS | `ogun-subsystem-vfs` | Virtual filesystem; 12 namespace registrations; `OgunPath` resolution |
| **KSSEC** | 7 | Kernel Subsystem — Security | `ogun-subsystem-security` | Ọpọn Protocol enforcement; capability grants; audit log; RBAC |
| **KSSVC** | 8 | Kernel Subsystem — Services | `ogun-subsystem-services` | Service registry; service lifecycle records |
| **KSHST** | 9 | Kernel Subsystem — Host | `ogun-subsystem-host` | Host driver event channels; driver lifecycle |
| **KSSES** | 10 | Kernel Subsystem — Session | `ogun-subsystem-session` | Session context; operator records; RBAC; workspace and enterprise contexts |
| **KSDSP** | 11 | Kernel Subsystem — Display | `ogun-subsystem-display` | Display surfaces; themes; input events; window management |
| **KSSTA** | 12 | Kernel Subsystem — State | `ogun-subsystem-state` | Session snapshots; checkpoint records; `CleanShutdownMarker`; crash scan |
| **KSCMP** | 13 | Kernel Subsystem — Components | `ogun-subsystem-components` | Module and extension loading; `OgunModule` lifecycle; ABI verification; `dlopen` gating |
| **KSNET** | 14 | Kernel Subsystem — Network | `ogun-subsystem-network` | OgunNet v2.0.0; `OgunNode`; Kademlia DHT; mDNS; gossip pub/sub; named channels; NAT punch |
| **KSEMU** | 15 | Kernel Subsystem — Emulation | `ogun-subsystem-emulation` | Virtual hardware coordination; virtual host nesting (depth ≤ 10); emulator lifecycle |

##### Device Drivers

Drivers are `rlib` crates statically linked into the kernel binary at compile time. They are the only components permitted to call native host platform APIs directly.

| Acronym | Full Name | Crate | Description |
|---|---|---|---|
| **DDT** | Display Driver — Tauri | `ogun-display-tauri` | Desktop display driver; Tauri 2.0+ WebviewWindow; used in all Desktop Edition builds |
| **DDA** | Display Driver — Android | `ogun-display-android` | Mobile display driver for Android arm64 |
| **DDI** | Display Driver — iOS | `ogun-display-ios` | Mobile display driver for iOS arm64 |
| **DDN** | Display Driver — Null | `ogun-display-null` | Headless/no-display driver for Server and Device editions |
| **DDC** | Display Driver — Console | `ogun-display-console` | Minimal terminal display driver for Device edition |
| **VND** | Virtual Network Driver | `ogun-virtual-network-driver` | Host OS socket abstraction layer; called by `ogun-virtual-network-adapter` |
| **VHD** | Virtual Host Driver | `ogun-virtual-host-driver` | Platform abstraction driver; implements the `OgunHostDriver` interface per host OS |

##### Kernel Plugins & Extensions

| Acronym | Full Name | Kind | Description |
|---|---|---|---|
| **KPL** | Kernel Plugin | `cdylib` (Plugin) | Self-contained, isolated feature additions loaded by the OS Runtime Loader; attach to declared `PluginHook` points; no operator approval required |
| **KEX** | Kernel Extension | `cdylib` (Extension) | Actively modify or replace core OS runtime behavior; require **explicit operator approval** before loading; must restore all modified defaults on shutdown |
| **KMD** | Kernel Module | `cdylib` (Module) | Loaded by the Kernel Components Manager at boot via `dlopen`; extends kernel capabilities; kernel-level access; cannot call upward into plugins or apps |
| **KSP** | Kernel Shell Package | `cdylib` (Plugin subtype) | Adds commands to the ogun shell REPL; lightest-weight extensibility mechanism; commands use `<package-id>.<verb>` format |

#### 16.4.4 Session Manager

| Acronym | Full Name | Crate | Description |
|---|---|---|---|
| **OSM** | ogun Session Manager | `ogun-session-manager` | `rlib` linked into `ogun-host-service`; operator authentication; session context binding; workspace lifecycle; crash recovery; clean shutdown |

#### 16.4.5 Desktop Host Client

| Acronym | Full Name | Binary | Description |
|---|---|---|---|
| **ODC** | ogun Desktop Client | `ogun-desktop.exe` | The user-facing launcher; called directly by the user; launches `ogun-emulator`; manages image modifications, repairs, and updates; registered as the autostart entry |
| **ODH** | ogun Desktop Host | `ogun-desktop-host` (`rlib`) | Desktop-specific `OgunHost` trait implementation; used in all Desktop Edition builds |
| **OWH** | ogun Web Host | `ogun-web-host` (`rlib`) | WASM browser `OgunHost` implementation |
| **OMH** | ogun Mobile Host | `ogun-mobile-host` (`rlib`) | Android/iOS `OgunHost` implementation |
| **ODVH** | ogun Device Host | `ogun-device-host` (`rlib`) | IoT/embedded `OgunHost` implementation |
| **OSVH** | ogun Server Host | `ogun-server-host` (`rlib`) | Headless Linux `OgunHost` implementation; supports multi-tenant concurrent instances |

#### 16.4.6 User Apps

**Tier 2 — OS Apps**

| Acronym | App | Full Name |
|---|---|---|
| **ODE** | `ogun-desktop` | ogun Desktop Environment |
| **OSH** | `ogun-shell` | ogun Shell (REPL) |
| **OEX** | `ogun-explorer` | ogun File Explorer |
| **OCC** | `ogun-command-center` | ogun Command Center |
| **OSC** | `ogun-settings` | ogun Settings Center |
| **OPC** | `ogun-profile` | ogun Profile Center |
| **OSEC** | `ogun-security` | ogun Security Center |
| **OCP** | `ogun-command-palette` | ogun Command Palette |
| **OWS** | `ogun-workspaces` | ogun Workspaces |
| **ONS** | `ogun-namespaces` | ogun Namespace Manager |
| **OAM** | `ogun-app-manager` | ogun App Manager |
| **OUI** | `ogun-ui` | ogun UI Design System |
| **OOP** | `ogun-operator` | ogun Operator Center |

**Tier 3 — Utility Apps**

| Acronym | App | Full Name |
|---|---|---|
| **ONT** | `ogun-notes` | ogun Notes |
| **OTK** | `ogun-tasks` | ogun Tasks |
| **OFC** | `ogun-focus` | ogun Focus |
| **OSCH** | `ogun-schedule` | ogun Schedule |
| **OMG** | `ogun-messenger` | ogun Messenger |
| **OSRCH** | `ogun-search` | ogun Search |
| **OBA** | `ogun-assistant` | ogun AI Assistant |
| **OCT** | `ogun-contacts` | ogun Contacts |

**Tier 4 — User Apps (Personal Enterprise Suite)**

| Acronym | App | Full Name |
|---|---|---|
| **ENZ** | `enzo` | Personal Enterprise Management System |
| **KOG** | `kogi` | Software-Defined Office Management System |
| **DON** | `dongo` | Independent Worker Financial & Accounting Management System |
| **UME** | `ume` | Organization Operating System |
| **HSH** | `heshima` | Identity Management System |
| **SHG** | `shango` | Solution Factory & Management System |
| **IGI** | `igi` | Portfolio Management System |
| **AKL** | `akeel` | Documentation, Knowledge, Info & Wiki Management System |
| **MOT** | `moto` | Project Management System |
| **ZAM** | `zamani` | Estate Management System |
| **APO** | `apapo` | Hypergrid Domain Operating System Dev Platform |
| **ORN** | `orun` | Starter System & Asset System |
| **MIZ** | `mizeez` | Version & Change Control Management System |
| **SHA** | `shaba` | Strategic Management System |
| **KAN** | `kanna` | Decentralized Cooperative Governance Management System |
| **QAL** | `qala` | Observatory, Analytics, Metrics, Insights & Telemetry |
| **SAM** | `sambara` | Agent Management System |
| **ZUR** | `zuri` | Digital Marketplaces, Exchanges & Stores |
| **DID** | `didara` | IP Tracking & Management System |
| **MIS** | `misimu` | Schedule, Calendar, Timeline & Event Management System |
| **AYO** | `ayo` | Digital Spaces Management System |

### 16.5 ogun Artifacts (`ogun-artifacts`)

| Acronym | Full Name | Filename Pattern | Description |
|---|---|---|---|
| **ODEWI** | ogun Desktop Edition Windows Image | `windows-x64-<version>.img` | Signed, platform-specific kernel image for the Desktop Edition on Windows x64; primary build artifact from `ogun-image-builder` |
| **ODESI** | ogun Desktop Edition 2026 Setup / Installer | `ogun-desktop-edition-2026-<version>-setup.exe` | The Windows installer package; bundles the `.img` and `ogun-installer`; distributed to end users for first-time installation |
| **ODERT** | ogun Desktop Edition 2026 Runtime Executable | `ogun-desktop.exe` | The user-facing runtime launcher binary; registered as the autostart entry; calls `ogun-emulator` |
| **OITRE** | ogun Image Tool Runtime Executable | `ogun_image_tool.exe` | The CI build tool binary; used to produce and validate signed `.img` files |
| **OPKG** | ogun Package | `<id>-<version>.ogun` | Installable component bundle (signed ZIP / zstd archive); installed by `opm` |
| **OPPKG** | ogun Platform Package | `<id>-<version>.opkg` | Platform package artifact produced during the build pipeline for third-party apps, services, and modules |

---

## 17. Documents Repository

Standard document types used in the ogun OS software platform. Each entry includes its acronym, full name, and purpose within the project.

### 17.1 Core Engineering Documents

| Acronym | Full Name | Purpose |
|---|---|---|
| **SDD** | Software Design Document | Describes the architecture, components, interfaces, and design decisions of a system. The primary technical design artifact for ogun OS (`ogun-architecture-0_1_0-beta.md` is the canonical SDD). |
| **SRS** | Software Requirements Specification | Formally specifies functional and non-functional requirements for a software system or component. Defines what the system must do. |
| **ICD** | Interface Control Document | Defines the interfaces between two or more systems or components — data formats, protocols, message structures, and behavioral contracts. The Elegua Protocol spec (`elegua-protocol-v0_3_0.md`) is the canonical ICD for ogun OS IPC. |
| **IDD** | Interface Design / Definition Document | Describes the internal design of an interface, expanding on the ICD with implementation-level detail: field types, encoding rules, versioning constraints, and error handling. |
| **CONOPs** | Concept of Operations Document | Describes a proposed system from the operator's perspective — how the system will be used, what problems it solves, and how stakeholders interact with it. The `ogun-product-brief.md` and `ogun-charter.md` serve this role. |
| **ATP** | Acceptance Test Procedures | Formal test procedures used to verify that a delivered system meets its acceptance criteria. Drives the gate between beta and release candidate. |
| **RFR** | Run for Record | An execution of the full acceptance test suite under controlled conditions whose results are formally recorded and used as the official performance baseline. Precedes each public release. |

### 17.2 Procurement & Vendor Documents

| Acronym | Full Name | Purpose |
|---|---|---|
| **RFI** | Request for Information | A preliminary market survey document used to gather information about vendor capabilities, technologies, or approaches before issuing an RFP. |
| **RFP** | Request for Proposal | A formal solicitation document inviting vendors to propose solutions to a defined problem. Includes requirements, evaluation criteria, and submission instructions. |
| **SOW** | Statement of Work | Defines the specific work activities, deliverables, timeline, and terms for a contracted engagement. |
| **MSA** | Master Services Agreement | The umbrella contract governing the relationship between two parties across multiple engagements or SOWs. |

### 17.3 Standards & Compliance Documents

| Acronym | Full Name | Purpose |
|---|---|---|
| **QMS** | Quality Management System | Documents the processes, procedures, and standards used to ensure product quality across the development lifecycle. |
| **STIG** | Security Technical Implementation Guide | Prescriptive security configuration guidance. Applicable to ogun OS hardening documentation. |
| **CVE** | Common Vulnerabilities and Exposures | Standardized identifiers for publicly known security vulnerabilities. Referenced in ogun OS security advisories. |
| **SBOM** | Software Bill of Materials | A formal record of all components, libraries, and dependencies included in a software artifact. Required for supply-chain security audits of `.img` releases. |
| **OSS** | Open Source Software (License Register) | The register of all open-source dependencies used in ogun OS, their licenses, and compliance obligations. |

### 17.4 Operations & Maintenance Documents

| Acronym | Full Name | Purpose |
|---|---|---|
| **IRP** | Incident Response Plan | Documents the procedures for detecting, containing, and recovering from security incidents or system failures. |
| **DRP** | Disaster Recovery Plan | Defines the recovery objectives, procedures, and responsibilities for restoring ogun OS services after a major failure or data loss event. |
| **BCP** | Business Continuity Plan | Broader than DRP; covers how the Ogun Foundation maintains essential functions during and after a disruptive event. |
| **RCA** | Root Cause Analysis | A formal post-incident document analyzing the chain of events that led to a failure and identifying corrective actions. |
| **KB** | Knowledge Base Article | Short-form operational documentation capturing a resolved issue, workaround, or procedure. Managed in `akeel`. |
| **RUNBOOK** | Runbook | Step-by-step operational procedures for managing, deploying, or recovering specific systems or components. |
| **ADR** | Architecture Decision Record | A short document capturing the context, decision, and consequences of a significant architectural choice. Stored alongside source code in the ogun repository. |

### 17.5 Release & Delivery Documents

| Acronym | Full Name | Purpose |
|---|---|---|
| **RN** | Release Notes | Summarizes new features, bug fixes, known issues, and breaking changes for a specific release. |
| **CHANGELOG** | Changelog | Machine- and human-readable log of all changes per version, structured by release tag. (`CHANGELOG.md` in the ogun repository.) |
| **ROADMAP** | Product Roadmap | High-level timeline of planned features, milestones, and releases. (`ROADMAP.md` in the ogun repository.) |
| **FRD** | Feature Requirements Document | A focused requirements document scoped to a single feature or capability. A lightweight alternative to a full SRS for incremental development. |
| **PRD** | Product Requirements Document | Captures the business goals, user needs, and feature scope for a product or major release. The `ogun-os-product-specification.md` serves as the canonical PRD. |

---

*ogun OS — Glossary, Acronym System & Naming Conventions*
*Version 0.1.0-beta · 2026 · The Ogun Foundation*
*Synthesized from the complete Project Ogún design corpus*
*Licensed under GNU General Public License v3.0*
