# src/chanpy/api/data/akshare_adapter.py
"""
数据获取相关路由
"""
from flask import jsonify, request

from chanpy.data_fetcher import akshare_adapter
from . import data_bp
from ...utils.exceptions import DataFetchError
from ...utils.logger import get_logger

logger = get_logger(__name__)


@data_bp.route("/stocks", methods=["GET"])
def get_all_stocks():
    """获取所有股票列表"""
    try:
        # 获取查询参数
        exchange = request.args.get('exchange', None)  # 可选过滤条件
        limit = request.args.get('limit', None)

        # 获取所有股票
        stocks_df = akshare_adapter.get_all_a_stocks()

        # 应用过滤条件
        if exchange:
            stocks_df = stocks_df[stocks_df['exchange'].str.contains(exchange)]

        # 转换为字典列表
        stocks_list = stocks_df.to_dict(orient='records')

        # 应用限制
        if limit and limit.isdigit():
            stocks_list = stocks_list[:int(limit)]

        return jsonify({
            "status": "success",
            "count": len(stocks_list),
            "stocks": stocks_list
        })
    except DataFetchError as e:
        logger.error(f"获取股票列表失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "details": e.details if hasattr(e, 'details') else {}
        }), 503
    except Exception as e:
        logger.error(f"获取股票列表发生未预期错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "获取股票列表失败，请稍后重试"
        }), 500

@data_bp.route("/stock-info", methods=["GET"])
def get_stock_info():
    """获取股票基本信息"""
    # 示例路由，实际实现可能包含数据获取逻辑
    stock_code = request.args.get('code', '')
    if not stock_code:
        return jsonify({"error": True, "message": "股票代码不能为空"}), 400

    # TODO: 实现实际的数据获取逻辑
    return jsonify({
        "code": stock_code,
        "name": "示例股票",
        "exchange": "示例交易所",
        "status": "active"
    })


@data_bp.route("/historical", methods=["GET"])
def get_historical_data():
    """获取历史行情数据"""
    # 示例路由，实际实现可能包含数据获取逻辑
    stock_code = request.args.get('code', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    if not stock_code:
        return jsonify({"error": True, "message": "股票代码不能为空"}), 400

    # TODO: 实现实际的数据获取逻辑
    return jsonify({
        "code": stock_code,
        "data": [
            {"date": "2023-01-01", "open": 100, "high": 105, "low": 95, "close": 102, "volume": 10000},
            {"date": "2023-01-02", "open": 102, "high": 107, "low": 100, "close": 106, "volume": 12000}
        ]
    })