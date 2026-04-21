import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="HSB AI Counselor", page_icon="🎓")

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
# HSB DATA
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
# MODEL FALLBACK (CHỐNG CHẾT MODEL)
# ======================
MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.2-11b-text-preview"
]

# ======================
# AI COUNSELOR
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
                            "Bạn là chuyên gia tư vấn tuyển sinh HSB. "
                            "Chỉ được chọn 7 ngành: Marketing & Truyền thông, "
                            "Công nghệ & Doanh nghiệp, Dịch vụ & Chăm sóc, "
                            "Nhân lực & Lãnh đạo, An ninh & Quản trị, "
                            "An ninh phi truyền thống, Kinh doanh & Phân tích. "
                            "KHÔNG được bịa ngành mới.\n\n"
                            "Yêu cầu:\n"
                            "- Phân tích tính cách\n"
                            "- Chấm điểm từng ngành (0-10)\n"
                            "- Chọn ngành phù hợp nhất\n"
                            "- Giải thích lý do\n"
                            "- Luôn hỏi ngược lại 2 câu để khai thác thêm thông tin"
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

if "init" not in st.session_state:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "🎓 Chào bạn! Mình là cố vấn tuyển sinh HSB.\n\n"
            "Mình sẽ giúp bạn chọn ngành phù hợp nhất.\n\n"
            "👉 Hãy bắt đầu bằng cách mô tả **điểm mạnh** của bạn"
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

    # STEP 3 → AI ANALYSIS
    elif st.session_state.step == 3:
        st.session_state.profile += " Sở thích: " + user_input

        reply = "🎓 Đang phân tích hồ sơ của bạn...\n\n"

        ai_text = hoi_ai(st.session_state.profile)

        reply += ai_text

        st.session_state.step = 4

    # STEP 4 → hỏi ngược tiếp
    elif st.session_state.step == 4:
        reply = (
            "👍 Mình hiểu thêm rồi.\n\n"
            "👉 Bạn thích môi trường nào hơn?\n"
            "- Văn phòng\n"
            "- Ngoài thực địa\n"
            "- Hay kết hợp cả hai?"
        )
        st.session_state.step = 5

    else:
        reply = "👉 Bạn muốn làm lại? Hãy refresh trang nhé."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
