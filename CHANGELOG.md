# 更新日志

本文档记录了 Lee DevKit 的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 无

### 更改
- 无

### 修复
- 无

## [1.0.0] - 2024-02-09

### 新增
- 🚀 快速创建 CocoaPods 库项目功能
- 📦 基于 Git 模板仓库的项目生成
- 🏷️ Git Tag 管理功能，支持本地和远程同步
- ⚙️ 可配置的作者信息和组织信息
- 🎯 Example 项目支持，可选择是否包含示例项目
- 🔧 支持自定义输出目录
- 📋 自动更新 podspec 元数据
- 📤 CocoaPods 仓库管理，推送 podspec 到 spec 仓库
- 🌐 专为 macOS 平台优化设计
- 统一配置管理系统，使用 `~/.config/lee_devkit` 目录
- 完整的命令行界面，支持多种操作模式

### 技术特性
- Python 3.7+ 支持
- 模块化架构设计
- 完整的错误处理和用户反馈
- 自动模板目录设置
- 支持多种安装方式（pipx、源码安装）

### 命令支持
- `lee-devkit create` - 创建新的 CocoaPods 库
- `lee-devkit config` - 配置管理
- `lee-devkit pod-push` - 发布 podspec 到仓库
- 完整的帮助系统和版本信息

[未发布]: https://github.com/DargonLee/lee-devkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/DargonLee/lee-devkit/releases/tag/v1.0.0