# src/chanpy/data_fetcher/__init__.py
"""
数据获取模块，负责从各种数据源获取金融数据
"""
from .akshare_adapter import AKShareAdapter

# 创建全局AKShare适配器实例
akshare_adapter = AKShareAdapter()

__all__ = ['akshare_adapter']