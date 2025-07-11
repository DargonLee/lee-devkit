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
        self.config_dir = Path.home() / ".ninebot_cli"
        self.config_file = self.config_dir / "config.json"
        self.templates_dir = self.config_dir / "template"
        
        # 默认配置
        self.default_config = {
            "template_repo": "git@git.ninebot.com:iOS/podmaker.git",
            "author": "hailong.li",
            "email": "hailong.li@ninebot.com",
            "organization": "ninebot",
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
        """克隆或更新模板，只保留 template 文件夹内容"""
        import tempfile
        config = self.load_config()
        repo_url = config.get("template_repo")
        
        if not repo_url:
            repo_url = "git@git.ninebot.com:iOS/podmaker.git"
        
        template_path = self.templates_dir
        
        # 检查是否在项目根目录，如果是则使用本地模板
        local_template_path = Path.cwd() / "template"
        if local_template_path.exists() and (local_template_path / "NBTemplateModule").exists():
            print("🔧 检测到本地模板，使用项目中的模板...")
            # 清理旧缓存
            if template_path.exists():
                shutil.rmtree(template_path)
            template_path.mkdir(parents=True, exist_ok=True)
            
            # 复制本地模板
            success = self.run_command([
                "cp", "-r", f"{local_template_path}/.", str(template_path)
            ])
            if success:
                print(f"✅ 已使用本地模板: {local_template_path}")
                return True
            else:
                print("⚠️  使用本地模板失败，回退到远程模板...")
        
        if template_path.exists() and not force_update:
            print("✅ 模板已存在，使用现有模板")
            return True
        
        # 清理旧模板
        if template_path.exists():
            shutil.rmtree(template_path)
        
        # 临时目录用于克隆
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"📥 正在克隆模板仓库到临时目录: {repo_url}")
            success = self.run_command([
                "git", "clone", repo_url, tmpdir
            ])
            if not success:
                print("❌ 模板克隆失败")
                return False
            
            # 切换到 develop 分支
            print("🔄 切换到 develop 分支...")
            success = self.run_command([
                "git", "checkout", "develop"
            ], cwd=tmpdir)
            if not success:
                print("⚠️  切换到 develop 分支失败，使用默认分支")
            
            # 复制整个 template 目录内容
            src_template = Path(tmpdir) / "template"
            if not src_template.exists():
                print(f"❌ 仓库中未找到 template 文件夹: {src_template}")
                return False
            
            # 确保目标目录存在
            template_path.mkdir(parents=True, exist_ok=True)
            
            # 使用 cp 命令复制所有内容
            success = self.run_command([
                "cp", "-r", f"{src_template}/.", str(template_path)
            ])
            if not success:
                print("❌ 复制模板内容失败")
                return False
            
            print(f"✅ 已复制 template 内容到: {template_path}")
        return True
    
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
        import tempfile
        
        # 检查模板
        if not self.clone_or_update_template(force_update):
            return False
        
        template_dir = self.templates_dir / self.template_name
        if not template_dir.exists():
            print(f"❌ 模板目录不存在: {template_dir}")
            return False
        
        # 确保输出目录存在
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 检查目标目录（module_name 文件夹）
        project_path = output_path / module_name
        if project_path.exists():
            print(f"❌ 目标目录已存在: {project_path}")
            return False
        
        print(f"🚀 正在创建项目: {module_name}")
        print(f"📁 输出路径: {project_path}")
        
        # 使用临时目录处理模板
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_project_path = Path(tmpdir) / module_name
            temp_project_path.mkdir(parents=True)
            
            # 1. 复制整个模板目录的内容到临时目录
            # 首先复制 NBTemplateModule 目录的内容到项目根目录
            template_module_dir = self.templates_dir / self.template_name
            if template_module_dir.exists():
                success = self.run_command([
                    "cp", "-r", f"{template_module_dir}/.", str(temp_project_path)
                ])
                if not success:
                    print("❌ 复制模板模块内容失败")
                    return False
            
            # 然后复制根级别的文件（如 .podspec, LICENSE 等）
            for item in self.templates_dir.iterdir():
                if item.is_file():
                    success = self.run_command([
                        "cp", str(item), str(temp_project_path / item.name)
                    ])
                    if not success:
                        print(f"⚠️  复制文件 {item.name} 失败")
            
            # 2. 重命名文件和目录
            self.rename_files_and_dirs(temp_project_path, self.template_name, module_name)
            
            # 3. 替换文件内容
            files_to_process = self.find_template_files(temp_project_path)
            for file_path in files_to_process:
                self.replace_file_content(file_path, self.template_name, module_name)
            
            # 4. 处理 Example 目录
            self.remove_example_if_needed(temp_project_path, include_example)
            
            # 5. 更新 podspec
            podspec_path = temp_project_path / f"{module_name}.podspec"
            if podspec_path.exists():
                self.update_podspec_metadata(podspec_path, module_name)
            
            # 6. 清理临时文件
            for pattern in ["*.orig", "*~"]:
                for file in temp_project_path.rglob(pattern):
                    file.unlink()
            
            # 7. 最后复制处理好的项目到目标目录
            success = self.run_command([
                "cp", "-r", str(temp_project_path), str(project_path.parent)
            ])
            if not success:
                print("❌ 复制最终项目失败")
                return False
        
        print(f"✅ 项目创建成功: {project_path}")
        self.print_next_steps(module_name, project_path, include_example)
        
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

def register_arguments(parser):
    parser.add_argument('action', choices=['create'], help='操作类型')
    parser.add_argument('module_name', help='新库名称')
    parser.add_argument('--include-example', action='store_true', help='包含 Example 工程')
    parser.add_argument('--output', default='.', help='输出目录（默认为当前目录）')
    parser.add_argument('--force-update', action='store_true', help='强制更新模板')

def execute(args, config):
    if args.action == 'create':
        scaffold = CocoaPodsScaffold()
        include_example = args.include_example  # 默认不包含，只有使用 --include-example 时才包含
        
        # 确保输出目录是绝对路径，默认为当前工作目录
        output_dir = Path(args.output).resolve()
        
        return scaffold.create_project(
            module_name=args.module_name,
            include_example=include_example,
            output_dir=str(output_dir),
            force_update=args.force_update
        )
    else:
        print(f'❌ 未知操作: {args.action}')
        return False
