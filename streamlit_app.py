import streamlit as st
from groq import Groq

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="HSB Tư Vấn Tuyển Sinh",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# CONSTANTS
# =========================================================
HSB_MAJORS = [
    "Marketing & Truyền thông",
    "Công nghệ & Doanh nghiệp",
    "Dịch vụ & Chăm sóc",
    "Nhân lực & Lãnh đạo",
    "An ninh & Quản trị",
    "An ninh phi truyền thống",
    "Kinh doanh & Phân tích"
]

# =========================================================
# FLOW DEFINITION
# step type: "question" | "checkpoint" | "final"
# =========================================================
FLOW = [
    {
        "type": "question",
        "key": "intro",
        "text": "👋 Chào bạn! Mình là cố vấn tuyển sinh HSB.\n\nMình sẽ hỏi bạn một vài câu để hiểu rõ hơn — không có đúng sai đâu nhé, cứ trả lời tự nhiên thôi 😊\n\n**Bạn đang học lớp mấy, và điều khiến bạn băn khoăn nhất khi chọn ngành là gì?**"
    },
    {
        "type": "question",
        "key": "academics",
        "text": "Cảm ơn bạn đã chia sẻ! 📚\n\n**Học lực của bạn đang như thế nào?** Bạn học khối nào, môn nào mạnh nhất, môn nào yếu nhất? (Không cần điểm chính xác, ước lượng cũng được)"
    },
    {
        "type": "question",
        "key": "strength",
        "text": "**Điểm mạnh lớn nhất của bạn là gì?** 💪\n\n(ví dụ: giao tiếp tốt, tư duy logic, sáng tạo, kỷ luật, lãnh đạo…)"
    },
    {
        "type": "question",
        "key": "weakness",
        "text": "Thành thật vậy là tốt lắm! 🙏\n\n**Điểm yếu lớn nhất của bạn là gì?** Đừng ngại — mình cần biết để tư vấn thật sự phù hợp, không phải để đánh giá bạn đâu."
    },
    {
        "type": "checkpoint",
        "key": "checkpoint_1",
        "spinner": "✨ Đang đọc hồ sơ của bạn...",
        "prompt_template": """Dựa trên thông tin sau của học sinh:
- Băn khoăn: {intro}
- Học lực/môn mạnh-yếu: {academics}
- Điểm mạnh: {strength}
- Điểm yếu: {weakness}

Hãy viết 2–3 câu nhận xét ngắn, ấm áp, mang tính cá nhân hóa cao — như thể mày đang nói chuyện trực tiếp với học sinh. KHÔNG phân tích ngành, KHÔNG đưa ra kết luận. Chỉ nhận xét về con người họ một cách tinh tế, rồi hỏi tiếp câu sau:

"**Bạn hứng thú với lĩnh vực nào nhất?**\n(công nghệ / kinh doanh / truyền thông / con người & xã hội / an ninh / sáng tạo… hoặc nếu chưa biết cũng nói nhé)"

Trả lời bằng tiếng Việt, tự nhiên, KHÔNG dùng markdown quá nhiều."""
    },
    {
        "type": "question",
        "key": "interest",
        "text": None  # được generate bởi checkpoint ở trên
    },
    {
        "type": "question",
        "key": "workstyle",
        "text": "**Bạn thích làm việc với Con Người hay với Dữ liệu/Công nghệ?** 🤔\n\nHoặc cả hai đều thích? Hay chưa chắc? Cứ nói thật nhé."
    },
    {
        "type": "question",
        "key": "career_goal",
        "text": "Gần xong rồi! 🎯\n\n**5–10 năm nữa bạn muốn làm gì?** Không cần cụ thể, kể cả 'chưa biết' cũng được — nhưng nếu có hình dung gì dù mờ nhạt, cứ kể mình nghe."
    },
    {
        "type": "question",
        "key": "family",
        "text": "**Gia đình bạn có định hướng gì cho việc chọn ngành không?** 👨‍👩‍👦\n\nVí dụ: muốn bạn nối nghiệp, muốn ngành ổn định, hay hoàn toàn để bạn tự quyết? Và về tài chính, gia đình có thể hỗ trợ học phí ở mức nào?"
    },
    {
        "type": "question",
        "key": "experience",
        "text": "Câu cuối cùng! 🏁\n\n**Bạn đã từng làm thêm, tham gia CLB, dự án, hay hoạt động ngoại khóa nào chưa?** Nếu có, kể cho mình nghe — đây thường là manh mối quan trọng nhất để hiểu bạn thật sự phù hợp với gì."
    },
    {
        "type": "checkpoint",
        "key": "checkpoint_2",
        "spinner": "🔍 Đang tổng hợp toàn bộ hồ sơ...",
        "prompt_template": """Dựa trên toàn bộ hồ sơ học sinh:
- Băn khoăn ban đầu: {intro}
- Học lực: {academics}
- Điểm mạnh: {strength}
- Điểm yếu: {weakness}
- Hứng thú: {interest}
- Phong cách làm việc: {workstyle}
- Mục tiêu nghề nghiệp: {career_goal}
- Gia đình & tài chính: {family}
- Trải nghiệm thực tế: {experience}

Hãy viết một đoạn TÓM TẮT HỒ SƠ ngắn gọn (3–4 câu), như thể mày đang đọc to cho học sinh nghe để họ xác nhận — "Để mình tóm tắt lại những gì mình hiểu về bạn nhé...". Giọng ấm áp, cụ thể, mang tính cá nhân. KHÔNG đưa ra kết quả ngành. Kết thúc bằng: "Bây giờ mình sẽ phân tích kỹ và đưa ra kết quả cho bạn nhé! 🎯"

Tiếng Việt, tự nhiên."""
    },
    {
        "type": "final",
        "key": "result"
    }
]

