import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="HSB AI Counselor",
    page_icon="🎓",
    layout="centered"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ======================
# UI STYLE (CHATGPT STYLE)
# ======================
st.markdown("""
<style>
/* nền */
.stApp {
    background: linear-gradient(135deg, #eef2f7, #ffffff);
    font-family: 'Arial';
}

/* chat bubble user */
div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]) {
    padding: 10px;
}

/* header */
h1 {
    text-align: center;
    color: #1f4e79;
}

/* container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* input box */
div[data-testid="stChatInput"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# TITLE
# ======================
st.title("🎓 HSB AI Admission Counselor")
st.caption("AI tư vấn ngành học giống cố vấn thật")

# ======================
# DATA
# ======================
hsb = {
    "mac": "Marketing & Truyền thông",
    "met": "Công nghệ & Doanh nghiệp",
    "has": "Dịch vụ & Chăm sóc",
    "hat": "Nhân lực & Lãnh đạo",
    "mas": "An ninh & Quản trị",
    "bns": "An ninh phi truyền thống",
    "kinh doanh": "Kinh doanh & Phân tích"
}

MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-text-preview"
]

# ======================
# AI FUNCTION
# ======================
def hoi_ai(profile):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Bạn là cố vấn tuyển sinh chuyên nghiệp HSB. "
                            "Chỉ dùng 7 ngành HSB, không bịa ngành. "
                            "Luôn phân tích chi tiết + hỏi ngược lại 2 câu."
                        )
                    },
                    {"role": "user", "content": profile}
                ]
            )
            return response.choices[0].message.content
        except:
            continue

    return "⚠️ AI đang lỗi, thử lại sau."

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "profile" not in st.session_state:
    st.session_state.profile = ""

# ======================
# INIT MESSAGE
# ======================
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Chào bạn! Mình sẽ giúp bạn chọn ngành phù hợp.\n\n👉 Hãy mô tả **điểm mạnh** của bạn"
    })
    st.session_state.step = 1

# ======================
# CHAT DISPLAY (CLEAN UI)
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ======================
# INPUT
# ======================
user_input = st.chat_input("Nhập câu trả lời của bạn...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # STEP 1
    if st.session_state.step == 1:
        st.session_state.profile += " Điểm mạnh: " + user_input
        reply = "👉 Điểm yếu của bạn là gì?"
        st.session_state.step = 2

    # STEP 2
    elif st.session_state.step == 2:
        st.session_state.profile += " Điểm yếu: " + user_input
        reply = "👉 Bạn thích làm việc với con người hay công nghệ?"
        st.session_state.step = 3

    # STEP 3 → AI ANALYSIS
    elif st.session_state.step == 3:
        st.session_state.profile += " Sở thích: " + user_input

        with st.spinner("🎓 Đang phân tích hồ sơ..."):
            ai_text = hoi_ai(st.session_state.profile)

        reply = f"""
---

## 🎯 Kết quả tư vấn

{ai_text}

---

💡 *HSB AI Counselor*
"""

        st.session_state.step = 4

    # STEP 4
    elif st.session_state.step == 4:
        reply = (
            "👉 Mình hỏi thêm nhé:\n\n"
            "Bạn thích môi trường nào hơn?\n"
            "🏢 Văn phòng\n"
            "🌿 Ngoài thực địa\n"
            "🔄 Kết hợp cả hai"
        )
        st.session_state.step = 5

    else:
        reply = "👉 Nhấn refresh để làm lại bài test nhé."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
