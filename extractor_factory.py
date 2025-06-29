#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注释提取器工厂
根据文件扩展名返回对应的语言提取器
"""

from pathlib import Path
from py_extractors import PythonExtractor
from ts_extractors import TypeScriptExtractor

class ExtractorFactory:
    """注释提取器工厂类"""
    
    @staticmethod
    def get_extractor(file_path: Path) -> 'BaseExtractor':
        """
        根据文件扩展名获取对应的注释提取器
        
        Args:
            file_path: 源代码文件路径
            
        Returns:
            对应语言的注释提取器实例
            
        Raises:
            ValueError: 当文件扩展名不被支持时
        """
        ext = file_path.suffix.lower()
        if ext == '.py':
            return PythonExtractor
        elif ext == '.ts':
            return TypeScriptExtractor
        else:
            raise ValueError(f"不支持的文件类型: {ext}")
