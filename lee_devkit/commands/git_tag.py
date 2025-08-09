#!/usr/bin/env python3
"""
Git Tag 管理命令模块
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

from ..config import Config
from ..utils.logger import setup_logger


def register_arguments(parser: argparse.ArgumentParser):
    """注册命令参数"""
    subparsers = parser.add_subparsers(dest='tag_action', help='Tag 操作')
    # create 子命令
    create_parser = subparsers.add_parser(
        'create',
        help='创建并推送 Git tag',
        description='创建新的 Git tag 并推送到远程仓库'
    )
    
    create_parser.add_argument(
        'tag_name',
        help='要创建的 tag 名称'
    )
    
    create_parser.add_argument(
        '--commit',
        help='指定 commit hash 或分支名（默认为当前 HEAD）'
    )
    
    create_parser.add_argument(
        '--message', '-m',
        help='tag 消息（创建带注释的 tag）'
    )
    
    create_parser.add_argument(
        '--remote',
        default='origin',
        help='远程仓库名称（默认: origin）'
    )
    
    create_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要执行的命令，不实际执行'
    )
    
    create_parser.add_argument(
        '--no-push',
        action='store_true',
        help='只创建本地 tag，不推送到远程'
    )
    # retag 子命令
    retag_parser = subparsers.add_parser(
        'retag',
        help='删除并重新创建 Git tag',
        description='删除本地和远程的 Git tag，然后重新创建并推送'
    )
    
    retag_parser.add_argument(
        'tag_name',
        help='要重新创建的 tag 名称'
    )
    
    retag_parser.add_argument(
        '--commit',
        help='指定 commit hash 或分支名（默认为当前 HEAD）'
    )
    
    retag_parser.add_argument(
        '--message', '-m',
        help='tag 消息（创建带注释的 tag）'
    )
    
    retag_parser.add_argument(
        '--remote',
        default='origin',
        help='远程仓库名称（默认: origin）'
    )
    
    retag_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='仅显示将要执行的命令，不实际执行'
    )
    
    retag_parser.add_argument(
        '--force',
        action='store_true',
        help='强制执行，即使本地或远程 tag 不存在也继续'
    )


def execute(args: argparse.Namespace, config: Config) -> bool:
    """执行命令"""
    logger = setup_logger()
    
    if not hasattr(args, 'tag_action') or args.tag_action != 'retag':
        logger.error("请指定 retag 操作")
        return False
    
    return _handle_retag(args, config, logger)


def _handle_retag(args: argparse.Namespace, config: Config, logger) -> bool:
    """处理 retag 命令"""
    tag_name = args.tag_name
    remote = args.remote
    commit = args.commit or 'HEAD'
    
    # 检查是否在 Git 仓库中
    if not _is_git_repo():
        logger.error("❌ 当前目录不是 Git 仓库")
        return False
    
    logger.info(f"🏷️  开始重新创建 tag: {tag_name}")
    
    # 步骤1: 删除本地 tag
    if not _delete_local_tag(tag_name, logger, args.dry_run, args.force):
        if not args.force:
            return False
    
    # 步骤2: 删除远程 tag
    if not _delete_remote_tag(tag_name, remote, logger, args.dry_run, args.force):
        if not args.force:
            return False
    
    # 步骤3: 创建新的 tag
    if not _create_tag(tag_name, commit, args.message, logger, args.dry_run):
        return False
    
    # 步骤4: 推送 tag 到远程
    if not _push_tags(remote, logger, args.dry_run):
        return False
    
    if not args.dry_run:
        logger.info(f"✅ 成功重新创建并推送 tag: {tag_name}")
    else:
        logger.info("🔍 干运行模式完成")
    
    return True


def _is_git_repo() -> bool:
    """检查当前目录是否是 Git 仓库"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--git-dir'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _delete_local_tag(tag_name: str, logger, dry_run: bool, force: bool) -> bool:
    """删除本地 tag"""
    cmd = ['git', 'tag', '-d', tag_name]
    cmd_str = ' '.join(cmd)
    
    logger.info(f"🗑️  删除本地 tag: {cmd_str}")
    
    if dry_run:
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ 成功删除本地 tag: {tag_name}")
            return True
        else:
            if "not found" in result.stderr.lower():
                logger.warning(f"⚠️  本地 tag 不存在: {tag_name}")
                return force
            else:
                logger.error(f"❌ 删除本地 tag 失败: {result.stderr.strip()}")
                return False
    except Exception as e:
        logger.error(f"❌ 删除本地 tag 时发生错误: {e}")
        return False


def _delete_remote_tag(tag_name: str, remote: str, logger, dry_run: bool, force: bool) -> bool:
    """删除远程 tag"""
    cmd = ['git', 'push', remote, f':refs/tags/{tag_name}']
    cmd_str = ' '.join(cmd)
    
    logger.info(f"🗑️  删除远程 tag: {cmd_str}")
    
    if dry_run:
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ 成功删除远程 tag: {tag_name}")
            return True
        else:
            if "unable to delete" in result.stderr.lower() or "does not exist" in result.stderr.lower():
                logger.warning(f"⚠️  远程 tag 不存在: {tag_name}")
                return force
            else:
                logger.error(f"❌ 删除远程 tag 失败: {result.stderr.strip()}")
                return False
    except Exception as e:
        logger.error(f"❌ 删除远程 tag 时发生错误: {e}")
        return False


def _create_tag(tag_name: str, commit: str, message: Optional[str], logger, dry_run: bool) -> bool:
    """创建新的 tag"""
    cmd = ['git', 'tag']
    
    if message:
        cmd.extend(['-a', tag_name, '-m', message])
    else:
        cmd.append(tag_name)
    
    if commit != 'HEAD':
        cmd.append(commit)
    
    cmd_str = ' '.join(cmd)
    logger.info(f"🏷️  创建新 tag: {cmd_str}")
    
    if dry_run:
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ 成功创建 tag: {tag_name}")
            return True
        else:
            logger.error(f"❌ 创建 tag 失败: {result.stderr.strip()}")
            return False
    except Exception as e:
        logger.error(f"❌ 创建 tag 时发生错误: {e}")
        return False


def _push_tags(remote: str, logger, dry_run: bool) -> bool:
    """推送 tags 到远程"""
    cmd = ['git', 'push', '--tags', remote]
    cmd_str = ' '.join(cmd)
    
    logger.info(f"📤 推送 tags: {cmd_str}")
    
    if dry_run:
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ 成功推送 tags")
            return True
        else:
            logger.error(f"❌ 推送 tags 失败: {result.stderr.strip()}")
            return False
    except Exception as e:
        logger.error(f"❌ 推送 tags 时发生错误: {e}")
        return False


def _get_current_commit() -> Optional[str]:
    """获取当前 commit hash"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None


def _list_tags() -> list:
    """获取所有 tag 列表"""
    try:
        result = subprocess.run(
            ['git', 'tag', '-l'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return [tag.strip() for tag in result.stdout.split('\n') if tag.strip()]
        return []
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return []