# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Đoàn Vũ Hoàng - 2A202601727
**Nhóm:** 404NotFound
**Ngày:** 2026-08-04

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Cosine similarity đo lường góc giữa hai vector embedding trong không gian nhiều chiều, thể hiện độ tương đồng về mặt hướng và ngữ nghĩa của hai đoạn văn bản. Giá trị càng gần 1 biểu thị hai câu càng đồng nghĩa/tương đồng, còn giá trị gần 0 hoặc âm biểu thị hai câu khác biệt về mặt ngữ nghĩa.

**Ví dụ có độ tương tự CAO:**
- Câu A: Thư viện trường mở cửa phục vụ bạn đọc từ 7h30 sáng đến 21h00 tối.
- Câu B: Thời gian hoạt động hàng ngày của thư viện là từ 7h30 đến 21h00.
- Tại sao tương đồng: Cả hai câu đều biểu diễn cùng một ý niệm ngữ nghĩa về thời gian mở cửa của thư viện, dù từ ngữ diễn đạt khác nhau.

**Ví dụ có độ tương tự THẤP:**
- Câu A: Trả sách trễ hạn sẽ bị phạt 2.000 đồng một ngày.
- Câu B: Phòng tra cứu đa phương tiện được trang bị hệ thống máy tính hiện đại.
- Tại sao khác: Câu A nói về quy định xử phạt vi phạm mượn sách, còn Câu B nói về trang thiết bị phòng vi tính.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity chỉ đo lường góc giữa hai vector mà không phụ thuộc vào độ dài (magnitude) của vector. Khi nhúng văn bản, độ dài văn bản có thể làm biến đổi độ lớn vector, khiến khoảng cách Euclid bị sai lệch dù hai đoạn văn cùng nói về một chủ đề.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* Bước nhảy (step) = 500 - 50 = 450. Số chunk = ceil((10000 - 50) / 450) = ceil(9950 / 450) = ceil(22.11) = 23 chunks.
> *Đáp án:* 23 chunks

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Bước nhảy giảm xuống còn 400 ký tự, làm tăng tổng số chunk lên ceil((10000 - 100) / 400) = 25 chunks. Việc tăng overlap giúp bảo tồn ngữ cảnh ở các ranh giới cắt, tránh việc từ/câu quan trọng bị ngắt đôi làm mất ngữ nghĩa khi nhúng vector.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Tôi sử dụng biểu thức chính quy (Regex) `(?<=[.!?])\s+` để phân tách câu tại khoảng trắng đứng ngay sau các dấu chấm, chấm hỏi, chấm cảm. Cách làm này giữ nguyên dấu câu ở cuối câu trước thay vì làm mất. Vòng lặp gom nhóm các câu thành chunk tối đa `max_sentences_per_chunk` và `strip()` khoảng trắng thừa.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Thuật toán áp dụng phương pháp chia để trị đệ quy theo danh sách ưu tiên `["\n\n", "\n", ". ", " ", ""]`. Nếu văn bản dài hơn `chunk_size`, nó thử cắt theo dấu phân cách cao nhất (`\n\n`), sau đó tiến hành gộp các đoạn nhỏ lân cận lại nếu tổng kích thước vẫn nằm trong giới hạn mốc `chunk_size` để tối ưu hóa ngữ cảnh.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Với `add_documents`, tôi nhân bản `metadata`, bổ sung `doc_id` và tạo ID duy nhất cho chunk `doc_id::index` rồi nhúng nội dung thành vector lưu vào mảng `_store`. Hàm `search` tính nhúng cho query 1 lần duy nhất, sau đó tính tích vô hướng (`_dot`) với từng record và sắp xếp score giảm dần để lấy top_k.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Áp dụng chiến lược **Pre-filtering (Lọc trước, xếp hạng sau)**: Nếu có `metadata_filter`, hàm sẽ lọc danh sách `_store` để chọn ra các chunk khớp 100% các cặp key/value trước, sau đó mới gọi `_search_records` tính similarity. Với `delete_document`, hệ thống lọc loại bỏ mọi record có `id` hoặc `metadata['doc_id']` bằng ID đầu vào và trả về `True` nếu có phần tử bị xóa.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Hàm gọi `store.search(question, top_k)` để truy xuất top-k chunk liên quan, nối các đoạn `content` thành một chuỗi `context` duy nhất. Sau đó xây dựng prompt theo cấu trúc `Context:\n{context}\n\nQuestion: {question}\nAnswer:` và truyền vào hàm callback `llm_fn` để tổng hợp câu trả lời.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
========================== test session starts ===========================
platform win32 -- Python 3.11.6, pytest-9.1.1, pluggy-1.6.0 -- D:\code\aithucchien\K3-Day07-Data-Foundations\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\code\aithucchien\K3-Day07-Data-Foundations
plugins: anyio-4.14.2
collected 42 items                                                        

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED [100%]

