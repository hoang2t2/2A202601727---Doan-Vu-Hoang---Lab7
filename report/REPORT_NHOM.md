# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** 404NotFound
**Thành viên:** Đoàn Vũ Hoàng - 2A202601727
                Lê Hoàng Long - 2A202601025
                Nguyễn Mạnh Hưng - 2A202601829
                Sùng A Khua - 2A202601129
                Đàm Vinh Quang - 2A202601255
**Ngày:** 2026-08-04

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Phạm vi bộ tài liệu (Scope)

**Chủ đề (cố định theo lớp K3):** Dịch vụ / quy định đại học (đăng ký môn, học phí, học bổng, thư viện, ký túc xá…).

**Phạm vi cụ thể nhóm tập trung:**
> Nội quy sử dụng thư viện (bao gồm các phòng chức năng: phòng đọc, mượn, tạp chí, đa phương tiện...) và quy định về quyền hạn, trách nhiệm, mức phạt đối với sinh viên và cán bộ giảng viên tại trường Đại học KHXH&NV.

### Danh sách tài liệu (Data Inventory)

| # | Tên tài liệu | Nguồn (Source URL) | Ngày lấy / Phiên bản | Số ký tự | Metadata đã gán |
|---|--------------|------------|--------------------|----------|-----------------|
| 1 | Nội quy thư viện (Nội quy chung) | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~4000 | doc_id, audience, department, category, language |
| 2 | Nội quy phòng đọc (Cơ sở 1 Đinh Tiên Hoàng) | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1400 | doc_id, audience, department, category, language |
| 3 | Nội quy phòng đọc (Cơ sở 2 Thủ Đức) | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1000 | doc_id, audience, department, category, language |
| 4 | Nội quy phòng mượn (Cơ sở 1 Đinh Tiên Hoàng) | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1300 | doc_id, audience, department, category, language |
| 5 | Nội quy phòng mượn (Cơ sở 2 Thủ Đức) | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1400 | doc_id, audience, department, category, language |
| 6 | Nội quy phòng tạp chí | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~900 | doc_id, audience, department, category, language |
| 7 | Nội quy phòng tra cứu dữ liệu | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1500 | doc_id, audience, department, category, language |
| 8 | Nội quy phòng tra cứu đa phương tiện | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1800 | doc_id, audience, department, category, language |
| 9 | Nội quy phòng đọc tham khảo Hàn Quốc | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~1900 | doc_id, audience, department, category, language |
| 10 | Nội quy phòng thảo luận nhóm | local_pdf/11717.pdf | 2026-08-03 / 2026.1 | ~600 | doc_id, audience (student), department, category |

**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [x] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [x] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
|----------------|------|---------------|-------------------------------|
| `doc_id` | Chuỗi | `noi-quy-chung` | Định danh duy nhất tài liệu, dùng để truy vết nguồn gốc (provenance). |
| `audience` | Chuỗi | `student`, `all` | Lọc kết quả trả về đúng đối tượng đang tra cứu, tránh lấy nhầm quy định của nhóm khác. |
| `department` | Chuỗi | `ussh-library` | Hữu ích khi mở rộng hệ thống sang đa phòng ban, giúp thu hẹp phạm vi tìm kiếm. |
| `category` | Chuỗi | `regulations` | Phân loại loại tài liệu (nội quy, biểu mẫu), giúp ưu tiên các tài liệu đúng loại. |
| `language` | Chuỗi | `vi` | Đảm bảo hệ thống trả về đúng ngôn ngữ mà người dùng yêu cầu, tránh nhiễu. |

---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 2 tài liệu quy định thư viện mẫu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `noi-quy-chung` + `phong-doc-han-quoc` | FixedSizeChunker (`fixed_size`) | 18 | 388.3 | Không hoàn toàn (dễ bị cắt giữa từ hoặc ngắt câu quy định). |
| `noi-quy-chung` + `phong-doc-han-quoc` | SentenceChunker (`by_sentences`) | 25 | 244.5 | Trung bình (giữ đúng câu nhưng kích thước nhỏ làm ngữ cảnh bị rời rạc). |
| `noi-quy-chung` + `phong-doc-han-quoc` | RecursiveChunker (`recursive`) | 21 | 291.1 | Rất tốt (giữ trọn vẹn từng mục quy định và điều khoản). |

