"""
文本处理工具
提供常用的文本处理和字符串操作功能
"""

import re
import string
import unicodedata
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path


class TextProcessor:
    """文本处理工具类"""
    
    @staticmethod
    def normalize_text(text: str, 
                      remove_accents: bool = True,
                      to_lowercase: bool = True,
                      remove_punctuation: bool = False) -> str:
        """标准化文本
        
        Args:
            text: 输入文本
            remove_accents: 是否移除重音符号
            to_lowercase: 是否转换为小写
            remove_punctuation: 是否移除标点符号
            
        Returns:
            标准化后的文本
        """
        if remove_accents:
            # 移除重音符号
            text = unicodedata.normalize('NFKD', text)
            text = ''.join(c for c in text if not unicodedata.combining(c))
        
        if to_lowercase:
            text = text.lower()
        
        if remove_punctuation:
            text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text.strip()
    
    @staticmethod
    def camel_to_snake(text: str) -> str:
        """驼峰命名转蛇形命名
        
        Args:
            text: 驼峰命名字符串
            
        Returns:
            蛇形命名字符串
        """
        # 在大写字母前插入下划线
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        # 处理连续大写字母
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(text: str, capitalize_first: bool = False) -> str:
        """蛇形命名转驼峰命名
        
        Args:
            text: 蛇形命名字符串
            capitalize_first: 是否首字母大写
            
        Returns:
            驼峰命名字符串
        """
        components = text.split('_')
        if capitalize_first:
            return ''.join(word.capitalize() for word in components)
        else:
            return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @staticmethod
    def kebab_to_camel(text: str, capitalize_first: bool = False) -> str:
        """短横线命名转驼峰命名
        
        Args:
            text: 短横线命名字符串
            capitalize_first: 是否首字母大写
            
        Returns:
            驼峰命名字符串
        """
        components = text.split('-')
        if capitalize_first:
            return ''.join(word.capitalize() for word in components)
        else:
            return components[0] + ''.join(word.capitalize() for word in components[1:])
    
    @staticmethod
    def camel_to_kebab(text: str) -> str:
        """驼峰命名转短横线命名
        
        Args:
            text: 驼峰命名字符串
            
        Returns:
            短横线命名字符串
        """
        # 在大写字母前插入短横线
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', text)
        # 处理连续大写字母
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
    
    @staticmethod
    def extract_variables(text: str, pattern: str = r'\{\{(\w+)\}\}') -> List[str]:
        """从文本中提取变量
        
        Args:
            text: 输入文本
            pattern: 变量匹配模式，默认为 {{variable}}
            
        Returns:
            变量名列表
        """
        return re.findall(pattern, text)
    
    @staticmethod
    def replace_variables(text: str, 
                         variables: Dict[str, str],
                         pattern: str = r'\{\{(\w+)\}\}') -> str:
        """替换文本中的变量
        
        Args:
            text: 输入文本
            variables: 变量字典
            pattern: 变量匹配模式，默认为 {{variable}}
            
        Returns:
            替换后的文本
        """
        def replace_func(match: re.Match[str]) -> str:
            var_name = match.group(1)
            return variables.get(var_name, match.group(0))
        
        return re.sub(pattern, replace_func, text)
    
    @staticmethod
    def remove_empty_lines(text: str, keep_single: bool = True) -> str:
        """移除空行
        
        Args:
            text: 输入文本
            keep_single: 是否保留单个空行
            
        Returns:
            处理后的文本
        """
        if keep_single:
            # 将多个连续空行替换为单个空行
            return re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        else:
            # 移除所有空行
            return re.sub(r'\n\s*\n', '\n', text)
    
    @staticmethod
    def indent_text(text: str, spaces: int = 4, first_line: bool = True) -> str:
        """缩进文本
        
        Args:
            text: 输入文本
            spaces: 缩进空格数
            first_line: 是否缩进第一行
            
        Returns:
            缩进后的文本
        """
        indent = ' ' * spaces
        lines = text.split('\n')
        
        if not first_line and lines:
            return lines[0] + '\n' + '\n'.join(indent + line for line in lines[1:])
        else:
            return '\n'.join(indent + line for line in lines)
    
    @staticmethod
    def wrap_text(text: str, width: int = 80, indent: int = 0) -> str:
        """文本换行
        
        Args:
            text: 输入文本
            width: 行宽度
            indent: 缩进空格数
            
        Returns:
            换行后的文本
        """
        import textwrap
        
        wrapper = textwrap.TextWrapper(
            width=width,
            initial_indent=' ' * indent,
            subsequent_indent=' ' * indent
        )
        
        return wrapper.fill(text)
    
    @staticmethod
    def extract_code_blocks(text: str, language: Optional[str] = None) -> List[Dict[str, str]]:
        """从Markdown文本中提取代码块
        
        Args:
            text: Markdown文本
            language: 指定语言，None表示提取所有
            
        Returns:
            代码块列表，每个元素包含language和code字段
        """
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        code_blocks = []
        for lang, code in matches:
            if language is None or lang == language:
                code_blocks.append({
                    'language': lang or 'text',
                    'code': code.strip()
                })
        
        return code_blocks
    
    @staticmethod
    def generate_slug(text: str, max_length: int = 50) -> str:
        """生成URL友好的slug
        
        Args:
            text: 输入文本
            max_length: 最大长度
            
        Returns:
            slug字符串
        """
        # 转换为小写并移除重音
        text = TextProcessor.normalize_text(text, remove_accents=True, to_lowercase=True)
        
        # 只保留字母、数字和空格
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        
        # 将空格和多个短横线替换为单个短横线
        text = re.sub(r'[\s-]+', '-', text)
        
        # 移除首尾短横线
        text = text.strip('-')
        
        # 限制长度
        if len(text) > max_length:
            text = text[:max_length].rstrip('-')
        
        return text
    
    @staticmethod
    def count_words(text: str, exclude_common: bool = False) -> Dict[str, int]:
        """统计词频
        
        Args:
            text: 输入文本
            exclude_common: 是否排除常见词汇
            
        Returns:
            词频字典
        """
        # 常见词汇列表
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'can', 'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those'
        }
        
        # 标准化文本并分词
        normalized = TextProcessor.normalize_text(text, remove_punctuation=True)
        words = normalized.split()
        
        # 统计词频
        word_count = {}
        for word in words:
            if exclude_common and word.lower() in common_words:
                continue
            word_count[word] = word_count.get(word, 0) + 1
        
        return word_count
    
    @staticmethod
    def find_and_replace_patterns(text: str, patterns: List[Tuple[str, str]]) -> str:
        """批量查找替换模式
        
        Args:
            text: 输入文本
            patterns: 模式列表，每个元素为(查找模式, 替换文本)元组
            
        Returns:
            替换后的文本
        """
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)
        return text
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """从文本中提取URL
        
        Args:
            text: 输入文本
            
        Returns:
            URL列表
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(url_pattern, text)
    
    @staticmethod
    def extract_emails(text: str) -> List[str]:
        """从文本中提取邮箱地址
        
        Args:
            text: 输入文本
            
        Returns:
            邮箱地址列表
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
    
    @staticmethod
    def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
        """截断文本
        
        Args:
            text: 输入文本
            max_length: 最大长度
            suffix: 截断后缀
            
        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        
        truncate_length = max_length - len(suffix)
        return text[:truncate_length] + suffix
    
    @staticmethod
    def similarity(text1: str, text2: str) -> float:
        """计算两个文本的相似度（简单的字符级别）
        
        Args:
            text1: 第一个文本
            text2: 第二个文本
            
        Returns:
            相似度分数 (0-1)
        """
        # 使用简单的字符集合交集计算相似度
        set1 = set(text1.lower())
        set2 = set(text2.lower())
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        if union == 0:
            return 1.0 if len(text1) == 0 and len(text2) == 0 else 0.0
        
        return intersection / union
    
    @staticmethod
    def format_template(template: str, **kwargs) -> str:
        """格式化模板字符串
        
        Args:
            template: 模板字符串
            **kwargs: 模板变量
            
        Returns:
            格式化后的字符串
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            print(f"❌ 模板变量缺失: {e}")
            return template
    
    @staticmethod
    def clean_filename(filename: str, replacement: str = '_') -> str:
        """清理文件名，移除非法字符
        
        Args:
            filename: 原始文件名
            replacement: 替换字符
            
        Returns:
            清理后的文件名
        """
        # Windows 和 Unix 系统的非法字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
        
        # 替换非法字符
        cleaned = re.sub(illegal_chars, replacement, filename)
        
        # 移除首尾空格和点
        cleaned = cleaned.strip(' .')
        
        # 限制长度（考虑文件系统限制）
        if len(cleaned) > 255:
            name, ext = Path(cleaned).stem, Path(cleaned).suffix
            max_name_length = 255 - len(ext)
            cleaned = name[:max_name_length] + ext
        
        return cleaned or 'untitled'