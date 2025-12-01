import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # App Settings
    SECRET_KEY = os.getenv("SECRET_KEY", " ")
    
    # Pinecone Config (New)
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
        
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PDF_PATH = os.path.join(BASE_DIR, "data", "HRPolicies.pdf")
    DB_PATH = os.path.join(BASE_DIR, "vectorstore")

    BM25_PARAMS_PATH = os.path.join(DB_PATH, "bm25_values.json")
    
    # Models
    EMBEDDING_MODEL = "nomic-embed-text"
    LLM_MODEL = "llama3.2:latest"
    
    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"