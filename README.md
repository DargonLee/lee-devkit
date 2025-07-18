# Lee DevKit - 日常开发脚手架工具

基于模板快速创建和管理 CocoaPods 库的命令行工具。

<p align="center">
  <img src="https://img.shields.io/badge/平台-macOS%20%7C%20Linux%20%7C%20Windows-blue" alt="平台">
  <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-green" alt="许可证">
</p>

## ✨ 特性

- � **快支速创建 CocoaPods 库项目** - 基于模板快速搭建库结构
- 📦 **基于 Git 模板仓库** - 使用标准化的 Git 模板
- ⚙️ **可配置的作者信息和组织信息** - 自定义库的元数据
- 🎯 **Example 项目支持** - 可选择是否包含示例项目
- 🔧 **支持自定义输出目录** - 指定生成库的位置
- 📋 **自动更新 podspec 元数据** - 自动填充必要信息
- 📤 **CocoaPods 仓库管理** - 推送 podspec 到 spec 仓库
- 🌐 **跨平台支持** - 支持 macOS、Linux 和 Windows

## 📋 目录

- [Lee DevKit - 日常开发脚手架工具](#lee-devkit---日常开发脚手架工具)
  - [✨ 特性](#-特性)
  - [📋 目录](#-目录)
  - [🔧 安装](#-安装)
    - [前置条件](#前置条件)
    - [方式一：使用 pipx 安装（推荐）](#方式一使用-pipx-安装推荐)
    - [方式二：从源码安装](#方式二从源码安装)
  - [🚀 使用方法](#-使用方法)
    - [创建库](#创建库)
    - [配置工具](#配置工具)
    - [发布库](#发布库)
    - [其他命令](#其他命令)
  - [⚙️ 配置文件](#️-配置文件)
  - [📝 模板要求](#-模板要求)
    - [模板结构](#模板结构)
  - [💻 开发](#-开发)
    - [设置开发环境](#设置开发环境)
    - [运行测试](#运行测试)
  - [📄 许可证](#-许可证)
  - [👥 贡献](#-贡献)
    - [如何贡献](#如何贡献)

## 🔧 安装

### 前置条件

首先，安装 pipx 以获得更好的 Python CLI 工具体验：

```bash
# macOS
brew install pipx
```

### 方式一：使用 pipx 安装（推荐）

```bash
pipx install git+ssh://git@github.com:DargonLee/lee-devkit.git
```

### 方式二：从源码安装

```bash
curl -fsSL https://github.com/DargonLee/lee-devkit/blob/main/install.sh | bash
```

## 🚀 使用方法

### 创建库

```bash
# 创建包含 Example 的项目
lee-devkit create MyLibrary

# 创建不包含 Example 的项目
lee-devkit create MyLibrary --no-example

# 指定输出目录
lee-devkit create MyLibrary --output ~/Projects

# 强制更新模板后创建
lee-devkit create MyLibrary --force-update
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

### 其他命令

```bash
# 更新模板缓存
lee-devkit update

# 列出可用模板
lee-devkit list

# 显示帮助信息
lee-devkit --help

# 显示版本信息
lee-devkit --version
```

## ⚙️ 配置文件

工具会在 `~/.lee_devkit/config.json` 中保存配置信息：

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
    "template_repo": "git@github.com:DargonLee/lee-devkit.git",
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
git clone git@github.com:DargonLee/lee-devkit.git
cd lee-devkit

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

### 运行测试

```bash
# 运行所有测试
python -m unittest discover

# 运行特定测试
python -m unittest tests.test_pod_repo_push
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