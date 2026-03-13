import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from models.embeddings import get_embedding_model
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS
# Import from models — their job is just to return model objects
from models.embeddings import get_embedding_model
from config.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts all text from an uploaded PDF file.
    
    HOW TO EXTEND:
    - Support .txt?  → return pdf_file.read().decode("utf-8")
    - Support .docx? → use python-docx library
    - Support URL?   → use requests + BeautifulSoup
    """
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
    """
    Splits text into overlapping chunks using LangChain splitter.
    
    WHY RecursiveCharacterTextSplitter?
    - Tries to split by paragraph → sentence → word
    - Never cuts a sentence in half
    - Much better than manual fixed-size splitting
    
    HOW TO EXTEND:
    - Bigger chunks?      increase CHUNK_SIZE in config.py
    - More overlap?       increase CHUNK_OVERLAP in config.py
    - Sentence level?     use NLTKTextSplitter instead
    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        raw_chunks = splitter.split_text(text)

        # Wrap in Document objects so we can attach metadata later
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
    """
    Converts chunks into vectors and stores in FAISS.
    
    HOW IT WORKS:
    1. Takes each document's text
    2. Runs through embedding model → vector
    3. Stores all vectors in FAISS index
    
    HOW TO EXTEND:
    - Save to disk?   → vector_store.save_local("faiss_index")
    - Load from disk? → FAISS.load_local("faiss_index", embeddings)
    - Add more docs?  → vector_store.add_documents(new_docs)
    """
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
    """
    Finds most relevant chunks for a user query.
    
    HOW IT WORKS:
    1. Embeds the query into a vector
    2. FAISS finds closest chunk vectors
    3. Returns original text of those chunks
    
    HOW TO EXTEND:
    - With scores?    → similarity_search_with_score(query, k=...)
    - Avoid repeats?  → max_marginal_relevance_search(query, k=...)
    - With filter?    → similarity_search(query, filter={"source": "x"})
    """
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