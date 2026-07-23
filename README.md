# Hermes AI Operating System

Hermes AI OS is an event-driven multi-agent framework where internship discovery is the first application.

## 🏗️ Architecture Overview

The system transitions from a linear pipeline into a modular, event-driven operating system:

```
Slack (Control Plane)
  └── Hermes (Orchestrator & Dispatcher)
       ├── Event Bus
       ├── Agent Registry & Lifecycle Manager
       ├── MCP Gateway (Careers, Greenhouse, Lever, Ashby)
       ├── AI Providers (OpenAI, Claude, Gemini)
       ├── Shared Memory
       └── Specialized Agents (Scout, Validator, Duplicate, Ranking, Salary, Analytics, Publisher)
```

### Core Principles
- **Event-Driven**: Agents never call each other directly; all communication occurs via the `EventBus`.
- **Hermes Orchestration**: Hermes manages lifecycle, registration, and dispatching.
- **MCP Abstraction**: Model Context Protocol connectors abstract underlying ATS platforms and job boards.
- **AI Providers**: Uniform interface for OpenAI, Anthropic Claude, and Google Gemini models.
- **Shared Memory**: Thread-safe state storage across agents with persistence support.
- **Slack Control Plane**: Mission control via Slack Bolt slash commands.

## 📁 Repository Structure

```
Internship-AI/
├── agents/
│   ├── scout/
│   ├── validator/
│   ├── publisher/
│   ├── ranking/
│   ├── salary/
│   ├── duplicate/
│   ├── analytics/
│   └── base.py
├── core/
│   ├── event_bus.py
│   ├── orchestrator.py
│   ├── registry.py
│   ├── dispatcher.py
│   └── lifecycle.py
├── providers/
│   ├── base_provider.py
│   ├── openai_provider.py
│   ├── claude_provider.py
│   └── gemini_provider.py
├── mcps/
│   ├── gateway.py
│   ├── careers.py
│   ├── greenhouse.py
│   ├── lever.py
│   └── ashby.py
├── memory/
│   └── shared_memory.py
├── services/
│   ├── logger.py
│   ├── scheduler.py
│   └── comparator.py
├── slack/
│   └── bot.py
├── commands/
│   ├── scan.py
│   ├── company.py
│   ├── status.py
│   └── help.py
├── config/
│   └── settings.py
├── prompts/
├── logs/
├── data/
│   └── companies.json
└── main.py
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Main Execution**:
   ```bash
   python main.py
   ```

3. **Slack Commands**:
   - `/hermes-scan` : Trigger internship discovery scan
   - `/hermes-status` : Check system and agent health
   - `/hermes-analytics` : Generate analytics report