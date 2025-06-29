#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TypeScript语言注释提取器实现
"""

import re
from pathlib import Path
from .base_extractor import BaseExtractor

class TypeScriptExtractor(BaseExtractor):
    """TypeScript语言注释提取器实现"""
    
    @staticmethod
    def extract_comments(file_path: Path) -> str:
        """
        从TypeScript文件中提取注释
        支持单行(//)和多行(/**/)注释
        
        Args:
            file_path: TypeScript源文件路径
            
        Returns:
            合并后的注释字符串
        """
        try:
            content = file_path.read_text(encoding="utf-8")
            # 匹配单行注释和多行注释
            pattern = r"(\/\/[^\n]*|\/\*[\s\S]*?\*\/)"
            matches = re.findall(pattern, content)
            return " ".join(match.strip() for match in matches)
        except (UnicodeDecodeError, re.error) as e:
            logger = logging.getLogger("PyCommentIndexer")
            logger.error(f"解析失败: {file_path} - {str(e)}")
            return ""
