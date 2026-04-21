
import streamlit as st


# ====== (TÙY CHỌN) AI ======
USE_AI = False
try:
    from openai import OpenAI
    client = OpenAI(api_key="YOUR_API_KEY")  # thay nếu dùng
    USE_AI = True
except:
    USE_AI = False

def hoi_ai(cau_hoi):
    if not USE_AI:
        return "Mình chưa hiểu rõ, bạn có thể hỏi cụ thể hơn về HSB nhé 🤔"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Bạn là chatbot tư vấn tuyển sinh của HSB (ĐHQGHN), trả lời ngắn gọn, dễ hiểu"
            },
            {"role": "user", "content": cau_hoi}
        ]
    )
    return response.choices[0].message.content


# ====== DATA HSB ======
hsb_info = {
    "ten": "Trường Quản trị và Kinh doanh (HSB - ĐHQGHN)",
    "nganh": {
        "marketing": "Marketing",
        "kinh doanh": "Kinh doanh quốc tế",
        "nhân lực": "Quản trị nhân lực",
        "quan ly": "Quản trị doanh nghiệp"
    },
    "hoc_phi": "60-80 triệu/năm",
    "to_hop": ["D01", "A01", "C14"],
    "diem_chuan": 20,
    "mo_ta": "Trường đào tạo theo hướng thực tiễn, năng động, phù hợp với người thích kinh doanh"
}


# ====== UI ======
st.set_page_config(page_title="Chatbot HSB", layout="centered")

st.title("🎓 Chatbot tư vấn HSB")

# sidebar
st.sidebar.title("Thông tin nhanh")
st.sidebar.write("📍 HSB - ĐHQGHN")
st.sidebar.write("💰 60-80 triệu/năm")
st.sidebar.write("📚 Marketing, KDQT, Nhân lực")

# lưu lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# hiển thị chat cũ
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# nhập chat
user_input = st.chat_input("Hỏi về HSB...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    cau = user_input.lower()

    # ====== LOGIC ======
    if "ngành" in cau:
        reply = "HSB có các ngành: " + ", ".join(hsb_info["nganh"].values())

    elif "học phí" in cau:
        reply = "Học phí khoảng: " + hsb_info["hoc_phi"]

    elif "khối" in cau or "tổ hợp" in cau:
        reply = "Xét các tổ hợp: " + ", ".join(hsb_info["to_hop"])

    elif "giới thiệu" in cau:
        reply = hsb_info["mo_ta"]

    elif "có nên học" in cau:
        reply = "Nếu bạn thích môi trường năng động, thực tế thì HSB rất đáng cân nhắc 👍"

    elif "tư vấn" in cau:
        reply = "Bạn hãy nhập theo dạng: [sở thích] + [điểm] (VD: marketing 22)"

    # ====== TƯ VẤN THÔNG MINH ======
    elif any(x in cau for x in ["marketing", "kinh doanh", "nhân lực", "quan ly"]):
        words = cau.split()
        diem = None

        for w in words:
            if w.isdigit():
                diem = int(w)

        if diem is None:
            reply = "Bạn hãy nhập thêm điểm nhé (VD: marketing 22)"
        else:
            if diem >= hsb_info["diem_chuan"]:
                for key in hsb_info["nganh"]:
                    if key in cau:
                        reply = f"Bạn hợp ngành {hsb_info['nganh'][key]} tại HSB 🎯"
                        break
                else:
                    reply = "Bạn có thể học Quản trị doanh nghiệp"
            else:
                reply = "Điểm của bạn hơi thấp, nên cố gắng thêm để vào HSB"

    # ====== FALLBACK AI ======
    else:
        reply = hoi_ai(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
