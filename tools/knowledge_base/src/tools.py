from typing import Annotated

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

client = chromadb.HttpClient(host="localhost", port=8000)

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434",
)

collection = client.get_collection("knowledge_base", embedding_function=ef)


def search_knowledge(
    query: Annotated[str, "What to search for (e.g., 'AC troubleshooting steps', 'lockout tagout procedure', 'gas leak response')."],
    n_results: Annotated[int, "Number of results to return."] = 3,
) -> str:
    """Search technical manuals, troubleshooting procedures, safety protocols, and company documentation. Returns matching excerpts with source references."""

    results = collection.query(query_texts=[query], n_results=n_results)

    if not results["documents"][0]:
        return "No relevant documentation found."

    formatted = []

    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        formatted.append(f"[Source: {meta['source']}]\n{doc}")
    return "\n\n---\n\n".join(formatted)


if __name__ == "__main__":
    print()
    print("Test: 'how to troubleshoot an AC that is not cooling'")
    print()
    print(search_knowledge("how to troubleshoot an AC that is not cooling"))
    print()
