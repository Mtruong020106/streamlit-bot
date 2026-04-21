import streamlit as st

# ====== CONFIG ======
st.set_page_config(page_title="HSB AI Advisor", page_icon="🎓", layout="centered")

# ====== STYLE ======
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
}
.chat-user {
    background-color: #0084ff;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.chat-bot {
    background-color: #e4e6eb;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# ====== DATA ======
hsb = {
    "mac": {"ten": "Marketing & Truyền thông", "desc": "Sáng tạo, content, truyền thông"},
    "met": {"ten": "Công nghệ & Doanh nghiệp", "desc": "Startup, công nghệ, đổi mới"},
    "has": {"ten": "Dịch vụ & Chăm sóc", "desc": "Giao tiếp, chăm sóc, phục vụ"},
    "hat": {"ten": "Nhân lực & Lãnh đạo", "desc": "Quản lý con người, lãnh đạo"},
    "mas": {"ten": "An ninh & Quản trị", "desc": "Logic, kiểm soát rủi ro"},
    "bns": {"ten": "An ninh phi truyền thống", "desc": "Xã hội, an ninh hiện đại"},
    "kinh doanh": {"ten": "Kinh doanh & Phân tích", "desc": "Logic, số liệu, kinh doanh"}
}

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

# ====== BOT FLOW ======

if st.session_state.step == 0:
    msg = "👋 Mình sẽ giúp bạn chọn ngành HSB.\n\n👉 Bạn hãy mô tả **điểm mạnh** của bạn (ví dụ: sáng tạo, giao tiếp tốt, thích công nghệ...)"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.session_state.step = 1

# ====== INPUT ======
user_input = st.chat_input("Nhập tại đây...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ====== STEP 1 ======
    if st.session_state.step == 1:
        st.session_state.profile += " " + user_input
        reply = "👍 Ok. Giờ cho mình biết **điểm yếu** của bạn? (vd: yếu toán, ngại giao tiếp...)"
        st.session_state.step = 2

    # ====== STEP 2 ======
    elif st.session_state.step == 2:
        st.session_state.profile += " " + user_input
        reply = "👉 Bạn thích làm việc với:\n- con người\n- máy tính/công nghệ\n- hay làm việc độc lập?"
        st.session_state.step = 3

    # ====== STEP 3 ======
    elif st.session_state.step == 3:
        st.session_state.profile += " " + user_input
        reply = "👉 Bạn có chịu được áp lực cao không? (có / không / trung bình)"
        st.session_state.step = 4

    # ====== STEP 4 ======
    elif st.session_state.step == 4:
        st.session_state.profile += " " + user_input

        # ====== PHÂN TÍCH ======
        text = st.session_state.profile.lower()

        score = {k:0 for k in hsb}
        explain = []

        # sáng tạo
        if "sáng tạo" in text:
            score["mac"] += 3
            explain.append("Bạn sáng tạo → cực hợp Marketing")

        # giao tiếp
        if "giao tiếp" in text:
            score["has"] += 2
            score["hat"] += 2
            explain.append("Bạn giao tiếp tốt → hợp dịch vụ / nhân sự")

        # công nghệ
        if "công nghệ" in text or "it" in text:
            score["met"] += 3
            explain.append("Bạn thích công nghệ → hợp MET")

        # logic
        if "logic" in text or "phân tích" in text:
            score["kinh doanh"] += 3
            explain.append("Bạn có tư duy logic → hợp ngành phân tích")

        # yếu toán
        if "yếu toán" in text:
            score["kinh doanh"] -= 2
            explain.append("Bạn yếu toán → hạn chế ngành phân tích")

        # hướng nội
        if "hướng nội" in text:
            score["has"] -= 2
            explain.append("Bạn hướng nội → không hợp ngành giao tiếp nhiều")

        # áp lực
        if "không" in text and "áp lực" in text:
            score["mac"] -= 1
            explain.append("Bạn không thích áp lực → nên tránh ngành cạnh tranh cao")

        # ====== SORT ======
        sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)

        best = sorted_score[0]
        second = sorted_score[1]

        reply = "📊 **PHÂN TÍCH CHI TIẾT**\n\n"

        for e in explain:
            reply += f"- {e}\n"

        reply += "\n📈 **ĐIỂM TỪNG NGÀNH:**\n"
        for k,v in sorted_score:
            reply += f"- {hsb[k]['ten']}: {v} điểm\n"

        reply += f"\n🎯 **KẾT LUẬN:**\n👉 Ngành phù hợp nhất: **{hsb[best[0]]['ten']}**\n"
        reply += f"👉 Gợi ý thêm: **{hsb[second[0]]['ten']}**\n\n"

        reply += "💡 " + hsb[best[0]]["desc"]

        st.session_state.step = 5

    else:
        reply = "👉 Reload để tư vấn lại nhé!"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
