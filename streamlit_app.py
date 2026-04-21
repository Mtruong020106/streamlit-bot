import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# ====== LOAD API KEY ======
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ====== CONFIG ======
st.set_page_config(page_title="HSB AI Advisor", page_icon="🎓")

# ====== STYLE ======
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f0f2f5, #ffffff);
}
</style>
""", unsafe_allow_html=True)

# ====== DATA ======
hsb = {
    "mac": "Marketing & Truyền thông",
    "met": "Công nghệ & Doanh nghiệp",
    "has": "Dịch vụ & Chăm sóc",
    "hat": "Nhân lực & Lãnh đạo",
    "mas": "An ninh & Quản trị",
    "bns": "An ninh phi truyền thống",
    "kinh doanh": "Kinh doanh & Phân tích"
}

# ====== AI ======
def hoi_ai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là chuyên gia tư vấn ngành HSB. Hãy phân tích cực kỳ chi tiết điểm mạnh, điểm yếu, tính cách và gợi ý ngành phù hợp trong 7 ngành HSB."
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI lỗi: {e}"

# ====== INIT ======
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "profile" not in st.session_state:
    st.session_state.profile = ""

# ====== HIỂN THỊ CHAT ======
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ====== BOT HỎI ======
if st.session_state.step == 0:
    msg = "👋 Mình sẽ tư vấn ngành cho bạn.\n\n👉 Bạn hãy mô tả **điểm mạnh** của bạn"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.session_state.step = 1

# ====== INPUT ======
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

        # ===== RULE BASE =====
        text = st.session_state.profile.lower()
        score = {k:0 for k in hsb}

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

        # ===== AI =====
        ai_text = hoi_ai(st.session_state.profile)

        reply += "🤖 Phân tích AI:\n"
        reply += ai_text

        st.session_state.step = 4

    else:
        reply = "👉 Reload để làm lại nhé!"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
