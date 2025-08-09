#!/usr/bin/env python3
"""
Lee Scaffold - 个人开发工具集
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

from . import __version__
from .config import Config
from .utils.logger import setup_logger
from .commands import cocoapods, git_tools, file_tools, code_gen, project_init, pod_repo_push, git_tag


class LeeScaffold:
    """主命令行工具类"""
    
    def __init__(self):
        self.config = Config()
        self.logger = setup_logger()
        self.commands = {}
        self._register_commands()
    
    def _register_commands(self):
        """注册所有命令"""
        # 注册 CocoaPods 命令
        self.commands['cocoapods'] = {
            'module': cocoapods,
            'description': 'CocoaPods 相关工具',
            'aliases': ['pod', 'cp']
        }
        
        # 注册 Git 工具
        self.commands['git'] = {
            'module': git_tools,
            'description': 'Git 操作工具',
            'aliases': ['g']
        }

        # 注册 Git Tag 命令
        self.commands['tag'] = {
            'module': git_tag,
            'description': 'Git Tag 管理',
            'aliases': ['gt']
        }
        
        # 注册文件工具
        self.commands['file'] = {
            'module': file_tools,
            'description': '文件处理工具',
            'aliases': ['f']
        }
        
        # 注册代码生成工具
        self.commands['codegen'] = {
            'module': code_gen,
            'description': '代码生成工具',
            'aliases': ['gen', 'cg']
        }
        
        # 注册项目初始化工具
        self.commands['init'] = {
            'module': project_init,
            'description': '项目初始化工具',
            'aliases': ['new', 'create']
        }
        
        # 注册 Pod Repo Push 工具
        self.commands['pod-push'] = {
            'module': pod_repo_push,
            'description': 'CocoaPods 库发布工具',
            'aliases': ['push', 'pp']
        }
    
    def create_parser(self) -> argparse.ArgumentParser:
        """创建主命令解析器"""
        parser = argparse.ArgumentParser(
            prog='lee-devkit',
            description='Lee 个人开发工具集 - 提高开发效率的命令行工具',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=self._get_examples()
        )
        
        parser.add_argument(
            '--version', 
            action='version', 
            version=f'lee-devkit {__version__}'
        )
        
        parser.add_argument(
            '--config', 
            help='配置文件路径'
        )
        
        parser.add_argument(
            '--verbose', '-v', 
            action='store_true',
            help='详细输出'
        )
        
        parser.add_argument(
            '--quiet', '-q', 
            action='store_true',
            help='静默模式'
        )
        
        # 创建子命令解析器
        subparsers = parser.add_subparsers(
            dest='command',
            title='可用命令',
            description='选择要执行的命令',
            help='使用 lee-devkit <command> --help 查看详细帮助'
        )
        
        # 注册所有子命令
        for cmd_name, cmd_info in self.commands.items():
            cmd_module = cmd_info['module']
            cmd_desc = cmd_info['description']
            cmd_aliases = cmd_info.get('aliases', [])
            
            # 创建子命令解析器
            cmd_parser = subparsers.add_parser(
                cmd_name,
                aliases=cmd_aliases,
                help=cmd_desc,
                description=cmd_desc
            )
            
            # 让模块自己注册参数
            if hasattr(cmd_module, 'register_arguments'):
                cmd_module.register_arguments(cmd_parser)
        
        # 添加配置命令
        config_parser = subparsers.add_parser(
            'config',
            help='配置管理',
            description='管理工具配置'
        )
        self._add_config_arguments(config_parser)
        
        return parser
    
    def _add_config_arguments(self, parser: argparse.ArgumentParser):
        """添加配置相关参数"""
        config_group = parser.add_mutually_exclusive_group()
        
        config_group.add_argument(
            '--show',
            action='store_true',
            help='显示当前配置'
        )
        
        config_group.add_argument(
            '--edit',
            action='store_true',
            help='编辑配置文件'
        )
        
        config_group.add_argument(
            '--reset',
            action='store_true',
            help='重置为默认配置'
        )
        
        # 具体配置项
        parser.add_argument('--author', help='设置作者名称')
        parser.add_argument('--email', help='设置邮箱地址')
        parser.add_argument('--organization', help='设置组织名称')
        parser.add_argument('--editor', help='设置默认编辑器')
    
    def _get_examples(self) -> str:
        """获取使用示例"""
        return """
使用示例:
  # CocoaPods 相关
  lee-devkit cocoapods create MyLibrary
  lee-devkit pod create MyLibrary --no-example
  
  # Git 工具
  lee-devkit git clone-batch repos.txt
  lee-devkit git status-all ~/Projects

  # Git Tag 管理
  lee-devkit tag create 1.2.8
  lee-devkit tag create 1.2.8 --message "Release version 1.2.8"
  lee-devkit tag retag 1.2.8
  lee-devkit tag retag 1.2.8 --message "Release version 1.2.8"
  
  # 文件工具
  lee-devkit file rename-batch --pattern "*.jpg"
  lee-devkit file convert-encoding --from gbk --to utf-8
  
  # 代码生成
  lee-devkit codegen swift-model --json data.json
  lee-devkit gen api-client --swagger api.yaml
  
  # 项目初始化
  lee-devkit init react-app MyApp
  lee-devkit new fastapi-project MyAPI
  
  # 配置管理
  lee-devkit config --show
  lee-devkit config --author "Lee" --email "lee@example.com"
        """
    
    def handle_config_command(self, args: argparse.Namespace):
        """处理配置命令"""
        if args.show:
            self.config.show()
        elif args.edit:
            self.config.edit()
        elif args.reset:
            self.config.reset()
        else:
            # 更新配置
            updates = {}
            if args.author:
                updates['author'] = args.author
            if args.email:
                updates['email'] = args.email
            if args.organization:
                updates['organization'] = args.organization
            if args.editor:
                updates['editor'] = args.editor
            
            if updates:
                self.config.update(updates)
                print("✅ 配置已更新")
            else:
                print("❌ 没有指定要更新的配置项")
    
    def run(self, args: Optional[List[str]] = None):
        """运行命令行工具"""
        if args is None:
            args = sys.argv[1:]
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        # 处理全局参数
        if parsed_args.config:
            self.config.load_from_file(parsed_args.config)
        
        if parsed_args.verbose:
            self.logger.setLevel('DEBUG')
        elif parsed_args.quiet:
            self.logger.setLevel('ERROR')
        
        # 如果没有指定命令，显示帮助
        if not parsed_args.command:
            parser.print_help()
            return
        
        # 处理配置命令
        if parsed_args.command == 'config':
            self.handle_config_command(parsed_args)
            return
        
        # 查找并执行命令
        cmd_name = parsed_args.command
        
        # 处理别名
        for name, info in self.commands.items():
            if cmd_name in info.get('aliases', []):
                cmd_name = name
                break
        
        if cmd_name not in self.commands:
            print(f"❌ 未知命令: {parsed_args.command}")
            parser.print_help()
            sys.exit(1)
        
        # 执行命令
        try:
            cmd_module = self.commands[cmd_name]['module']
            if hasattr(cmd_module, 'execute'):
                # 更新 parsed_args.command 为实际命令名，以便模块内部使用
                parsed_args.command = cmd_name
                success = cmd_module.execute(parsed_args, self.config)
                if not success:
                    sys.exit(1)
            else:
                print(f"❌ 命令 {cmd_name} 未实现")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n⚠️  操作被用户中断")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"执行命令时发生错误: {e}")
            if parsed_args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)