import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="HSB Admission Counselor", page_icon="🎓")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2f7, #ffffff);
}
</style>
""", unsafe_allow_html=True)

# ======================
# NGÀNH HSB
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

# ======================
# AI COUNSELOR (GIỐNG TƯ VẤN THẬT)
# ======================
def hoi_ai(profile):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là chuyên gia tư vấn tuyển sinh đại học HSB. "
                        "Nhiệm vụ: phân tích học sinh như cố vấn thật.\n\n"
                        "QUY TẮC:\n"
                        "- Chỉ chọn 7 ngành HSB\n"
                        "- Chấm điểm từng ngành (0-10)\n"
                        "- Giải thích ngắn gọn vì sao phù hợp\n"
                        "- Luôn hỏi NGƯỢC LẠI 2 câu để khai thác thêm thông tin\n\n"
                        "FORMAT OUTPUT:\n"
                        "1. Phân tích tính cách\n"
                        "2. Bảng điểm ngành\n"
                        "3. Ngành phù hợp nhất\n"
                        "4. Lý do\n"
                        "5. 2 câu hỏi ngược lại người dùng"
                    )
                },
                {"role": "user", "content": profile}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI lỗi: {e}"

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "profile" not in st.session_state:
    st.session_state.profile = ""

if "init" not in st.session_state:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "🎓 Chào bạn, mình là cố vấn tuyển sinh HSB.\n\n"
            "Mình sẽ giúp bạn chọn ngành phù hợp nhất.\n\n"
            "👉 Đầu tiên: Hãy mô tả điểm mạnh của bạn"
        )
    })
    st.session_state.init = True
    st.session_state.step = 1

# ======================
# CHAT DISPLAY
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

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
        reply = "👉 Bạn thích làm việc với con người hay công nghệ?"
        st.session_state.step = 3

    # STEP 3 → AI COUNSELOR
    elif st.session_state.step == 3:
        st.session_state.profile += " Sở thích: " + user_input

        reply = "🎓 Đang phân tích hồ sơ của bạn...\n\n"

        ai_text = hoi_ai(st.session_state.profile)

        reply += ai_text

        st.session_state.step = 4

    # STEP 4 → hỏi tiếp như tư vấn thật
    else:
        reply = (
            "👍 Mình hiểu thêm rồi.\n\n"
            "👉 Bạn muốn làm việc môi trường:\n"
            "- Văn phòng\n"
            "- Ngoài thực địa\n"
            "- Hay kết hợp cả hai?"
        )
        st.session_state.step = 5

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
