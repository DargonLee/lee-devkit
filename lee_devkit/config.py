
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
        self.config_dir = Path.home() / '.lee_devkit'
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
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        
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