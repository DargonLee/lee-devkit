
# lee_scaffold/config.py
"""
配置管理模块
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """配置管理类"""
    
    def __init__(self):
        # 使用 .config/lee_devkit 作为配置目录
        self.config_base_dir = Path.home() / '.config'
        self.config_dir = self.config_base_dir / 'lee_devkit'
        self.config_file = self.config_dir / 'config.json'
        self.default_config = {
            'author': 'DargonLee',
            'email': '2461414445@qq.com',
            'organization': 'Personal',
            'editor': 'code',  # VS Code
            'git': {
                'default_branch': 'main',
                'auto_push': False,
                'commit_template': 'feat: {message}'
            },
            'cocoapods': {
                'template_repo': 'git@github.com:DargonLee/lee-devkit.git',
                'default_platform': 'iOS',
                'swift_version': '5.0'
            },
            'spec_repos': {
                'default': 'NBSpecs',
                'repos': {
                    'NBSpecs': 'git@git.ninebot.com:iOS/NBSpecs.git'
                }
            },
            'codegen': {
                'templates_dir': str(self.config_dir / 'templates'),
                'output_dir': './generated'
            }
        }
        
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        # 检查 .config 目录是否存在，不存在则创建
        if not self.config_base_dir.exists():
            print(f"创建配置基础目录: {self.config_base_dir}")
            self.config_base_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查 lee_devkit 目录是否存在，不存在则创建
        if not self.config_dir.exists():
            print(f"创建工具配置目录: {self.config_dir}")
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
        # 检查并设置模板目录
        self._setup_template_directory()
        
        if not self.config_file.exists():
            self._save_config(self.default_config)
            return self.default_config.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 合并默认配置（处理新增的配置项）
            merged_config = self._merge_config(self.default_config, config)
            
            # 如果有新增配置，保存回文件
            if merged_config != config:
                self._save_config(merged_config)
            
            return merged_config
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  配置文件损坏，使用默认配置: {e}")
            return self.default_config.copy()
    
    def _merge_config(self, default: Dict, user: Dict) -> Dict:
        """合并配置，保留用户配置并添加默认值"""
        merged = default.copy()
        
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_config(merged[key], value)
            else:
                merged[key] = value
        
        return merged
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值，支持点号分隔的嵌套键"""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值，支持点号分隔的嵌套键"""
        keys = key.split('.')
        config = self.config_data
        
        # 导航到目标位置
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        
        # 保存配置
        self._save_config(self.config_data)
    
    def update(self, updates: Dict[str, Any]):
        """批量更新配置"""
        for key, value in updates.items():
            self.set(key, value)
    
    def show(self):
        """显示当前配置"""
        print("📋 当前配置:")
        self._print_config(self.config_data)
    
    def _print_config(self, config: Dict, indent: int = 0):
        """递归打印配置"""
        for key, value in config.items():
            prefix = "  " * indent
            if isinstance(value, dict):
                print(f"{prefix}{key}:")
                self._print_config(value, indent + 1)
            else:
                print(f"{prefix}{key}: {value}")
    
    def edit(self):
        """使用编辑器编辑配置文件"""
        editor = self.get('editor', 'nano')
        
        try:
            subprocess.run([editor, str(self.config_file)], check=True)
            print("✅ 配置文件已编辑")
            
            # 重新加载配置
            self.config_data = self._load_config()
            
        except subprocess.CalledProcessError:
            print(f"❌ 无法打开编辑器: {editor}")
        except FileNotFoundError:
            print(f"❌ 编辑器不存在: {editor}")
    
    def reset(self):
        """重置为默认配置"""
        self.config_data = self.default_config.copy()
        self._save_config(self.config_data)
        print("✅ 配置已重置为默认值")
    
    def load_from_file(self, file_path: str):
        """从指定文件加载配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 合并配置
            self.config_data = self._merge_config(self.config_data, config)
            print(f"✅ 已从 {file_path} 加载配置")
            
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
    
    def export_to_file(self, file_path: str):
        """导出配置到文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=2, ensure_ascii=False)
            print(f"✅ 配置已导出到 {file_path}")
            
        except Exception as e:
            print(f"❌ 导出配置文件失败: {e}")
    
    def get_templates_dir(self) -> Path:
        """获取模板目录"""
        templates_dir = Path(self.get('codegen.templates_dir', 
                                    str(self.config_dir / 'templates')))
        
        if not templates_dir.exists():
            templates_dir.mkdir(parents=True)
        
        return templates_dir
    
    def get_cache_dir(self) -> Path:
        """获取缓存目录"""
        cache_dir = self.config_dir / 'cache'
        
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        
        return cache_dir
        
    # Spec Repository 相关方法
    
    def get_spec_repos(self) -> Dict[str, str]:
        """获取所有配置的 spec 仓库"""
        return self.get('spec_repos.repos', {})
    
    def get_default_spec_repo(self) -> Optional[str]:
        """获取默认 spec 仓库名称"""
        return self.get('spec_repos.default')
    
    def get_spec_repo_url(self, name: str) -> Optional[str]:
        """获取指定 spec 仓库的 URL"""
        repos = self.get_spec_repos()
        return repos.get(name)
    
    def add_spec_repo(self, name: str, url: str) -> bool:
        """添加 spec 仓库"""
        # 确保 spec_repos 结构存在
        if not self.get('spec_repos'):
            self.set('spec_repos', {})
        if not self.get('spec_repos.repos'):
            self.set('spec_repos.repos', {})
        
        # 添加仓库
        repos = self.get_spec_repos()
        repos[name] = url
        self.set('spec_repos.repos', repos)
        
        # 如果这是第一个仓库，设为默认
        if len(repos) == 1:
            self.set('spec_repos.default', name)
            
        return True
    
    def remove_spec_repo(self, name: str) -> bool:
        """移除 spec 仓库"""
        repos = self.get_spec_repos()
        if name not in repos:
            return False
        
        # 移除仓库
        del repos[name]
        self.set('spec_repos.repos', repos)
        
        # 如果这是默认仓库，清除默认设置
        if self.get('spec_repos.default') == name:
            self.set('spec_repos.default', None)
            
        return True
    
    def set_default_spec_repo(self, name: str) -> bool:
        """设置默认 spec 仓库"""
        repos = self.get_spec_repos()
        if name not in repos:
            return False
        
        self.set('spec_repos.default', name)
        return True
    
    def _setup_template_directory(self):
        """设置模板目录"""
        template_dir = self.config_dir / "template"
        
        # 如果模板目录已存在，则跳过
        if template_dir.exists() and (template_dir / "NBTemplateModule").exists():
            return
        
        print(f"🔧 正在设置模板目录: {template_dir}")
        
        # 检查当前目录是否有模板（用于开发环境）
        import os
        current_dir = Path(os.getcwd())
        local_template = None
        
        # 检查多个可能的模板位置
        possible_locations = [
            current_dir / "template",
            current_dir.parent / "template",  # 如果在子目录中运行
            Path(__file__).parent.parent / "template",  # 相对于当前文件
        ]
        
        for location in possible_locations:
            if location.exists() and (location / "NBTemplateModule").exists():
                local_template = location
                break
        
        if local_template:
            print(f"📂 使用本地模板: {local_template}")
            try:
                # 确保目标目录存在
                template_dir.mkdir(parents=True, exist_ok=True)
                
                # 使用系统命令复制，更可靠
                if os.name == 'posix':  # Unix/Linux/Mac
                    os.system(f"cp -r '{local_template}'/* '{template_dir}'/")
                elif os.name == 'nt':  # Windows
                    os.system(f'xcopy "{local_template}" "{template_dir}" /E /I /Y')
                    
                print(f"✅ 模板设置完成: {template_dir}")
                return
            except Exception as e:
                print(f"⚠️ 复制本地模板失败: {e}")
        
        # 如果没有本地模板，尝试从远程获取
        self._download_template_from_remote(template_dir)
    
    def _download_template_from_remote(self, template_dir: Path):
        """从远程仓库下载模板"""
        import tempfile
        import subprocess
        import shutil
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                
                # 克隆仓库
                print("📥 正在从远程获取模板...")
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", "git@github.com:DargonLee/lee-devkit.git", str(tmp_path)],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"⚠️ 无法克隆仓库: {result.stderr}")
                    print("首次使用时将自动下载模板")
                    return
                
                # 检查模板目录是否存在
                src_template = tmp_path / "template"
                
                if src_template.exists() and (src_template / "NBTemplateModule").exists():
                    print(f"找到模板目录: {src_template}")
                else:
                    print("⚠️ 仓库中未找到模板目录")
                    return
                
                # 复制模板
                template_dir.mkdir(parents=True, exist_ok=True)
                
                # 使用系统命令复制
                import os
                if os.name == 'posix':  # Unix/Linux/Mac
                    os.system(f"cp -r '{src_template}'/* '{template_dir}'/")
                elif os.name == 'nt':  # Windows
                    os.system(f'xcopy "{src_template}" "{template_dir}" /E /I /Y')
                
                print(f"✅ 模板设置完成: {template_dir}")
                
        except Exception as e:
            print(f"⚠️ 设置模板目录时出错: {e}")
            print("首次使用时将自动下载模板")