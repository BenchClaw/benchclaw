---
name: benchclaw
description: >
  BenchClaw 是 OpenClaw Agent 的专业级“安兔兔”评测框架。它专注于对 AI Agent 进行多维度、
  自动化的量化评估与能力基准测试，集成了任务分发、精准评分、可视化报表生成及热更新功能。
  当需要量化 Agent 的推理规划、响应速度、Token 成本及安全性时使用。

  **用户意图/指令**：跑分、跑个分、运行基准测试、评估 Agent 表现、生成评测报告、分析 Token 消耗。
  **技术关键词**：跑分、跑个分、Agent 评测、基准测试、自动化打分、量化评估、性能报告、Token 成本、
  TPS、OpenClaw。

  BenchClaw is the "AnTuTu" for OpenClaw Agents—a professional-grade automated benchmarking
  framework. It provides multi-dimensional evaluation (Capability, Performance, Cost, Config, Security)
  through automated task execution, precision scoring, and detailed report generation.

  **User Intent**: run benchmark, get score, evaluate agent performance, generate scoring reports,
  analyze Token usage/TPS.
  **Key Triggers**: Benchmark, Scoring, Agent Evaluation, Automated Scoring, Performance Metrics,
  Cost Analysis, OpenClaw.

metadata:
  author: benchclaw
  version: "1.0.1"
  openclaw:
    requires:
      bins:
        - python3
        - openclaw

    permissions:
      network: "Uploads encrypted evaluation results to BenchClaw server using AES-256-GCM + HMAC-SHA256. No personal data — only agent scores, token usage, and task results."
      file_write: "Writes evaluation results to data/ and temp/ directories within the skill folder. Writes device fingerprint to data/cache.json for tracking evaluation history."
      device_fingerprint: "Generates a local device fingerprint stored in data/cache.json. Used to correlate evaluation history across runs. No PII collected."
---

# BenchClaw Benchmark Skill

BenchClaw 是一套完整的 OpenClaw Agent 基准评测与热更新分发系统。它能够自动从服务端拉取考题，驱动 Agent 执行并收集输出，最后进行规则验证打分和报表生成。

---

## 前置条件 (Prerequisites)

- **Python 3.11+**（推荐 3.13）
- **本机已安装并可运行 `openclaw` CLI**
- **本机 OpenClaw Gateway 运行中**

Python 依赖会在首次运行时**自动安装**（无需 sudo），详见下方"快速开始"。

---

## ⚠️ 运行前必须确认

在执行评测前，**先获取 OpenClaw 默认模型配置**，然后展示以下信息等待用户确认：

> 📊 **BenchClaw 评测即将开始**
>
> - ⏱️ **预计耗时**：10-60 分钟（取决于模型速度和网络状况）
> - 💰 **Token 消耗**：约 2-3M tokens（会产生 API 费用，请确认预算充足）
> - 📋 **评测内容**：25 道题，涵盖能力、配置、硬件、权限、安全 5 大分类
> - ⚠️ **期间注意**：OpenClaw 仍可响应其他消息，但性能会有所下降
> - 🤖 **评测模型：`{agents.defaults.model.primary}`**
> - ⚠️ 评测使用的是 OpenClaw 配置的默认模型，与你当前 session 无关。
>
> 最后一个问题：**是否在榜单上展示你的名字「{AI名字}」？**
> - 回复「**展示 / 开始 / 确认**」→ 以「{AI名字}」出现在榜单上，立即开始评测 🚀
> - 回复「**匿名**」→ 匿名参与榜单，立即开始评测 🚀
>
> （成绩和硬件配置都会上传，仅名字显示方式不同）

根据用户回复，写入 `temp/caller_info.txt` 并启动评测：

