import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
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
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        GEMINI_MODEL = "gemini-2.5-pro"
        EMBEDDING_MODEL = "models/text-embedding-004"
        CHUNK_SIZE = 1000
        CHUNK_OVERLAP = 50


def get_response(memory, question):
    file_path = Config.PDF_FILE_PATH

    model = ChatGoogleGenerativeAI(
        model=Config.GEMINI_MODEL, 
        api_key=Config.GOOGLE_API_KEY,
        temperature=0
    )
    
    embeddings_zh = GoogleGenerativeAIEmbeddings(
        model=Config.EMBEDDING_MODEL,
        google_api_key=Config.GOOGLE_API_KEY
    )

    loader = PyPDFLoader(file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        separators=['\n','。','？','！','；','，','、']
    )
    texts = text_splitter.split_documents(docs)
    
    db = Chroma.from_documents(texts, embeddings_zh)
    
    retriever = db.as_retriever(search_kwargs={"k": 20})
    
    qa = ConversationalRetrievalChain.from_llm(
        llm = model,
        retriever = retriever,
        memory = memory,
        # 可选：如果你想在后台看到它到底引用了哪一段，可以加上 return_source_documents=True
        #return_source_documents=True 
    )
    
    response = qa.invoke({"chat_history": memory, "question": question})
    return response

