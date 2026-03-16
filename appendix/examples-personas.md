# Ví Dụ Thực Tế Theo Persona

> Tailored use cases cho từng người học — cùng công cụ, khác cách dùng.

---

## 👷 Anh Sơn — Thiết Kế Nội Thất

### Tổng quan công cụ

| Công cụ | Use Case | Level |
|---------|----------|-------|
| **Gemini (Gem)** | Tạo "Interior Design Consultant" — paste ảnh phòng → AI suggest bố trí, vật liệu, bảng màu | 1 |
| **Gemini + Vision** | Upload ảnh công trình → phân tích ánh sáng, tỷ lệ, suggest cải thiện | 1 |
| **Gemini + Imagen** | Từ brief text → generate hình render nội thất preview cho khách trước khi làm 3D | 1 |
| **Google AI Studio** | Test prompt pipeline: brief → concept → vật liệu → giá. So sánh Flash vs Pro | 2 |
| **AI Studio (Structured)** | Input brief → Output JSON: `{style, palette, materials[], furniture[], budget}` | 2 |
| **NotebookLM** | Upload catalog vật liệu + bảng giá → chatbot tra cứu nhanh, tạo podcast overview | 1 |
| **Flow / Automation** | Brief khách → AI tạo concept → estimate budget → gửi email proposal tự động | 2 |
| **Antigravity** | Build website portfolio dự án — gallery, landing page, contact form | 3 |
| **Nano (On-device)** | Đi khảo sát → chụp ảnh → AI nhận diện vật liệu, gợi ý sửa chữa tại chỗ (offline) | 1 |

---

### Gem mẫu: Interior Design Consultant

```
# Role
Bạn là cố vấn thiết kế nội thất với 15 năm kinh nghiệm tại Việt Nam.

# Expertise
- Phong cách: minimalist, Scandinavian, industrial, Japandi, indochine
- Thị trường: Việt Nam (vật liệu nội địa + nhập khẩu)
- Budget range: 200tr - 2 tỷ VND

# Rules
- Luôn hỏi diện tích phòng + ngân sách TRƯỚC khi suggest
- Ưu tiên vật liệu có sẵn tại VN
- Mỗi suggestion kèm giá tham khảo (VND)
- Format: Mood → Vật liệu → Nội thất → Ánh sáng → Budget
- Khi nhận ảnh: phân tích điểm mạnh/yếu → suggest 3 phương án

# Examples
Input: "Phòng khách 30m², budget 150tr, thích minimalist"
Output:
🎨 Mood: Warm minimalist — tone trắng kem + gỗ sồi tự nhiên
🧱 Vật liệu: Sàn gỗ SPC (35tr) + Sơn Dulux trắng ngà (5tr)
🪑 Nội thất: Sofa L 2m4 (25tr) + Bàn trà gỗ (8tr) + Kệ TV (15tr)
💡 Ánh sáng: Downlight âm trần 4000K (12tr) + Đèn sàn accent (3tr)
💰 Tổng estimate: ~103tr (còn 47tr buffer cho decor + rèm)
```

---

### Workflow mẫu: /proposal

```
---
description: Tạo proposal thiết kế nội thất từ brief khách hàng
---

# /proposal — Interior Design Proposal

## Step 1: Analyze Brief
Đọc brief khách → Extract: diện tích, phong cách, budget, timeline, yêu cầu đặc biệt.

## Step 2: Mood & Concept
Tạo concept board text: palette màu, vật liệu chính, mood keywords, inspiration references.

## Step 3: Space Planning
Suggest bố trí không gian → danh sách đồ nội thất + kích thước + vị trí.

## Step 4: Budget Breakdown
Chia budget: Vật liệu 40% · Nội thất 35% · Thi công 20% · Buffer 5%.

## Step 5: Generate Proposal
Tổng hợp thành proposal Markdown → chuyển PDF gửi khách.
```

---

### Use Cases chi tiết

#### 1. Gemini: Phân tích ảnh phòng (Level 1)

**Prompt:**
> Phân tích ảnh phòng khách này. Cho biết:
> 1. Diện tích ước tính
> 2. Ánh sáng tự nhiên (tốt/trung bình/yếu)
> 3. Điểm mạnh cần giữ
> 4. Điểm yếu cần cải thiện
> 5. 3 phương án thiết kế (budget thấp/trung/cao)

**Kết quả:** AI cho ra phân tích chuyên nghiệp, tiết kiệm 30-60 phút khảo sát ban đầu.

#### 2. AI Studio: Structured Output (Level 2)

**System prompt:**
> Bạn là Interior Design AI. Nhận brief khách hàng, output JSON.

