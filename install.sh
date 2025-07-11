#!/bin/bash
# 九号 iOS 脚手架工具安装脚本

set -e

echo "🚀 正在安装 九号 iOS 脚手架工具..."

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要 Python 3.7 或更高版本"
    exit 1
fi

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 需要 git"
    exit 1
fi

echo "✅ 环境检查通过"

# 检查是否有 pipx
if command -v pipx &> /dev/null; then
    echo "📦 使用 pipx 安装..."
    pipx install git+ssh://git@git.ninebot.com/iOS/podmaker.git@develop
    echo "✅ 安装完成！现在可以在任何地方使用 'ninebot-cli' 命令"
fi

# 验证安装
if command -v ninebot-cli &> /dev/null; then
    echo "🎉 安装成功！"
    echo ""
    echo "使用方法:"
    echo "  ninebot-cli cocoapods create MyLibrary              # 创建不包含 Example 的项目"
    echo "  ninebot-cli cocoapods create MyLibrary --include-example # 创建包含 Example 的项目"
    echo "  ninebot-cli config --author \"Your Name\"   # 配置作者信息"
    echo "  ninebot-cli cocoapods create MyLibrary --force-update # 强制更新模板"
    echo ""
    echo "运行 'ninebot-cli --help' 查看更多选项"
else
    echo "❌ 安装失败，请检查错误信息"
    echo ""
    echo "如果使用虚拟环境安装，请确保："
    echo "1. ~/.local/bin 在 PATH 中"
    echo "2. 重新加载了 shell 配置"
    echo "3. 或者手动运行: source ~/.ninebot-cli-env/bin/activate"
    exit 1
fi
