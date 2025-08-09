# Lee DevKit Makefile
# 简化开发和部署流程

.PHONY: help install install-dev test lint format clean build upload check dev-install
.PHONY: release pre-release version-check changelog-check quick-release release-candidate rollback-version show-version

# 默认目标
help:
	@echo "Lee DevKit 开发工具"
	@echo ""
	@echo "📦 开发命令:"
	@echo "  install         - 安装项目依赖"
	@echo "  install-dev     - 安装开发依赖"
	@echo "  dev-install     - 开发模式安装"
	@echo "  test            - 运行测试"
	@echo "  lint            - 代码检查"
	@echo "  format          - 格式化代码"
	@echo "  clean           - 清理构建文件"
	@echo ""
	@echo "🚀 发布命令:"
	@echo "  show-version    - 显示当前版本信息"
	@echo "  version-check   - 检查版本一致性"
	@echo "  changelog-check - 检查 CHANGELOG 更新"
	@echo "  pre-release     - 发布前检查"
	@echo "  release         - 交互式发布新版本"
	@echo "  quick-release   - 快速发布 (需要 VERSION=x.x.x)"
	@echo "  release-candidate - 创建发布候选版本"
	@echo "  rollback-version - 回滚版本更改"
	@echo ""
	@echo "📦 构建命令:"
	@echo "  build           - 构建分发包"
	@echo "  check           - 检查包"
	@echo "  upload          - 上传到 PyPI"
	@echo ""
	@echo "💡 使用示例:"
	@echo "  make release                    # 交互式发布"
	@echo "  make quick-release VERSION=1.1.0  # 快速发布指定版本"
	@echo "  make pre-release               # 只执行发布前检查"

# 安装依赖
install:
	pip install -r requirements.txt

# 安装开发依赖
install-dev:
	pip install -r requirements-dev.txt

# 开发模式安装
dev-install:
	pip install -e .

# 运行测试
test:
	python -m pytest tests/ -v --cov=lee_devkit --cov-report=html

# 代码检查
lint:
	flake8 lee_devkit tests
	mypy lee_devkit

# 格式化代码
format:
	black lee_devkit tests
	isort lee_devkit tests

# 清理构建文件
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# 构建分发包
build: clean
	python -m build

# 上传到 PyPI
upload: build
	python -m twine upload dist/*

# 检查包
check:
	python -m twine check dist/*

# 发布相关命令
.PHONY: release pre-release version-check changelog-check

# 检查版本一致性
version-check:
	@echo "🔍 检查版本一致性..."
	@INIT_VERSION=$$(grep "__version__ = " lee_devkit/__init__.py | sed 's/.*"\(.*\)".*/\1/'); \
	TOML_VERSION=$$(grep "version = " pyproject.toml | head -1 | sed 's/.*"\(.*\)".*/\1/'); \
	if [ "$$INIT_VERSION" != "$$TOML_VERSION" ]; then \
		echo "❌ 版本不一致: __init__.py ($$INIT_VERSION) vs pyproject.toml ($$TOML_VERSION)"; \
		exit 1; \
	else \
		echo "✅ 版本一致: $$INIT_VERSION"; \
	fi

# 检查 CHANGELOG 是否更新
changelog-check:
	@echo "🔍 检查 CHANGELOG.md..."
	@if grep -q "## \[未发布\]" CHANGELOG.md && ! grep -A 10 "## \[未发布\]" CHANGELOG.md | grep -q "### 新增\|### 更改\|### 修复" | grep -v "- 无"; then \
		echo "⚠️  CHANGELOG.md 中的 [未发布] 部分似乎为空，请确保已更新"; \
	else \
		echo "✅ CHANGELOG.md 检查通过"; \
	fi

# 发布前检查
pre-release: clean test lint version-check changelog-check
	@echo "🔍 执行发布前检查..."
	@echo "✅ 所有检查通过，可以发布！"