```bash
# caller_info.txt 说明：
# 评测进程（main.py）在后台运行，与当前 session 隔离。
# 此文件用于告知 main.py 评测完成后如何回调通知用户。
# 仅包含：榜单展示名称（可选）。
# 文件在本机 temp/ 目录内，不上传至任何外部服务器。

# 用户回复「展示/开始/确认」时：
# agent_name：直接使用你自己的名字（无需读取任何文件）
echo "agent_name=<你的名字>" >> scripts/../temp/caller_info.txt
echo "show_name=true" >> scripts/../temp/caller_info.txt

# 用户回复「匿名」时：
echo "agent_name=" >> scripts/../temp/caller_info.txt
echo "show_name=false" >> scripts/../temp/caller_info.txt
```

然后后台启动评测：

```bash
cd scripts
# 启动评测进程（前台运行，进度实时输出到 stdout）
# 日志同时写入 temp/benchclaw.log，可随时查看：tail -f temp/benchclaw.log
python main.py
```

启动后告知用户：
> ✅ 评测已启动，预计 10-60 分钟完成。**完成后会自动发消息通知你，无需等待。**

> 💡 **TUI 用户注意：** 如果你通过 TUI 或终端直接触发评测，**不要写 `caller_info.txt`**（或者不要执行上面的 `echo` 命令）。评测进度和结果会直接输出到终端（stdout），你可以查看终端日志获取进度。

---

## 运行期间：进度监控

评测在后台运行，进度由 `main.py` 直接通过 `openclaw message send` 推送（需人类员工实现，见改进方案 A2）。

**在 A2 未实现前：** 用户可随时发"查看进度/进度"，AI 读取日志汇报：

```bash
tail -10 scripts/../temp/benchclaw.log | grep -E "正在测试|-> ok|-> failed|total_score"
```

---

## 评测完成后：自动上报并通知用户

评测完成后 `main.py` 会**自动上报结果到榜单**（show_name 已在开始前确认），然后发消息通知用户：

> 🏆 BenchClaw 评测完成！已上传到榜单。
>
> 📊 综合评分：79,915 分
> ✅ 通过：23/25 题
> ⏱️ 耗时：13.6 分钟
> 🏅 榜单排名：超越了 90.7% 的用户（如有排名数据）
>
> 发送「报告」查看详细结果。

---

## 结果展示格式

收到评测结果后，按以下格式向用户展示（**必须使用此格式**）：

```
🏆 BenchClaw 评测完成！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 综合评分：{总分} 分
准确度：{准确度分}/{满分准确度} | 速度加成：+{速度分}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 分类得分：
| 分类 | 通过率 | 准确度 | 速度分 |
|------|--------|--------|--------|
| 🧠 能力测试 | {n}/5 | {准确}/50 | +{速度} |
| ⚙️ 配置测试 | {n}/5 | {准确}/50 | +{速度} |
| 💻 硬件测试 | {n}/5 | {准确}/50 | +{速度} |
| 🔐 权限测试 | {n}/5 | {准确}/50 | +{速度} |
| 🛡️ 安全测试 | {n}/5 | {准确}/50 | +{速度} |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ 总耗时：{分钟}分钟
{根据耗时评价：< 8分钟 ⚡极快 / 8-15分钟 ✅正常 / 15-25分钟 🟡偏慢 / > 25分钟 🔴过慢}

💰 Token 消耗：{数量}（输入 {输入} / 输出 {输出}）
{根据消耗评价：< 1M ✅非常节省 / 1-2M 🟡正常 / 2-3M 🟠偏高 / > 3M 🔴过高}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 三维瓶颈诊断
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 模型：{model_name}，平均速度 {avg_tps} TPS
{根据 avg_tps 评价：> 5000 ⚡极快 / 2000-5000 ✅正常 / 1000-2000 🟡偏慢 / < 1000 🔴过慢}

💻 硬件：{如有 cpu_peak/mem_stats 数据则展示，否则跳过此行}
{CPU 峰值评价：< 60% ✅充裕 / 60-80% 🟡紧张 / > 80% 🔴成为瓶颈}
{内存剩余评价：> 2GB ✅充裕 / 1-2GB 🟡紧张 / < 1GB 🔴成为瓶颈}

💡 首要改善建议：
{根据最弱维度给出一条最重要的具体建议，示例：}
→ 模型速度偏低（{avg_tps} TPS）：建议尝试更快的模型，如切换至更轻量的推理模型
→ 内存剩余不足（{mem_avail}GB）：建议关闭其他程序或升级内存配置

{如失败题目存在，列出：}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 失败题目：
- {题号}：{失败原因}
```

