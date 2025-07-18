from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lee-devkit",
    version="1.0.0",
    author="DargonLee",
    author_email="2461414445@qq.com",
    description="CocoaPods 脚手架工具 - 基于模板快速创建 CocoaPods 库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DargonLee/lee-devkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    install_requires=[
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "lee-devkit=lee_devkit.cli:main",
        ],
    },
    include_package_data=True,
)