# src/chanpy/utils/exceptions.py
from typing import Optional, Dict, Any


class FinanceTradingError(Exception):
    """财务交易系统的基础异常类"""

    def __init__(
            self,
            message: str = "An error occurred in the finance trading system",
            status_code: int = 500,
            details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """将异常转换为字典，用于API响应"""
        result = {
            "error": True,
            "message": self.message,
            "status_code": self.status_code
        }

        if self.details:
            result["details"] = self.details

        return result


class ConfigError(FinanceTradingError):
    """配置错误"""

    def __init__(
            self,
            message: str = "Configuration error",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=500, details=details)


class DataFetchError(FinanceTradingError):
    """数据获取错误"""

    def __init__(
            self,
            message: str = "Failed to fetch data",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=503, details=details)


class DataProcessError(FinanceTradingError):
    """数据处理错误"""

    def __init__(
            self,
            message: str = "Failed to process data",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=500, details=details)


class DatabaseError(FinanceTradingError):
    """数据库错误"""

    def __init__(
            self,
            message: str = "Database operation failed",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=500, details=details)


class StrategyError(FinanceTradingError):
    """策略执行错误"""

    def __init__(
            self,
            message: str = "Strategy execution failed",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=500, details=details)


class ValidationError(FinanceTradingError):
    """输入验证错误"""

    def __init__(
            self,
            message: str = "Validation failed for input data",
            details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message=message, status_code=400, details=details)