# Tổng số câu hỏi thật (không tính checkpoint, final)
TOTAL_QUESTIONS = sum(1 for s in FLOW if s["type"] == "question")

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --navy:      #0f2d52;
    --navy-mid:  #1a4a7a;
    --navy-light:#2563a8;
    --gold:      #c9a84c;
    --gold-light:#e8c97a;
    --white:     #ffffff;
    --off-white: #f4f7fb;
    --text:      #1a2b3c;
    --text-muted:#5a7a99;
    --border:    #d0dcea;
    --shadow:    0 4px 24px rgba(15,45,82,0.10);
    --green:     #16a34a;
}

.stApp {
    background: var(--off-white) !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 780px !important;
    margin: 0 auto !important;
}

/* ── HEADER ── */
.hsb-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, var(--navy-light) 100%);
    padding: 32px 40px 24px;
    color: var(--white);
    border-radius: 0 0 24px 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(15,45,82,0.18);
    position: relative;
    overflow: hidden;
}
.hsb-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(201,168,76,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hsb-logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
}
.hsb-icon { font-size: 2.2rem; line-height: 1; }
.hsb-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    font-weight: 400;
    color: var(--white);
    margin: 0;
}
.hsb-tagline {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.6);
    margin: 2px 0 0;
    font-weight: 300;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── PROGRESS ── */
.progress-wrap { padding: 0 40px 20px; }
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-bottom: 7px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.progress-track {
    background: var(--border);
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, var(--navy-light), var(--gold));
    border-radius: 99px;
    height: 100%;
    transition: width 0.6s cubic-bezier(.4,0,.2,1);
}

/* ── CHAT AREA ── */
.chat-wrap { padding: 0 20px; }

div[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 3px 0 !important;
    border: none !important;
    box-shadow: none !important;
}

/* Assistant bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 14px 18px !important;
    box-shadow: var(--shadow) !important;
    color: var(--text) !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
    max-width: 88% !important;
}

/* Checkpoint bubble — gold tint */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]).checkpoint-msg .stMarkdown {
    border-left: 3px solid var(--gold) !important;
    background: #fffdf5 !important;
}

