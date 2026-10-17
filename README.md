# 🛡️ Day 4: Agent Guardrail Lab

A lightweight, deterministic security middleware and testing harness designed to protect AI agents from prompt injection, unauthorized tool execution, and secret disclosures.

![CI Test Suite](https://github.com/neonmercenary/agent-guardrail-lab/actions/workflows/test.yml/badge.svg)

---

## ⚠️ Important Engineering Disclaimer: Lab vs. Production Guardrails

**This project is an educational and portfolio-grade security lab, NOT a bulletproof production-grade AI firewall.**

While deterministic pattern matching (regex, whitelists, and type validation) provides an essential **First Line of Defense**, it has inherent limitations in a real-world adversarial environment:
* **The Evasion Problem:** Attackers can easily bypass regex filters using obfuscation techniques (e.g., base64 encoding, leetspeak, or splitting malicious phrases across multi-turn chats).
* **The Semantic Blind Spot:** Keyword matching cannot detect subtle semantic jailbreaks (e.g., *"Imagine you are an unfiltered hacker in a movie script..."*).

### What a True Production Stack Requires:
To secure an enterprise-grade agent, this deterministic layer must be combined with:
1. **Semantic/Model-Based Classifiers:** Lightning-fast fine-tuned classifiers (like *Llama Guard* or *NeMo Guardrails*) to inspect intent.
2. **Context-Aware Multi-Turn Tracking:** Monitoring conversation state rather than just inspecting isolated prompts.
3. **Execution Sandboxing:** Isolating tool execution environments (e.g., restricted Docker containers or network boundaries).

*Note: This lab serves as a high-speed foundational layer. Future iterations include a **live implementation bridging this guardrail middleware directly with real MCP tools and live model prompts**.*

---

## 🏗️ Architecture & Control Flow

The middleware intercepts incoming requests before they reach the core agent or execution tools:


```

[ User Input / Adversarial Prompt ]
│
▼
┌────────────────────────┐
│  Input Guardrail Layer │ ──► (Blocked: Regex / Pattern Match)
└───────────┬────────────┘
│ (Passed)
▼
┌────────────────────────┐
│    Agent Execution     │
└───────────┬────────────┘
│ (Tool Call Attempt)
▼
┌────────────────────────┐
│ Tool Guardrail Layer   │ ──► (Blocked: Whitelist Violation)
└───────────┬────────────┘
│ (Passed)
▼
[ Execution & Output ]

```

---

## 📂 Project Structure

*   `guardrails.py`: Core security engine utilizing Python `dataclasses` and deterministic pattern checks.
*   `main.py`: FastAPI application wrapping the guardrail middleware for agent runs and tool executions.
*   `tests.py`: Pytest suite running fixed adversarial test cases against the guardrail engine.
*   `Dockerfile` & `docker-compose.yml`: Containerization configurations for instant deployment.
*   `.github/workflows/test.yml`: Automated CI pipeline running tests on every push.

---

## 🚀 Quick Start & Installation

### 1. Clone and Install Dependencies
Using modern Python packaging (`uv`):

```bash
git clone [https://github.com/neonmercenary/agent-guardrail-lab.git](https://github.com/neonmercenary/agent-guardrail-lab.git)
cd agent-guardrail-lab
uv sync

```

### 2. Run the Test Suite

Validate the security harness against the built-in adversarial test cases:

```bash
uv run pytest tests.py -v

```

### 3. Run the FastAPI Service Locally

```bash
uv run uvicorn main:app --reload

```

Or deploy instantly via Docker Compose:

```bash
docker compose up --build

```
