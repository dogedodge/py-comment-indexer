#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyCommentIndexer - Python注释向量化索引工具
将代码注释存入ChromaDB实现语义搜索
"""

import logging
from pathlib import Path
from typing import List, Tuple
from tqdm import tqdm

import click
from rich import print
from rich.logging import RichHandler
import questionary
from dotenv import load_dotenv

DEFAULT_DB_PATH = "chroma_db"  # 默认数据库存储路径

from extractor_factory import ExtractorFactory
from database import ChromaManager, CommentDict
from utils import scan_source_files, confirm_dangerous

# 配置彩色日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("PyCommentIndexer")
  
# ---------------------- CLI命令实现 ----------------------
@click.group()
@click.option("--verbose", is_flag=True, help="显示调试信息")
def cli(verbose):
    """Python注释向量化索引工具"""
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("调试模式已启用")

@cli.command()
@click.argument("directory", type=click.Path(exists=True), required=False)
def init(directory):
    """初始化数据库（当首次使用时自动调用）"""
    db = ChromaManager()
    print(f"[bold green]✓ ChromaDB已初始化在 {DEFAULT_DB_PATH}[/]")

@cli.command()
@click.argument("directory", type=click.Path(exists=True), default=".")
@click.option("--batch", default=100, help="批量操作大小")
def add(directory, batch):
    """添加目录中的注释到数据库"""
    base_dir = Path(directory)
    source_files = scan_source_files(base_dir)
    if not source_files:
        print("[yellow]! 未找到支持的源代码文件(.py/.ts)[/]")
        return
  
    db = ChromaManager()
    comment_dict = {}
  
    print(f"[bold]扫描到 {len(source_files)} 个源代码文件:[/]")
    for file in tqdm(source_files, desc="处理文件中"):
        rel_path = str(file.relative_to(base_dir))
        extractor = ExtractorFactory.get_extractor(file)
        comments = extractor.extract_comments(file)
        comment_dict[rel_path] = comments
        
        # 保存原始注释到.raw目录
        raw_dir = base_dir / ".raw"
        raw_dir.mkdir(exist_ok=True)
        raw_path = rel_path.replace("/", "_") + ".txt"
        raw_file = raw_dir / raw_path
        try:
            with open(raw_file, "w", encoding="utf-8") as f:
                f.write(comments)
        except IOError as e:
            logger.error(f"无法保存原始注释文件: {raw_file} - {str(e)}")
  
    # 过滤空注释文件
    valid_files = {k:v for k,v in comment_dict.items() if v.strip()}
    print(f"找到{len(valid_files)}个有注释的文件 (已跳过{len(source_files)-len(valid_files)}个空文件)")
  
    if valid_files:
        db.add_comments(valid_files, batch_size=batch)
        print(f"[bold green]✓ 已添加{len(valid_files)}个文件注释到数据库[/]")
    else:
        print("[yellow]! 无有效注释可添加[/]")

@cli.command()
@click.option("--query", "-q", help="直接输入查询字符串")
def search(query):
    """查询相似注释（支持交互）"""
    if not query:
        user_query = questionary.text("输入要查询的注释关键词:").ask().strip()
        if not user_query:
            return
    else:
        user_query = query
  
    db = ChromaManager()
    results = db.query_similar(user_query)
  
    if results:
        print(f"[bold]与'[cyan]{user_query}[/cyan]'相似的注释:[/]")
        for i, (file_path, score) in enumerate(results, 1):
            print(f"  {i}. [yellow][相似度:{score}][/] [green]{file_path}[/]")
    else:
        print("[yellow]! 未找到匹配结果[/]")

@cli.command()
def clear():
    """清空整个数据库（需确认）"""
    if confirm_dangerous("清空数据库吗？操作不可逆！"):
        db = ChromaManager()
        db.clear_database()

# ---------------------- 主入口 ----------------------
if __name__ == "__main__":
    import os
    os.environ["CHROMA_TELEMETRY"] = "false"  # 完全禁用ChromaDB遥测
    load_dotenv()  # 加载环境变量
    cli()
