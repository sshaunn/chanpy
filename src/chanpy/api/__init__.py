# src/chanpy/api/__init__.py
"""
API路由模块，负责处理HTTP请求和响应。
"""

from flask import Blueprint

# 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

# 导入所有子模块路由
from .health.routes import health_bp
from .data.routes import data_bp
from .strategy.routes import strategy_bp
# from .stock_pool.routes import stock_pool_bp

# 注册子蓝图
api_bp.register_blueprint(health_bp)
api_bp.register_blueprint(data_bp)
api_bp.register_blueprint(strategy_bp)
# api_bp.register_blueprint(stock_pool_bp)

# 导入错误处理器
from . import error_handlers