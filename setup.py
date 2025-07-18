from setuptools import setup, find_packages
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path
from setuptools.command.install import install
from setuptools.command.develop import develop

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def setup_template_directory():
    """设置模板目录"""
    # 配置目录路径
    config_base = Path.home / ".config"
    config_dir = config_base / "lee_devkit"
    template_dir = config_dir / "template"
    
    # 创建配置目录
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # 如果模板目录已存在，则跳过
    if template_dir.exists():
        print(f"✅ 模板目录已存在: {template_dir}")
        return
    
    print(f"🔧 正在设置模板目录: {template_dir}")
    
    # 尝试从 Git 仓库获取模板
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            
            # 克隆仓库
            print("📥 正在获取模板...")
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "git@github.com:DargonLee/lee-devkit.git", str(tmp_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"⚠️ 无法克隆仓库: {result.stderr}")
                print("首次使用时将自动下载模板")
                return
            
            # 检查模板目录是否存在
            src_template = tmp_path / "template"
            if not src_template.exists():
                print("⚠️ 仓库中未找到模板目录")
                print("首次使用时将自动下载模板")
                return
            
            # 复制模板
            template_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src_template, template_dir, dirs_exist_ok=True)
            print(f"✅ 模板设置完成: {template_dir}")
            
    except Exception as e:
        print(f"⚠️ 设置模板目录时出错: {e}")
        print("首次使用时将自动下载模板")

# 安装后脚本
def run_post_install_script():
    """运行安装后脚本"""
    try:
        setup_template_directory()
    except Exception as e:
        print(f"⚠️ 安装后脚本执行失败: {e}")

# 自定义安装命令
class PostInstallCommand(install):
    """安装后运行脚本的自定义安装命令"""
    def run(self):
        install.run(self)
        run_post_install_script()

# 自定义开发模式安装命令
class PostDevelopCommand(develop):
    """安装后运行脚本的自定义开发模式安装命令"""
    def run(self):
        develop.run(self)
        run_post_install_script()

setup(
    name="lee-devkit",
    version="1.0.0",
    author="DargonLee",
    author_email="2461414445@qq.com",
    description="CocoaPods 脚手架工具 - 基于模板快速创建 CocoaPods 库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DargonLee/lee-devkit",
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
            "lee-devkit=lee_devkit.cli:main",
        ],
    },
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
)