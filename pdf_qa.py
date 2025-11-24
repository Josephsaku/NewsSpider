import os
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory

# 导入配置
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import Config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    class Config:
        PDF_FILE_PATH = "./News.pdf"
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        DEEPSEEK_MODEL = "deepseek-chat"
        EMBEDDING_MODEL = "quentinz/bge-large-zh-v1.5:latest"
        CHUNK_SIZE = 1000
        CHUNK_OVERLAP = 50

def get_response(memory, question):
    file_path = Config.PDF_FILE_PATH

    model = ChatDeepSeek(model=Config.DEEPSEEK_MODEL, api_key=Config.DEEPSEEK_API_KEY,
                         temperature=0)
    embeddings_zh = OllamaEmbeddings(model=Config.EMBEDDING_MODEL)

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        separators=['\n','。','？','！','；','，','、']
    )
    # memory = ConversationBufferMemory(return_messages=True,memory_key='chat_history',output_key='answer')
    texts = text_splitter.split_documents(docs)
    db = Chroma.from_documents(texts, embeddings_zh)
    retriever = db.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm = model,
        retriever = retriever,
        memory = memory
    )
    response = qa.invoke({"chat_history": memory, "question": question})
    return response