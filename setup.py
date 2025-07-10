# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cocoapods-scaffold",
    version="1.0.0",
    author="Your Company",
    author_email="dev@yourcompany.com",
    description="CocoaPods 脚手架工具 - 基于模板快速创建 CocoaPods 库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-company/cocoapods-scaffold",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=[
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "podscaffold=cocoapods_scaffold.cli:main",
        ],
    },
    include_package_data=True,
)

# ---

# cocoapods_scaffold/__init__.py


# ---

# cocoapods_scaffold/cli.py
# 这里放置上面创建的主要代码

# ---

# install.sh
#!/bin/bash

# CocoaPods 脚手架工具安装脚本

set -e

INSTALL_DIR="/usr/local/bin"
SCRIPT_NAME="podscaffold"

echo "🚀 正在安装 CocoaPods 脚手架工具..."

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3.7 或更高版本"
    exit 1
fi

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 需要 pip3"
    exit 1
fi

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 需要 git"
    exit 1
fi

echo "✅ 环境检查通过"

# 创建临时目录
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "📥 正在下载最新版本..."

# 如果是从源码安装
if [ -f "setup.py" ]; then
    echo "🔧 从源码安装..."
    pip3 install -e .
else
    # 从 PyPI 安装 (如果已发布)
    echo "🔧 从 PyPI 安装..."
    pip3 install cocoapods-scaffold
fi

echo "✅ 安装完成！"

# 验证安装
if command -v podscaffold &> /dev/null; then
    echo "🎉 安装成功！"
    echo ""
    echo "使用方法:"
    echo "  podscaffold create MyLibrary              # 创建包含 Example 的项目"
    echo "  podscaffold create MyLibrary --no-example # 创建不包含 Example 的项目"
    echo "  podscaffold config --author \"Your Name\"   # 配置作者信息"
    echo "  podscaffold update                        # 更新模板"
    echo ""
    echo "运行 'podscaffold --help' 查看更多选项"
else
    echo "❌ 安装失败，请检查错误信息"
    exit 1
fi

# 清理临时文件
rm -rf "$TEMP_DIR"

# ---

# README.md

