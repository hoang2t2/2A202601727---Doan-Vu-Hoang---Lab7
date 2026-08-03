# Kịch Bản Thuyết Trình Demo (Nhóm 404NotFound)

## 1. Giới thiệu phạm vi, nguồn và metadata schema (1 phút)
*(Người nói: Thành viên 1)*
- Xin chào thầy và các bạn, nhóm mình là 404NotFound. Hôm nay nhóm xin trình bày về bài Lab 7: Embedding & Vector Store.
- **Phạm vi tài liệu:** Nhóm chọn phạm vi là Nội quy sử dụng thư viện của ĐH KHXH&NV, bao gồm các quy định ở các phòng chức năng (phòng đọc, phòng mượn, phòng đa phương tiện, v.v.).
- **Nguồn dữ liệu:** Dữ liệu được trích xuất từ 1 file PDF gốc (Nội quy thư viện), chia thành 10 file Markdown riêng biệt.
- **Metadata Schema:** Từng file được gán các metadata cực kỳ chi tiết. Ngoài `doc_id`, `source_url`, `retrieved_at` bắt buộc, nhóm thiết kế thêm trường `audience` (đối tượng: student, staff, all) để phân loại đúng nội quy theo người dùng, `department` (ussh-library) để gom nhóm phòng ban, và `category` (regulations).

## 2. Mỗi thành viên giải thích strategy của mình (2 phút)
*(Người nói: Lần lượt từng thành viên)*
- **Hoàng (RecursiveChunker - 400 chars):** Chiến lược của mình là phân tách đệ quy ưu tiên cắt theo đoạn văn (`\n\n`), câu và từ. Phù hợp nhất cho văn bản quy định học vụ vì nó không bẻ gãy cấu trúc logic của từng "Điều", "Khoản", giúp vector bắt được toàn bộ bối cảnh của điều khoản đó.
- **Thành viên B (FixedSizeChunker - 400 chars, overlap 50):** Mình dùng kích thước cố định để tất cả các chunk có dung lượng đồng đều, tốc độ nhúng nhanh. Tuy nhiên thỉnh thoảng nó cắt đôi một câu quan trọng, làm giảm nhẹ độ chính xác ở một số truy vấn.
- **Thành viên C (SentenceChunker - 3 câu/chunk):** Mình chia tuyệt đối theo câu để đảm bảo ngữ pháp. Tuy nhiên, nội quy thư viện có những điều khoản trải dài trên nhiều câu ngắn (ví dụ danh sách gạch đầu dòng), khiến ngữ cảnh bị xé vụn và lọt khỏi top 3.

## 3. So sánh kết quả chi tiết 3 chiến lược & Failure Case (3 phút)
*(Người nói: Hoàng hoặc Thành viên tổng hợp)*

- Dưới đây là bảng tổng hợp khi chạy `ChunkingStrategyComparator` và Benchmark trên 5 câu hỏi truy xuất:

| Chiến lược | Đặc điểm cắt | Số lượng Chunk | Độ dài TB | Điểm Benchmark | Đánh giá |
|:---|:---|:---:|:---:|:---:|:---|
| **Recursive** | Đệ quy theo đoạn/câu | 21 | 291.1 | **8/10** | Giữ trọn vẹn ngữ cảnh điều khoản, chính xác nhất. |
| **FixedSize** | Cố định 400 chars | 18 | 388.3 | **7/10** | Đồng đều nhưng dễ ngắt đôi câu/ý quan trọng. |
| **Sentence** | Theo câu (max 3) | 25 | 244.5 | **5/10** | Ngữ cảnh bị xé vụn, lọt top-3 nhưng thiếu ý. |

- Nhìn vào bảng, **RecursiveChunker** chiến thắng tuyệt đối nhờ việc tôn trọng cấu trúc văn bản gốc thay vì ép kích thước cứng nhắc.
- **Phân tích A/B Metadata Filter:** Hãy xem câu hỏi: *"Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người?"*.
  - *Không có Filter:* Hệ thống có thể lôi lên các quy định sử dụng phòng khác của Giảng viên (khác số người và quy trình) do độ tương đồng từ vựng "đăng ký, phòng" rất cao.
  - *Có Filter (`audience: student`):* Cơ chế Pre-filtering đã chủ động lọc và gạt bỏ hoàn toàn các file không dành cho sinh viên TRƯỚC KHI tính Cosine Similarity. Kết quả là Top-1 trả về chuẩn xác file nội quy phòng thảo luận nhóm của sinh viên.
