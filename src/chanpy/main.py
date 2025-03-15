# src/chanpy/main.py
from flask import Flask
from flask_cors import CORS

from src.chanpy.utils.config import config
from src.chanpy.utils.logger import get_logger
from src.chanpy.api.routes import register_routes

logger = get_logger(__name__)

def create_app():
    """创建并配置Flask应用"""
    # 确保配置已加载
    config.load()

    app = Flask(__name__)

    # 配置CORS
    if config.get("api.enable_cors", False):
        origins = config.get("api.cors_origins", ["*"])
        CORS(app, resources={r"/*": {"origins": origins}})

    # 注册API路由
    register_routes(app)

    logger.info(f"应用已创建，环境: {config.env}")
    return app


def run_app():
    """运行应用（开发环境）"""
    app = create_app()
    host = config.get("api.host", "127.0.0.1")
    port = config.get("api.port", 5000)
    debug = config.get("system.debug", False)

    logger.info(f"启动应用服务器，监听地址: {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_app()