import os
import shutil
import fnmatch
from pathlib import Path
from typing import List, Optional, Callable, Dict, Any


class FileOperations:
    """文件操作工具类"""
    
    @staticmethod
    def copy_directory(src: Path, dst: Path, 
                      ignore_patterns: Optional[List[str]] = None) -> bool:
        """复制目录，支持忽略模式"""
        try:
            if ignore_patterns:
                def ignore_func(dir_path, files):
                    ignored = []
                    for file in files:
                        for pattern in ignore_patterns:
                            if fnmatch.fnmatch(file, pattern):
                                ignored.append(file)
                                break
                    return ignored
                
                shutil.copytree(src, dst, ignore=ignore_func)
            else:
                shutil.copytree(src, dst)
            
            return True
            
        except Exception as e:
            print(f"❌ 复制目录失败: {e}")
            return False
    
    @staticmethod
    def find_files(directory: Path, patterns: List[str], 
                  recursive: bool = True) -> List[Path]:
        """查找匹配模式的文件"""
        files = []
        
        if recursive:
            for pattern in patterns:
                files.extend(directory.rglob(pattern))
        else:
            for pattern in patterns:
                files.extend(directory.glob(pattern))
        
        return files
    
    @staticmethod
    def replace_in_file(file_path: Path, replacements: Dict[str, str]) -> bool:
        """替换文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except UnicodeDecodeError:
            # 处理二进制文件
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                for old, new in replacements.items():
                    old_bytes = old.encode('utf-8')
                    new_bytes = new.encode('utf-8')
                    content = content.replace(old_bytes, new_bytes)
                
                with open(file_path, 'wb') as f:
                    f.write(content)
                
                return True
                
            except Exception as e:
                print(f"⚠️  跳过文件 {file_path}: {e}")
                return False
        
        except Exception as e:
            print(f"❌ 替换文件内容失败 {file_path}: {e}")
            return False
    
    @staticmethod
    def rename_files(directory: Path, old_name: str, new_name: str) -> List[Path]:
        """重命名文件和目录"""
        renamed_items = []
        
        # 收集需要重命名的项目（从深层开始）
        items_to_rename = []
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files + dirs:
                if old_name in name:
                    old_path = Path(root) / name
                    new_filename = name.replace(old_name, new_name)
                    new_path = Path(root) / new_filename
                    items_to_rename.append((old_path, new_path))
        
        # 执行重命名
        for old_path, new_path in items_to_rename:
            try:
                if old_path.exists():
                    old_path.rename(new_path)
                    renamed_items.append(new_path)
            except Exception as e:
                print(f"❌ 重命名失败 {old_path} -> {new_path}: {e}")
        
        return renamed_items
    
    @staticmethod
    def create_directory_structure(base_path: Path, 
                                 structure: Dict[str, Any]) -> bool:
        """根据字典创建目录结构"""
        try:
            for name, content in structure.items():
                path = base_path / name
                
                if isinstance(content, dict):
                    # 创建目录
                    path.mkdir(parents=True, exist_ok=True)
                    # 递归创建子结构
                    FileOperations.create_directory_structure(path, content)
                else:
                    # 创建文件
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content or '')
            
            return True
            
        except Exception as e:
            print(f"❌ 创建目录结构失败: {e}")
            return False