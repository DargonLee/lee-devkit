# 贡献指南

感谢您对 Lee DevKit 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/DargonLee/lee-devkit/issues) 确保问题尚未被报告
2. 创建新的 Issue，包含：
   - 清晰的标题和描述
   - 重现步骤（如果是 bug）
   - 期望的行为
   - 实际的行为
   - 系统信息（macOS 版本、Python 版本等）

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/YOUR_USERNAME/lee-devkit.git
   cd lee-devkit
   ```

2. **设置开发环境**
   ```bash
   # 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate
   
   # 安装开发依赖
   make install-dev
   
   # 开发模式安装
   make dev-install
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **编写代码**
   - 遵循现有的代码风格
   - 添加必要的测试
   - 更新文档（如果需要）

5. **运行测试**
   ```bash
   make test
   make lint
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

7. **推送并创建 Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 开发规范

### 代码风格

- 使用 [Black](https://black.readthedocs.io/) 进行代码格式化
- 使用 [isort](https://pycqa.github.io/isort/) 整理导入
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用类型提示（Python 3.7+）

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式（不影响功能）
- `refactor:` 重构代码
- `test:` 添加或修改测试
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加 Git tag 管理功能
fix: 修复配置文件路径问题
docs: 更新安装说明
```

### 测试

- 为新功能编写测试
- 确保所有测试通过
- 保持测试覆盖率在 80% 以上

### 文档

- 更新 README.md（如果需要）
- 添加或更新 docstring
- 更新 CHANGELOG.md

## 开发工具

项目提供了 Makefile 来简化开发流程：

```bash
make help          # 查看所有可用命令
make install-dev   # 安装开发依赖
make test          # 运行测试
make lint          # 代码检查
make format        # 格式化代码
make clean         # 清理构建文件
```

## 发布流程

1. 更新版本号（`lee_devkit/__init__.py` 和 `pyproject.toml`）
2. 更新 `CHANGELOG.md`
3. 创建 Git tag
4. 构建和发布包

## 获得帮助

如果您在贡献过程中遇到问题，可以：

- 查看现有的 [Issues](https://github.com/DargonLee/lee-devkit/issues)
- 创建新的 Issue 寻求帮助
- 查看项目文档

再次感谢您的贡献！🎉