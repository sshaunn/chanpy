# src/chanpy/api/health/akshare_adapter.py
"""
健康检查相关路由
"""
from flask import jsonify

from ...utils.config import config
from ...utils.logger import get_logger
from . import health_bp

logger = get_logger(__name__)


@health_bp.route("", methods=["GET"])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "UP",
        "version": "0.1.0",
        "environment": config.env
    })


@health_bp.route("/detailed", methods=["GET"])
def detailed_health():
    """详细的健康检查，包括组件状态"""
    # 这里可以添加数据库连接检查、外部服务检查等
    components = {
        "api": "ok",
        "database": "in progress",  # 未来可添加实际检查
        "data_fetcher": "in progress"  # 未来可添加实际检查
    }

    overall_status = all(status == "UP" for status in components.values())

    return jsonify({
        "status": "UP" if overall_status else "degraded",
        "version": "0.1.0",
        "environment": config.env,
        "components": components
    })