#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for PyCommentIndexer
"""

from pathlib import Path
from typing import List
from PyInquirer import prompt  # Dependency listed in requirements.txt

def scan_python_files(directory: Path) -> List[Path]:
    """递归扫描目录中的Python文件
    
    Args:
        directory: Root directory to scan
        
    Returns:
        List of Path objects to Python files
    """
    return [
        p for p in directory.rglob("*.py")
        if p.is_file() and not p.name.startswith(".")
    ]

def confirm_dangerous(action: str) -> bool:
    """危险操作确认提示
    
    Args:
        action: Description of dangerous action
        
    Returns:
        True if user confirms, False otherwise
    """
    question = {
        "type": "confirm",
        "name": "confirm",
        "message": f"你确定要{action}吗？",
        "default": False
    }
    return prompt([question]).get("confirm", False)