- **Failure Case (Trường hợp thất bại của SentenceChunker):** Ở câu hỏi *"Trả sách trễ hạn bị phạt bao nhiêu tiền?"*, chiến lược chia câu (SentenceChunker) cắt quy định phạt tiền thành 1 câu ở một chunk, và hậu quả khóa thẻ ở 1 câu khác thuộc chunk khác. Do đó, hệ thống chỉ lấy được 1 nửa thông tin, khiến LLM trả lời thiếu ý, bị trừ 1 điểm.

## 4. Chạy Live Demo Tích Hợp (1-2 phút)
*(Người nói: Thành viên Demo chạy code trên Terminal)*

**Phần 4A: Demo 3 Chiến Lược (run_all_benchmarks.py)**
- Nhóm đã chuẩn bị script để đánh giá tự động trên cả 3 chiến lược cùng lúc để mọi người có cái nhìn trực quan.
- *(Mở Terminal)* Chạy lệnh: `.venv\Scripts\python.exe run_all_benchmarks.py`
- Màn hình sẽ log ra kết quả truy xuất (FixedSize, Sentence, Recursive).
- Chỉ vào kết quả để nhấn mạnh sự khác biệt: "Ở câu hỏi X, trong khi Sentence trả về sai, thì Recursive lại gọi ra Top-1 đúng ngữ cảnh."

**Phần 4B: Demo Sức Mạnh Của Metadata Filter (demo_filter.py)**
- Tiếp theo, để chứng minh sức mạnh của việc giảm nhiễu, nhóm sẽ chạy 1 truy vấn A/B test trực tiếp.
- *(Mở Terminal)* Chạy lệnh: `.venv\Scripts\python.exe demo_filter.py`
- Màn hình sẽ in ra Top-3 chunk khi **không dùng Filter** (bị lẫn quy định các phòng chung) và khi **có dùng Filter** (`audience=student`). Kết quả có Filter đưa đúng chuẩn xác file phòng thảo luận nhóm lên Top 1!

---

## 5. Trả lời Hỏi Đáp (Q&A Chuẩn Bị Trước)

> **Lưu ý cho nhóm:** Các câu hỏi này dùng để trả lời khi giảng viên hoặc nhóm khác phản biện.

**Q1: Chiến lược chunking nào có thể tái sử dụng (reuse) khi đổi domain (lĩnh vực dữ liệu) khác? Tại sao?**
- **Trả lời:** `RecursiveChunker` là chiến lược linh hoạt và an toàn nhất để tái sử dụng cho các domain khác (như y tế, luật pháp, báo chí). Nguyên nhân là vì nó tuân theo **cấu trúc ngữ nghĩa trình bày tự nhiên** của con người (đoạn văn -> dòng -> câu -> từ). Dù từ vựng domain có thay đổi thế nào, ngữ pháp phân tách đoạn vẫn không đổi, giúp bảo tồn trọn vẹn cụm ý nghĩa tự thân (self-contained logic) mà không cần phải hard-code lại các dấu phân cách chuyên biệt. 

**Q2: Metadata filter giúp giảm nhiễu ở đâu trong không gian vector?**
- **Trả lời:** Filter giảm nhiễu lớn nhất ở các khu vực tập trung dữ liệu **"Đồng âm / Đồng chủ đề nhưng khác bối cảnh (Context)"**. Ví dụ: Cùng là "chính sách bồi thường" nhưng của sinh viên khác giảng viên, của cơ sở 1 khác cơ sở 2. Embedding rất dễ bị đánh lừa bởi bề mặt từ vựng giống nhau ở hai tài liệu này. Lọc metadata bằng thuật toán **Pre-filtering** sẽ trực tiếp thu hẹp không gian tìm kiếm, loại bỏ các vector khác bối cảnh trước khi so sánh khoảng cách Cosine, giúp top-k hoàn toàn là các chunk hợp lệ.

**Q3: Đánh đổi (Trade-off) của Metadata Filter đối với độ phủ (Recall) như thế nào?**
- **Trả lời:** Khi áp dụng filter, chúng ta đang đánh đổi **Recall (Độ phủ)** để tối ưu **Precision (Độ chính xác)**. Nếu bộ lọc quá khắt khe hoặc việc gán nhãn dữ liệu có sai sót (ví dụ file đó áp dụng cho mọi người nhưng người dán nhãn quên thêm thẻ `audience: student`), Pre-filtering sẽ loại bỏ phăng file đó ra khỏi tầm ngắm. Kết quả là hệ thống trả về 0 tài liệu liên quan (Recall = 0) dù thực tế câu trả lời nằm ở đó. Để khắc phục sự đánh đổi này, hệ thống cần được thiết kế metadata có các giá trị fallback (như `audience: all`) hoặc cơ chế nới lỏng filter nếu kết quả rỗng.
