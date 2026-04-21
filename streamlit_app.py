import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="HSB Counselor", page_icon="🎓", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ======================
# STYLE (GIẢ TƯ VẤN VIÊN THẬT)
# ======================
st.markdown("""
<style>
.stApp {
    background: #f6f8fb;
    font-family: Arial;
}

h1 {
    text-align: center;
    color: #1f4e79;
}

.chat-bubble {
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 HSB Admission Counselor (Realistic Mode)")
st.caption("Tư vấn viên AI - hỏi sâu - không bịa ngành")

# ======================
# NGÀNH KHÓA CỨNG (TUYỆT ĐỐI KHÔNG THAY ĐỔI)
# ======================
HSB = [
    "Marketing & Truyền thông",
    "Công nghệ & Doanh nghiệp",
    "Dịch vụ & Chăm sóc",
    "Nhân lực & Lãnh đạo",
    "An ninh & Quản trị",
    "An ninh phi truyền thống",
    "Kinh doanh & Phân tích"
]

# ======================
# MODEL SAFE
# ======================
MODELS = [
    "llama-3.1-8b-instant"
]

# ======================
# AI COUNSELOR (GIỐNG NGƯỜI THẬT)
# ======================
def counselor_ai(profile, user_reply_round=None):
    try:
        system_prompt = f"""
Bạn là cố vấn tuyển sinh đại học chuyên nghiệp.

⚠️ QUY TẮC TUYỆT ĐỐI:
- Chỉ được chọn trong 7 ngành sau:
{HSB}
- Không được tạo ngành mới
- Không được nhắc ngành ngoài danh sách

🎯 PHONG CÁCH:
- Giống tư vấn viên thật 1:1
- Không trả lời máy móc
- Có cảm xúc, có phân tích logic

🎯 QUY TRÌNH:
1. Phân tích học sinh
2. So sánh các ngành (CHỈ trong danh sách)
3. Chọn 1 ngành phù hợp nhất
4. Giải thích ngắn gọn
5. HỎI NGƯỢC 1–2 câu để hiểu sâu hơn

🔥 QUAN TRỌNG:
Nếu thông tin chưa đủ → phải hỏi lại, không được đoán.
"""

        if user_reply_round:
            profile = profile + "\n\nCập nhật từ học sinh: " + user_reply_round

        response = client.chat.completions.create(
            model=MODELS[0],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": profile}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Lỗi AI: {e}"

# ======================
# SESSION
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 1

if "profile" not in st.session_state:
    st.session_state.profile = ""

if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Mình là cố vấn tuyển sinh HSB.\n\n👉 Bạn hãy nói điểm mạnh của bạn trước."
    })

# ======================
# CHAT DISPLAY
# ======================
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ======================
# INPUT
# ======================
user_input = st.chat_input("Nhập câu trả lời...")

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
        reply = "👉 Bạn thích làm việc với CON NGƯỜI hay CÔNG NGHỆ?"
        st.session_state.step = 3

    # STEP 3 → AI LẦN 1
    elif st.session_state.step == 3:
        st.session_state.profile += " Sở thích: " + user_input

        with st.spinner("🧠 Cố vấn đang phân tích..."):
            ai = counselor_ai(st.session_state.profile)

        reply = "## 🎯 Phân tích ban đầu\n\n" + ai
        reply += "\n\n👉 Mình hỏi thêm: Bạn thích môi trường ổn định hay áp lực cao?"
        st.session_state.step = 4

    # STEP 4 → THINK AGAIN (GIỐNG TƯ VẤN THẬT)
    elif st.session_state.step == 4:
        with st.spinner("🔄 Cố vấn đang suy nghĩ lại..."):
            ai = counselor_ai(st.session_state.profile, user_input)

        reply = "## 🔄 Cập nhật tư vấn (giống tư vấn viên thật)\n\n" + ai
        reply += "\n\n👉 Nếu muốn, mình có thể phân tích sâu hơn 1 ngành cụ thể cho bạn."
        st.session_state.step = 5

    else:
        reply = "👉 Bạn có thể refresh để làm lại bài test."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
