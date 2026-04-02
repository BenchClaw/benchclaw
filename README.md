# BenchClaw

**BenchClaw** 是专为 **OpenClaw Agent** 设计的自动化基准评测系统。它能够提供端到端的评测闭环，包括：从云端拉取试题、驱动本地 Agent 执行任务、收集输出与 Token 消耗、通过多维度规则引擎进行打分、生成详细的 Markdown 评测报告，并安全地将成绩加密上报至服务端。

---

## ✨ 核心特性

- 🔄 **全自动化评测闭环**：拉取题目 -> 任务执行 -> 结果校验 -> 报表生成 -> 成绩上报。
- 🛡️ **安全与隔离**：
  - 采用 **AES-256-GCM** 和 **HMAC-SHA256** 加密传输数据，确保试题与结果安全。
  - 为每道题目自动分配独立的隔离 Session (`benchclaw_session_<id>`)。
  - 执行前后自动清理测试工作区 (`~/.openclaw/workspace/bench_claw`)。
- 📊 **细粒度多维度评分**：
  - **准确度**：支持文件存在性校验、正则匹配、关键字统计、精准内容提取。
  - **安全性/规范性**：支持触发危险词/错误行为的扣分（Penalty）机制，甚至一票否决（Fatal）。
  - **性能加分**：基于 Token 吞吐量（TPS）给予性能奖励。
- 📡 **离线与弱网容灾**：网络异常导致成绩上报失败时，自动加密序列化保存至本地 `cache/`，下次运行自动补报。
- 📑 **丰富的可视化报表**：自动生成全局汇总与题目详情的双份 Markdown 报表，并记录模型预估计费。

---

## 📂 目录结构

```text
benchclaw/
├── scripts/                 # 核心代码逻辑目录
│   ├── main.py              # 主入口控制程序
│   ├── agent_cli.py         # 封装与 OpenClaw CLI 的交互进程
│   ├── verification.py      # 验证与评分核心规则引擎
│   ├── server.py            # API 交互（拉取试题与上报结果）
│   ├── crypto.py            # AES-256-GCM 加解密工具
│   ├── report.py            # Markdown 报表生成器
│   ├── config.py            # 全局配置参数
│   ├── utils.py             # 文件与环境清理、指纹生成
│   ├── openclawbot.py       # 解析本机 OpenClaw 配置信息
│   └── requirements.txt     # Python 依赖清单
├── data/                    # 评测产出数据目录
│   ├── report_summary.md    # [生成] 评测结果简报
│   ├── report_detail.md     # [生成] 评测结果详情
│   └── cache.json           # [生成] 设备指纹信息
├── temp/                    # 临时运行目录
│   ├── results.json         # [生成] 原始详细评测数据(含日志与评分细节)
│   ├── benchclaw.log        # [生成] 详细运行日志文件
│   └── prompt.md            # [生成] 运行时动态注入的任务描述
└── cache/                   # [生成] 断网容灾的上传缓存包 (.dat)
```

---

## 🛠️ 安装与前置要求

1. **运行环境**: Python 3.11 推荐。
2. **依赖安装**:
   进入 `scripts` 目录并安装依赖包：
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```
   *(核心依赖包含 `cryptography>=42.0`)*
3. **OpenClaw 要求**:
   - 机器已安装并配置好 `openclaw` CLI 工具。
   - `openclaw` 在命令行路径中可直接调用 (`openclaw --version`)。
   - 本地 OpenClaw Gateway 处于运行状态。

---

## 🚀 快速使用

### 1. 运行完整评测

```bash
cd scripts
python main.py
```
这将会触发一次完整的评测流程。控制台会实时输出当前评测的题号、耗时、得分以及总体验收情况。

### 2. 生成/重写报表

如果在测试后修改了报表模板，或者只希望利用已有的 `results.json` 重新生成 markdown 报告：
```bash
cd scripts
python report.py --input ../temp/results.json
```

### 3. 加解密测试与密钥生成

检查本地加解密配置是否正常：
```bash
cd scripts
python crypto.py check
```

---

## ⚙️ 核心模块说明

### 1. `main.py` - 主控节点
负责编排整个生命周期：初始化环境及清理缓存 -> 拉取设备指纹 -> 获取试题 -> 遍历执行单题 (`agent_cli.py`) -> 聚合统计 -> 触发生成报表 (`report.py`) -> 提交数据 (`server.py`)。

### 2. `verification.py` - 规则验证引擎
实现基于特定 Schema 的自动化打分机制：
- **目标类型**：支持验证生成的文件 (`file`)、或者 Agent 在 stdout 中的标准回复 (`reply`)。
- **匹配规则** (`content_rules`)：包含 `contains`, `regex_match`, `regex_count`, `keyword_match`, `keyword_frequency`。
- **惩罚规则** (`penalty_rules`)：包含违禁词或危险操作正则（支持扣分 `deduction` 和直接判零 `fatal`）。
- **指标提取** (`metric_extractors`)：支持用正则从指定文件中提取核心数据，以便二次计算。

### 3. `agent_cli.py` - 子进程调度器
拉起 `openclaw agent` 子进程并跟踪其运行：
- 使用 `--session-id` 参数实现会话级别沙箱隔离。
- 包含超时强杀和错误恢复机制。
- 执行结束后，自动定位并解析 `~/.openclaw/agents/<agent_id>/sessions/` 下的 `jsonl` 文件，精准提取 Token 消耗（Input/Output/Cache）。

---

## 📈 评分体系

最终任务得分公式：**`单题总分 = 准确度得分 + 性能速度分`**

1. **准确度得分 (Accuracy Score)**
   - 基础分（比如文件存在即给分 `exist_score`）。
   - 内容分（每个 `content_rule` 匹配成功获得其 `score`）。
   - 扣除项（触犯 `penalty_rule` 扣减相应的分数；如果标记为 `fatal=true` 则该题彻底计 0 分）。
2. **性能速度分 (TPS Score)**
   - 计算公式： `TPS = Total Tokens / Duration (Seconds)`
   - 速度加分： `TPS * 0.01` (向下取整)。这意味着生成速度越快、处理效率越高的模型，能够获得额外的性能奖励分。

---

## 🔒 配置与环境变量

大部分核心参数可通过 `scripts/config.py` 调整。
你也可以通过设置环境变量来覆写敏感信息：

- **`BENCHCLAW_CLIENT_KEY`**：通信加密密钥（Base64编码，32字节）。系统默认包含一把内测密钥，生产评测时应当通过环境变量动态注入，防止数据伪造。

```bash
# Windows (CMD)
set BENCHCLAW_CLIENT_KEY=你的Base64密钥
python main.py
```

## 📝 日志与排错

- **控制台日志**：打印 `INFO` 级别的执行概要。
- **详细文件日志**：所有的 `DEBUG` 信息、包括网络请求 Raw Data、每个正则匹配的具体匹配情况，都会被详细记录到 **`temp/benchclaw.log`**。排查某道题为何得分低时，请首选查阅此文件。
- **请求 Payload 排查**：服务端上报的原始组装数据会被写入 `temp/uploads_payload.json` 以便人工核对。
