#!/usr/bin/env python3
"""
CocoaPods 脚手架工具 - 基于模板快速创建 CocoaPods 库
"""

import os
import shutil
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

__version__ = "1.0.0"

class CocoaPodsScaffold:
    def __init__(self):
        self.template_name = "NBTemplateModule"
        self.config_dir = Path.home() / ".cocoapods-scaffold"
        self.config_file = self.config_dir / "config.json"
        self.templates_dir = self.config_dir / "templates"
        
        # 默认配置
        self.default_config = {
            "template_repo": "https://github.com/your-company/cocoapods-template.git",
            "author": "Your Name",
            "email": "your.email@company.com",
            "organization": "Your Company",
            "prefix": "YC"
        }
        
        self.setup_config()
    
    def setup_config(self):
        """初始化配置目录和文件"""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
            
        if not self.config_file.exists():
            self.save_config(self.default_config)
    
    def load_config(self) -> Dict:
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self.default_config
    
    def save_config(self, config: Dict):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def run_command(self, command: List[str], cwd: Optional[str] = None) -> bool:
        """执行命令"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 命令执行失败: {' '.join(command)}")
            print(f"错误: {e.stderr}")
            return False
    
    def clone_or_update_template(self, force_update: bool = False) -> bool:
        """克隆或更新模板"""
        config = self.load_config()
        repo_url = config.get("template_repo")
        
        if not repo_url:
            print("❌ 模板仓库 URL 未配置")
            return False
        
        template_path = self.templates_dir / "template"
        
        if template_path.exists() and not force_update:
            print("✅ 模板已存在，使用现有模板")
            return True
        
        if template_path.exists():
            shutil.rmtree(template_path)
        
        print(f"📥 正在克隆模板: {repo_url}")
        
        # 克隆模板
        success = self.run_command([
            "git", "clone", repo_url, str(template_path)
        ])
        
        if success:
            print("✅ 模板克隆成功")
            return True
        else:
            print("❌ 模板克隆失败")
            return False
    
    def find_template_files(self, template_dir: Path) -> List[Path]:
        """查找需要处理的文件"""
        text_extensions = {
            '.swift', '.h', '.m', '.mm', '.podspec', '.md', '.txt',
            '.json', '.yml', '.yaml', '.plist', '.pbxproj', '.xcscheme'
        }
        
        files = []
        for root, dirs, filenames in os.walk(template_dir):
            # 跳过 .git 目录
            if '.git' in dirs:
                dirs.remove('.git')
            
            for filename in filenames:
                file_path = Path(root) / filename
                if file_path.suffix in text_extensions or filename == "Podfile":
                    files.append(file_path)
        
        return files
    
    def rename_files_and_dirs(self, base_dir: Path, old_name: str, new_name: str):
        """重命名文件和目录"""
        items_to_rename = []
        
        # 收集需要重命名的项目
        for root, dirs, files in os.walk(base_dir, topdown=False):
            for name in files + dirs:
                if old_name in name:
                    old_path = Path(root) / name
                    new_filename = name.replace(old_name, new_name)
                    new_path = Path(root) / new_filename
                    items_to_rename.append((old_path, new_path))
        
        # 执行重命名
        for old_path, new_path in items_to_rename:
            if old_path.exists():
                old_path.rename(new_path)
                print(f"重命名: {old_path.name} -> {new_path.name}")
    
    def replace_file_content(self, file_path: Path, old_name: str, new_name: str):
        """替换文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_name in content:
                new_content = content.replace(old_name, new_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"替换内容: {file_path.name}")
                
        except UnicodeDecodeError:
            # 处理二进制文件
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                old_bytes = old_name.encode('utf-8')
                new_bytes = new_name.encode('utf-8')
                
                if old_bytes in content:
                    new_content = content.replace(old_bytes, new_bytes)
                    with open(file_path, 'wb') as f:
                        f.write(new_content)
                    print(f"替换二进制内容: {file_path.name}")
            except:
                print(f"⚠️  跳过文件: {file_path.name}")
    
    def remove_example_if_needed(self, project_dir: Path, include_example: bool):
        """根据需要移除 Example 目录"""
        if not include_example:
            example_dir = project_dir / "Example"
            if example_dir.exists():
                shutil.rmtree(example_dir)
                print("🗑️  已移除 Example 目录")
    
    def update_podspec_metadata(self, podspec_path: Path, module_name: str):
        """更新 podspec 元数据"""
        config = self.load_config()
        
        try:
            with open(podspec_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新基本信息
            replacements = {
                r"s\.author\s*=\s*['\"].*?['\"]": f"s.author = '{config.get('author', 'Unknown')}'",
                r"s\.email\s*=\s*['\"].*?['\"]": f"s.email = '{config.get('email', 'unknown@example.com')}'",
                r"s\.summary\s*=\s*['\"].*?['\"]": f"s.summary = 'A brief description of {module_name}'",
                r"s\.description\s*=\s*['\"].*?['\"]": f"s.description = 'A longer description of {module_name} library'",
            }
            
            for pattern, replacement in replacements.items():
                content = re.sub(pattern, replacement, content)
            
            with open(podspec_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ 已更新 {podspec_path.name}")
            
        except Exception as e:
            print(f"⚠️  更新 podspec 文件失败: {e}")
    
    def create_project(self, module_name: str, include_example: bool = True,
                      output_dir: str = ".", force_update: bool = False) -> bool:
        """创建新项目"""
        # 检查模板
        if not self.clone_or_update_template(force_update):
            return False
        
        template_dir = self.templates_dir / "template" / self.template_name
        if not template_dir.exists():
            print(f"❌ 模板目录不存在: {template_dir}")
            return False
        
        # 检查目标目录
        output_path = Path(output_dir) / module_name
        if output_path.exists():
            print(f"❌ 目标目录已存在: {output_path}")
            return False
        
        print(f"🚀 正在创建项目: {module_name}")
        
        # 复制模板
        shutil.copytree(template_dir, output_path)
        
        # 重命名文件和目录
        self.rename_files_and_dirs(output_path, self.template_name, module_name)
        
        # 替换文件内容
        files_to_process = self.find_template_files(output_path)
        for file_path in files_to_process:
            self.replace_file_content(file_path, self.template_name, module_name)
        
        # 处理 Example 目录
        self.remove_example_if_needed(output_path, include_example)
        
        # 更新 podspec
        podspec_path = output_path / f"{module_name}.podspec"
        if podspec_path.exists():
            self.update_podspec_metadata(podspec_path, module_name)
        
        # 清理临时文件
        for pattern in ["*.orig", "*~"]:
            for file in output_path.rglob(pattern):
                file.unlink()
        
        print(f"✅ 项目创建成功: {output_path}")
        self.print_next_steps(module_name, output_path, include_example)
        
        return True
    
    def print_next_steps(self, module_name: str, project_path: Path, include_example: bool):
        """打印下一步操作"""
        print("\n📋 接下来你可以：")
        print(f"1. 进入项目目录: cd {project_path}")
        print(f"2. 编辑 {module_name}.podspec 文件")
        
        if include_example:
            print("3. 进入 Example 目录安装依赖:")
            print("   cd Example && pod install")
            print("4. 打开 .xcworkspace 文件开始开发")
        else:
            print("3. 开始开发你的库代码")
        
        print("5. 初始化 Git 仓库: git init")
        print("6. 提交代码: git add . && git commit -m 'Initial commit'")
    
    def configure(self, **kwargs):
        """配置工具"""
        config = self.load_config()
        
        for key, value in kwargs.items():
            if value is not None:
                config[key] = value
        
        self.save_config(config)
        print("✅ 配置已保存")
        
        print("\n📋 当前配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    def show_config(self):
        """显示当前配置"""
        config = self.load_config()
        print("📋 当前配置:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    def list_templates(self):
        """列出可用模板"""
        templates_path = self.templates_dir / "template"
        if templates_path.exists():
            print("📦 可用模板:")
            for item in templates_path.iterdir():
                if item.is_dir():
                    print(f"  - {item.name}")
        else:
            print("❌ 没有找到模板")