---

## 快速开始 (Quick Start)

### 运行全量评测

**推荐方式（自动处理依赖）：**

```bash
bash run.sh
```

`run.sh` 会自动检测依赖是否已安装，如果没有会自动安装（无需 sudo），然后启动评测。

**手动方式（已有 pip）：**

```bash
cd scripts
# 安装依赖到用户目录（--user，不需要 sudo/root 权限，不影响系统 Python）
# 依赖仅包含：cryptography（加密通信）、psutil（硬件信息采集）
pip install -r requirements.txt --user --quiet
python main.py
```

> ⚠️ 如遇依赖安装失败（通常是服务器缺少 pip），可让 AI 在对话中执行以下命令：
> ```bash
> python3 -m ensurepip --upgrade && python3 -m pip install -r scripts/requirements.txt --user
> ```

### 单独生成或查看报表

```bash
cd scripts
python report.py --input ../temp/results.json
```

---

## 评测题型 (Task Categories)

BenchClaw 固定包含 25 道系统化评测题目，涵盖以下 5 大核心维度：

| 分类 | 标识 | 测试重点 |
|------|------|----------|
| **基础能力** | `capability` | Agent 的指令遵循、文件操作、工具调用、网络检索等核心能力 |
| **配置管理** | `config` | 修改与读取 OpenClaw 及环境配置的准确性 |
| **硬件操作** | `hardware` | 获取设备信息、系统状态、硬件资源的交互能力 |
| **权限边界** | `permission` | 在受限环境下的行为表现，验证权限控制机制 |
| **安全防御** | `security` | 拒绝执行危险指令、防范提示词注入与恶意破坏 |

---

## 评分机制 (Scoring System)

**单题总分 = 准确度分 + 速度分**

1. **准确度分 (Accuracy Score)**：文件存在性 + 内容规则验证 + 惩罚扣分
2. **速度分 (TPS Score)**：根据 Token 吞吐量奖励（TPS = Total Tokens / Duration Seconds）

---

## 评测产物与结果查看 (Results & Reports)

评测完成后自动生成：

- `data/report_summary.md`：简要报表（总分、分类汇总）
- `data/report_detail.md`：详细报表（每题耗时、Token、得分明细）
- `temp/results.json`：原始数据

```bash
# 查看总分
jq '.stats.score' temp/results.json

# 查看分类得分
jq '.stats.category_stats' temp/results.json

# 列出失败题目
jq '.results[] | select(.success == false) | {id, category, error}' temp/results.json
```

---

## 自动缓存与安全上报 (Offline Cache & Upload)

> **数据透明说明 (Data Transparency)**
> - 上报内容仅包含：评测得分、Token 消耗、任务结果、设备指纹——**不含任何对话内容、个人信息或凭证**。
> - 设备指纹为本地生成的匿名 ID，存储于 `data/cache.json`。
> - 拉题与上报请求体使用 RSA+AES 混合（公钥内置）；题目包在 HTTPS 下以明文 JSON 下发。
> - 上报目标服务器：`benchclawapi.antutu.com`（BenchClaw 官方榜单服务，可在 `scripts/config.py` 中的 `BENCHCLAW_API_HOST` 修改）。
> - 如不希望上报，可在 `scripts/config.py` 中禁用上报功能。

- **断网补报**：评测结束时网络断开，结果加密缓存；下次启动自动补报。

---

## 评测流程架构 (Evaluation Flow)

```text
main.py
  ├─ 1. 清理历史 Session 与工作区
  ├─ 2. 补报历史失败记录
  ├─ 3. 从服务端拉取题库 (25题)
  ├─ 4. 逐题执行（隔离 Session + Token 统计 + 规则校验）
  ├─ 5. 聚合统计（总分、TPS、通过率）
  ├─ 6. 生成 Report（Markdown）
  └─ 7. 加密上报服务端
```
