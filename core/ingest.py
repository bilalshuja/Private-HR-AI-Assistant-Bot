import os
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder
from core.config import Config

def ingest_data():
    print("Starting Pinecone Native Hybrid Ingestion...")

    # --- CHANGE 1: Folder Path Check ---
    data_folder = os.path.dirname(Config.PDF_PATH)
    if not os.path.exists(data_folder):
        print(f"Error: Data folder not found at {data_folder}")
        return

    # --- CHANGE 2: Directory Loader (Multiple Files) ---
    print(f" Loading PDFs from {data_folder}...")
    loader = DirectoryLoader(data_folder, glob="*.pdf", loader_cls=PyMuPDFLoader)
    raw_documents = loader.load()

    print("Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ".", " "]
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f" Created {len(documents)} chunks.")

    print(f" Loading Embeddings ({Config.EMBEDDING_MODEL})...")
    embeddings = OllamaEmbeddings(model=Config.EMBEDDING_MODEL)

   
    print(" Training BM25 Encoder...")
    bm25_encoder = BM25Encoder().default()
    
   
    chunk_texts = [doc.page_content for doc in documents]
    bm25_encoder.fit(chunk_texts)
   
    if not os.path.exists(Config.DB_PATH):
        os.makedirs(Config.DB_PATH)
    
    print(" Saving BM25 params to json...")
    bm25_encoder.dump(Config.BM25_PARAMS_PATH)

    # --- CHANGE 4: Uploading via Retriever (Dense + Sparse) ---
    print("Uploading Hybrid Vectors to Pinecone Cloud...")
    
    pc = Pinecone(api_key=Config.PINECONE_API_KEY)
    index = pc.Index(Config.PINECONE_INDEX_NAME)

    retriever = PineconeHybridSearchRetriever(
        embeddings=embeddings,
        sparse_encoder=bm25_encoder,
        index=index
    )

    # Data Upload
    retriever.add_texts(
        texts=chunk_texts,
        metadatas=[doc.metadata for doc in documents]
    )

    print("🎉 Ingestion Complete! Vectors on Cloud.")

if __name__ == "__main__":
    ingest_data()