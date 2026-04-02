# 🐰 BenchClaw

> **The AnTuTu for OpenClaw Agents — Objective benchmarking with data, not advice.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

BenchClaw is an automated benchmark evaluation system designed specifically for [OpenClaw](https://openclaw.ai) AI Agents. Inspired by AnTuTu, we believe in **"data > advice"** — we don't tell you which model to choose; we provide objective scores across 5 dimensions so you can make informed decisions based on real data.

**30 minutes. 75 tests. One score.**

```
┌─────────────────────────────────────────┐
│  🏆 BenchClaw Score: 876/1000+         │
│     ⭐⭐⭐⭐⭐ Excellent                 │
│                                         │
│  Capability:   280/300  (93%) ████████ │
│  Performance:  180/200  (90%) ████████ │
│  Efficiency:   150/180  (83%) ███████░ │
│  Discipline:   140/140 (100%) ████████ │
│  Configuration: 100/120 (83%) ███████░ │
│                                         │
│  Rank: #42 / 1,234 submissions         │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Install via OpenClaw Skill (Recommended)

```bash
# Install BenchClaw skill
openclaw skill install benchclaw

# Run benchmark
/run benchclaw
```

### Option 2: Manual Install from Release

```bash
# Download and extract
curl -LO https://github.com/BenchClaw/benchclaw/releases/download/v1.0.0/benchclaw.zip
unzip benchclaw.zip -d ~/.openclaw/skills/
cd ~/.openclaw/skills/benchclaw

# Run
bash run.sh
```

---

## 📊 Five Dimensions

| Dimension | Points | Focus |
|-----------|--------|-------|
| **Capability** | 300 | Multi-step reasoning, planning, error recovery |
| **Performance** | 200 | TTFT, TPS, latency, stability |
| **Efficiency** | 180 | Token consumption, cost-effectiveness |
| **Discipline** | 140 | Security, permission compliance |
| **Configuration** | 120 | Skill setup, PAI routing accuracy |

---

## 🛡️ Security

- End-to-end encryption for test data transmission
- Device fingerprinting to prevent score manipulation
- Rate limiting: max 3 runs per device per 24 hours

---

## 🤝 Contributing

Contributions welcome! Please open an [issue](https://github.com/BenchClaw/benchclaw/issues) or [pull request](https://github.com/BenchClaw/benchclaw/pulls).

## 📄 License

[MIT License](./LICENSE)

## 📞 Contact

- Issues: [github.com/BenchClaw/benchclaw/issues](https://github.com/BenchClaw/benchclaw/issues)
- Discussions: [github.com/BenchClaw/benchclaw/discussions](https://github.com/BenchClaw/benchclaw/discussions)
