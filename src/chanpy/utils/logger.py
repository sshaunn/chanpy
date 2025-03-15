# src/chanpy/utils/logger.py
import logging
import os
import sys
from pathlib import Path
from typing import Dict

from .config import config


class Logger:
    """日志管理类"""

    def __init__(self):
        self._loggers: Dict[str, logging.Logger] = {}
        self._configured = False

    def configure(self) -> None:
        """配置日志系统"""
        if self._configured:
            return

        log_level_str = config.get("system.log_level", "INFO")
        log_level = getattr(logging, log_level_str.upper(), logging.INFO)

        # 配置根日志器
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

        # 如果在生产环境，添加文件处理器
        if config.env == "production":
            log_dir = Path("/var/log/finance_trading")
            os.makedirs(log_dir, exist_ok=True)

            file_handler = logging.FileHandler(log_dir / "app.log")
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))

            logging.getLogger().addHandler(file_handler)

        self._configured = True

    def get_logger(self, name: str) -> logging.Logger:
        """获取指定名称的日志器"""
        if not self._configured:
            self.configure()

        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)

        return self._loggers[name]


# 创建全局日志管理实例
logger_manager = Logger()


def get_logger(name: str) -> logging.Logger:
    """便捷函数，获取指定名称的日志器"""
    return logger_manager.get_logger(name)