**Output format:**
```json
{
  "style": "Japandi",
  "colorPalette": ["#F5F0EB", "#2C2C2C", "#8B7355"],
  "materials": [
    {"name": "Sàn gỗ sồi", "supplier": "An Cường", "pricePerM2": 450000}
  ],
  "furniture": [
    {"item": "Sofa 3 chỗ", "brand": "JYSK", "price": 15000000}
  ],
  "totalEstimate": 120000000,
  "timeline": "6-8 tuần"
}
```

**Ứng dụng:** Copy JSON → paste vào spreadsheet quotation → gửi khách. Chuẩn hóa quy trình.

#### 3. Imagen: Render preview (Level 1)

**Prompt:**
> Modern minimalist living room, 30sqm, white oak flooring, cream walls,
> L-shaped grey sofa, round wooden coffee table, track lighting 4000K,
> large window with sheer curtains, Vietnamese tropical plants,
> photorealistic interior photography, natural daylight

**Ứng dụng:** Khách xem preview nhanh trước khi invest vào 3D render chi tiết. Tiết kiệm 1-2 ngày + chi phí render.

#### 4. NotebookLM: Tra cứu vật liệu (Level 1)

**Upload:** Catalog An Cường 2026 (PDF) + Bảng giá nội thất (Excel) + Sổ tay thi công

**Hỏi:** "Sàn gỗ nào phù hợp phòng tắm, budget dưới 500k/m²?"

**Kết quả:** AI tra trong catalog → suggest đúng mã sản phẩm + giá + specs kỹ thuật.

#### 5. Flow: Automation proposal (Level 2)

**Pipeline tự động:**
```
Khách gửi brief (Google Form)
    │
    ▼
AI đọc brief → tạo concept text
    │
    ▼
Generate moodboard (Imagen)
    │
    ▼
Estimate budget (Structured Output)
    │
    ▼
Compile proposal (Google Docs)
    │
    ▼
Email cho khách (Gmail) + Notify Sơn (Telegram)
```

**Tiết kiệm:** Từ 3-4 giờ manual → 15 phút review + gửi.

---

## 🐶 Cún — Sinh Viên Học AI

### Tổng quan công cụ

| Công cụ | Use Case | Level |
|---------|----------|-------|
| **Gemini (Gem)** | Tạo "AI Tutor" — Socratic method, hỏi ngược thay vì cho đáp án thẳng | 1 |
| **Gemini + PDF** | Upload paper → tóm tắt: Problem → Method → Results → Limitations | 1 |
| **Gemini + Code** | Paste Python code → AI explain, debug, suggest optimization | 1 |
| **Google AI Studio** | Playground: test temperature, top-k, top-p → hiểu cách model hoạt động | 1 |
| **AI Studio (API)** | Build mini chatbot RAG từ ghi chú bài giảng — project thực hành | 2 |
| **NotebookLM** | Upload bài giảng + textbook → tạo podcast 2 người thảo luận → nghe khi đi bus | 1 |
| **Antigravity** | Build portfolio website showcase project ML/AI. Agent system cho research workflow | 3 |
| **Nano (On-device)** | Chụp whiteboard tại lớp → AI OCR + restructure thành notes đẹp | 1 |
| **Flow / Automation** | ArXiv paper mới về topic → AI tóm tắt → gửi Telegram notification | 2 |

---

### Gem mẫu: AI Tutor (Socratic)

```
# Role
Bạn là tutor AI/ML theo phương pháp Socratic — KHÔNG cho đáp án thẳng.

# Teaching Style
- Luôn hỏi ngược: "Bạn hiểu concept này thế nào trước khi mình giải thích?"
- Dùng analogy đời thường:
  - Neural network = hệ thống đường giao thông
  - Gradient descent = lăn bi xuống đồi
  - Overfitting = học thuộc đề cũ mà không hiểu bài
- Chia concept phức tạp thành 3 bước đơn giản
- Khi student stuck → cho hint, KHÔNG cho solution

# Format
- Explanation: Max 5 câu, dùng bullet point
- Code: Kèm comment giải thích từng dòng quan trọng
- Math: LaTeX + giải thích bằng lời
- Luôn kết thúc bằng 1 câu hỏi kiểm tra hiểu biết

# Subjects
Machine Learning, Deep Learning, NLP, Computer Vision, Statistics, Python

# Anti-patterns
- KHÔNG viết code hoàn chỉnh cho bài tập (chỉ pseudocode + hints)
- KHÔNG dùng jargon không giải thích
- KHÔNG nói "đơn giản thôi" khi student đang struggle
```

---

### Workflow mẫu: /paper-review

