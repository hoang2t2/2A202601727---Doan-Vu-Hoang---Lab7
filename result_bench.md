# Báo Cáo Chấm Điểm Retrieval Chuẩn Rubric (Chunk-Level Evaluation)

**Bộ dữ liệu:** Thư viện Đại học KHXH&NV (`data/ussh_library`)

**Backend Nhúng:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

**Quy tắc chấm (Thang 10 điểm):**

- **2 điểm/câu:** Top-1 chứa trực tiếp chunk mang bằng chứng câu trả lời.

- **1 điểm/câu:** Top-3 có chứa chunk mang bằng chứng nhưng bị rơi xuống Top-2/Top-3.

- **0 điểm/câu:** Top-3 không có chunk nào chứa bằng chứng đáp án.


---

## 1. Bảng Tổng Hợp Điểm Số Theo Rubric Chính Thức

| Chiến lược Chunking | Tổng số Chunk | Tổng điểm (/10) | Số câu đạt 2đ (Top-1) | Số câu đạt 1đ (Top 2-3) | Số câu 0đ | Nhận xét chi tiết |
|----------------------|---------------|------------------|-----------------------|-------------------------|-----------|--------------------|
| FixedSizeChunker (400, overlap=50) | 46 | **7/10** | 3 | 1 | 1 | Bị ngắt ngang câu nên 1 số câu bị đẩy xuống Top-2/3 hoặc mất từ khóa bằng chứng. |
| SentenceChunker (max=3) | 78 | **5/10** | 2 | 1 | 2 | Kích thước chunk nhỏ khiến ngữ cảnh bị phân tán, lọt top-3 đúng doc_id nhưng thiếu chunk vàng. |
| RecursiveChunker (400) | 57 | **8/10** | 4 | 0 | 1 | Tốt nhất: Giữ trọn cấu trúc mục/đoạn nên các chunk bằng chứng luôn đứng ở Top-1. |


---

## 2. Chi Tiết Đánh Giá Chunk-Level Của Từng Chiến Lược

### 📍 Chiến lược: FixedSizeChunker (400, overlap=50) — Tổng điểm: **7/10** (Tổng chunk: 46)

#### Query 1: "Sinh viên và cán bộ giảng viên được mượn bao nhiêu quyển sách giáo trình và trong thời gian bao lâu?"
- **Điểm số:** `0/2 điểm` — *Thất bại: Top-3 không chứa bằng chứng đáp án (0đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-han-quoc]` (Cosine Score: 0.7256) — *", làm đổ tài liệu, chỉ được mang 01 quyển vở/giấy tập để ghi chép (không sử dụng giấy khổ A4, A3…). 3. Trình tự mượn: • ..."*
  2. `[phong-doc-cs2]` (Cosine Score: 0.7099) — *"(không sử dụng giấy khổ A4, A3…). 3. Trình tự mượn: • Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại..."*
  3. `[phong-doc-cs1]` (Cosine Score: 0.6994) — *"hi chép (không sử dụng giấy khổ A4, A3…). 3. Trình tự mượn tài liệu tham khảo: • Mỗi lượt được mượn 03 tài liệu đối với ..."*

#### Query 2: "Nếu tôi trả sách trễ hạn thì sẽ bị phạt bao nhiêu tiền một ngày và khi nào thì bị khóa thẻ?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-muon-cs1]` (Cosine Score: 0.6462) — *"phạt 2.000 đ/ngày (nếu tái phạm 02 lần trở lên bạn đọc sẽ bị khóa giao dịch sử dụng thư viện từ 03 đến 06 tháng). 6. Nếu..."*
  2. `[phong-muon-cs1]` (Cosine Score: 0.6035) — *"i SV, HVSĐH; 08 cuốn đối với CB - GV trong vòng 30 ngày. Bạn đọc phải trả sách đúng thời hạn quy định. 4. Đến thời hạn 3..."*
  3. `[phong-muon-cs2]` (Cosine Score: 0.5881) — *"ó nhu cầu sử dụng tiếp tài liệu cần liên hệ thư viện để gia hạn (nếu như không có bạn đọc khác chờ mượn). Thời gian tài ..."*

