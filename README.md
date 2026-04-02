# 🐰 BenchClaw

[中文](#chinese) ｜ [English](#english)

<a name="chinese"></a>
<details open>
<summary><b>中文版</b></summary>

> **OpenClaw Agent 的"安兔兔" — 用数据说话，而非建议。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

BenchClaw 是专为 [OpenClaw](https://openclaw.ai) AI Agent 设计的自动化基准评测系统。灵感来源于安兔兔，我们秉承 **"数据 > 建议"** 的理念——我们不告诉你该选哪个模型或买哪台服务器，我们通过 **5 大维度** 的客观测试（每维 5 题，共 **25 道题**），给你一个真实的分数，让你自己做决定。

**约 30–60 分钟。25 道题。一个总分 + 五维子分。**

```
┌───────────────────────────────────────┐
│  🏆 BenchClaw 综合得分 79,915（示例）   │
│                                       │
│  能力：   280/500  (93%) ████████░░    │
│  性能：   450/500  (90%) ████████░░    │
│  成本：   400/500  (80%) ████████░░    │
│  配置：   380/500  (76%) ███████░░░    │
│  安全：   490/500  (98%) ████████░░    │
│                                       │
│  榜单排名：#42 / 共 1,234 次提交         │
└───────────────────────────────────────┘
```

---

## 🚀 快速开始

### 方式一：通过 OpenClaw Skill 安装（推荐）

```bash
# 安装 BenchClaw 技能（技能标识：benchclaw）
openclaw skills install benchclaw

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

## 📊 五大评测维度（各占 25% 权重，与官网、龙虾榜单一致）

| 维度 | 权重 | 题量 | 说明 |
|------|------|------|------|
| **能力 Capability** | 25% | 5 题 | 多步推理、复杂规划与错误恢复 |
| **性能 Performance** | 25% | 5 题 | TTFT、Tokens/s、资源占用与稳定性 |
| **成本效率 Cost** | 25% | 5 题 | Token 消耗、成本与性价比 |
| **配置优化 Config** | 25% | 5 题 | Skills 完整度、PAI 路由与环境配置 |
| **安全防御 Security** | 25% | 5 题 | 代码注入防护、权限隔离与恶意 Skill 扫描 |

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
</details>

<a name="english"></a>
<details open>
<summary><b>English Version</b></summary>

> **The AnTuTu for OpenClaw Agents — Objective benchmarking with data, not advice.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/BenchClaw/benchclaw/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

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
</details>


