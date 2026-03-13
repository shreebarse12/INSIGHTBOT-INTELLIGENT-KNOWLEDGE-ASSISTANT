import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from models.embeddings import get_embedding_model
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS
from models.embeddings import get_embedding_model
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS


def extract_text_from_pdf(pdf_file) -> str:
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        print(f"[PDF] Extracted {len(text)} characters")
        return text
    except Exception as e:
        print(f"[PDF ERROR] {e}")
        return ""


def chunk_text(text: str) -> list:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        raw_chunks = splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={"chunk_index": i}
            )
            for i, chunk in enumerate(raw_chunks)
        ]

        print(f"[CHUNKING] Created {len(documents)} chunks")
        return documents
    except Exception as e:
        print(f"[CHUNK ERROR] {e}")
        return []


def build_vector_store(documents: list):
    try:
        embeddings = get_embedding_model()

        vector_store = FAISS.from_documents(
            documents=documents,
            embedding=embeddings
        )
    
        print(f"[FAISS] Built store with {len(documents)} chunks")
        return vector_store
    except Exception as e:
        print(f"[VECTOR STORE ERROR] {e}")
        raise


def retrieve_relevant_chunks(query: str, vector_store) -> str:
    try:
        results = vector_store.similarity_search(
            query=query,
            k=TOP_K_RESULTS
        )

        if not results:
            return ""

        context = "\n\n---\n\n".join([
            doc.page_content for doc in results
        ])

        print(f"[RETRIEVAL] Found {len(results)} chunks")
        return context
    except Exception as e:
        print(f"[RETRIEVAL ERROR] {e}")
        return ""