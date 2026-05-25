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
 
QUESTIONS = [
    ("intro",       "👋 Chào bạn! Mình là cố vấn tuyển sinh HSB.\n\nĐể tư vấn chính xác nhất, mình cần hiểu bạn một chút. Bạn đang học lớp mấy, và điều khiến bạn **băn khoăn nhất** khi chọn ngành là gì?"),
    ("strength",    "Cảm ơn bạn đã chia sẻ! 💪\n\n**Điểm mạnh lớn nhất của bạn là gì?** (ví dụ: giao tiếp tốt, tư duy logic, sáng tạo, kỷ luật…)"),
    ("weakness",    "Thành thật như vậy rất tốt! 🙏\n\n**Điểm yếu lớn nhất của bạn là gì?** Đừng ngại — mình cần biết để tư vấn phù hợp hơn."),
    ("interest",    "**Bạn hứng thú với lĩnh vực nào nhất?**\n\n(công nghệ / kinh doanh / truyền thông / con người & xã hội / an ninh / sáng tạo…)"),
    ("workstyle",   "Câu cuối cùng! 🎯\n\n**Bạn thích làm việc với Con Người hay Dữ liệu/Công nghệ?** Hay cả hai?"),
]
 
TOTAL_STEPS = len(QUESTIONS)
 
# =========================================================
# CSS — CORPORATE NAVY, CLEAN, PREMIUM
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');
 
/* ── Root variables ── */
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
}
 
/* ── Reset app background ── */
.stApp {
    background: var(--off-white) !important;
    font-family: 'DM Sans', sans-serif !important;
}
 
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 !important;
    max-width: 780px !important;
    margin: 0 auto !important;
}
 
/* ── HEADER BANNER ── */
.hsb-header {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, var(--navy-light) 100%);
    padding: 36px 40px 28px;
    color: var(--white);
    border-radius: 0 0 24px 24px;
    margin-bottom: 28px;
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
.hsb-header::after {
    content: '';
    position: absolute;
    bottom: -20px; left: 30%;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hsb-logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 10px;
}
.hsb-icon {
    font-size: 2.2rem;
    line-height: 1;
}
.hsb-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    font-weight: 400;
    letter-spacing: 0.02em;
    color: var(--white);
    margin: 0;
}
.hsb-tagline {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.65);
    margin: 0;
    font-weight: 300;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
 
/* ── PROGRESS BAR ── */
.progress-wrap {
    padding: 0 40px 24px;
}
.progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-bottom: 8px;
    font-weight: 500;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}
.progress-track {
    background: var(--border);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, var(--navy-light), var(--gold));
    border-radius: 99px;
    height: 100%;
    transition: width 0.5s cubic-bezier(.4,0,.2,1);
}
 
/* ── CHAT AREA ── */
.chat-wrap {
    padding: 0 24px;
}
 
/* ── Message bubbles ── */
div[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
    border: none !important;
    box-shadow: none !important;
}
 
/* Assistant bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown,
div[data-testid="stChatMessage"][data-role="assistant"] .stMarkdown {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 14px 18px !important;
    box-shadow: var(--shadow) !important;
    color: var(--text) !important;
    font-size: 0.93rem !important;
    line-height: 1.65 !important;
    max-width: 88% !important;
}
 
/* User bubble */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown,
div[data-testid="stChatMessage"][data-role="user"] .stMarkdown {
    background: var(--navy) !important;
    border-radius: 18px 4px 18px 18px !important;
    padding: 12px 18px !important;
    color: var(--white) !important;
    font-size: 0.93rem !important;
    line-height: 1.6 !important;
    max-width: 80% !important;
    margin-left: auto !important;
}
 
/* ── RESULT CARD ── */
.result-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin: 12px 0 16px;
    box-shadow: var(--shadow);
}
.result-card h2 {
    font-family: 'DM Serif Display', serif;
    color: var(--navy);
    font-size: 1.35rem;
    margin-bottom: 16px;
    border-bottom: 2px solid var(--gold);
    padding-bottom: 10px;
}
 
