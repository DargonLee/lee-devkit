"""
日志工具
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(name: str = 'lee-scaffold', level: str = 'INFO') -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # 设置日志级别
    logger.setLevel(getattr(logging, level.upper()))
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    
    return logger