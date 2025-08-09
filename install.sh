#!/bin/bash
# Lee DevKit 脚手架工具安装脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_header() {
    echo -e "\n${BLUE}==== $1 ====${NC}\n"
}

# 显示欢迎信息
print_header "Lee DevKit 安装程序"
print_info "正在准备安装 Lee DevKit 脚手架工具..."

# 检查系统类型
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "错误: 此工具仅支持 macOS 系统"
    exit 1
fi

print_info "检查系统依赖..."

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    print_error "错误: 未找到 Python 3"
    print_info "请安装 Python 3.8 或更高版本: brew install python"
    exit 1
fi

# 检查 Python 版本
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    print_error "错误: Python 版本过低 ($PYTHON_VERSION)"
    print_info "请安装 Python 3.8 或更高版本: brew install python"
    exit 1
fi

print_success "Python 版本: $PYTHON_VERSION"

# 检查 git
if ! command -v git &> /dev/null; then
    print_error "错误: 未找到 git"
    print_info "请安装 git: brew install git"
    exit 1
fi

print_success "Git 已安装"

# 检查 CocoaPods
if ! command -v pod &> /dev/null; then
    print_warning "未找到 CocoaPods，某些功能可能受限"
    print_info "建议安装 CocoaPods: sudo gem install cocoapods"
else
    POD_VERSION=$(pod --version)
    print_success "CocoaPods 版本: $POD_VERSION"
fi

print_header "开始安装"

# 安装 pipx（如果需要）
if ! command -v pipx &> /dev/null; then
    print_info "未找到 pipx，正在安装..."
    if command -v brew &> /dev/null; then
        brew install pipx
        pipx ensurepath
    else
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
    fi
    
    # 确保 pipx 在 PATH 中
    if ! command -v pipx &> /dev/null; then
        print_warning "pipx 安装完成，但未在 PATH 中找到"
        print_info "请重新打开终端或运行: source ~/.bash_profile 或 source ~/.zshrc"
        print_info "然后重新运行此安装脚本"
        exit 1
    fi
    
    print_success "pipx 安装完成"
else
    print_success "pipx 已安装"
fi

# 安装 lee-devkit
print_info "正在安装 lee-devkit..."

# 检查是否已安装
if command -v lee-devkit &> /dev/null; then
    CURRENT_VERSION=$(lee-devkit --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "未知")
    print_warning "检测到已安装版本: $CURRENT_VERSION"
    read -p "是否继续更新? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "安装已取消"
        exit 0
    fi
fi

# 执行安装
print_info "正在安装 lee-devkit..."
pipx install --force git+https://github.com/DargonLee/lee-devkit.git

# 安装后脚本会自动设置模板目录，但我们在这里也进行检查
CONFIG_BASE_DIR="$HOME/.config"
CONFIG_DIR="$CONFIG_BASE_DIR/lee_devkit"
TEMPLATE_DIR="$CONFIG_DIR/template"

# 确保 .config 目录存在
if [ ! -d "$CONFIG_BASE_DIR" ]; then
    print_info "创建配置基础目录: $CONFIG_BASE_DIR"
    mkdir -p "$CONFIG_BASE_DIR"
fi

print_info "检查模板目录..."
if [ ! -d "$TEMPLATE_DIR" ]; then
    print_info "模板目录不存在，正在设置..."
    # 创建配置目录和模板目录
    mkdir -p "$CONFIG_DIR"
    
    # 检查当前目录是否有模板
    if [ -d "./template" ] && [ -d "./template/NBTemplateModule" ]; then
        print_info "使用当前目录的模板"
        mkdir -p "$TEMPLATE_DIR"
        cp -r ./template/* "$TEMPLATE_DIR/"
        print_success "模板设置完成"
    else
        # 从远程获取模板
        print_info "正在获取模板..."
        TMP_DIR=$(mktemp -d)
        if git clone --depth 1 https://github.com/DargonLee/lee-devkit.git "$TMP_DIR"; then
            # 检查模板位置
            if [ -d "$TMP_DIR/template" ] && [ -d "$TMP_DIR/template/NBTemplateModule" ]; then
                # 模板在 template 子目录
                print_info "找到模板目录: $TMP_DIR/template"
                mkdir -p "$TEMPLATE_DIR"
                cp -r "$TMP_DIR/template/." "$TEMPLATE_DIR"
                print_success "模板设置完成"
            elif [ -d "$TMP_DIR/NBTemplateModule" ]; then
                # 模板在根目录
                print_info "模板在仓库根目录"
                mkdir -p "$TEMPLATE_DIR"
                cp -r "$TMP_DIR/." "$TEMPLATE_DIR"
                print_success "模板设置完成"
            else
                print_warning "仓库中未找到模板目录，首次使用时将自动下载"
            fi
            rm -rf "$TMP_DIR"
        else
            print_warning "无法获取模板，首次使用时将自动下载"
        fi
    fi
else
    print_success "模板目录已存在"
fi

# 验证安装
if command -v lee-devkit &> /dev/null; then
    VERSION=$(lee-devkit --version 2>/dev/null | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "未知")
    print_header "安装成功!"
    print_success "Lee DevKit 版本: $VERSION"
    
    echo
    print_info "常用命令:"
    echo "  lee-devkit create MyLibrary                   # 创建 CocoaPods 库"
    echo "  lee-devkit create MyLibrary --no-example      # 创建不包含 Example 的库"
    echo "  lee-devkit config --author \"Your Name\"        # 配置作者信息"
    echo "  lee-devkit pod-push                           # 发布 podspec 到 spec 仓库"
    echo "  lee-devkit pod-push --list-repos              # 列出配置的 spec 仓库"
    echo
    echo "运行 'lee-devkit --help' 查看更多选项"
else
    print_error "安装失败，请检查错误信息"
    echo
    print_info "可能的解决方案:"
    echo "1. 确保 ~/.local/bin 在 PATH 中"
    echo "2. 重新加载 shell 配置: source ~/.bash_profile 或 source ~/.zshrc"
    echo "3. 尝试手动安装: pip3 install --user git+https://github.com/DargonLee/lee-devkit.git"
    exit 1
fi