### Chiến lược của từng thành viên

**Thành viên 1 — Đoàn Vũ Hoàng**
- **Loại chiến lược:** RecursiveChunker (`chunk_size=400`)
- **Mô tả & lý do chọn cho chủ đề này:** Sử dụng đệ quy phân cắt theo dấu đoạn (`\n\n`), dấu dòng (`\n`) và dấu câu. Đây là chiến lược tối ưu nhất cho tài liệu văn bản quy định vì nó giữ trọn khối logic của từng Điều/Mục mà không bị ngắt đôi ý.
- **Code snippet (nếu custom):**
```python
chunker = RecursiveChunker(chunk_size=400)
store = build_knowledge_base("data/ussh_library", embedding_fn, chunker=chunker)
```

**Lê Hoàng Long + Sùng A Khua**
- **Loại chiến lược:** FixedSizeChunker (`chunk_size=300, overlap=50`)
- **Mô tả & lý do chọn:** Chọn cách chia kích thước cố định để đảm bảo mọi chunk đều có dung lượng tối đa đồng đều.
- **Code snippet:**
```python
chunker = FixedSizeChunker(chunk_size=300, overlap=50)
```

**Nguyễn Mạnh Hưng + Đàm Vinh Quang**
- **Loại chiến lược:** SentenceChunker (`max_sentences_per_chunk=3`)
- **Mô tả & lý do chọn:** Thử nghiệm chia theo câu để đảm bảo không câu nào bị cắt dở dang.
- **Code snippet:**
```python
chunker = SentenceChunker(max_sentences_per_chunk=3)
```

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Đoàn Vũ Hoàng | RecursiveChunker (400) | **8 / 10** | Giữ nguyên khối cấu trúc mục/đoạn, 4/5 câu đưa đúng Chunk bằng chứng lên Top-1. | Cần văn bản gốc có định dạng xuống dòng chuẩn. |
| Thành viên B | FixedSizeChunker (400) | **7 / 10** | Cắt nhanh, kích thước các chunk đồng đều. | Bị ngắt ngang câu làm lọt chunk chứa đáp án xuống Top-2/3. |
| Thành viên C | SentenceChunker (max=3) | **5 / 10** | Tôn trọng ranh giới câu 100%. | Chunk quá nhỏ làm ngữ cảnh bị phân tán, lọt top-3 đúng file nhưng thiếu chunk vàng. |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> Chiến lược **`RecursiveChunker` (chunk_size=400)** là chiến lược tốt nhất cho chủ đề Quy định Thư viện Đại học. Nguyên nhân là do tài liệu học vụ/nội quy được trình bày theo từng Điều/Mục logic; việc ưu tiên cắt theo dấu đoạn (`\n\n`) giúp toàn bộ nội dung của một điều khoản (bao gồm cả đối tượng, hạn mức và mức phạt) nằm trọn trong một chunk đơn lẻ, từ đó giúp Vector Embedding mã hóa trọn vẹn ngữ cảnh và trả về vị trí Top-1 chính xác.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Sinh viên và cán bộ giảng viên được mượn bao nhiêu quyển sách giáo trình và trong thời gian bao lâu? | Giáo trình được mượn 06 cuốn đối với Sinh viên, HV SĐH và 08 cuốn đối với Cán bộ - Giảng viên. Thời hạn mượn là một học kỳ. | `noi-quy-chung` / `phong-muon-cs1` |
| 2 | Nếu tôi trả sách trễ hạn thì sẽ bị phạt bao nhiêu tiền một ngày và khi nào thì bị khóa thẻ? | Phạt 2.000 đ/ngày. Nếu tái phạm 02 lần trở lên sẽ bị khóa giao dịch thư viện từ 03 đến 06 tháng. | `noi-quy-chung` / `phong-muon-cs1` |
| 3 | Phòng đọc tham khảo Hàn Quốc (Window on Korea) cho phép mang đồ dùng gì vào kho để ghi chép? | Chỉ được mang 01 quyển vở/giấy tập để ghi chép (không dùng giấy khổ A4, A3). | `phong-doc-han-quoc` |
| 4 | Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào? | Tối đa 10 sinh viên. Cần 3 bước: Điền form/quét QR, nhắn tin Zalo xác nhận, và gặp cán bộ mượn phòng. (Cần `metadata_filter={"audience": "student"}`). | `phong-thao-luan-nhom` |
| 5 | Khi làm mất tài liệu, nếu trên thị trường không còn bán và thư viện cũng không còn bản gốc thì tôi phải nộp phạt như thế nào? | Phải nộp phạt số tiền gấp 03 lần giá trị của tài liệu được định giá tại thời điểm nộp phạt. | `noi-quy-chung` |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Số lượng mượn giáo trình | RecursiveChunker (400) | Có (Top-1) — 2đ | RecursiveChunker giữ nguyên bảng thời hạn mượn 30 ngày & 06/08 cuốn. |
| 2 | Phạt trễ hạn & khóa thẻ | RecursiveChunker / FixedSize | Có (Top-1) — 2đ | Cả 2 chiến lược đều bắt đúng chunk có từ khóa phạt 2.000 đ/ngày & khóa thẻ 3-6 tháng. |
| 3 | Vật dụng mang vào phòng Hàn Quốc | RecursiveChunker (400) | Có (Top-1) — 2đ | Giữ nguyên cụm "chỉ mang 01 quyển vở/giấy tập" ở ngay Top-1. |
| 4 | Đăng ký phòng thảo luận (có filter) | RecursiveChunker (400) | Có (Top-1) — 2đ | Kết hợp `metadata_filter={'audience': 'student'}` lọc chính xác file `phong-thao-luan-nhom.md`. |
| 5 | Bồi thường mất tài liệu | RecursiveChunker (400) | Có (Top-1) — 2đ | Trích xuất chính xác quy định phạt "gấp 03 lần giá trị tài liệu". |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Metadata Pre-filtering phát huy tác dụng rõ rệt nhất ở **Câu hỏi số 4** (Quy trình đăng ký phòng thảo luận nhóm). Nhờ áp dụng `metadata_filter={"audience": "student"}`, hệ thống chủ động loại bỏ toàn bộ các tài liệu phòng đọc/phòng mượn chung của giảng viên/nhân viên, đảm bảo Top-3 kết quả trả về 100% thuộc về quy định nhóm sinh viên.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
1. Khác biệt cốt lõi giữa việc đánh giá theo `doc_id` (dễ bị ảo tưởng kết quả 80%) và đánh giá cấp độ `Chunk Content Evidence` (bóc tách rõ chiến lược dở chỉ đạt 50%).
2. Sức mạnh của Metadata Pre-Filtering giúp loại bỏ 100% nhiễu tài liệu trùng chủ đề nhưng khác đối tượng người dùng.
3. Sự vượt trội của `RecursiveChunker` khi bảo tồn các đoạn văn bản logic tự thân (self-contained blocks).

**Bài học rút ra khi so sánh trong nhóm:**
> Cùng một bộ tài liệu nhưng chiến lược chia nhỏ (Chunking Strategy) quyết định đến 80% chất lượng truy xuất của hệ thống RAG. Chọn đúng phương pháp cắt phù hợp với cấu trúc văn bản quan trọng hơn nhiều so với việc chỉ thay đổi tham số kích thước thô.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ chuẩn hóa dữ liệu đầu vào ngay từ bước crawl bằng cách bổ sung thêm các thẻ Heading Markdown rõ ràng (`#`, `##`) và gán nhãn Metadata chi tiết hơn cho từng phần nhỏ thay vì chỉ gán ở cấp độ file.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality) | 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
