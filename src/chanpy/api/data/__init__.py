# src/chanpy/api/data/__init__.py
"""
数据获取API模块
"""
from flask import Blueprint

data_bp = Blueprint('data', __name__, url_prefix='/data')

from . import routes