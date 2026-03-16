#!/usr/bin/env python3
"""
Generate TTS narration audio for each workshop session using Gemini Native Audio.

Usage:
    export GEMINI_API_KEY="your-key"
    python generate_tts.py

Requires: pip install google-genai
"""

import os
import sys
import struct
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ pip install google-genai")
    sys.exit(1)

# Config
OUTPUT_DIR = Path(__file__).parent.parent / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-2.5-flash-preview-tts"

# Narration scripts — Vietnamese
NARRATIONS = {
    "session-1.1-context-engineering": """
Chào bạn! Đây là phần hướng dẫn audio cho session 1.1 của workshop AI Agent Mastery.

Trong session này, chúng ta sẽ nói về Context Engineering — tại sao context quan trọng hơn model.

Có một công thức quan trọng bạn cần nhớ: Output Quality bằng Model nhân với Context nhân với Constraints.
Cùng một model, nhưng nếu không có context, chất lượng chỉ đạt khoảng 40%.
Nếu bạn viết prompt tốt, lên được 60%.
Nếu dùng system instructions, 75%.
Và nếu có agent system hoàn chỉnh, có thể đạt trên 90%.

Hai nguyên lý cốt lõi bạn cần nắm:
Thứ nhất, Context Window giống như bộ nhớ tạm. AI không nhớ gì ngoài cuộc hội thoại hiện tại. Custom instructions giúp nhồi context trước mỗi câu hỏi.
Thứ hai, Constraints quan trọng hơn Freedom. AI cho output tốt hơn nhiều khi bạn giới hạn rõ ràng: tone, format, độ dài, audience.

Bài tập: Hãy chọn 1 task bạn hay dùng AI, liệt kê context đang có và context đang thiếu, rồi viết lại prompt.
""",
    "session-1.2-gemini-gems": """
Trong session 1.2, chúng ta sẽ tìm hiểu về Gemini Gems.

Gem là gì? Đơn giản, Gem là một version Gemini đã được customize với system instructions cố định. Khi bạn dùng Gem, AI luôn tuân theo instructions đó mà không cần bạn nhắc lại mỗi lần.

Concept này giống nhau trên mọi platform: Gemini gọi là Gem, ChatGPT gọi là Custom GPT, Claude gọi là Project. Hiểu một cái là dùng được tất cả.

Để tạo Gem hiệu quả, bạn cần 4 phần: Role, Brand Voice, Format Rules, và quan trọng nhất là Examples. Few-shot examples là yếu tố quyết định chất lượng lớn nhất. AI bắt chước style từ examples tốt hơn bất kỳ instruction nào.

Một số Gem hữu ích bạn nên tạo: Meeting Summarizer, Code Reviewer, Email Drafter, Data Analyzer, và Learning Coach.

Bài tập: Hãy tạo Gem đầu tiên của bạn theo template, test với 3 câu hỏi, và so sánh kết quả với Gemini thường.
""",
    "session-1.3-prompt-patterns": """
Session 1.3 — 5 Prompt Patterns quan trọng nhất.

Pattern 1: Role, Task, Constraints, Format. Đây là nền tảng. Role giúp AI hiểu vai trò, Task là nhiệm vụ cụ thể, Constraints giới hạn phạm vi, Format quy định output.

Pattern 2: Chain of Thought. Bắt AI suy nghĩ từng bước thay vì nhảy thẳng sang kết luận. Dùng khi task phức tạp cần logic nhiều bước.

Pattern 3: Few-Shot Learning. Cho AI 2-3 ví dụ input output mẫu. AI sẽ học pattern và apply cho input mới.

Pattern 4: Negative Prompting. Nói rõ KHÔNG muốn gì. Ví dụ: "DO NOT dùng generic phrases", "DO NOT viết quá 3 đoạn".

Pattern 5: Iterative Refinement. Không bao giờ accept output đầu tiên. Luôn iterate ít nhất 1 lần. Chỉ rõ cần thay đổi gì, ở đâu, bao nhiêu.

Tránh 5 anti-patterns phổ biến: prompt mơ hồ, copy paste quá nhiều context, hỏi cùng câu, tin output đầu tiên, và dùng 1 prompt cho mọi task.
""",
    "session-2.1-rules-files": """
Session 2.1 — Rules Files.

Nếu Gem là customize AI trong app chat, thì Rules File là customize AI trong code editor. Sức mạnh lớn hơn rất nhiều: text, code, file access, terminal, và version control qua Git.

Khi bạn mở project trong code editor, editor sẽ tìm rules file — GEMINI.md cho Antigravity, .cursorrules cho Cursor, CLAUDE.md cho Claude Code. Nội dung rules được inject vào mọi AI request tự động.

Key insight: concept giống nhau giữa tất cả platforms, chỉ syntax khác. Bạn viết rules 1 lần, có thể adapt cho nhiều nền tảng.

Rules file cơ bản nên có: About This Project, Code Style, Naming Convention, Architecture, và Constraints. Phần Constraints rất quan trọng — nơi bạn nói AI KHÔNG được làm gì.

Bài tập: Viết rules file cho project hiện tại, test bằng cách yêu cầu AI tạo component, xem có tuân thủ không.
""",
    "session-2.2-workflows": """
Session 2.2 — Workflows.

Workflow là chuỗi bước có thứ tự mà AI thực hiện khi bạn trigger bằng slash command. Prompt đơn là 1 bước. Gem hay Rules lặp lại nhưng vẫn 1 bước. Workflow là nhiều bước, có thứ tự, multi-file output.

Cấu trúc rất đơn giản: frontmatter YAML có description, rồi các bước markdown. Ví dụ workflow /ship: Step 1 Merge Latest, Step 2 Run Tests nếu fail thì STOP, Step 3 Lint, Step 4 Version Bump, Step 5 Commit, Step 6 Push.

Một tính năng hay là turbo annotation. Đặt // turbo trước 1 step để AI tự chạy không hỏi. // turbo-all cho toàn bộ workflow.

Mỗi vai trò đều có thể thiết kế workflow: Developer có /deploy, Designer có /handoff, PM có /sprint-review, Content có /publish.

Bài tập: Thiết kế 1 workflow cho task bạn lặp đi lặp lại nhiều nhất trong công việc.
""",
    "session-2.3-anti-patterns": """
Session 2.3 — Khi nào KHÔNG dùng Agent.

Đây là phần quan trọng mà ít ai nói. 6 anti-patterns phổ biến: Automate Everything khi setup tốn hơn tiết kiệm, AI viết tôi paste gây technical debt, 1 mega prompt gây overload, AI thay thế thinking dẫn đến bad decisions, Context dump nơi noise vượt signal, và Trust first output bỏ qua hallucination.

Framework đơn giản: Frequency nhân Effort. High frequency low effort? Do it, no brainer. Low frequency high effort? Don't — waste of time.

KHÔNG dùng khi: task dưới 2 phút, cần 100% chính xác, không verify được output, cần empathy thật, hoặc security-sensitive.

NÊN dùng khi: task lặp với pattern rõ, explore options nhanh, boilerplate code, refactoring theo chuẩn, research và summarization.
""",
    "session-3.1-agent-architecture": """
Session 3.1 — Agent System Architecture.

Case study thực tế: Antigravity Kit với 20 Agents, 60 Skills, 11 Workflows. Key insight: không phải 1 AI biết hết, mà là nhiều AI chuyên gia, mỗi AI biết rõ lĩnh vực mình — giống cách team thật hoạt động.

Cấu trúc thư mục .agent/ gồm: agents/ chứa specialist agents, skills/ chứa kiến thức module, workflows/ chứa slash commands, rules/ chứa global rules.

Flow khi nhận request: GEMINI.md classify request → Intelligent Router phân tích domain → Chọn đúng agent → Agent load skills → Execute.

3 components: Agent là vai trò + chuyên môn + quy tắc. Skill là kiến thức chuyên sâu, tái sử dụng, gắn được vào nhiều agent. GEMINI.md là bộ não trung tâm có Request Classifier và Intelligent Routing.
""",
    "session-3.2-design-framework": """
Session 3.2 — 5-Step Design Framework.

Bước 1: Identify Roles. Ai trong team xử lý task gì? Mỗi role thành 1 Agent.
Bước 2: List Knowledge. Mỗi agent cần biết gì? Mỗi domain thành 1 Skill.
Bước 3: Map Processes. Quy trình nào lặp? Mỗi process thành 1 Workflow.
Bước 4: Write Router. Request nào đi đến agent nào? Keyword mapping trong GEMINI.md.
Bước 5: Start Small. 1 GEMINI.md + 2-3 skills + 1 workflow. Dùng 2 tuần rồi thêm dần.

Quan trọng: KHÔNG cố xây 20 agents ngày đầu. Bắt đầu nhỏ, iterate theo nhu cầu thực tế.

Bài tập: Thiết kế agent system cho project của bạn. Xác định roles, knowledge domains, recurring processes, và routing table.
""",
    "session-3.3-advanced-patterns": """
Session 3.3 — 5 Advanced Patterns.

Pattern 1: Skill Loading Protocol. Agent chỉ đọc SKILL.md index trước, rồi đọc sub-sections matching task. Không đọc tất cả — tránh context overflow.

Pattern 2: Tiered Rules. 3 lớp ưu tiên: P0 là GEMINI.md luôn áp dụng, P1 là Agent markdown khi active, P2 là Skill khi loaded. Khi conflict, P0 thắng P1 thắng P2.

Pattern 3: Socratic Gate. Buộc AI hỏi trước khi làm. New Feature phải hỏi minimum 3 câu hỏi. Bug Fix phải confirm understanding. Tránh build sai thứ.

Pattern 4: Turbo Annotations. // turbo auto-run 1 step, // turbo-all auto-run toàn bộ workflow. Dùng cho safe steps.

Pattern 5: Multi-Agent Orchestration. Orchestrator phân task cho multiple specialists chạy song song, rồi tổng hợp. Agent phức tạp nhất — biết chia task, giao đúng người, tổng hợp kết quả.

Đây là những pattern nâng cao nhất, giúp hệ thống agent hoạt động thông minh và hiệu quả.
""",
}


