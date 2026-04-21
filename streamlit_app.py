import streamlit as st
from groq import Groq

# =========================================================
# 1. CONFIG HỆ THỐNG
# =========================================================
st.set_page_config(
    page_title="HSB Admission Counselor System",
    page_icon="🎓",
    layout="centered"
)

# Khởi tạo AI client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# 2. GIAO DIỆN (UI STYLE - GIỐNG APP TUYỂN SINH)
# =========================================================
st.markdown("""
<style>
/* nền tổng thể */
.stApp {
    background: linear-gradient(135deg, #eef2f7, #ffffff);
    font-family: Arial;
}

/* tiêu đề */
h1 {
    text-align: center;
    color: #1f4e79;
}

/* chat bubble */
div[data-testid="stChatMessage"] {
    padding: 10px;
    border-radius: 10px;
}

/* input box */
div[data-testid="stChatInput"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 HSB AI Admission Counselor System")
st.caption("Hệ thống tư vấn tuyển sinh mô phỏng cố vấn thật 1:1")

# =========================================================
# 3. DANH SÁCH NGÀNH (KHÓA CỨNG - KHÔNG ĐƯỢC THAY ĐỔI)
# =========================================================
HSB_MAJOR_LIST = [
    "Marketing & Truyền thông",
    "Công nghệ & Doanh nghiệp",
    "Dịch vụ & Chăm sóc",
    "Nhân lực & Lãnh đạo",
    "An ninh & Quản trị",
    "An ninh phi truyền thống",
    "Kinh doanh & Phân tích"
]

# =========================================================
# 4. MODEL AI (FALLBACK AN TOÀN)
# =========================================================
MODEL_LIST = [
    "llama-3.1-8b-instant"
]

# =========================================================
# 5. AI COUNSELOR ENGINE (QUAN TRỌNG NHẤT)
# =========================================================
def generate_counseling(profile_text: str, extra_input: str = None):
    """
    Hàm này chịu trách nhiệm:
    - Gửi dữ liệu học sinh cho AI
    - Ép AI chỉ chọn trong 7 ngành HSB
    - Trả về phân tích giống tư vấn viên thật
    """

    # nếu có câu hỏi bổ sung → cập nhật profile
    if extra_input:
        profile_text = profile_text + "\n\nThông tin bổ sung từ học sinh: " + extra_input

    system_prompt = f"""
Bạn là một CỐ VẤN TUYỂN SINH ĐẠI HỌC CHUYÊN NGHIỆP.

========================================
🎯 NHIỆM VỤ
========================================
- Phân tích tính cách học sinh
- Đánh giá mức độ phù hợp ngành học
- Chỉ chọn trong danh sách 7 ngành HSB

========================================
📌 DANH SÁCH NGÀNH HỢP LỆ (BẮT BUỘC)
========================================
{HSB_MAJOR_LIST}

❌ TUYỆT ĐỐI KHÔNG:
- Không tạo ngành mới
- Không gợi ý ngành ngoài danh sách
- Không nói lan man ngoài phạm vi

========================================
🧠 PHONG CÁCH TRẢ LỜI
========================================
- Giống tư vấn viên thật (không máy móc)
- Có phân tích logic + cảm xúc
- Không trả lời quá ngắn
- Có chiều sâu

========================================
📊 CẤU TRÚC BẮT BUỘC
========================================
1. Phân tích tính cách học sinh
2. Bảng đánh giá 7 ngành (0-10)
3. Chọn 1 ngành phù hợp nhất
4. Giải thích lý do chọn
5. Hỏi ngược lại 1–2 câu để hiểu sâu hơn

========================================
⚠️ QUAN TRỌNG
========================================
Nếu thiếu dữ liệu → phải hỏi lại thay vì đoán.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_LIST[0],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": profile_text}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Lỗi hệ thống AI: {e}"


# =========================================================
# 6. SESSION STATE (LƯU TRẠNG THÁI HỘI THOẠI)
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = 0

if "profile" not in st.session_state:
    st.session_state.profile = ""

# =========================================================
# 7. INTRO - LÀM QUEN (GIỐNG TƯ VẤN VIÊN THẬT)
# =========================================================
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": (
            "👋 Xin chào bạn!\n\n"
            "Mình là cố vấn tuyển sinh HSB.\n\n"
            "Trước khi tư vấn ngành học, mình muốn hiểu bạn rõ hơn một chút 😊\n\n"
            "👉 Bạn đang học lớp mấy?\n"
            "👉 Điều khiến bạn băn khoăn nhất khi chọn ngành là gì?"
        )
    })

    st.session_state.step = 0


