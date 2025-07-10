"""
Git 操作工具
提供常用的 Git 操作功能
"""

import subprocess
import os
from pathlib import Path
from typing import List, Optional, Tuple, Dict


class GitOperations:
    """Git操作工具类"""
    
    def __init__(self, repo_path: Optional[str] = None):
        """初始化Git操作工具
        
        Args:
            repo_path: Git仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        
    def run_git_command(self, args: List[str], check: bool = True) -> subprocess.CompletedProcess:
        """执行Git命令
        
        Args:
            args: Git命令参数列表
            check: 是否检查命令执行结果
            
        Returns:
            命令执行结果
        """
        cmd = ['git'] + args
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            print(f"❌ Git命令执行失败: {' '.join(cmd)}")
            print(f"错误信息: {e.stderr}")
            raise
    
    def is_git_repo(self) -> bool:
        """检查当前目录是否为Git仓库"""
        try:
            self.run_git_command(['rev-parse', '--git-dir'])
            return True
        except subprocess.CalledProcessError:
            return False
    
    def init_repo(self) -> bool:
        """初始化Git仓库"""
        try:
            self.run_git_command(['init'])
            print(f"✅ Git仓库初始化成功: {self.repo_path}")
            return True
        except subprocess.CalledProcessError:
            print("❌ Git仓库初始化失败")
            return False
    
    def add_files(self, files: Optional[List[str]] = None) -> bool:
        """添加文件到暂存区
        
        Args:
            files: 文件列表，默认添加所有文件
        """
        try:
            if files:
                self.run_git_command(['add'] + files)
            else:
                self.run_git_command(['add', '.'])
            print("✅ 文件已添加到暂存区")
            return True
        except subprocess.CalledProcessError:
            print("❌ 添加文件失败")
            return False
    
    def commit(self, message: str) -> bool:
        """提交更改
        
        Args:
            message: 提交信息
        """
        try:
            self.run_git_command(['commit', '-m', message])
            print(f"✅ 提交成功: {message}")
            return True
        except subprocess.CalledProcessError:
            print("❌ 提交失败")
            return False
    
    def get_status(self) -> Tuple[List[str], List[str], List[str]]:
        """获取Git状态
        
        Returns:
            (modified_files, untracked_files, staged_files)
        """
        try:
            result = self.run_git_command(['status', '--porcelain'])
            lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            modified_files = []
            untracked_files = []
            staged_files = []
            
            for line in lines:
                if len(line) >= 2:
                    status = line[:2]
                    file_path = line[3:]
                    
                    if status[0] == 'M':
                        staged_files.append(file_path)
                    elif status[1] == 'M':
                        modified_files.append(file_path)
                    elif status == '??':
                        untracked_files.append(file_path)
            
            return modified_files, untracked_files, staged_files
            
        except subprocess.CalledProcessError:
            print("❌ 获取Git状态失败")
            return [], [], []
    
    def get_branches(self) -> List[str]:
        """获取所有分支列表"""
        try:
            result = self.run_git_command(['branch'])
            branches = []
            for line in result.stdout.strip().split('\n'):
                branch = line.strip().lstrip('* ')
                if branch:
                    branches.append(branch)
            return branches
        except subprocess.CalledProcessError:
            print("❌ 获取分支列表失败")
            return []
    
    def get_current_branch(self) -> Optional[str]:
        """获取当前分支名"""
        try:
            result = self.run_git_command(['branch', '--show-current'])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            print("❌ 获取当前分支失败")
            return None
    
    def create_branch(self, branch_name: str, checkout: bool = True) -> bool:
        """创建新分支
        
        Args:
            branch_name: 分支名
            checkout: 是否切换到新分支
        """
        try:
            if checkout:
                self.run_git_command(['checkout', '-b', branch_name])
            else:
                self.run_git_command(['branch', branch_name])
            print(f"✅ 分支创建成功: {branch_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 分支创建失败: {branch_name}")
            return False
    
    def checkout_branch(self, branch_name: str) -> bool:
        """切换分支
        
        Args:
            branch_name: 分支名
        """
        try:
            self.run_git_command(['checkout', branch_name])
            print(f"✅ 切换到分支: {branch_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 切换分支失败: {branch_name}")
            return False
    
    def merge_branch(self, branch_name: str) -> bool:
        """合并分支
        
        Args:
            branch_name: 要合并的分支名
        """
        try:
            self.run_git_command(['merge', branch_name])
            print(f"✅ 分支合并成功: {branch_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 分支合并失败: {branch_name}")
            return False
    
    def add_remote(self, name: str, url: str) -> bool:
        """添加远程仓库
        
        Args:
            name: 远程仓库名称
            url: 远程仓库URL
        """
        try:
            self.run_git_command(['remote', 'add', name, url])
            print(f"✅ 远程仓库添加成功: {name} -> {url}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 远程仓库添加失败: {name}")
            return False
    
    def push(self, remote: str = 'origin', branch: Optional[str] = None) -> bool:
        """推送到远程仓库
        
        Args:
            remote: 远程仓库名称
            branch: 分支名，默认为当前分支
        """
        try:
            if branch:
                self.run_git_command(['push', remote, branch])
            else:
                self.run_git_command(['push', remote])
            print(f"✅ 推送成功到 {remote}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 推送失败到 {remote}")
            return False
    
    def pull(self, remote: str = 'origin', branch: Optional[str] = None) -> bool:
        """从远程仓库拉取
        
        Args:
            remote: 远程仓库名称
            branch: 分支名，默认为当前分支
        """
        try:
            if branch:
                self.run_git_command(['pull', remote, branch])
            else:
                self.run_git_command(['pull', remote])
            print(f"✅ 从 {remote} 拉取成功")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 从 {remote} 拉取失败")
            return False
    
    def get_commit_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """获取提交历史
        
        Args:
            limit: 限制返回的提交数量
            
        Returns:
            提交历史列表，每个元素包含hash、author、date、message
        """
        try:
            result = self.run_git_command([
                'log', 
                f'-{limit}', 
                '--pretty=format:%H|%an|%ad|%s',
                '--date=short'
            ])
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|', 3)
                    if len(parts) == 4:
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1],
                            'date': parts[2],
                            'message': parts[3]
                        })
            
            return commits
            
        except subprocess.CalledProcessError:
            print("❌ 获取提交历史失败")
            return []
    
    def has_uncommitted_changes(self) -> bool:
        """检查是否有未提交的更改"""
        try:
            result = self.run_git_command(['status', '--porcelain'])
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def stash(self, message: Optional[str] = None) -> bool:
        """暂存当前更改
        
        Args:
            message: 暂存消息
        """
        try:
            if message:
                self.run_git_command(['stash', 'push', '-m', message])
            else:
                self.run_git_command(['stash'])
            print("✅ 更改已暂存")
            return True
        except subprocess.CalledProcessError:
            print("❌ 暂存失败")
            return False
    
    def stash_pop(self) -> bool:
        """恢复最近的暂存"""
        try:
            self.run_git_command(['stash', 'pop'])
            print("✅ 暂存已恢复")
            return True
        except subprocess.CalledProcessError:
            print("❌ 暂存恢复失败")
            return False
    
    def clone_repo(self, url: str, destination: Optional[str] = None) -> bool:
        """克隆远程仓库
        
        Args:
            url: 远程仓库URL
            destination: 目标目录，默认为仓库名
        """
        try:
            if destination:
                self.run_git_command(['clone', url, destination])
            else:
                self.run_git_command(['clone', url])
            print(f"✅ 仓库克隆成功: {url}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 仓库克隆失败: {url}")
            return False
    
    def reset_hard(self, commit: str = 'HEAD') -> bool:
        """硬重置到指定提交
        
        Args:
            commit: 提交哈希或引用，默认为HEAD
        """
        try:
            self.run_git_command(['reset', '--hard', commit])
            print(f"✅ 重置成功到: {commit}")
            return True
        except subprocess.CalledProcessError:
            print(f"❌ 重置失败到: {commit}")
            return False