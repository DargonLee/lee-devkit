# 日常开发脚手架工具

基于模板快速创建 CocoaPods 库的命令行工具。

## 特性

- 🚀 快速创建 CocoaPods 库项目
- 📦 基于 Git 模板仓库
- ⚙️ 可配置的作者信息和组织信息
- 🎯 可选择是否包含 Example 项目
- 🔧 支持自定义输出目录
- 📋 自动更新 podspec 元数据
- 🌐 跨平台支持 (macOS, Linux, Windows)

## 安装

### 先安装 pipx
```bash
brew install pipx
```

### 方式一：使用 pipx 安装

```bash
pipx install git@github.com:DargonLee/lee-devkit.git
```

### 方式二：从源码安装

```bash
git clone https://github.com/DargonLee/lee-devkit.git
cd lee-devkit
pip3 install -e .
```

### 方式三：使用安装脚本

```bash
curl -fsSL https://github.com/DargonLee/lee-devkit/blob/main/install.sh | bash
```

## 使用方法

### 基本用法

```bash
# 创建包含 Example 的项目
lee-devkit create MyLibrary

# 创建不包含 Example 的项目
lee-devkit create MyLibrary --no-example

# 指定输出目录
lee-devkit create MyLibrary --output ~/Projects
```

### 配置工具

```bash
# 配置作者信息
lee-devkit config --author "Your Name" --email "your@email.com"

# 配置模板仓库
lee-devkit config --template-repo "https://github.com/your-company/template.git"

# 显示当前配置
lee-devkit config --show
```

### 其他命令

```bash
# 更新模板
lee-devkit update

# 列出可用模板
lee-devkit list

# 查看帮助
lee-devkit --help
```

## 配置说明

工具会在 `~/.lee_devkit/config.json` 中保存配置信息：

```json
{
  "template_repo": "https://github.com/your-company/cocoapods-template.git",
  "author": "Your Name",
  "email": "your.email@company.com",
  "organization": "Your Company",
  "prefix": "YC"
}
```

## 模板要求

模板仓库需要包含一个名为 `NBTemplateModule` 的目录，工具会：

1. 将所有文件和目录名中的 `NBTemplateModule` 替换为新的模块名
2. 将所有文件内容中的 `NBTemplateModule` 替换为新的模块名
3. 自动更新 podspec 文件的元数据

## 开发

### 本地开发环境

```bash
git clone git@git.ninebot.com:iOS/podmaker.git
cd podmaker
git checkout develop  # 切换到 develop 分支

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装
pip install -e .
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

