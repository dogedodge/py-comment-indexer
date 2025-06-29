# PyCommentIndexer - Python注释向量化索引工具

## 功能概述
- 递归遍历指定目录下的Python文件
- 提取每个Python文件的代码注释（行注释和文档字符串）
- 将注释与文件路径关联后存入Chroma向量数据库
- 提供CRUD操作和相似注释搜索功能

## 安装
1. 克隆仓库
```bash
git clone https://github.com/your-repo/py-comment-indexer.git
cd py-comment-indexer
```

2. 创建虚拟环境并安装依赖
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 使用说明

### 基本命令
1. **初始化数据库**（自动创建存储目录）:
   ```bash
   python comment_indexer.py init
   ```

2. **索引注释**（扫描指定目录）:
   ```bash
   python comment_indexer.py add /path/to/code
   # 使用当前目录
   python comment_indexer.py add
   ```

3. **搜索注释**:
   ```bash
   # 命令行直接查询
   python comment_indexer.py search -q "数据库连接"
   # 交互模式
   python comment_indexer.py search
   ```

4. **清空数据库**（高危操作）:
   ```bash
   python comment_indexer.py clear
   ```

### 示例
```bash
# 创建测试文件
mkdir test_project
echo \"\"\"
数据库配置模块
\"\"\n\n# 重要: MySQL连接设置 > test_project/db.py

# 索引并搜索
python comment_indexer.py add test_project
python comment_indexer.py search -q "重要配置"

# 输出结果
[bold]与'重要配置'相似的注释:[/]
  1. [相似度:0.85] db.py
```

## 设计特点
1. **智能解析**：AST+tokenize双模式精准提取注释
2. **内存优化**：分批写入防止内存溢出
3. **交互友好**：
   - Rich彩色输出
   - PyInquirer交互调查
   - 危险操作二次确认
4. **健壮性**：
   - 异常文件跳过机制
   - 语法错误自动处理
   - 详细操作日志

> 首次运行会自动下载`sentence-transformers/all-MiniLM-L6-v2`模型（约80MB）
