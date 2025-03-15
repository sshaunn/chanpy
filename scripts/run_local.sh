#!/bin/bash
# scripts/run_local.sh - 本地运行脚本

set -e  # 如果任何命令失败，脚本立即退出

# 确保在项目根目录执行
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# 设置环境变量
export ENV="local"

echo "===================================="
echo "以本地模式启动 chanpy"
echo "===================================="

# 激活Poetry环境并运行应用
poetry run python -m src.chanpy.main