/* ── CHAT INPUT ── */
div[data-testid="stChatInput"] {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: 0 2px 12px rgba(15,45,82,0.07) !important;
    margin: 16px 24px 24px !important;
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
 
/* ── SPINNER ── */
.stSpinner { color: var(--navy-light) !important; }
 
/* ── DIVIDER ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 8px 0 16px;
}
 
/* ── STEP BADGE ── */
.step-badge {
    display: inline-block;
    background: var(--navy);
    color: var(--white);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 99px;
    margin-bottom: 6px;
}
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
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "done" not in st.session_state:
    st.session_state.done = False
 
 
# =========================================================
# PROGRESS BAR
# =========================================================
current_step = min(st.session_state.step, TOTAL_STEPS)
pct = int((current_step / TOTAL_STEPS) * 100)
label = "Hoàn tất ✓" if st.session_state.done else f"Bước {current_step}/{TOTAL_STEPS}"
 
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
# AI ENGINE
# =========================================================
def build_profile_text(profile: dict) -> str:
    lines = []
    labels = {
        "intro":     "Thông tin ban đầu & băn khoăn",
        "strength":  "Điểm mạnh",
        "weakness":  "Điểm yếu",
        "interest":  "Lĩnh vực hứng thú",
        "workstyle": "Phong cách làm việc",
    }
    for k, v in profile.items():
        lines.append(f"- {labels.get(k, k)}: {v}")
    return "\n".join(lines)
 
 
def generate_analysis(profile: dict, followup: str = None) -> str:
    profile_text = build_profile_text(profile)
    if followup:
        profile_text += f"\n- Bổ sung thêm từ học sinh: {followup}"
 
    system_prompt = f"""Bạn là một CỐ VẤN TUYỂN SINH ĐẠI HỌC chuyên nghiệp, ấm áp và sắc bén.
 
## HỒ SƠ HỌC SINH
{profile_text}
 
## NGÀNH HỢP LỆ (chỉ được chọn trong danh sách này)
{chr(10).join(f'- {m}' for m in HSB_MAJORS)}
 
## NHIỆM VỤ
Phân tích hồ sơ và trả về đúng cấu trúc sau bằng Markdown:
 
### 🧠 Phân tích tính cách
[2–3 câu nhận xét sâu về học sinh dựa trên hồ sơ. Tránh chung chung.]
 
### 📊 Đánh giá mức độ phù hợp
| Ngành | Điểm (0–10) | Nhận xét ngắn |
|---|---|---|
[Liệt kê đủ 7 ngành, điểm số thực chất, nhận xét 1 câu]
 
### 🎯 Ngành phù hợp nhất
**[Tên ngành]**
 
[3–4 câu giải thích tại sao ngành này phù hợp với tính cách, điểm mạnh và định hướng của học sinh. Cụ thể, không chung chung.]
 
### ❓ Câu hỏi thêm
[Hỏi 1–2 câu để hiểu học sinh sâu hơn và tối ưu kết quả]
 
## QUY TẮC
- Không bịa ngành mới
- Không lặp lại lời học sinh một cách máy móc
- Phân tích phải có chiều sâu tâm lý, không chỉ liệt kê
- Điểm số phải phân hóa rõ ràng (không dàn đều 7/10 hết)
- Ngôn ngữ: tiếng Việt, tự nhiên, chuyên nghiệp"""
 
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Hãy phân tích hồ sơ và tư vấn ngành học cho tôi."}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        # fallback to smaller model
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Hãy phân tích hồ sơ và tư vấn ngành học cho tôi."}
                ],
                temperature=0.7,
                max_tokens=1500,
            )
            return response.choices[0].message.content
        except Exception as e2:
            return f"⚠️ Lỗi hệ thống: {e2}"
 
 
# =========================================================
# FIRST MESSAGE
# =========================================================
if len(st.session_state.messages) == 0:
    opening = QUESTIONS[0][1]
    st.session_state.messages.append({"role": "assistant", "content": opening})
 
 
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
placeholder = "Nhập câu trả lời của bạn..." if not st.session_state.done else "Hỏi thêm bất cứ điều gì..."
user_input = st.chat_input(placeholder)
 
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    step = st.session_state.step
    reply = ""
 
    # ── Bước 0: Intro ──
    if step == 0:
        st.session_state.profile["intro"] = user_input
        st.session_state.step = 1
        reply = QUESTIONS[1][1]
 
    # ── Bước 1: Điểm mạnh ──
    elif step == 1:
        st.session_state.profile["strength"] = user_input
        st.session_state.step = 2
        reply = QUESTIONS[2][1]
 
    # ── Bước 2: Điểm yếu ──
    elif step == 2:
        st.session_state.profile["weakness"] = user_input
        st.session_state.step = 3
        reply = QUESTIONS[3][1]
 
    # ── Bước 3: Sở thích ──
    elif step == 3:
        st.session_state.profile["interest"] = user_input
        st.session_state.step = 4
        reply = QUESTIONS[4][1]
 
    # ── Bước 4: Phong cách → Phân tích AI ──
    elif step == 4:
        st.session_state.profile["workstyle"] = user_input
        st.session_state.step = 5
        st.session_state.done = True
 
        with st.spinner("🧠 Đang phân tích hồ sơ của bạn..."):
            analysis = generate_analysis(st.session_state.profile)
 
        reply = f"""## 🎯 Kết quả tư vấn cá nhân
 
{analysis}
 
---
*💬 Bạn có thể hỏi thêm bất kỳ điều gì — mình luôn ở đây để hỗ trợ.*"""
 
    # ── Bước 5+: Hội thoại mở ──
    else:
        with st.spinner("🔄 Đang cập nhật phân tích..."):
            analysis = generate_analysis(st.session_state.profile, followup=user_input)
 
        reply = f"""## 🔄 Phân tích cập nhật
 
{analysis}"""
 
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
