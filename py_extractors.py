#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python语言注释提取器实现
"""

import ast
import tokenize
from pathlib import Path
import logging
from .base_extractor import BaseExtractor

logger = logging.getLogger("PyCommentIndexer")

class PythonExtractor(BaseExtractor):
    """Python语言注释提取器实现"""
  
    @staticmethod
    def extract_comments(file_path: Path) -> str:
        """
        提取文件中的文档字符串和行注释
        返回合并后的注释文本
        
        Args:
            file_path: Path to Python source file
            
        Returns:
            Combined docstrings and comments as single string
        """
        try:
            return (
                PythonExtractor.extract_docstrings(file_path) + " " +
                PythonExtractor.extract_line_comments(file_path)
            )
        except (SyntaxError, UnicodeDecodeError) as e:
            logger.error(f"解析失败: {file_path} - {str(e)}")
            return ""
  
    @staticmethod
    def extract_docstrings(file_path: Path) -> str:
        """使用AST解析文档字符串
        
        Args:
            file_path: Path to Python source file
            
        Returns:
            Combined docstrings as single string
        """
        docstrings = []
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return ""  # 忽略语法错误文件
      
        for node in ast.walk(tree):
            if hasattr(node, "docstring") and node.docstring:
                docstrings.append(node.docstring.strip())
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)) and ast.get_docstring(node):
                docstrings.append(ast.get_docstring(node).strip())
      
        return " ".join(docstrings)
  
    @staticmethod
    def extract_line_comments(file_path: Path) -> str:
        """使用tokenize提取行注释
        
        Args:
            file_path: Path to Python source file
            
        Returns:
            Combined line comments as single string
        """
        comments = []
        with open(file_path, "rb") as f:
            try:
                for tok in tokenize.tokenize(f.readline):
                    if tok.type == tokenize.COMMENT:
                        comments.append(tok.string.strip())
            except tokenize.TokenError:
                pass  # 忽略tokenize错误
        return " ".join(comments)
