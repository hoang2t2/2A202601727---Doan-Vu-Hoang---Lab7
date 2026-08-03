# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** [Tên nhóm]
**Thành viên:** [Họ tên từng thành viên]
**Ngày:** [Ngày nộp]

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

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| | FixedSizeChunker (`fixed_size`) | | | |
| | SentenceChunker (`by_sentences`) | | | |
| | RecursiveChunker (`recursive`) | | | |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — [Tên]**
- **Loại chiến lược:** [FixedSize / Sentence / Recursive / custom]
- **Mô tả & lý do chọn cho chủ đề này:** *(2-3 câu)*
- **Code snippet (nếu custom):**
```python
# Dán mã nguồn (implementation) vào đây
```

**Thành viên 2 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

**Thành viên 3 — [Tên]**
- **Loại chiến lược:**
- **Mô tả & lý do chọn:**
- **Code snippet (nếu custom):**

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| | | | | |
| | | | | |
| | | | | |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> *Viết 2-3 câu — đây là phần được đánh giá cao nhất (khả năng suy nghĩ & giải thích):*

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
> *Liệt kê 2-3 ý:*

**Bài học rút ra khi so sánh trong nhóm:**
> *Viết 2-3 câu — cùng tài liệu nhưng chiến lược khác nhau dẫn tới khác biệt gì?*

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Set Quality) | / 10 |
| Thiết kế chiến lược (Strategy Design) | / 15 |
| Chất lượng truy xuất (Retrieval Quality) | / 10 |
| Thuyết trình (Demo) | / 5 |
| **Tổng phần nhóm** | **/ 40** |
