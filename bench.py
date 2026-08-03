from __future__ import annotations

import os
import sys
import io

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pathlib import Path
from dotenv import load_dotenv

from ingest import build_knowledge_base
from src.chunking import RecursiveChunker
from src.agent import KnowledgeBaseAgent
from src.embeddings import (
    EMBEDDING_PROVIDER_ENV,
    LOCAL_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_MODEL,
    LocalEmbedder,
    OpenAIEmbedder,
    _mock_embed,
)

DATA_DIR = "data/ussh_library"


def select_embedder():
    load_dotenv(override=False)
    provider = os.getenv(EMBEDDING_PROVIDER_ENV, "mock").strip().lower()
    if provider == "local":
        try:
            return LocalEmbedder(model_name=os.getenv("LOCAL_EMBEDDING_MODEL", LOCAL_EMBEDDING_MODEL))
        except Exception:
            return _mock_embed
    elif provider == "openai":
        try:
            return OpenAIEmbedder(model_name=os.getenv("OPENAI_EMBEDDING_MODEL", OPENAI_EMBEDDING_MODEL))
        except Exception:
            return _mock_embed
    return _mock_embed


def mock_llm(prompt: str) -> str:
    preview = prompt[:300].replace("\n", " ")
    return f"[LLM Response Preview] Based on context: '{preview}...'"


def main():
    embedder = select_embedder()
    chunker = RecursiveChunker(chunk_size=400)
    
    print("=== BENCHMARK RETRIEVAL SYSTEM ===")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Strategy: RecursiveChunker(chunk_size=400)")
    print(f"Embedding Provider: {getattr(embedder, '_backend_name', embedder.__class__.__name__)}")

    store = build_knowledge_base(DATA_DIR, embedding_fn=embedder, chunker=chunker)
    total_chunks = store.get_collection_size()
    print(f"Total chunks loaded: {total_chunks}\n")

    queries = [
        {
            "id": 1,
            "type": "Số liệu / Điều kiện",
            "query": "Sinh viên và cán bộ giảng viên được mượn bao nhiêu quyển sách giáo trình và trong thời gian bao lâu?",
            "filter": None
        },
        {
            "id": 2,
            "type": "Ngoại lệ / Phạt",
            "query": "Nếu tôi trả sách trễ hạn thì sẽ bị phạt bao nhiêu tiền một ngày và khi nào thì bị khóa thẻ?",
            "filter": None
        },
        {
            "id": 3,
            "type": "Liệt kê",
            "query": "Phòng đọc tham khảo Hàn Quốc (Window on Korea) cho phép mang đồ dùng gì vào kho để ghi chép?",
            "filter": None
        },
        {
            "id": 4,
            "type": "Quy trình / Lọc theo Metadata",
            "query": "Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào?",
            "filter": {"audience": "student"}
        },
        {
            "id": 5,
            "type": "Ngoại lệ",
            "query": "Khi làm mất tài liệu, nếu trên thị trường không còn bán và thư viện cũng không còn bản gốc thì tôi phải nộp phạt như thế nào?",
            "filter": None
        }
    ]

    agent = KnowledgeBaseAgent(store=store, llm_fn=mock_llm)

    for q in queries:
        print(f"--- [Query {q['id']}] ({q['type']}) ---")
        print(f"Câu hỏi: {q['query']}")
        if q["filter"]:
            print(f"Metadata Filter: {q['filter']}")
            results = store.search_with_filter(q["query"], top_k=3, metadata_filter=q["filter"])
        else:
            results = store.search(q["query"], top_k=3)

        print(f"Top-3 Results:")
        for idx, r in enumerate(results, start=1):
            doc_id = r["metadata"].get("doc_id", r.get("id"))
            score = r["score"]
            preview = r["content"][:100].replace("\n", " ")
            print(f"  {idx}. [Score: {score:.4f}] doc_id={doc_id} -> {preview}...")

        answer = agent.answer(q["query"], top_k=3)
        print(f"Agent Answer: {answer}\n")


if __name__ == "__main__":
    main()