=========================== 42 passed in 0.27s ===========================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Thư viện mở cửa từ 7h30 sáng đến 21h00 tối. | Thời gian hoạt động của thư viện là từ 7h30 đến 21h00. | Cao | 0.8322 | Đúng |
| 2 | Sinh viên được mượn tối đa 6 cuốn sách giáo trình. | Giảng viên được mượn tối đa 8 cuốn tài liệu tham khảo. | Cao | 0.7710 | Đúng |
| 3 | Trả sách quá hạn sẽ bị phạt 2.000 đồng một ngày. | Thư viện trường mở cửa tất cả các ngày trong tuần. | Thấp | 0.1973 | Đúng |
| 4 | Quy định sử dụng phòng thảo luận nhóm tại cơ sở 1. | Hướng dẫn đăng ký phòng học nhóm dành cho sinh viên. | Cao | 0.5416 | Đúng |
| 5 | Sinh viên làm mất sách phải bồi thường gấp 3 lần giá trị. | Máy tính phòng tra cứu dữ liệu không được tự ý cài phần mềm. | Thấp | -0.0318 | Đúng |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp số 2 đạt điểm rất cao (0.7710) mặc dù hai câu đề cập đến hai đối tượng khác nhau (Sinh viên vs Giảng viên) và hai hạn mức khác nhau (6 cuốn vs 8 cuốn). Điều này cho thấy Embeddings biểu diễn ý nghĩa chủ đề tổng thể (quy định mượn tài liệu đại học) rất mạnh, nhưng đôi khi kém nhạy bén với các chi tiết thực thể số liệu cụ thể, lý giải vì sao cần kết hợp Metadata Filter để phân tách đối tượng.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Sinh viên & CB-GV được mượn bao nhiêu giáo trình? | 12. Nếu có hành vi vi phạm nội quy, tùy theo mức độ... | 0.3088 | Có | Trích xuất thông tin mượn 6 cuốn (SV) và 8 cuốn (GV) |
| 2 | Trả sách trễ hạn bị phạt bao nhiêu tiền? | Phạt 2.000 đ/ngày (nếu tái phạm 02 lần trở lên... | 0.6462 | Có | Phạt 2.000đ/ngày, khóa giao dịch 3-6 tháng |
| 3 | Vật dụng mang vào phòng Hàn Quốc để ghi chép? | 1. Khi vào phòng mượn, bạn đọc phải xuất trình... | 0.7044 | Có | Chỉ được mang 01 quyển vở/giấy tập |
| 4 | Đăng ký phòng thảo luận nhóm (có filter student)? | 1. Bạn đọc muốn sử dụng phòng thảo luận nhóm... | 0.7398 | Có | Tối đa 10 sinh viên, thực hiện 3 bước đăng ký |
| 5 | Mất tài liệu không còn bán bồi thường thế nào? | - Nếu trên thị trường và thư viện đều không còn... | 0.2113 | Có | Phạt nộp số tiền gấp 03 lần giá trị định giá |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Việc kết hợp chiến lược chia nhỏ đệ quy (Recursive Chunking) theo cấu trúc đoạn văn bản và bộ lọc Metadata Pre-filtering giúp tăng vượt trội độ chính xác truy xuất RAG so với các phương pháp chia cố định thông thường.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