def generate_audio(text: str, output_path: Path) -> bool:
    """Generate TTS audio using Gemini Native Audio model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set. Get from https://aistudio.google.com/apikey")
        return False

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"Đọc đoạn sau bằng giọng tiếng Việt, tone thân thiện, rõ ràng, như đang hướng dẫn 1-1:\n\n{text}",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Zephyr"
                        )
                    )
                ),
            ),
        )

        # Save audio
        audio_data = response.candidates[0].content.parts[0].inline_data.data
        
        # Write WAV file
        wav_path = output_path.with_suffix(".wav")
        with open(wav_path, "wb") as f:
            # WAV header for 24kHz mono 16-bit PCM
            sample_rate = 24000
            num_channels = 1
            bits_per_sample = 16
            data_size = len(audio_data)
            
            f.write(b"RIFF")
            f.write(struct.pack("<I", 36 + data_size))
            f.write(b"WAVE")
            f.write(b"fmt ")
            f.write(struct.pack("<I", 16))  # chunk size
            f.write(struct.pack("<H", 1))   # PCM format
            f.write(struct.pack("<H", num_channels))
            f.write(struct.pack("<I", sample_rate))
            f.write(struct.pack("<I", sample_rate * num_channels * bits_per_sample // 8))
            f.write(struct.pack("<H", num_channels * bits_per_sample // 8))
            f.write(struct.pack("<H", bits_per_sample))
            f.write(b"data")
            f.write(struct.pack("<I", data_size))
            f.write(audio_data)
        
        print(f"  ✅ {wav_path.name} ({data_size // 1024}KB)")
        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    print("🎙️  Generating TTS Audio for Workshop Sessions")
    print(f"📂 Output: {OUTPUT_DIR}")
    print(f"🤖 Model: {MODEL}")
    print()

    success = 0
    total = len(NARRATIONS)

    for name, script in NARRATIONS.items():
        print(f"🎧 {name}...")
        output_path = OUTPUT_DIR / name
        if generate_audio(script.strip(), output_path):
            success += 1
        print()

    print(f"\n✅ Generated {success}/{total} audio files")
    print(f"📂 Files in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
