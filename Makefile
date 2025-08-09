# Lee DevKit Makefile
# 简化开发和部署流程

.PHONY: help install install-dev test lint format clean build upload

# 默认目标
help:
	@echo "Lee DevKit 开发工具"
	@echo ""
	@echo "可用命令:"
	@echo "  install      - 安装项目依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  test         - 运行测试"
	@echo "  lint         - 代码检查"
	@echo "  format       - 格式化代码"
	@echo "  clean        - 清理构建文件"
	@echo "  build        - 构建分发包"
	@echo "  upload       - 上传到 PyPI"
	@echo "  dev-install  - 开发模式安装"

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