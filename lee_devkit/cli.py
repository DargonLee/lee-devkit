#!/usr/bin/env python3
"""
Lee DevKit CLI 入口点

提供命令行接口来访问所有 Lee DevKit 功能。
"""

import sys
from lee_devkit.scaffold import LeeScaffold
from lee_devkit import __version__


def main():
    """主入口函数"""
    try:
        scaffold = LeeScaffold()
        scaffold.run()
    except KeyboardInterrupt:
        print("\n⚠️  操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()