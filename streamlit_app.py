import streamlit as st

# ====== CONFIG ======
st.set_page_config(page_title="HSB Chatbot", page_icon="🎓", layout="centered")

# ====== STYLE ======
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #eef2ff, #ffffff);
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ====== DATA ======
hsb_info = {
    "nganh": {
        "mas": "Quản trị và An ninh (MAS)",
        "hat": "Quản trị nhân tài và nhân lực (HAT)",
        "met": "Quản trị doanh nghiệp và công nghệ (MET)",
        "bns": "Quản trị an ninh phi truyền thống (BNS)",
        "mac": "Marketing và truyền thông (MAC)",
        "has": "Quản trị dịch vụ khách hàng và chăm sóc sức khỏe (HAS)",
        "kinh doanh": "Ngành Kinh doanh (Marketing + Phân tích kinh doanh)"
    }
}

# ====== PHÂN TÍCH ======
def phan_tich(cau):
    cau = cau.lower()

    diem = {
        "mac": 0,
        "has": 0,
        "met": 0,
        "mas": 0,
        "hat": 0,
        "kinh doanh": 0,
        "bns": 0
    }

    ly_do = []

    # ===== ĐIỂM MẠNH =====
    if any(x in cau for x in ["sáng tạo", "content", "ý tưởng"]):
        diem["mac"] += 3
        ly_do.append("Bạn có tính sáng tạo → hợp Marketing")

    if any(x in cau for x in ["giao tiếp", "thuyết trình"]):
        diem["has"] += 2
        diem["hat"] += 2
        ly_do.append("Bạn giao tiếp tốt → hợp ngành dịch vụ / nhân sự")

    if any(x in cau for x in ["công nghệ", "it", "startup"]):
        diem["met"] += 3
        ly_do.append("Bạn thích công nghệ → hợp MET")

    if any(x in cau for x in ["logic", "phân tích", "số liệu"]):
        diem["kinh doanh"] += 3
        ly_do.append("Bạn mạnh logic → hợp ngành kinh doanh phân tích")

    if any(x in cau for x in ["giúp người", "dịch vụ"]):
        diem["has"] += 3
        ly_do.append("Bạn thích giúp người → hợp HAS")

    if any(x in cau for x in ["lãnh đạo", "quản lý"]):
        diem["hat"] += 3
        ly_do.append("Bạn có tố chất lãnh đạo → hợp HAT")

    if any(x in cau for x in ["an ninh", "rủi ro"]):
        diem["mas"] += 3
        diem["bns"] += 2
        ly_do.append("Bạn quan tâm an ninh → hợp MAS/BNS")

    # ===== ĐIỂM YẾU =====
    if "yếu toán" in cau:
        diem["kinh doanh"] -= 2
        ly_do.append("Bạn yếu toán → hạn chế ngành phân tích")

    if "ít nói" in cau or "hướng nội" in cau:
        diem["has"] -= 2
        diem["hat"] -= 2
        ly_do.append("Bạn ít giao tiếp → không hợp dịch vụ")

    # ===== XỬ LÝ KẾT QUẢ =====
    sorted_nganh = sorted(diem.items(), key=lambda x: x[1], reverse=True)

    top1 = sorted_nganh[0]
    top2 = sorted_nganh[1]

    tong = sum([max(v, 0) for v in diem.values()]) + 1

    percent1 = int((max(top1[1],0) / tong) * 100)
    percent2 = int((max(top2[1],0) / tong) * 100)

    return top1, top2, percent1, percent2, ly_do

# ====== UI ======
st.title("🎓 Chatbot tư vấn ngành HSB")
st.caption("Nhập điểm mạnh / điểm yếu để được tư vấn")

# ====== CHAT ======
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

# hiển thị chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ====== BOT HỎI NGƯỢC ======
if st.session_state.step == 0:
    st.chat_message("assistant").write("Bạn hãy mô tả điểm mạnh / điểm yếu của bạn (VD: sáng tạo, yếu toán...)")
    st.session_state.step = 1

# ====== INPUT ======
user_input = st.chat_input("Nhập tại đây...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # ====== PHÂN TÍCH ======
    top1, top2, p1, p2, ly_do = phan_tich(user_input)

    nganh1 = hsb_info["nganh"][top1[0]]
    nganh2 = hsb_info["nganh"][top2[0]]

    reply = f"""
🎯 **Ngành phù hợp nhất:** {nganh1} ({p1}%)

🥈 **Gợi ý thêm:** {nganh2} ({p2}%)

📊 **Phân tích:**
"""

    for ld in ly_do:
        reply += f"\n- {ld}"

    reply += "\n\n👉 Bạn có muốn mình phân tích sâu hơn không?"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
