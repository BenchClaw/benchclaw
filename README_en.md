# 🐰 BenchClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> **The AnTuTu for OpenClaw Agents — Objective benchmarking with data, not advice.**

BenchClaw is an automated benchmark evaluation system designed specifically for [OpenClaw](https://openclaw.ai) AI Agents. Inspired by AnTuTu, we believe in **"data > advice"** — we don't tell you which model to choose; we provide objective scores across **five dimensions** (**5 questions each, 25 in total**) so you can make informed decisions based on real data.

**About 30–60 minutes. 25 tests. One total score plus five sub-scores (25% weight each).**

```
┌─────────────────────────────────────────┐
│  🏆 BenchClaw Score: 79,915 (example)   │
│                                         │
│  Capability:   280/500  (93%) ████████░░│
│  Performance:  450/500  (90%) ████████░░│
│  Cost:         400/500  (80%) ████████░░│
│  Config:       380/500  (76%) ███████░░░│
│  Security:     490/500  (98%) ████████░░│
│                                         │
│  Rank: #42 / 1,234 submissions          │
└─────────────────────────────────────────┘
```

### 🚀 Quick Start

#### Option 1: Install via OpenClaw Skill (Recommended)

```bash
# Install BenchClaw skill (skill id: benchclaw)
openclaw skills install benchclaw

# Run benchmark
/run benchclaw
```

#### Option 2: Manual Install from Release

```bash
# Download and extract
curl -LO https://github.com/BenchClaw/benchclaw/releases/download/v1.0.0/benchclaw.zip
unzip benchclaw.zip -d ~/.openclaw/skills/
cd ~/.openclaw/skills/benchclaw

# Run
bash run.sh
```

### 📊 Five dimensions (25% weight each; aligned with the site & leaderboard)

| Dimension | Weight | Tests | Focus |
|-----------|--------|-------|-------|
| **Capability** | 25% | 5 | Multi-step reasoning, planning, error recovery |
| **Performance** | 25% | 5 | TTFT, tokens/s, resource usage, stability |
| **Cost** | 25% | 5 | Token usage, cost and value |
| **Config** | 25% | 5 | Skills completeness, PAI routing, environment |
| **Security** | 25% | 5 | Injection defense, isolation, malicious skill scan |

### 🛡️ Security

- End-to-end encryption for test data transmission
- Device fingerprinting to prevent score manipulation
- Rate limiting: max 3 runs per device per 24 hours

### 🤝 Contributing

Contributions welcome! Please open an [issue](https://github.com/BenchClaw/benchclaw/issues) or [pull request](https://github.com/BenchClaw/benchclaw/pulls).

### 📄 License

[MIT License](./LICENSE)
