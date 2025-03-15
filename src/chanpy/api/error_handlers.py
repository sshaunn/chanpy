# src/chanpy/api/error_handlers.py
"""
API错误处理器
"""
from flask import jsonify

from ..utils.exceptions import FinanceTradingError
from ..utils.logger import get_logger
from . import api_bp

logger = get_logger(__name__)

@api_bp.errorhandler(FinanceTradingError)
def handle_chanpy_error(err):
    """处理自定义异常"""
    response = jsonify(err.to_dict())
    response.status_code = err.status_code
    return response

@api_bp.errorhandler(404)
def resource_not_found(e):
    """处理404错误"""
    return jsonify(error=True, message="资源不存在"), 404

@api_bp.errorhandler(500)
def internal_server_error(e):
    """处理500错误"""
    logger.error(f"未处理的服务器错误: {str(e)}")
    return jsonify(error=True, message="服务器内部错误"), 500

def register_error_handlers(app):
    """注册全局错误处理器"""
    @app.errorhandler(404)
    def global_not_found(e):
        return jsonify(error=True, message="资源不存在"), 404

    @app.errorhandler(500)
    def global_server_error(e):
        logger.error(f"全局未处理服务器错误: {str(e)}")
        return jsonify(error=True, message="服务器内部错误"), 500

    @app.errorhandler(FinanceTradingError)
    def global_chanpy_error(err):
        response = jsonify(err.to_dict())
        response.status_code = err.status_code
        return response