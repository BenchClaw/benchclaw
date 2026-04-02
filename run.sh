#!/bin/bash
# run.sh - BenchClaw 评测启动脚本
# 自动检测并安装依赖（无需 sudo，无需手动操作）

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"
REQUIREMENTS="$SCRIPTS_DIR/requirements.txt"

# 检查依赖是否已安装
check_deps() {
    python3 -c "import cryptography, psutil" 2>/dev/null
}

# 自动安装依赖（无需 sudo，仅使用系统自带工具）
install_deps() {
    echo "📦 检测到缺少依赖，正在自动安装..."

    # 确保 pip 可用（使用 Python 标准库 ensurepip，无需联网）
    if ! python3 -m pip --version &>/dev/null; then
        echo "  → pip 未安装，尝试用 ensurepip 安装..."
        python3 -m ensurepip --upgrade 2>/dev/null
    fi

    if ! python3 -m pip --version &>/dev/null; then
        echo "  → ensurepip 失败，尝试从 PyPA 下载 get-pip.py..."
        # get-pip.py 是 Python 官方 pip 安装工具（https://bootstrap.pypa.io），
        # 用于在系统未自带 pip 的环境（如精简版 Linux 镜像）中安装 pip。
        # 仅在 ensurepip 失败时作为 fallback 使用。
        python3 -c "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', '/tmp/get-pip.py')" 2>/dev/null && \
        python3 /tmp/get-pip.py --user 2>/dev/null
    fi

    if ! python3 -m pip --version &>/dev/null; then
        echo "❌ pip 不可用，请手动安装后重试："
        echo "   Ubuntu/Debian: sudo apt install python3-pip -y"
        echo "   CentOS/RHEL:   sudo yum install python3-pip -y"
        echo "   macOS:         brew install python3"
        exit 1
    fi

    # 安装项目依赖到用户目录（--user，不需要 root 权限，不影响系统 Python）
    # 依赖仅包含：cryptography（加密通信）、psutil（硬件信息采集）
    python3 -m pip install -r "$REQUIREMENTS" --user --quiet
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请检查网络连接"
        exit 1
    fi
    echo "✅ 依赖安装完成"
}

# 主流程
if ! check_deps; then
    install_deps
fi

echo "▶ 启动 BenchClaw 评测..."
cd "$SCRIPTS_DIR" && python3 main.py "$@"
