#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChromaDB database management for PyCommentIndexer
"""

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger("PyCommentIndexer")

# ChromaDB配置常量
DEFAULT_DB_PATH = "./chroma_db"
COLLECTION_NAME = "python_comments"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# 类型别名
CommentDict = Dict[str, str]

class ChromaManager:
    """管理ChromaDB连接和操作"""
  
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """初始化ChromaDB客户端
        
        Args:
            db_path: Path to ChromaDB persistent storage
        """
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            logger.error("ChromaDB未安装！请运行: pip install chromadb")
            raise RuntimeError("依赖未安装")
          
        self.client = chromadb.PersistentClient(
            path=db_path, 
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
      
    def get_collection(self) -> "chromadb.Collection":
        """获取或创建注释集合
        
        Returns:
            ChromaDB collection instance
            
        Raises:
            Exception: If connection fails
        """
        try:
            return self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
                embedding_function=EMBEDDING_MODEL
            )
        except Exception as e:
            logger.error(f"DB连接失败: {str(e)}")
            raise
  
    def clear_database(self) -> None:
        """清空整个数据库（危险操作）"""
        self.client.reset()
        logger.info("✅ 数据库已清空")

    def add_comments(self, comment_dict: CommentDict, batch_size=100) -> None:
        """批量添加注释到数据库
        
        Args:
            comment_dict: Dictionary of {file_path: comment_text}
            batch_size: Batch size for database operations
        """
        collection = self.get_collection()
        ids, texts = [], []
      
        for file_id, comment in comment_dict.items():
            if comment:  # 跳过空注释
                ids.append(file_id)
                texts.append(comment)
              
                if len(ids) >= batch_size:
                    collection.add(ids=ids, documents=texts)
                    ids, texts = [], []
      
        if ids:  # 处理最后一批
            collection.add(ids=ids, documents=texts)
  
    def query_similar(self, query: str, n_results=5) -> List[Tuple[str, float]]:
        """查询相似注释
        
        Args:
            query: Search query string
            n_results: Number of results to return
            
        Returns:
            List of (file_path, similarity_score) tuples
        """
        result = []
        try:
            collection = self.get_collection()
            response = collection.query(query_texts=[query], n_results=n_results)
            result = list(zip(
                response['ids'][0],
                [round(score, 3) for score in response['distances'][0]]
            ))
        except Exception as e:
            logger.error(f"查询失败: {str(e)}")
        return result
