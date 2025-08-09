# Lee DevKit - 日常开发脚手架工具

基于模板快速创建和管理 CocoaPods 库的命令行工具。

<p align="center">
  <img src="https://img.shields.io/badge/平台-macOS-blue" alt="平台">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-green" alt="许可证">
</p>

## ✨ 特性

- 🚀 **快速创建 CocoaPods 库项目** - 基于模板快速搭建库结构
- 📦 **基于 Git 模板仓库** - 使用标准化的 Git 模板
- 🏷️ **Git Tag 管理** - 删除并重新创建 Git tag，支持本地和远程同步
- ⚙️ **可配置的作者信息和组织信息** - 自定义库的元数据
- 🎯 **Example 项目支持** - 可选择是否包含示例项目
- 🔧 **支持自定义输出目录** - 指定生成库的位置
- 📋 **自动更新 podspec 元数据** - 自动填充必要信息
- 📤 **CocoaPods 仓库管理** - 推送 podspec 到 spec 仓库
- 🌐 **macOS 平台支持** - 专为 macOS 平台优化设计

## 📋 目录

- [Lee DevKit - 日常开发脚手架工具](#lee-devkit---日常开发脚手架工具)
  - [✨ 特性](#-特性)
  - [📋 目录](#-目录)
  - [🔧 安装](#-安装)
    - [系统要求](#系统要求)
    - [前置条件](#前置条件)
      - [1. 安装 pipx（推荐）](#1-安装-pipx推荐)
      - [2. 验证环境](#2-验证环境)
    - [安装方式](#安装方式)
      - [方式一：使用 pipx 安装（推荐）](#方式一使用-pipx-安装推荐)
      - [方式二：使用安装脚本](#方式二使用安装脚本)
      - [方式三：从源码安装（开发者）](#方式三从源码安装开发者)
    - [升级](#升级)
      - [升级到最新版本](#升级到最新版本)
      - [检查更新](#检查更新)
    - [卸载](#卸载)
      - [完全卸载](#完全卸载)
      - [重置配置](#重置配置)
      - [验证安装](#验证安装)
      - [获取帮助](#获取帮助)
  - [🚀 使用方法](#-使用方法)
    - [快速开始](#快速开始)
    - [创建 CocoaPods 库](#创建-cocoapods-库)
      - [基本用法](#基本用法)
      - [高级选项](#高级选项)
      - [创建后的步骤](#创建后的步骤)
    - [配置工具](#配置工具)
    - [发布库](#发布库)
    - [Git Tag 管理 ✅](#git-tag-管理-)
      - [创建 Tag](#创建-tag)
      - [重新创建 Tag](#重新创建-tag)
    - [版本和更新管理](#版本和更新管理)
    - [维护和管理](#维护和管理)
      - [清理和重置](#清理和重置)
      - [备份和恢复配置](#备份和恢复配置)
  - [⚙️ 配置文件](#️-配置文件)
  - [📝 模板要求](#-模板要求)
    - [模板结构](#模板结构)
  - [💻 开发](#-开发)
    - [设置开发环境](#设置开发环境)
    - [卸载开发环境](#卸载开发环境)
    - [运行测试](#运行测试)
    - [代码质量](#代码质量)
  - [📄 许可证](#-许可证)
  - [👥 贡献](#-贡献)
    - [如何贡献](#如何贡献)

## 🔧 安装

### 系统要求

- **操作系统**: macOS 10.14 或更高版本
- **Python**: 3.8 或更高版本
- **Git**: 用于模板管理和版本控制
- **CocoaPods**: 用于 iOS 开发（可选，但推荐）

### 前置条件

#### 1. 安装 pipx（推荐）

pipx 是安装 Python CLI 工具的最佳方式，它会为每个工具创建独立的虚拟环境：

```bash
# 使用 Homebrew 安装 pipx
brew install pipx

# 确保 pipx 的 bin 目录在 PATH 中
pipx ensurepath

# 重新加载 shell 配置
source ~/.zshrc  # 或 source ~/.bash_profile
```

#### 2. 验证环境

```bash
# 检查 Python 版本
python3 --version  # 应该是 3.8 或更高

# 检查 Git
git --version

# 检查 CocoaPods（可选）
pod --version
```

### 安装方式

#### 方式一：使用 pipx 安装（推荐）

```bash
# 安装最新版本
pipx install git+https://github.com/DargonLee/lee-devkit.git

# 验证安装
lee-devkit --version
```

#### 方式二：使用安装脚本

```bash
# 一键安装脚本（会自动安装 pipx 和 lee-devkit）
curl -fsSL https://raw.githubusercontent.com/DargonLee/lee-devkit/main/install.sh | bash
```

#### 方式三：从源码安装（开发者）

```bash
# 克隆仓库
git clone https://github.com/DargonLee/lee-devkit.git
cd lee-devkit

# 使用 pipx 安装本地版本
pipx install .

# 或者使用 pip 安装到当前环境
pip install .
```

### 升级

#### 升级到最新版本

```bash
# 使用 pipx 升级
pipx upgrade lee-devkit

# 或者强制重新安装最新版本
pipx install --force git+https://github.com/DargonLee/lee-devkit.git
```

#### 检查更新

```bash
# 查看当前版本
lee-devkit --version

# 查看可用版本（在 GitHub Releases 页面）
# https://github.com/DargonLee/lee-devkit/releases
```

### 卸载

#### 完全卸载

```bash
# 1. 卸载程序
pipx uninstall lee-devkit

# 2. 删除配置文件和模板（可选）
rm -rf ~/.config/lee_devkit

# 3. 清理缓存（可选）
rm -rf ~/.cache/lee_devkit  # 如果存在
```

#### 重置配置

如果只想重置配置而不卸载程序：

```bash
# 重置配置到默认值
lee-devkit config --reset

# 或者手动删除配置文件
rm -rf ~/.config/lee_devkit
```

#### 验证安装

安装完成后，验证是否正常工作：

```bash
# 检查版本
lee-devkit --version

# 检查配置
lee-devkit config --show

# 测试创建功能（不会实际创建项目）
lee-devkit create --help

# 检查模板是否正常
lee-devkit list
```

#### 获取帮助

- 查看帮助信息：`lee-devkit --help`
- 报告问题：[GitHub Issues](https://github.com/DargonLee/lee-devkit/issues)
- 查看文档：[项目 README](https://github.com/DargonLee/lee-devkit#readme)
- 查看更新日志：[CHANGELOG.md](CHANGELOG.md)

## 🚀 使用方法

### 快速开始

首次使用前，建议先配置基本信息：

```bash
# 配置作者信息（必需）
lee-devkit config --author "Your Name" --email "your@email.com"

# 查看当前配置
lee-devkit config --show

# 查看帮助
lee-devkit --help
```

### 创建 CocoaPods 库

#### 基本用法

```bash
# 创建包含 Example 项目的库（推荐用于开发和测试）
lee-devkit create MyLibrary --include-example

# 创建不包含 Example 的库（适用于纯库项目）
lee-devkit create MyLibrary

# 查看创建选项
lee-devkit create --help
```

#### 高级选项

```bash
# 指定输出目录
lee-devkit create MyLibrary --output ~/Projects

# 强制更新模板后创建（获取最新模板）
lee-devkit create MyLibrary --force-update

# 组合使用多个选项
lee-devkit create MyAwesomeLibrary \
  --include-example \
  --output ~/iOS-Libraries \
  --force-update
```

#### 创建后的步骤

创建完成后，按照提示进行后续操作：

```bash
# 1. 进入项目目录
cd MyLibrary

# 2. 如果包含 Example 项目，安装依赖
cd Example
pod install

# 3. 打开项目开始开发
open MyLibrary.xcworkspace  # 如果有 Example
# 或者直接编辑库代码
```

### 配置工具

```bash
# 配置作者信息
lee-devkit config --author "Your Name" --email "your@email.com"

# 配置组织信息
lee-devkit config --organization "Your Company"

# 配置模板仓库
lee-devkit config --template-repo "https://github.com/your-company/template.git"

# 显示当前配置
lee-devkit config --show

# 使用默认编辑器编辑配置
lee-devkit config --edit

# 重置为默认配置
lee-devkit config --reset
```

### 发布库

```bash
# 自动检测当前目录下的 podspec 文件并发布
lee-devkit pod-push

# 发布指定的 podspec 文件
lee-devkit pod-push MyLibrary.podspec

# 发布到指定的 spec 仓库
lee-devkit pod-push --repo MySpecs

# 管理 spec 仓库
lee-devkit pod-push --list-repos                           # 列出所有配置的 spec 仓库
lee-devkit pod-push --add-repo MySpecs git@example.com:MySpecs.git  # 添加 spec 仓库
lee-devkit pod-push --remove-repo MySpecs                  # 移除 spec 仓库
lee-devkit pod-push --set-default-repo MySpecs             # 设置默认 spec 仓库

# 发布选项
lee-devkit pod-push --no-allow-warnings                    # 禁用 --allow-warnings 选项
lee-devkit pod-push --no-verbose                           # 禁用 --verbose 选项
lee-devkit pod-push --no-skip-import-validation            # 禁用 --skip-import-validation 选项
lee-devkit pod-push --no-use-libraries                     # 禁用 --use-libraries 选项
lee-devkit pod-push --no-use-modular-headers               # 禁用 --use-modular-headers 选项
lee-devkit pod-push --extra-args="--swift-version=5.0"     # 添加额外参数
```

### Git Tag 管理 ✅

#### 创建 Tag

```bash
# 创建并推送 tag（基本用法）
lee-devkit tag create 1.2.8

# 创建带注释的 tag
lee-devkit tag create 1.2.8 --message "Release version 1.2.8"

# 指定 commit 或分支
lee-devkit tag create 1.2.8 --commit abc1234

# 只创建本地 tag，不推送
lee-devkit tag create 1.2.8 --no-push

# 指定远程仓库名称
lee-devkit tag create 1.2.8 --remote upstream

# 预览将要执行的命令（不实际执行）
lee-devkit tag create 1.2.8 --dry-run
```

#### 重新创建 Tag

```bash
# 删除并重新创建 tag（基本用法）
lee-devkit tag retag 1.2.8

# 创建带注释的 tag
lee-devkit tag retag 1.2.8 --message "Release version 1.2.8"

# 指定 commit 或分支
lee-devkit tag retag 1.2.8 --commit abc1234

# 指定远程仓库名称
lee-devkit tag retag 1.2.8 --remote upstream

# 预览将要执行的命令（不实际执行）
lee-devkit tag retag 1.2.8 --dry-run

# 强制执行（即使 tag 不存在也继续）
lee-devkit tag retag 1.2.8 --force

# 组合使用多个参数
lee-devkit tag retag 1.2.8 --message "Release version 1.2.8" --commit main --remote origin
```

### 版本和更新管理

```bash
# 显示版本信息
lee-devkit --version

# 更新模板缓存（获取最新模板）
lee-devkit update

# 列出可用模板
lee-devkit list

# 显示帮助信息
lee-devkit --help

# 显示特定命令的帮助
lee-devkit create --help
lee-devkit config --help
lee-devkit pod-push --help
```

### 维护和管理

#### 清理和重置

```bash
# 清理模板缓存
rm -rf ~/.config/lee_devkit/template

# 重置配置到默认值
lee-devkit config --reset

# 查看配置文件位置
echo ~/.config/lee_devkit/config.json
```

#### 备份和恢复配置

```bash
# 备份配置
cp ~/.config/lee_devkit/config.json ~/lee-devkit-config-backup.json

# 恢复配置
cp ~/lee-devkit-config-backup.json ~/.config/lee_devkit/config.json
```

## ⚙️ 配置文件

工具会在 `~/.config/lee_devkit/config.json` 中保存配置信息：

```json
{
  "author": "Your Name",
  "email": "your.email@company.com",
  "organization": "Your Company",
  "prefix": "YC",
  "editor": "code",
  "git": {
    "default_branch": "main",
    "auto_push": false,
    "commit_template": "feat: {message}"
  },
  "cocoapods": {
    "template_repo": "https://github.com/DargonLee/lee-devkit.git",
    "default_platform": "iOS",
    "swift_version": "5.0"
  },
  "spec_repos": {
    "default": "NBSpecs",
    "repos": {
      "NBSpecs": "git@git.ninebot.com:iOS/NBSpecs.git"
    }
  }
}
```

## 📝 模板要求

模板仓库需要包含一个名为 `NBTemplateModule` 的目录，工具会：

1. 将所有文件和目录名中的 `NBTemplateModule` 替换为新的模块名
2. 将所有文件内容中的 `NBTemplateModule` 替换为新的模块名
3. 自动更新 podspec 文件的元数据

### 模板结构

```
template/
├── NBTemplateModule/          # 主库目录
│   ├── Resources/             # 资源目录
│   └── Sources/               # 源代码目录
├── Example/                   # 示例项目（可选）
├── NBTemplateModule.podspec   # Podspec 文件
├── LICENSE                    # 许可证文件
└── README.md                  # README 文件
```

## 💻 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/DargonLee/lee-devkit.git
cd lee-devkit

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

### 卸载开发环境

```bash
# 如果使用开发模式安装，卸载
pip uninstall -y lee-devkit
# 删除配置文件和模板
rm -rf ~/.config/lee_devkit

# 删除虚拟环境（可选）
deactivate  # 如果当前在虚拟环境中
rm -rf venv
```

### 运行测试

```bash
# 使用 Makefile（推荐）
make test

# 或者直接使用 pytest
python -m pytest tests/ -v

# 运行特定测试
python -m unittest tests.test_pod_repo_push

# 生成覆盖率报告
make test  # 会自动生成 htmlcov/ 目录
```

### 代码质量

```bash
# 代码格式化
make format

# 代码检查
make lint

# 类型检查
mypy lee_devkit
```

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 👥 贡献

欢迎贡献！请随时提交 Pull Request 或创建 Issue。

### 如何贡献

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m '添加一些很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request