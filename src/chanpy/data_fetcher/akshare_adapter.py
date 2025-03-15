# src/chanpy/data_fetcher/akshare_adapter.py
"""
AKShare适配器，负责从AKShare获取数据
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import akshare as ak
import pandas as pd

from ..utils.config import config
from ..utils.exceptions import DataFetchError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AKShareAdapter:
    """AKShare数据获取适配器"""

    def __init__(self):
        self.cache_enabled = config.get("data_fetcher.cache_enabled", True)
        self.cache_path = Path(config.get("data_fetcher.cache_path", "./data/cache"))
        self.cache_expiry_hours = config.get("data_fetcher.cache_expiry_hours", 24)

        # 确保缓存目录存在
        if self.cache_enabled:
            os.makedirs(self.cache_path, exist_ok=True)

    def get_all_a_stocks(self):
        """
        获取所有A股股票列表

        返回:
            pandas.DataFrame: 包含所有A股股票信息的DataFrame
        """
        cache_file = self.cache_path / "all_a_stocks.json"

        # 尝试从缓存加载
        if self.cache_enabled and self._is_cache_valid(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                logger.info(f"从缓存加载A股股票列表: {cache_file}")
                return pd.DataFrame(cache_data)
            except Exception as e:
                logger.warning(f"从缓存加载A股股票列表失败: {e}")

        try:
            # 使用AKShare获取股票列表
            logger.info("从AKShare获取A股股票列表")

            # 使用单一方法获取所有A股股票
            stock_info = ak.stock_info_a_code_name()

            # 只保留主板、中小板和创业板，去掉北交所等
            stock_info = stock_info[stock_info['code'].apply(lambda x: str(x).startswith(('60', '00', '30')))]

            # 重命名列以使用统一的命名约定
            stock_info = stock_info.rename(columns={
                'code': 'code',
                'name': 'name'
            })

            # 添加交易所信息
            def determine_exchange(code):
                code_str = str(code)
                if code_str.startswith('60'):
                    return "上海证券交易所"
                elif code_str.startswith(('00', '30')):
                    return "深圳证券交易所"
                else:
                    return "其他"

            stock_info['exchange'] = stock_info['code'].apply(determine_exchange)

            # 写入缓存
            if self.cache_enabled:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(stock_info.to_json(orient="records", force_ascii=False))
                logger.info(f"A股股票列表已缓存: {cache_file}")

            return stock_info

        except Exception as e:
            error_msg = f"获取A股股票列表失败: {str(e)}"
            logger.error(error_msg)
            raise DataFetchError(error_msg, details={"source": "akshare", "method": "get_all_a_stocks"})

    def get_stock_info(self, stock_code):
        """
        获取单只股票的详细信息

        参数:
            stock_code (str): 股票代码

        返回:
            dict: 股票详细信息
        """
        cache_file = self.cache_path / f"stock_info_{stock_code}.json"

        # 尝试从缓存加载
        if self.cache_enabled and self._is_cache_valid(cache_file):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"从缓存加载股票信息失败: {e}")

        try:
            # 首先获取所有股票列表，以确定交易所
            all_stocks = self.get_all_a_stocks()

            # 确保股票代码是字符串并且去除空格
            stock_code = str(stock_code).strip()

            # 过滤出匹配的股票
            stock_record = all_stocks[all_stocks["code"] == stock_code]

            if stock_record.empty:
                raise DataFetchError(f"未找到股票代码: {stock_code}")

            # 基本信息
            stock_info = stock_record.iloc[0].to_dict()

            # 将所有值转换为字符串，避免JSON序列化问题
            stock_info = {k: str(v) if not isinstance(v, (int, float, bool, type(None))) else v
                          for k, v in stock_info.items()}

            # 获取更多信息可以根据需要添加额外的AKShare调用
            # 例如：财务信息、公司简介等

            # 写入缓存
            if self.cache_enabled:
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(stock_info, f, ensure_ascii=False)

            return stock_info

        except DataFetchError:
            # 直接重新抛出DataFetchError
            raise
        except Exception as e:
            error_msg = f"获取股票信息失败: {str(e)}"
            logger.error(error_msg)
            raise DataFetchError(error_msg, details={"stock_code": stock_code})

    def _is_cache_valid(self, cache_file):
        """检查缓存文件是否存在且未过期"""
        if not cache_file.exists():
            return False

        # 检查文件修改时间
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        expiry_time = datetime.now() - timedelta(hours=self.cache_expiry_hours)

        return mtime > expiry_time