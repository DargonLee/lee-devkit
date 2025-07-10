# CocoaPods 脚手架工具

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

### 方式一：使用 pip 安装

```bash
pip3 install cocoapods-scaffold
```

### 方式二：从源码安装

```bash
git clone https://github.com/your-company/cocoapods-scaffold.git
cd cocoapods-scaffold
pip3 install -e .
```

### 方式三：使用安装脚本

```bash
curl -fsSL https://raw.githubusercontent.com/your-company/cocoapods-scaffold/main/install.sh | bash
```

## 使用方法

### 基本用法

```bash
# 创建包含 Example 的项目
podscaffold create MyLibrary

# 创建不包含 Example 的项目
podscaffold create MyLibrary --no-example

# 指定输出目录
podscaffold create MyLibrary --output ~/Projects
```

### 配置工具

```bash
# 配置作者信息
podscaffold config --author "Your Name" --email "your@email.com"

# 配置模板仓库
podscaffold config --template-repo "https://github.com/your-company/template.git"

# 显示当前配置
podscaffold config --show
```

### 其他命令

```bash
# 更新模板
podscaffold update

# 列出可用模板
podscaffold list

# 查看帮助
podscaffold --help
```

## 配置说明

工具会在 `~/.cocoapods-scaffold/config.json` 中保存配置信息：

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

### 本地开发

```bash
git clone https://github.com/your-company/cocoapods-scaffold.git
cd cocoapods-scaffold
pip3 install -e .
```

### 运行测试

```bash
python -m pytest tests/
```

### 发布新版本

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