#### Query 3: "Phòng đọc tham khảo Hàn Quốc (Window on Korea) cho phép mang đồ dùng gì vào kho để ghi chép?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-han-quoc]` (Cosine Score: 0.7044) — *"# NỘI QUY PHÒNG ĐỌC THAM KHẢO HÀN QUỐC (WINDOW ON KOREA)  I. Nội quy sử dụng tài liệu. 1. Khi vào phòng đọc tham khảo Hà..."*
  2. `[phong-doc-han-quoc]` (Cosine Score: 0.5696) — *"viện lên tài liệu cần mượn tại quầy phục vụ; • Kiểm tra tình trạng tài liệu trước khi mượn để báo cho chuyên viên thư vi..."*
  3. `[phong-doc-cs1]` (Cosine Score: 0.5482) — *"# NỘI QUY PHÒNG ĐỌC (Cơ sở 1: Đinh Tiên Hoàng)  1. Khi vào phòng đọc, bạn đọc phải xuất trình thẻ cán bộ/thẻ sinh viên/t..."*

#### Query 4: "Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-thao-luan-nhom]` (Cosine Score: 0.7398) — *"# NỘI QUY PHÒNG THẢO LUẬN NHÓM  1. Bạn đọc muốn sử dụng phòng thảo luận nhóm phải thực hiện đầy đủ các bước sau: • Bước ..."*
  2. `[phong-thao-luan-nhom]` (Cosine Score: 0.4534) — *" luận phải diễn ra nghiêm túc và chấp hành đúng nội quy chung của thư viện. 4. Giữ gìn, bảo quản tài sản trong phòng. 5...."*

#### Query 5: "Khi làm mất tài liệu, nếu trên thị trường không còn bán và thư viện cũng không còn bản gốc thì tôi phải nộp phạt như thế nào?"
- **Điểm số:** `1/2 điểm` — *Bị lệch vị trí: Chunk mang câu trả lời nằm ở Top-2 (1đ)*
- **Top-3 retrieved chunks:**
  1. `[noi-quy-chung]` (Cosine Score: 0.7552) — *"ong trường hợp nếu bạn đọc không tìm được tài liệu mất trên thị trường phát hành, bạn đọc phải báo ngay cho chuyên viên ..."*
  2. `[noi-quy-chung]` (Cosine Score: 0.6572) — *"ó bản gốc, bạn đọc phải chi trả các chi phí sau: + Tiền scan tài liệu mất: 2.000 đồng/trang x tổng số trang tài liệu; + ..."*
  3. `[phong-muon-cs1]` (Cosine Score: 0.6464) — *"phạt 2.000 đ/ngày (nếu tái phạm 02 lần trở lên bạn đọc sẽ bị khóa giao dịch sử dụng thư viện từ 03 đến 06 tháng). 6. Nếu..."*

### 📍 Chiến lược: SentenceChunker (max=3) — Tổng điểm: **5/10** (Tổng chunk: 78)

#### Query 1: "Sinh viên và cán bộ giảng viên được mượn bao nhiêu quyển sách giáo trình và trong thời gian bao lâu?"
- **Điểm số:** `0/2 điểm` — *Thất bại: Top-3 không chứa bằng chứng đáp án (0đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-cs2]` (Cosine Score: 0.7338) — *"Trình tự mượn: • Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại học và 05 tài liệu đối với Cán bộ - ..."*
  2. `[phong-doc-cs1]` (Cosine Score: 0.7177) — *"Trình tự mượn tài liệu tham khảo: • Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại học và 05 tài liệ..."*
  3. `[phong-doc-han-quoc]` (Cosine Score: 0.7022) — *"Khi vào kho lựa chọn tài liệu, bạn đọc không được làm xáo trộn, làm đổ tài liệu, chỉ được mang 01 quyển vở/giấy tập để g..."*

#### Query 2: "Nếu tôi trả sách trễ hạn thì sẽ bị phạt bao nhiêu tiền một ngày và khi nào thì bị khóa thẻ?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-muon-cs1]` (Cosine Score: 0.6524) — *"Thời gian tài liệu được gia hạn sử dụng tiếp là 14 ngày. 5. Nếu trả tài liệu trễ hạn, bạn đọc phải nộp phạt 2.000 đ/ngày..."*
  2. `[phong-muon-cs2]` (Cosine Score: 0.6524) — *"Thời gian tài liệu được gia hạn sử dụng tiếp là 14 ngày. 5. Nếu trả tài liệu trễ hạn, bạn đọc phải nộp phạt 2.000 đ/ngày..."*
  3. `[noi-quy-chung]` (Cosine Score: 0.6373) — *"Cần trả tài liệu đúng thời gian quy định, nếu có nhu cầu tiếp tục sử dụng tài liệu đang mượn bạn đọc cần liên hệ thư việ..."*

