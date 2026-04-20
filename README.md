# KnowledgeBase
RAG 问答系统，支持文件上传构建知识库和多轮对话。
## 技术栈
python + LangChain + Streamlit + Chroma

## 结构
KnowledgeBase/  
├─ app_file_uploader.py       # 知识库上传服务（Streamlit）  
├─ app_qa.py                  # 智能客服问答（Streamlit）  
├─ knowledge_base.py          # 知识库处理：读取、切分、写库、去重  
├─ rag.py                     # RAG 链组装  
├─ vector_stores.py           # 向量库检索封装（持久化）  
├─ file_history_store.py      # 会话历史存储  
├─ config_data.py             # 模型、路径、chunk 等参数配置  
├─ requirements.txt           # 项目依赖（配置环境）  
└─ data/                      # 文本数据 

## 启动页面
启动文件上传页面
```
streamlit run app_file_uploader.py
```
启动对话页面
```
streamlit run app_qa.py
```

