# src/chanpy/api/strategy/__init__.py
"""
策略API模块
"""
from flask import Blueprint

strategy_bp = Blueprint('strategy', __name__, url_prefix='/strategy')

from . import routes