/* User bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: var(--navy) !important;
    border-radius: 18px 4px 18px 18px !important;
    padding: 12px 18px !important;
    color: var(--white) !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    max-width: 80% !important;
    margin-left: auto !important;
}

/* ── CHAT INPUT ── */
div[data-testid="stChatInput"] {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: 0 2px 12px rgba(15,45,82,0.07) !important;
    margin: 12px 20px 20px !important;
    background: var(--white) !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: var(--navy-light) !important;
    box-shadow: 0 0 0 3px rgba(37,99,168,0.12) !important;
}
div[data-testid="stChatInput"] textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--text) !important;
}

.stSpinner > div { color: var(--navy-light) !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hsb-header">
    <div class="hsb-logo-row">
        <span class="hsb-icon">🎓</span>
        <div>
            <p class="hsb-brand">HSB Admission Counselor</p>
            <p class="hsb-tagline">Hệ thống tư vấn tuyển sinh thông minh</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "messages"     not in st.session_state: st.session_state.messages = []
if "flow_step"    not in st.session_state: st.session_state.flow_step = 0
if "profile"      not in st.session_state: st.session_state.profile = {}
if "done"         not in st.session_state: st.session_state.done = False
if "q_count"      not in st.session_state: st.session_state.q_count = 0

# =========================================================
# PROGRESS BAR
# =========================================================
pct = int((st.session_state.q_count / TOTAL_QUESTIONS) * 100)
label = "Hoàn tất ✓" if st.session_state.done else f"Câu {st.session_state.q_count}/{TOTAL_QUESTIONS}"

st.markdown(f"""
<div class="progress-wrap">
    <div class="progress-label">
        <span>Tiến trình tư vấn</span>
        <span>{label}</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# AI HELPERS
# =========================================================
def call_groq(system: str, user: str, max_tokens: int = 600) -> str:
    for model in ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"]:
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ],
                temperature=0.75,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception:
            continue
    return "⚠️ Lỗi kết nối AI. Vui lòng thử lại."


def generate_checkpoint(template: str, profile: dict) -> str:
    prompt = template.format(**{k: profile.get(k, "chưa có") for k in profile})
    return call_groq(
        system="Bạn là cố vấn tuyển sinh ấm áp, nói chuyện tự nhiên như người thật. Tiếng Việt.",
        user=prompt,
        max_tokens=400
    )


def build_profile_text(profile: dict) -> str:
    labels = {
        "intro":       "Băn khoăn ban đầu",
        "academics":   "Học lực & môn mạnh/yếu",
        "strength":    "Điểm mạnh",
        "weakness":    "Điểm yếu",
        "interest":    "Lĩnh vực hứng thú",
        "workstyle":   "Phong cách làm việc",
        "career_goal": "Mục tiêu nghề nghiệp",
        "family":      "Định hướng & nguồn lực gia đình",
        "experience":  "Trải nghiệm thực tế",
    }
    return "\n".join(f"- {labels.get(k,k)}: {v}" for k, v in profile.items())


def generate_final_analysis(profile: dict) -> str:
    profile_text = build_profile_text(profile)
    majors_list  = "\n".join(f"- {m}" for m in HSB_MAJORS)

    system = f"""Bạn là CỐ VẤN TUYỂN SINH chuyên nghiệp, sắc bén và ấm áp.

HỒ SƠ HỌC SINH:
{profile_text}

NGÀNH HỢP LỆ (bắt buộc chỉ chọn trong danh sách):
{majors_list}

NHIỆM VỤ: Phân tích hồ sơ và trả về đúng cấu trúc Markdown sau:

### 🧠 Nhận xét về bạn
[2–3 câu nhận xét tâm lý sâu, cụ thể, cá nhân hóa. Không chung chung.]

### 📊 Mức độ phù hợp các ngành
| Ngành | Điểm | Nhận xét |
|---|:---:|---|
[7 ngành đầy đủ. Điểm phân hóa thật (không dàn đều). Nhận xét 1 câu cụ thể.]

### 🎯 Ngành phù hợp nhất: [Tên ngành]
[4–5 câu lý giải tại sao ngành này khớp với tính cách, học lực, mục tiêu, hoàn cảnh gia đình của học sinh. Cụ thể, thuyết phục.]

### 💡 Lời khuyên thực tế
[2–3 gạch đầu dòng: những thứ học sinh nên chuẩn bị hoặc lưu ý khi theo đuổi ngành này]

### ❓ Mình muốn hỏi thêm
[1–2 câu hỏi để tiếp tục hội thoại nếu học sinh muốn tìm hiểu sâu hơn]

QUY TẮC: Không bịa ngành mới. Điểm số phải phân hóa. Tiếng Việt tự nhiên."""

    return call_groq(system=system, user="Hãy phân tích và tư vấn ngành học cho tôi.", max_tokens=1800)


def generate_followup(profile: dict, user_msg: str) -> str:
    profile_text = build_profile_text(profile)
    majors_list  = "\n".join(f"- {m}" for m in HSB_MAJORS)
    system = f"""Bạn là cố vấn tuyển sinh HSB. Hồ sơ học sinh:
{profile_text}

Ngành hợp lệ: {majors_list}

Hãy trả lời câu hỏi/yêu cầu của học sinh một cách cụ thể, cá nhân hóa dựa trên hồ sơ đã có. Tiếng Việt tự nhiên."""
    return call_groq(system=system, user=user_msg, max_tokens=800)


# =========================================================
# INIT — gửi câu hỏi đầu tiên
# =========================================================
if len(st.session_state.messages) == 0:
    first = FLOW[0]
    st.session_state.messages.append({"role": "assistant", "content": first["text"]})

# =========================================================
# RENDER CHAT
# =========================================================
st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# USER INPUT
# =========================================================
placeholder = "Nhập câu trả lời..." if not st.session_state.done else "Hỏi thêm bất cứ điều gì..."
user_input = st.chat_input(placeholder)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    fs   = st.session_state.flow_step
    step = FLOW[fs] if fs < len(FLOW) else None

    # ── Đang trong flow ──
    if step and not st.session_state.done:

        # Lưu câu trả lời nếu là question
        if step["type"] == "question":
            st.session_state.profile[step["key"]] = user_input
            st.session_state.q_count += 1
            st.session_state.flow_step += 1
            next_fs = st.session_state.flow_step

        # Tiến tới bước tiếp theo
        while st.session_state.flow_step < len(FLOW):
            next_step = FLOW[st.session_state.flow_step]

            # ── Checkpoint ──
            if next_step["type"] == "checkpoint":
                with st.spinner(next_step["spinner"]):
                    cp_reply = generate_checkpoint(next_step["prompt_template"], st.session_state.profile)
                st.session_state.messages.append({"role": "assistant", "content": cp_reply})
                st.session_state.flow_step += 1

                # Bỏ qua bước question ngay sau checkpoint (nếu text=None)
                if st.session_state.flow_step < len(FLOW):
                    nxt = FLOW[st.session_state.flow_step]
                    if nxt["type"] == "question" and nxt["text"] is None:
                        # câu hỏi đã được nhúng vào checkpoint text rồi
                        # đánh dấu bước này là "chờ nhận input"
                        break
                break

            # ── Final ──
            elif next_step["type"] == "final":
                with st.spinner("🧠 Đang tạo kết quả phân tích toàn diện..."):
                    analysis = generate_final_analysis(st.session_state.profile)
                reply = f"""## 🎯 Kết quả tư vấn cá nhân

{analysis}

---
*💬 Bạn có thể hỏi thêm bất kỳ điều gì — về ngành học, lộ trình, hay bất cứ thứ gì bạn còn thắc mắc.*"""
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.done = True
                st.session_state.flow_step += 1
                break

            # ── Question thường ──
            elif next_step["type"] == "question" and next_step["text"] is not None:
                st.session_state.messages.append({"role": "assistant", "content": next_step["text"]})
                break

            else:
                st.session_state.flow_step += 1

    # ── Sau khi done → hội thoại mở ──
    elif st.session_state.done:
        with st.spinner("🔄 Đang xử lý..."):
            reply = generate_followup(st.session_state.profile, user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()
