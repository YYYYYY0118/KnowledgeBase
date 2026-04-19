"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    """检查传入的md5字符串是否已经被处理过了"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip() #处理前后空格和回车
            if line == md5_str:
                return True
        return False

def save_md5(md5_str: str):
    """将传入的md5字符串，记录到文件内保存"""
    with open(config.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""
    # 将字符串转换为md5
    str_bytes = input_str.encode(encoding=encoding)

    md5_obj = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹存在则跳过
        os.makedirs(config.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )

    def upload_by_str(self, data:str, filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容以及存在知识库中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小鱼",
        }
        # 加载到向量库
        self.chroma.add_texts(
            # iterable -> list \ tuple
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"