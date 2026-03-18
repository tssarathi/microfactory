from typing import Annotated

import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

client = chromadb.HttpClient(host="localhost", port=8000)

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434",
)

collection = client.get_collection("knowledge_base", embedding_function=ef)


def search_knowledge_base(
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


def get_article(
    source: Annotated[str, "Exact source name of the article (e.g., 'gas_leak_emergency_response')."],
) -> str:
    """Retrieve the full text of a specific knowledge base article by its source name."""

    results = collection.get(
        where={"source": source},
        include=["documents", "metadatas"],
    )

    if not results["documents"]:
        return f"No article found with source '{source}'."

    paired = sorted(
        zip(results["documents"], results["metadatas"]),
        key=lambda x: x[1]["chunk_index"],
    )

    full_text = "\n\n".join(doc for doc, _ in paired)
    return f"[Source: {source}]\n\n{full_text}"


def list_articles(
    category: Annotated[str | None, "Filter by category (e.g., 'safety', 'maintenance'). Leave empty to list all."] = None,
) -> str:
    """List all available knowledge base articles, optionally filtered by category."""

    results = collection.get(include=["metadatas"])

    if not results["metadatas"]:
        return "No articles found in the knowledge base."

    articles = set()
    for meta in results["metadatas"]:
        articles.add((meta["source"], meta.get("category", "uncategorized")))

    if category:
        articles = {(s, c) for s, c in articles if c == category}
        if not articles:
            return f"No articles found in category '{category}'."

    grouped: dict[str, list[str]] = {}
    for source, cat in sorted(articles):
        grouped.setdefault(cat, []).append(source)

    lines = []
    for cat in sorted(grouped):
        lines.append(f"\n## {cat}")
        for source in grouped[cat]:
            lines.append(f"  - {source}")

    return "\n".join(lines).strip()


if __name__ == "__main__":
    print()
    print("Test: search_knowledge_base")
    print(search_knowledge_base("how to troubleshoot an AC that is not cooling"))
    print()
    print("Test: get_article")
    print(get_article("gas_leak_emergency_response"))
    print()
    print("Test: list_articles")
    print(list_articles())
    print()
    print("Test: list_articles('safety')")
    print(list_articles("safety"))
    print()
