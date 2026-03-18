import shutil
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter

KB_DIR = Path("data/bronze/knowledge_base/")

client = chromadb.HttpClient(host="localhost", port=8000)

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434",
)

# Clean up orphaned HNSW segment directories
VECTORS_DIR = Path("data/silver/vectors/")
for item in VECTORS_DIR.iterdir():
    if item.is_dir():
        shutil.rmtree(item)

try:
    client.delete_collection("knowledge_base")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="knowledge_base",
    embedding_function=ef,
    configuration={"hnsw": {"space": "cosine"}},
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=0)

total_chunks = 0

print()

for file in KB_DIR.rglob("*.md"):
    test = file.read_text()
    chunks = text_splitter.split_text(test)
    ids = [f"{file.stem}__chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": file.stem,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "category": file.parent.name,
        }
        for i in range(len(chunks))
    ]

    collection.add(ids=ids, documents=chunks, metadatas=metadatas)
    total_chunks += len(chunks)
    print(f"Ingested: {file.name} into {len(chunks)} chunks")

print(f"\nDone. {total_chunks} chunks in collection 'knowledge_base'.\n")

# Test
print("Test: 'gas leak emergency procedure'\n")
results = collection.query(query_texts=["gas leak emergency procedure"], n_results=3)

for i, (doc_id, dist) in enumerate(zip(results["ids"][0], results["distances"][0])):
    print(f"Result {i + 1} (similarity: {1 - dist:.3f}) from {doc_id}")

print()
