#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽象注释提取器基类
定义多语言提取器统一接口
"""

from pathlib import Path
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """所有语言特定提取器必须继承的抽象基类"""
    
    @staticmethod
    @abstractmethod
    def extract_comments(file_path: Path) -> str:
        """
        从指定文件路径提取注释内容
        返回合并后的注释文本
        
        Args:
            file_path: 源代码文件路径
            
        Returns:
            合并后的注释字符串
        """
        pass