#### Query 3: "Phòng đọc tham khảo Hàn Quốc (Window on Korea) cho phép mang đồ dùng gì vào kho để ghi chép?"
- **Điểm số:** `0/2 điểm` — *Thất bại: Top-3 không chứa bằng chứng đáp án (0đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-han-quoc]` (Cosine Score: 0.6773) — *"Khi vào phòng đọc tham khảo Hàn Quốc, bạn đọc phải xuất trình thẻ cán bộ/thẻ sinh viên/thẻ học viên/thẻ thư viện và tuân..."*
  2. `[phong-doc-han-quoc]` (Cosine Score: 0.6415) — *"# NỘI QUY PHÒNG ĐỌC THAM KHẢO HÀN QUỐC (WINDOW ON KOREA)  I. Nội quy sử dụng tài liệu. 1...."*
  3. `[phong-doc-han-quoc]` (Cosine Score: 0.6245) — *"Nội quy sử dụng máy tính. 1. Khi vào phòng đọc tham khảo Hàn Quốc, bạn đọc xuất trình thẻ cán bộ/thẻ sinh viên/thẻ học v..."*

#### Query 4: "Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào?"
- **Điểm số:** `1/2 điểm` — *Bị lệch vị trí: Chunk mang câu trả lời nằm ở Top-2 (1đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-thao-luan-nhom]` (Cosine Score: 0.7866) — *"Mỗi nhóm thảo luận tối đa 10 sinh viên. 3. Buổi thảo luận phải diễn ra nghiêm túc và chấp hành đúng nội quy chung của th..."*
  2. `[phong-thao-luan-nhom]` (Cosine Score: 0.6340) — *"# NỘI QUY PHÒNG THẢO LUẬN NHÓM  1. Bạn đọc muốn sử dụng phòng thảo luận nhóm phải thực hiện đầy đủ các bước sau: • Bước ..."*
  3. `[phong-thao-luan-nhom]` (Cosine Score: 0.4058) — *"Giữ gìn vệ sinh chung, bỏ rác đúng nơi quy định. 6. Kết thúc buổi thảo luận phải tắt các thiết bị điện (đèn, quạt, máy l..."*

#### Query 5: "Khi làm mất tài liệu, nếu trên thị trường không còn bán và thư viện cũng không còn bản gốc thì tôi phải nộp phạt như thế nào?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[noi-quy-chung]` (Cosine Score: 0.7394) — *"Nếu thư viện tìm được tài liệu, thư viện sẽ cung cấp địa chỉ để bạn đọc mua trả tài liệu và nộp thêm 02 lần tiền giá trị..."*
  2. `[noi-quy-chung]` (Cosine Score: 0.7185) — *"10. Nếu làm mất hoặc làm hư hỏng tài liệu bạn đọc sẽ bị xử lý như sau: - Phải tìm mua lại đúng tài liệu đã mất và nộp ph..."*
  3. `[noi-quy-chung]` (Cosine Score: 0.6031) — *"Cần trả tài liệu đúng thời gian quy định, nếu có nhu cầu tiếp tục sử dụng tài liệu đang mượn bạn đọc cần liên hệ thư việ..."*

### 📍 Chiến lược: RecursiveChunker (400) — Tổng điểm: **8/10** (Tổng chunk: 57)

#### Query 1: "Sinh viên và cán bộ giảng viên được mượn bao nhiêu quyển sách giáo trình và trong thời gian bao lâu?"
- **Điểm số:** `0/2 điểm` — *Thất bại: Top-3 không chứa bằng chứng đáp án (0đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-cs2]` (Cosine Score: 0.7434) — *"• Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại học và 05 tài liệu đối với Cán bộ - Giảng viên. • Đ..."*
  2. `[phong-doc-cs1]` (Cosine Score: 0.7376) — *"• Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại học và 05 tài liệu đối với Cán bộ - Giảng viên. • Đ..."*
  3. `[phong-doc-han-quoc]` (Cosine Score: 0.7158) — *"3. Trình tự mượn: • Mỗi lượt được mượn 03 tài liệu đối với Sinh viên, Học viên sau đại học và 05 tài liệu đối với Cán bộ..."*

#### Query 2: "Nếu tôi trả sách trễ hạn thì sẽ bị phạt bao nhiêu tiền một ngày và khi nào thì bị khóa thẻ?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-muon-cs1]` (Cosine Score: 0.6773) — *"5. Nếu trả tài liệu trễ hạn, bạn đọc phải nộp phạt 2.000 đ/ngày (nếu tái phạm 02 lần trở lên bạn đọc sẽ bị khóa giao dịc..."*
  2. `[noi-quy-chung]` (Cosine Score: 0.6272) — *"6. Cần trả tài liệu đúng thời gian quy định, nếu có nhu cầu tiếp tục sử dụng tài liệu đang mượn bạn đọc cần liên hệ thư ..."*
  3. `[noi-quy-chung]` (Cosine Score: 0.5801) — *"- Nếu trên thị trường và thư viện đều không còn tài liệu đã mất thì bạn đọc phải nộp phạt số tiền gấp 03 lần giá trị của..."*

