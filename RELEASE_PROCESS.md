# Lee DevKit 发布流程指南

本文档详细说明了 Lee DevKit 项目的发布流程，基于项目 Makefile 中定义的自动化命令。

## 📋 发布前准备

### 1. 环境检查
确保你的开发环境已正确设置：
```bash
# 安装开发依赖
make install-dev

# 开发模式安装
make dev-install
```

### 2. 代码质量检查
```bash
# 运行测试
make test

# 代码检查
make lint

# 格式化代码
make format
```

## 🚀 发布流程

### 方式一：交互式发布（推荐）

这是最安全的发布方式，包含完整的检查和确认步骤：

```bash
make release
```

**流程说明：**
1. 自动执行发布前检查（测试、代码检查、版本一致性检查等）
2. 显示当前版本号
3. 提示输入新版本号
4. 自动更新 `lee_devkit/__init__.py` 和 `pyproject.toml` 中的版本号
5. 提醒手动更新 `CHANGELOG.md`
6. 确认 CHANGELOG 更新完成后继续
7. 提交版本更新到 Git
8. 创建版本标签
9. 推送到远程仓库

### 方式二：快速发布

适用于紧急修复或已经确认所有检查都通过的情况：

```bash
make quick-release VERSION=1.1.0
```

**注意：** 
- 必须指定 VERSION 参数
- 跳过交互确认，但仍会执行发布前检查
- 需要手动更新 CHANGELOG.md

### 方式三：发布候选版本

用于创建测试版本：

```bash
make release-candidate
```

适用于创建如 `1.1.0-rc1` 这样的候选版本。

## 📝 版本管理

### 版本号规范
项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：
- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 版本检查命令
```bash
# 显示当前版本信息
make show-version

# 检查版本一致性
make version-check

# 检查 CHANGELOG 更新
make changelog-check
```

## 📋 CHANGELOG.md 更新指南

发布前必须更新 `CHANGELOG.md`：

1. 将 `## [未发布]` 改为 `## [版本号] - 日期`
2. 确保包含以下部分（如适用）：
   - `### 新增` - 新功能
   - `### 更改` - 现有功能的更改
   - `### 修复` - 问题修复
   - `### 移除` - 移除的功能

**示例：**
```markdown
## [1.1.0] - 2024-01-15

### 新增
- 添加了新的命令行选项
- 支持自定义模板路径

### 修复
- 修复了配置文件读取问题
- 解决了 Windows 平台兼容性问题
```

## 🔧 发布前检查清单

使用 `make pre-release` 命令会自动执行以下检查：

- [ ] 清理构建文件
- [ ] 运行所有测试
- [ ] 代码风格检查
- [ ] 版本号一致性检查（`__init__.py` 和 `pyproject.toml`）
- [ ] CHANGELOG.md 更新检查

## 🆘 问题处理

### 版本回滚
如果发现版本更新有误，可以回滚：
```bash
make rollback-version
```

### 常见问题

1. **版本不一致错误**
   ```
   ❌ 版本不一致: __init__.py (1.0.0) vs pyproject.toml (1.0.1)
   ```
   **解决方案：** 手动同步两个文件中的版本号

2. **测试失败**
   **解决方案：** 修复测试问题后重新运行发布流程

3. **CHANGELOG 未更新**
   **解决方案：** 按照上述指南更新 CHANGELOG.md

## 📦 构建和上传

如需手动构建和上传到 PyPI：

```bash
# 构建分发包
make build

# 检查包
make check

# 上传到 PyPI
make upload
```

## 🔗 发布后验证

发布完成后，验证发布是否成功：

1. 检查 GitHub 上的标签和发布页面
2. 验证 PyPI 上的新版本
3. 测试安装新版本：
   ```bash
   pipx install --force git+https://github.com/DargonLee/lee-devkit.git
   ```

## 📞 获取帮助

查看所有可用的 Make 命令：
```bash
make help
```

---

**提示：** 建议在发布前在测试环境中验证所有功能，确保新版本的稳定性。