```
---
description: Review và tóm tắt paper nghiên cứu AI/ML
---

# /paper-review — AI Paper Review

## Step 1: Extract Structure
Đọc paper → Tách: Title, Authors, Year, Venue, Abstract, Key Terms.

## Step 2: Summarize (5 bullets)
1. Problem — Bài toán gì?
2. Method — Giải quyết bằng cách nào?
3. Key Innovation — Cái mới so với trước?
4. Results — Kết quả ra sao? (metrics cụ thể)
5. Limitations — Hạn chế gì?

## Step 3: Connect
Link đến related papers/concepts đã học. "Paper này build on top of [X]".

## Step 4: Quiz
Tạo 3 câu hỏi tự kiểm tra:
- 1 câu factual (nhớ)
- 1 câu conceptual (hiểu)
- 1 câu application (áp dụng)

## Step 5: Note
Output: 1 trang note Markdown → lưu vào thư mục research/[year]/
```

---

### Use Cases chi tiết

#### 1. Gemini: Explain complex concept (Level 1)

**Prompt:**
> Giải thích Transformer attention mechanism cho người mới.
> Dùng analogy đời thường.
> Sau khi giải thích, cho 1 ví dụ bằng Python pseudocode.

**Kết quả:** AI giải thích bằng analogy "đọc sách và highlight" — attention = quyết định từ nào quan trọng nhất trong câu, giống cách mình highlight textbook.

#### 2. AI Studio: So sánh model (Level 1)

**Bài tập tự thực hành:**
```
1. Mở AI Studio → chọn cùng 1 prompt
2. Test với:
   - Gemini Flash (nhanh, rẻ)
   - Gemini Pro (chính xác hơn)
3. Thay đổi temperature: 0.0 → 0.5 → 1.0 → 2.0
4. Quan sát: output khác nhau thế nào?
5. Kết luận: khi nào dùng Flash vs Pro? Temperature nào cho task nào?
```

**Học được:** Hiểu trực quan về model parameters thay vì chỉ đọc lý thuyết.

#### 3. NotebookLM: Passive learning (Level 1)

**Upload:**
- Slide bài giảng Deep Learning (PDF)
- Chapter 6 textbook Goodfellow (PDF)
- Ghi chú tay đã scan (ảnh)

**Output:** Podcast 15 phút — 2 "người" thảo luận về Backpropagation bằng tiếng Việt.

**Nghe khi:** Đi bus, tập gym, nấu ăn = review bài không cần ngồi bàn.

#### 4. AI Studio API: Build mini RAG (Level 2)

**Project thực hành:**
```python
# Upload ghi chú bài giảng → chatbot trả lời dựa trên nội dung

import google.generativeai as genai

# 1. Load ghi chú bài giảng
notes = load_documents("notes/deep-learning/")

# 2. Tạo embeddings
embeddings = genai.embed_content(notes)

# 3. Khi hỏi → tìm chunk liên quan → trả lời
def ask(question):
    relevant = search(embeddings, question)
    return genai.generate(
        context=relevant,
        prompt=question
    )

# 4. Test
ask("Backpropagation hoạt động thế nào?")
# → AI trả lời DỰA TRÊN ghi chú của mình, không hallucinate
```

**Học được:** RAG pipeline thực tế, embeddings, similarity search — đều là skill hot trên thị trường.

#### 5. Antigravity: Research Agent (Level 3)

**Agent system cho nghiên cứu:**
```
.research-agent/
├── GEMINI.md              # Rules: academic rigor, citation format
├── agents/
│   ├── paper-reader.md    # Đọc + tóm tắt paper
│   ├── code-reviewer.md   # Review implementation
│   └── writer.md          # Viết report/thesis section
├── skills/
│   ├── ml-concepts/       # Kiến thức ML cơ bản
│   ├── pytorch/           # PyTorch patterns
│   └── academic-writing/  # Cách viết academic
└── workflows/
    ├── paper-review.md    # /paper-review
    └── experiment.md      # /experiment → setup → run → log → analyze
```

**Ứng dụng:** Mỗi khi đọc paper mới → `/paper-review` → AI tóm tắt + quiz + lưu note. Sau 1 học kỳ tích lũy được knowledge base cá nhân.

---

## 📊 So Sánh 2 Persona

| Chiều | Anh Sơn (Nội thất) | Cún (SV AI) |
|-------|--------------------|----|
| **Mục tiêu** | Tăng tốc proposal + impress khách | Học sâu + build portfolio |
| **Gem chính** | Interior Consultant | AI Tutor (Socratic) |
| **AI Studio** | Structured output: brief → quote | Playground: hiểu model behavior |
| **Vision/Imagen** | Render preview, phân tích phòng | OCR whiteboard, diagram analysis |
| **NotebookLM** | Tra cứu catalog vật liệu | Podcast bài giảng = passive learning |
| **Antigravity** | Website portfolio + auto proposal | Research agent + project coding |
| **Nano** | Nhận diện vật liệu tại công trình | OCR ghi bảng tại lớp |
| **Level focus** | Level 1 + 2 (practical tools) | Level 1 + 2 + 3 (build systems) |
| **ROI rõ nhất** | Tiết kiệm 3-4h/proposal | Học nhanh 2-3x, portfolio sẵn sàng |
