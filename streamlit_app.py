import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="HSB AI Counselor", page_icon="🎓", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2f7, #ffffff);
    font-family: Arial;
}

h1 {
    text-align: center;
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 HSB AI Admission Counselor")
st.caption("AI tư vấn ngành học + hỏi ngược + cập nhật lại phân tích")

# ======================
# NGÀNH HSB (KHÓA CỨNG)
# ======================
HSB_LIST = [
    "Marketing & Truyền thông",
    "Công nghệ & Doanh nghiệp",
    "Dịch vụ & Chăm sóc",
    "Nhân lực & Lãnh đạo",
    "An ninh & Quản trị",
    "An ninh phi truyền thống",
    "Kinh doanh & Phân tích"
]

# ======================
# MODEL FALLBACK
# ======================
MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-text-preview"
]

# ======================
# AI FUNCTION (KHÓA NGÀNH + HỎI NGƯỢC)
# ======================
def hoi_ai(profile):
    last_error = None

    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Bạn là chuyên gia tư vấn tuyển sinh HSB.\n\n"
                            "⚠️ QUY TẮC BẮT BUỘC:\n"
                            f"- CHỈ được chọn trong danh sách:\n{HSB_LIST}\n"
                            "- KHÔNG được tạo ngành mới\n"
                            "- KHÔNG được nói ngành ngoài danh sách\n\n"
                            "🎯 NHIỆM VỤ:\n"
                            "1. Phân tích tính cách học sinh\n"
                            "2. Chấm điểm từng ngành (0-10)\n"
                            "3. Chọn 1 ngành phù hợp nhất\n"
                            "4. Giải thích lý do\n"
                            "5. ĐẶC BIỆT: hỏi lại 2 câu sâu hơn để hiểu thêm\n\n"
                            "⚡ QUAN TRỌNG:\n"
                            "- Nếu thiếu thông tin → hỏi lại thay vì đoán\n"
                            "- Luôn tư duy lại sau khi có câu trả lời mới"
                        )
                    },
                    {"role": "user", "content": profile}
                ]
            )
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            continue

    return f"⚠️ AI lỗi toàn bộ model: {last_error}"

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
# INIT
# ======================
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 Chào bạn!\n\n"
            "Mình là cố vấn tuyển sinh HSB.\n"
            "Mình sẽ hỏi bạn từng bước để phân tích chính xác nhất.\n\n"
            "👉 Câu 1: Điểm mạnh lớn nhất của bạn là gì?"
        )
    })
    st.session_state.step = 1

# ======================
# CHAT DISPLAY
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

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

        with st.spinner("🎓 Đang phân tích..."):
            ai_text = hoi_ai(st.session_state.profile)

        reply = f"## 🎯 Phân tích ban đầu\n\n{ai_text}\n\n---\n👉 Bạn có thể bổ sung thêm: bạn thích môi trường áp lực cao hay ổn định?"
        st.session_state.step = 4

    # STEP 4 → UPDATE THINKING (QUAN TRỌNG)
    elif st.session_state.step == 4:
        st.session_state.profile += " Môi trường làm việc: " + user_input

        with st.spinner("🧠 Đang cập nhật lại phân tích..."):
            ai_text = hoi_ai(st.session_state.profile)

        reply = f"## 🔄 Phân tích cập nhật (tư duy lại)\n\n{ai_text}\n\n---\n👉 Bạn muốn mình giải thích sâu hơn về ngành nào không?"
        st.session_state.step = 5

    # STEP 5
    else:
        reply = "👉 Nếu muốn làm lại bài test, hãy refresh trang."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
