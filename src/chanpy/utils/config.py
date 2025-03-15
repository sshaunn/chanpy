# src/chanpy/utils/config.py
import os
from pathlib import Path
from typing import Dict, Any

import tomli


class ConfigError(Exception):
    """配置相关错误"""
    pass


class Config:
    """配置管理类"""

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._env = os.environ.get("ENV", "local").lower()
        self._loaded = False

    def load(self) -> None:
        """加载配置文件"""
        if self._loaded:
            return

        config_dir = Path(__file__).parent.parent.parent.parent / "config"

        # 加载基础配置
        base_config_path = config_dir / "base.toml"
        if not base_config_path.exists():
            raise ConfigError(f"基础配置文件不存在: {base_config_path}")

        with open(base_config_path, "rb") as f:
            self._config = tomli.load(f)

        # 加载环境特定配置
        env_config_path = config_dir / f"{self._env}.toml"
        if not env_config_path.exists():
            raise ConfigError(f"环境配置文件不存在: {env_config_path}")

        with open(env_config_path, "rb") as f:
            env_config = tomli.load(f)
            self._merge_configs(self._config, env_config)

        # 尝试加载机密配置(如果存在)
        secrets_path = config_dir / "secrets.toml"
        if secrets_path.exists():
            with open(secrets_path, "rb") as f:
                secrets_config = tomli.load(f)
                self._merge_configs(self._config, secrets_config)

        self._loaded = True

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """合并配置字典，允许深度合并嵌套字典"""
        for key, value in override.items():
            if (
                    key in base
                    and isinstance(base[key], dict)
                    and isinstance(value, dict)
            ):
                self._merge_configs(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持使用点号访问嵌套配置"""
        if not self._loaded:
            self.load()

        parts = key.split('.')
        config = self._config

        for part in parts:
            if isinstance(config, dict) and part in config:
                config = config[part]
            else:
                return default

        return config

    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        if not self._loaded:
            self.load()
        return self._config.copy()

    @property
    def env(self) -> str:
        """获取当前环境名称"""
        return self._env


# 创建全局配置实例
config = Config()