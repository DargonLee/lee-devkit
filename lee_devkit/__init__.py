"""Lee DevKit - CocoaPods 脚手架工具

基于模板快速创建和管理 CocoaPods 库的命令行工具。
"""

__version__ = "1.0.0"
__author__ = "DargonLee"
__email__ = "2461414445@qq.com"
__description__ = "CocoaPods 脚手架工具 - 基于模板快速创建 CocoaPods 库"
__url__ = "https://github.com/DargonLee/lee-devkit"

# 导出主要类和函数
from .config import Config
from .scaffold import LeeScaffold

__all__ = ['Config', 'LeeScaffold', '__version__']
