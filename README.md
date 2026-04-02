# 🐰 BenchClaw

> **OpenClaw Agent 的"安兔兔" — 用数据说话，而非建议。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

BenchClaw 是专为 [OpenClaw](https://openclaw.ai) AI Agent 设计的自动化基准评测系统。灵感来源于安兔兔，我们秉承 **"数据 > 建议"** 的理念——我们不告诉你该选哪个模型或买哪台服务器，我们通过 5 大维度的客观测试，给你一个真实的分数，让你自己做决定。

**30 分钟。75 道题。一个分数。**

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

## 🚀 快速开始

### 方式一：通过 OpenClaw Skill 安装（推荐）

```bash
# 安装 BenchClaw skill
openclaw skill install benchclaw

# 运行评测
/run benchclaw
```

### 方式二：从 Release 手动安装

```bash
# 下载并解压
curl -LO https://github.com/BenchClaw/benchclaw/releases/download/v1.0.0/benchclaw.zip
unzip benchclaw.zip -d ~/.openclaw/skills/
cd ~/.openclaw/skills/benchclaw

# 运行
bash run.sh
```

---

## 📊 五大评测维度

| 维度 | 分数 | 测试内容 |
|------|------|----------|
| **能力 (Capability)** | 300 | 多步推理、规划、错误恢复 |
| **性能 (Performance)** | 200 | TTFT、TPS、延迟、稳定性 |
| **效能 (Efficiency)** | 180 | Token 消耗、成本效益 |
| **纪律 (Discipline)** | 140 | 安全、权限合规 |
| **配置 (Configuration)** | 120 | Skills 配置、PAI 路由准确率 |

---

## 🛡️ 安全说明

- 评测数据端到端加密传输
- 设备指纹机制防止刷分
- 每台设备每 24 小时限跑 3 次

---

## 🤝 贡献

欢迎提交 Issue 或 PR！请查看 [Issues](https://github.com/BenchClaw/benchclaw/issues) 和 [Discussions](https://github.com/BenchClaw/benchclaw/discussions)。

## 📄 License

[MIT License](./LICENSE)

---

## English

> **The AnTuTu for OpenClaw Agents — Objective benchmarking with data, not advice.**

BenchClaw is an automated benchmark evaluation system designed specifically for [OpenClaw](https://openclaw.ai) AI Agents. Inspired by AnTuTu, we believe in **"data > advice"** — we don't tell you which model to choose; we provide objective scores across 5 dimensions so you can make informed decisions based on real data.

**30 minutes. 75 tests. One score.**

### 🚀 Quick Start

#### Option 1: Install via OpenClaw Skill (Recommended)

```bash
# Install BenchClaw skill
openclaw skill install benchclaw

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

### 📊 Five Dimensions

| Dimension | Points | Focus |
|-----------|--------|-------|
| **Capability** | 300 | Multi-step reasoning, planning, error recovery |
| **Performance** | 200 | TTFT, TPS, latency, stability |
| **Efficiency** | 180 | Token consumption, cost-effectiveness |
| **Discipline** | 140 | Security, permission compliance |
| **Configuration** | 120 | Skill setup, PAI routing accuracy |

### 🛡️ Security

- End-to-end encryption for test data transmission
- Device fingerprinting to prevent score manipulation
- Rate limiting: max 3 runs per device per 24 hours

### 🤝 Contributing

Contributions welcome! Please open an [issue](https://github.com/BenchClaw/benchclaw/issues) or [pull request](https://github.com/BenchClaw/benchclaw/pulls).

### 📄 License

[MIT License](./LICENSE)