# 交互式发布
release: pre-release
	@echo "🚀 准备发布新版本..."
	@echo "当前版本: $$(grep "__version__ = " lee_devkit/__init__.py | sed 's/.*"\(.*\)".*/\1/')"
	@read -p "输入新版本号 (例如: 1.1.0): " version; \
	if [ -z "$$version" ]; then \
		echo "❌ 版本号不能为空"; \
		exit 1; \
	fi; \
	echo "📝 更新版本号到 $$version..."; \
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$$version\"/" lee_devkit/__init__.py; \
	sed -i '' "s/version = \".*\"/version = \"$$version\"/" pyproject.toml; \
	echo "📋 请手动更新 CHANGELOG.md，将 [未发布] 改为 [$$version] - $$(date +%Y-%m-%d)"; \
	read -p "CHANGELOG.md 已更新完成？(y/N): " confirm; \
	if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
		echo "❌ 请先更新 CHANGELOG.md"; \
		exit 1; \
	fi; \
	echo "📦 提交版本更新..."; \
	git add .; \
	git commit -m "chore: bump version to $$version"; \
	echo "🏷️  创建标签..."; \
	git tag -a "v$$version" -m "Release version $$version"; \
	echo "📤 推送到远程仓库..."; \
	git push origin main; \
	git push origin "v$$version"; \
	echo "✅ 版本 $$version 发布完成！"; \
	echo "🔗 查看发布: https://github.com/DargonLee/lee-devkit/releases/tag/v$$version"

# 快速发布（跳过交互）
quick-release: pre-release
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ 请指定版本号: make quick-release VERSION=1.1.0"; \
		exit 1; \
	fi
	@echo "🚀 快速发布版本 $(VERSION)..."
	@sed -i '' "s/__version__ = \".*\"/__version__ = \"$(VERSION)\"/" lee_devkit/__init__.py
	@sed -i '' "s/version = \".*\"/version = \"$(VERSION)\"/" pyproject.toml
	@echo "⚠️  请记得手动更新 CHANGELOG.md"
	@git add .
	@git commit -m "chore: bump version to $(VERSION)"
	@git tag -a "v$(VERSION)" -m "Release version $(VERSION)"
	@git push origin main
	@git push origin "v$(VERSION)"
	@echo "✅ 版本 $(VERSION) 发布完成！"

# 创建发布候选版本
release-candidate: pre-release
	@echo "🧪 创建发布候选版本..."
	@read -p "输入 RC 版本号 (例如: 1.1.0-rc1): " version; \
	if [ -z "$$version" ]; then \
		echo "❌ 版本号不能为空"; \
		exit 1; \
	fi; \
	echo "📝 更新版本号到 $$version..."; \
	sed -i '' "s/__version__ = \".*\"/__version__ = \"$$version\"/" lee_devkit/__init__.py; \
	sed -i '' "s/version = \".*\"/version = \"$$version\"/" pyproject.toml; \
	git add .; \
	git commit -m "chore: bump version to $$version (release candidate)"; \
	git tag -a "v$$version" -m "Release candidate $$version"; \
	git push origin main; \
	git push origin "v$$version"; \
	echo "✅ 发布候选版本 $$version 创建完成！"

# 回滚版本
rollback-version:
	@echo "⚠️  回滚到上一个版本..."
	@read -p "确定要回滚吗？这将重置未提交的版本更改 (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		git checkout -- lee_devkit/__init__.py pyproject.toml; \
		echo "✅ 版本已回滚"; \
	else \
		echo "❌ 回滚已取消"; \
	fi

# 显示当前版本
show-version:
	@echo "📋 当前版本信息:"
	@echo "  __init__.py: $$(grep "__version__ = " lee_devkit/__init__.py | sed 's/.*"\(.*\)".*/\1/')"
	@echo "  pyproject.toml: $$(grep "version = " pyproject.toml | head -1 | sed 's/.*"\(.*\)".*/\1/')"
	@echo "  Git tags: $$(git tag -l | tail -3 | tr '\n' ' ')"