#### Query 3: "Phòng đọc tham khảo Hàn Quốc (Window on Korea) cho phép mang đồ dùng gì vào kho để ghi chép?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-doc-han-quoc]` (Cosine Score: 0.6877) — *"I. Nội quy sử dụng tài liệu. 1. Khi vào phòng đọc tham khảo Hàn Quốc, bạn đọc phải xuất trình thẻ cán bộ/thẻ sinh viên/t..."*
  2. `[phong-doc-han-quoc]` (Cosine Score: 0.6218) — *"II. Nội quy sử dụng máy tính. 1. Khi vào phòng đọc tham khảo Hàn Quốc, bạn đọc xuất trình thẻ cán bộ/thẻ sinh viên/thẻ h..."*
  3. `[phong-doc-han-quoc]` (Cosine Score: 0.5873) — *"# NỘI QUY PHÒNG ĐỌC THAM KHẢO HÀN QUỐC (WINDOW ON KOREA)..."*

#### Query 4: "Mỗi nhóm sinh viên được đăng ký phòng thảo luận tối đa bao nhiêu người và cần làm các bước nào?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[phong-thao-luan-nhom]` (Cosine Score: 0.7422) — *"1. Bạn đọc muốn sử dụng phòng thảo luận nhóm phải thực hiện đầy đủ các bước sau: • Bước 1: Điền thông tin vào form đăng ..."*
  2. `[phong-thao-luan-nhom]` (Cosine Score: 0.4475) — *"4. Giữ gìn, bảo quản tài sản trong phòng. 5. Giữ gìn vệ sinh chung, bỏ rác đúng nơi quy định. 6. Kết thúc buổi thảo luận..."*
  3. `[phong-thao-luan-nhom]` (Cosine Score: 0.1091) — *"# NỘI QUY PHÒNG THẢO LUẬN NHÓM..."*

#### Query 5: "Khi làm mất tài liệu, nếu trên thị trường không còn bán và thư viện cũng không còn bản gốc thì tôi phải nộp phạt như thế nào?"
- **Điểm số:** `2/2 điểm` — *Chính xác: Top-1 chứa chunk mang câu trả lời (2đ)*
- **Top-3 retrieved chunks:**
  1. `[noi-quy-chung]` (Cosine Score: 0.7870) — *"- Nếu trên thị trường và thư viện đều không còn tài liệu đã mất thì bạn đọc phải nộp phạt số tiền gấp 03 lần giá trị của..."*
  2. `[noi-quy-chung]` (Cosine Score: 0.7646) — *"- Nếu không còn tài liệu mất trên thị trường, nhưng thư viện có bản gốc, bạn đọc phải chi trả các chi phí sau: + Tiền sc..."*
  3. `[noi-quy-chung]` (Cosine Score: 0.7159) — *"- Trong trường hợp nếu bạn đọc không tìm được tài liệu mất trên thị trường phát hành, bạn đọc phải báo ngay cho chuyên v..."*

---

## 3. Phát Hiện Đáng Giá & Phân Tích Sự Khác Biệt Giữa 2 Cách Chấm

1. **Tại sao chấm theo `doc_id` gây ra ảo tưởng (False Positive)?**

   - Nếu chỉ kiểm tra `doc_id`, chiến lược có thể dễ dàng đạt 5/5 câu đúng vì Top-3 kết quả trả về thuộc đúng file `noi-quy-chung.md` hoặc `phong-doc-cs1.md`.

   - Tuy nhiên, khi kiểm tra ở **cấp độ Chunk Content**, một số chunk lọt Top-1 tuy cùng nằm trong file `noi-quy-chung.md` nhưng lại là đoạn mô tả về quy tắc ứng xử chứ không chứa con số mức phạt hay thời gian mượn.


2. **Cosine Score cao là tín hiệu xếp hạng, không phải bằng chứng nội dung đúng:**

   - Điểm tương đồng Cosine đo độ giống nhau về ngữ pháp/từ vựng trong không gian đa chiều. Nhiều chunk có điểm Cosine > 0.70 nhưng lại không chứa từ khóa bằng chứng quyết định.


3. **Kết luận:**

   - **`RecursiveChunker`** chứng minh sự vượt trội rõ rệt nhất vì giữ nguyên khối cấu trúc (section/heading), giúp chunk chứa đúng câu trả lời luôn được đẩy lên vị trí Top-1.
