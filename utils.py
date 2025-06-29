#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for PyCommentIndexer
"""

from pathlib import Path
from typing import List
import questionary

def scan_source_files(directory: Path) -> List[Path]:
    """递归扫描目录中的源代码文件（支持.py和.ts）
    
    Args:
        directory: Root directory to scan
        
    Returns:
        List of Path objects to source files
    """
    return [
        p for p in directory.rglob("*.*")
        if p.suffix in ('.py', '.ts')
        if p.is_file() 
        and not p.name.startswith(".")
        and ".venv" not in str(p)  # 排除.venv目录下的文件
    ]

def confirm_dangerous(action: str) -> bool:
    """危险操作确认提示
    
    Args:
        action: Description of dangerous action
        
    Returns:
        True if user confirms, False otherwise
    """
    return questionary.confirm(
        f"你确定要{action}吗？",
        default=False
    ).ask()
