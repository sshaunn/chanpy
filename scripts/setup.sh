#!/bin/bash
# scripts/setup.sh - 环境设置脚本

set -e  # 如果任何命令失败，脚本立即退出

# 确保在项目根目录执行
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "==========================================="
echo "设置 chanpy 开发环境"
echo "==========================================="

# 检查poetry是否已安装
if ! command -v poetry &> /dev/null; then
    echo "Poetry未安装，正在安装..."
    curl -sSL https://install.python-poetry.org | python3 -

    # 添加Poetry到PATH
    export PATH="$HOME/.poetry/bin:$PATH"

    # 为当前shell和未来的shell添加Poetry到PATH
    if [[ -f "$HOME/.bashrc" ]]; then
        echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> "$HOME/.bashrc"
    fi
    if [[ -f "$HOME/.zshrc" ]]; then
        echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> "$HOME/.zshrc"
    fi
fi

# 安装依赖
echo "安装项目依赖..."
poetry install

# 创建必要的目录
echo "创建数据目录..."
mkdir -p data/raw
mkdir -p data/processed

# 初始化配置文件
echo "设置配置文件..."
if [[ ! -f "config/secrets.toml" ]]; then
    cp config/secrets_template.toml config/secrets.toml
    echo "已创建secrets.toml，请编辑此文件添加您的敏感信息"
fi

# 设置环境变量
echo "设置环境变量..."
export ENV="local"

echo "==========================================="
echo "设置完成! 您可以使用以下命令运行应用："
echo "poetry shell"
echo "python -m src.chanpy.main"
echo "==========================================="