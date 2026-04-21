import streamlit as st
from groq import Groq

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="HSB AI Advisor", page_icon="🎓")

# 🔑 lấy API từ secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f0f2f5, #ffffff);
}
</style>
""", unsafe_allow_html=True)

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

# ======================
# AI FUNCTION
# ======================
def hoi_ai(text):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bạn là chuyên gia tư vấn ngành HSB. "
                        "Phân tích điểm mạnh, điểm yếu, tính cách "
                        "và gợi ý ngành phù hợp trong 7 ngành HSB."
                    )
                },
                {"role": "user", "content": text}
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
        "content": "👋 Mình sẽ tư vấn ngành cho bạn.\n\n👉 Bạn hãy mô tả **điểm mạnh** của bạn"
    })
    st.session_state.init = True
    st.session_state.step = 1

# ======================
# DISPLAY CHAT
# ======================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ======================
# INPUT
# ======================
user_input = st.chat_input("Nhập tại đây...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # STEP 1
    if st.session_state.step == 1:
        st.session_state.profile += " " + user_input
        reply = "👉 Điểm yếu của bạn là gì?"
        st.session_state.step = 2

    # STEP 2
    elif st.session_state.step == 2:
        st.session_state.profile += " " + user_input
        reply = "👉 Bạn thích làm việc với con người hay công nghệ?"
        st.session_state.step = 3

    # STEP 3
    elif st.session_state.step == 3:
        st.session_state.profile += " " + user_input

        text = st.session_state.profile.lower()
        score = {k: 0 for k in hsb}

        if "sáng tạo" in text:
            score["mac"] += 3
        if "giao tiếp" in text:
            score["has"] += 2
            score["hat"] += 2
        if "công nghệ" in text:
            score["met"] += 3
        if "logic" in text:
            score["kinh doanh"] += 3
        if "yếu toán" in text:
            score["kinh doanh"] -= 2

        best = max(score, key=score.get)

        reply = f"🎯 Gợi ý nhanh: {hsb[best]}\n\n"

        ai_text = hoi_ai(st.session_state.profile)

        reply += "🤖 Phân tích AI:\n"
        reply += ai_text

        st.session_state.step = 4

    else:
        reply = "👉 Reload trang để làm lại nhé!"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
