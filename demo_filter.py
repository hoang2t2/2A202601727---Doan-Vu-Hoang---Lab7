import os
import sys

# Đảm bảo mã hóa console trên Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from ingest import build_knowledge_base
from src.embeddings import LocalEmbedder
from src.chunking import RecursiveChunker

def main():
    print("=== CHUẨN BỊ MÔI TRƯỜNG TÌM KIẾM ===")
    embedding_fn = LocalEmbedder()
    chunker = RecursiveChunker(400)
    store = build_knowledge_base("data/ussh_library", embedding_fn, chunker)
    
    question = "Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào?"
    print(f"\n[Câu hỏi]: {question}")
    
    print("\n" + "="*50)
    print(" ❌ KỊCH BẢN 1: TÌM KIẾM KHÔNG CÓ FILTER")
    print("="*50)
    results_no_filter = store.search(question, top_k=3)
    for i, r in enumerate(results_no_filter, 1):
        doc = r['metadata'].get('doc_id')
        audience = r['metadata'].get('audience')
        content_preview = r['content'].replace('\n', ' ')[:120]
        print(f"Top {i} [Score: {r['score']:.4f}] | File: {doc} | Đối tượng: {audience}")
        print(f"   => {content_preview}...")

    print("\n" + "="*50)
    print(" ✅ KỊCH BẢN 2: TÌM KIẾM CÓ FILTER (audience=student)")
    print("="*50)
    results_filter = store.search_with_filter(question, filter_dict={"audience": "student"}, top_k=3)
    for i, r in enumerate(results_filter, 1):
        doc = r['metadata'].get('doc_id')
        audience = r['metadata'].get('audience')
        content_preview = r['content'].replace('\n', ' ')[:120]
        print(f"Top {i} [Score: {r['score']:.4f}] | File: {doc} | Đối tượng: {audience}")
        print(f"   => {content_preview}...")
        
    print("\n>>> Nhận xét: Không có filter, hệ thống bị nhiễu bởi các phòng đọc/mượn chung (audience: all). Có filter, kết quả thu hẹp chuẩn xác vào phòng thảo luận nhóm của sinh viên! <<<\n")

if __name__ == "__main__":
    main()
