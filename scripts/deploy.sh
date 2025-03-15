#!/bin/bash
# 部署脚本

set -e  # 任何命令失败时立即退出

# 输出彩色文本的函数
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

print_yellow() {
    echo -e "\033[0;33m$1\033[0m"
}

print_red() {
    echo -e "\033[0;31m$1\033[0m"
}

# 确保我们在项目根目录
cd "$(dirname "$0")/.."

# 检查是否指定了环境
if [ -z "$1" ]; then
    print_red "错误: 未指定部署环境"
    print_yellow "用法: ./scripts/deploy.sh [环境名称]"
    print_yellow "示例: ./scripts/deploy.sh prod"
    exit 1
fi

ENV_NAME=$1
export ENV=$ENV_NAME

# 加载指定环境的环境变量
if [ -f "./environments/${ENV_NAME}/.env" ]; then
    print_yellow "加载 ${ENV_NAME} 环境变量..."
    set -a
    source "./environments/${ENV_NAME}/.env"
    set +a
else
    print_red "错误: 缺少环境变量文件 (./environments/${ENV_NAME}/.env)"
    exit 1
fi

# 确保配置文件存在
if [ ! -f "./config/${ENV_NAME}.toml" ]; then
    print_red "错误: 缺少配置文件 (./config/${ENV_NAME}.toml)"
    exit 1
fi

print_green "开始部署到 ${ENV_NAME} 环境..."

# 生产环境使用gunicorn
if [ "$ENV_NAME" = "prod" ]; then
    print_yellow "使用Gunicorn启动生产服务器..."

    # 从配置中获取值（这需要Python帮助）
    HOST=$(python -c "from src.chanpy.utils.config import config; config.load(); print(config.get('api.host', '0.0.0.0'))")
    PORT=$(python -c "from src.chanpy.utils.config import config; config.load(); print(config.get('api.port', 8000))")
    WORKERS=$(python -c "from src.chanpy.utils.config import config; config.load(); print(config.get('api.workers', 4))")

    # 确保数据目录存在
    mkdir -p /data/chanpy
    mkdir -p /var/log/chanpy

    # 使用Poetry运行Gunicorn
    poetry run gunicorn "src.chanpy.main:create_app()" \
        --bind "$HOST:$PORT" \
        --workers $WORKERS \
        --log-file /var/log/chanpy/gunicorn.log \
        --access-logfile /var/log/chanpy/access.log \
        --error-logfile /var/log/chanpy/error.log \
        --daemon

    print_green "生产服务器已启动！"
    print_yellow "查看日志: tail -f /var/log/chanpy/gunicorn.log"
else
    # 开发环境直接使用Python
    print_yellow "启动 ${ENV_NAME} 环境开发服务器..."
    poetry run python src/chanpy/main.py
fi