# =========================================================
# 8. HIỂN THỊ CHAT
# =========================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================================================
# 9. INPUT NGƯỜI DÙNG
# =========================================================
user_input = st.chat_input("Nhập câu trả lời của bạn...")

if user_input:

    # lưu user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # =====================================================
    # STEP 0 - LÀM QUEN
    # =====================================================
    if st.session_state.step == 0:
        st.session_state.profile += " Thông tin ban đầu: " + user_input

        reply = (
            "👍 Cảm ơn bạn đã chia sẻ.\n\n"
            "Mình đã hiểu sơ bộ về bạn rồi.\n\n"
            "Bây giờ mình sẽ bắt đầu phân tích sâu hơn nhé.\n\n"
            "👉 Câu 1: Điểm mạnh lớn nhất của bạn là gì?"
        )

        st.session_state.step = 1

    # =====================================================
    # STEP 1 - ĐIỂM MẠNH
    # =====================================================
    elif st.session_state.step == 1:
        st.session_state.profile += " Điểm mạnh: " + user_input
        reply = "👉 Câu 2: Điểm yếu lớn nhất của bạn là gì?"
        st.session_state.step = 2

    # =====================================================
    # STEP 2 - ĐIỂM YẾU
    # =====================================================
    elif st.session_state.step == 2:
        st.session_state.profile += " Điểm yếu: " + user_input
        reply = "👉 Câu 3: Bạn thích lĩnh vực nào nhất (công nghệ / kinh doanh / xã hội / sáng tạo)?"
        st.session_state.step = 3

    # =====================================================
    # STEP 3 - SỞ THÍCH
    # =====================================================
    elif st.session_state.step == 3:
        st.session_state.profile += " Sở thích: " + user_input
        reply = "👉 Câu 4: Bạn thích làm việc với CON NGƯỜI hay CÔNG NGHỆ?"
        st.session_state.step = 4

    # =====================================================
    # STEP 4 - AI PHÂN TÍCH LẦN 1
    # =====================================================
    elif st.session_state.step == 4:
        st.session_state.profile += " Môi trường: " + user_input

        with st.spinner("🧠 Cố vấn đang phân tích hồ sơ..."):
            ai_result = generate_counseling(st.session_state.profile)

        reply = (
            "## 🎯 KẾT QUẢ PHÂN TÍCH BAN ĐẦU\n\n"
            + ai_result +
            "\n\n---\n👉 Bạn có muốn mình hỏi thêm để tối ưu kết quả không?"
        )

        st.session_state.step = 5

    # =====================================================
    # STEP 5 - TƯ DUY LẠI (GIỐNG TƯ VẤN VIÊN THẬT)
    # =====================================================
    else:
        with st.spinner("🔄 Cố vấn đang xem xét lại hồ sơ..."):
            ai_result = generate_counseling(st.session_state.profile, user_input)

        reply = (
            "## 🔄 PHÂN TÍCH CẬP NHẬT (SAU KHI HỎI THÊM)\n\n"
            + ai_result +
            "\n\n💡 Nếu bạn muốn, mình có thể phân tích sâu từng ngành chi tiết hơn."
        )

    # lưu assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # reload UI
    st.rerun()
