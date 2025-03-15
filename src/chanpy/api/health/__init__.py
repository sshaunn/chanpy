# src/finance_trading/api/health/__init__.py
"""
健康检查API模块
"""
from flask import Blueprint

health_bp = Blueprint('health', __name__, url_prefix='/health')

from . import routes