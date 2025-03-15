# src/chanpy/api/akshare_adapter.py
"""
API路由注册模块
"""
from flask import Flask

from . import api_bp
from .error_handlers import register_error_handlers


def register_routes(app: Flask):
    """注册所有API路由到Flask应用"""
    # 注册主API蓝图
    app.register_blueprint(api_bp)

    # 注册全局错误处理器
    register_error_handlers(app)