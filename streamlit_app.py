import streamlit as st
from groq import Groq
import json, re, html as html_lib

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="HSB Tư Vấn Tuyển Sinh",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================================================
# CONSTANTS
# =========================================================
HSB_MAJORS = [
    "Marketing & Truyền thông",
    "Công nghệ & Doanh nghiệp",
    "Dịch vụ & Chăm sóc",
    "Nhân lực & Lãnh đạo",
    "An ninh & Quản trị",
    "An ninh phi truyền thống",
    "Kinh doanh & Phân tích"
]

MAJOR_ICONS = {
    "Marketing & Truyền thông":   "📣",
    "Công nghệ & Doanh nghiệp":   "💻",
    "Dịch vụ & Chăm sóc":        "🤝",
    "Nhân lực & Lãnh đạo":       "👥",
    "An ninh & Quản trị":         "🛡️",
    "An ninh phi truyền thống":   "🌐",
    "Kinh doanh & Phân tích":     "📊",
}

# =========================================================
# FLOW
# =========================================================
FLOW = [
    {
        "type": "question",
        "key": "intro",
        "text": "👋 Chào bạn! Mình là cố vấn tuyển sinh HSB.\n\nMình sẽ hỏi bạn một vài câu để hiểu rõ hơn — không có đúng sai đâu nhé, cứ trả lời tự nhiên thôi 😊\n\n**Bạn đang học lớp mấy, và điều khiến bạn băn khoăn nhất khi chọn ngành là gì?**"
    },
    {
        "type": "question",
        "key": "academics",
        "text": "Cảm ơn bạn đã chia sẻ! 📚\n\n**Học lực của bạn đang như thế nào?** Bạn học khối nào, môn nào mạnh nhất, môn nào yếu nhất?\n\n*(Không cần điểm chính xác, ước lượng cũng được)*"
    },
    {
        "type": "question",
        "key": "strength",
        "text": "**Điểm mạnh lớn nhất của bạn là gì?** 💪\n\n*(ví dụ: giao tiếp tốt, tư duy logic, sáng tạo, kỷ luật, lãnh đạo, cảm xúc tốt…)*"
    },
    {
        "type": "question",
        "key": "weakness",
        "text": "Thành thật vậy là tốt lắm! 🙏\n\n**Điểm yếu lớn nhất của bạn là gì?**\n\nĐừng ngại — mình cần biết để tư vấn thật sự phù hợp, không phải để đánh giá bạn đâu."
    },
    {
        "type": "checkpoint",
        "key": "checkpoint_1",
        "spinner": "✨ Đang đọc hồ sơ của bạn...",
        "prompt_template": """Dựa trên thông tin sau của học sinh:
- Băn khoăn: {intro}
- Học lực/môn mạnh-yếu: {academics}
- Điểm mạnh: {strength}
- Điểm yếu: {weakness}

Hãy viết 2–3 câu nhận xét ngắn, ấm áp, mang tính cá nhân hóa cao — như thể mày đang nói chuyện trực tiếp với học sinh. KHÔNG phân tích ngành, KHÔNG đưa ra kết luận. Chỉ nhận xét về con người họ một cách tinh tế, khen đúng chỗ, rồi hỏi tiếp:

"**Bạn hứng thú với lĩnh vực nào nhất?**
(công nghệ / kinh doanh / truyền thông / con người & xã hội / an ninh / sáng tạo… hoặc nếu chưa biết cũng nói nhé)"

Tiếng Việt, tự nhiên, KHÔNG dùng markdown quá nhiều."""
    },
    {
        "type": "question",
        "key": "interest",
        "text": None
    },
    {
        "type": "question",
        "key": "workstyle",
        "text": "**Bạn thích làm việc với Con Người hay với Dữ liệu/Công nghệ?** 🤔\n\nHoặc cả hai đều thích? Hay chưa chắc? Cứ nói thật nhé."
    },
    {
        "type": "question",
        "key": "career_goal",
        "text": "Gần xong rồi! 🎯\n\n**5–10 năm nữa bạn muốn làm gì, hoặc muốn trở thành người như thế nào?**\n\nKhông cần cụ thể, kể cả 'chưa biết' cũng được — nhưng nếu có hình dung gì dù mờ nhạt, cứ kể mình nghe."
    },
    {
        "type": "question",
        "key": "family",
        "text": "**Gia đình bạn có định hướng gì cho việc chọn ngành không?** 👨‍👩‍👦\n\nVí dụ: muốn bạn nối nghiệp, muốn ngành ổn định, hay để bạn tự quyết? Và gia đình có thể hỗ trợ tài chính ở mức nào?"
    },
    {
        "type": "question",
        "key": "experience",
        "text": "Câu cuối cùng! 🏁\n\n**Bạn đã từng làm thêm, tham gia CLB, dự án, hay hoạt động ngoại khóa nào chưa?**\n\nNếu có, kể cho mình nghe — đây thường là manh mối quan trọng nhất để hiểu bạn thật sự phù hợp với gì."
    },
    {
        "type": "checkpoint",
        "key": "checkpoint_2",
        "spinner": "🔍 Đang tổng hợp toàn bộ hồ sơ...",
        "prompt_template": """Dựa trên toàn bộ hồ sơ học sinh:
- Băn khoăn ban đầu: {intro}
- Học lực: {academics}
- Điểm mạnh: {strength}
- Điểm yếu: {weakness}
- Hứng thú: {interest}
- Phong cách làm việc: {workstyle}
- Mục tiêu nghề nghiệp: {career_goal}
- Gia đình & tài chính: {family}
- Trải nghiệm thực tế: {experience}

Viết đoạn TÓM TẮT HỒ SƠ (3–4 câu), như thể mày đang đọc to cho học sinh nghe để họ xác nhận — bắt đầu bằng "Để mình tóm tắt lại những gì mình hiểu về bạn nhé...". Giọng ấm áp, cụ thể, mang tính cá nhân cao. KHÔNG đưa ra kết quả ngành. Kết thúc bằng: "Bây giờ mình sẽ phân tích kỹ và đưa ra kết quả chi tiết cho bạn nhé! 🎯"

Tiếng Việt, tự nhiên."""
    },
    {
        "type": "final",
        "key": "result"
    }
]

TOTAL_QUESTIONS = sum(1 for s in FLOW if s["type"] == "question" and s.get("text") is not None)

# =========================================================
# CSS — PREMIUM CORPORATE
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --navy:        #0b2545;
    --navy-mid:    #163d6e;
    --navy-light:  #1e5ca8;
    --navy-pale:   #e8f0fb;
    --gold:        #c9a44a;
    --gold-light:  #f0d883;
    --gold-pale:   #fdf8ec;
    --white:       #ffffff;
    --off-white:   #f2f5f9;
    --text:        #111827;
    --text-mid:    #374151;
    --text-muted:  #6b7280;
    --border:      #dde3ec;
    --border-dark: #b8c4d4;
    --green:       #059669;
    --green-pale:  #ecfdf5;
    --red-pale:    #fef2f2;
    --shadow-sm:   0 1px 4px rgba(11,37,69,0.08);
    --shadow-md:   0 4px 16px rgba(11,37,69,0.10);
    --shadow-lg:   0 8px 32px rgba(11,37,69,0.14);
}

* { box-sizing: border-box; }

.stApp {
    background: var(--off-white) !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 0 !important;
    max-width: 800px !important;
    margin: 0 auto !important;
}

/* HEADER */
.hsb-header {
    background: linear-gradient(140deg, #0b2545 0%, #163d6e 50%, #1e5ca8 100%);
    padding: 0;
    border-radius: 0 0 28px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-lg);
    overflow: hidden;
    position: relative;
}
.hsb-header-inner {
    padding: 30px 36px 26px;
    position: relative;
    z-index: 2;
}
.hsb-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(201,164,74,0.15) 0%, transparent 65%);
    border-radius: 50%;
    z-index: 1;
}
.hsb-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 65%);
    border-radius: 50%;
    z-index: 1;
}
.hsb-top-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 14px;
}
.hsb-logo-circle {
    width: 52px; height: 52px;
    background: rgba(255,255,255,0.12);
    border: 1.5px solid rgba(255,255,255,0.2);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    flex-shrink: 0;
    backdrop-filter: blur(8px);
}
.hsb-title-block { flex: 1; }
.hsb-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 2px;
    line-height: 1.2;
    letter-spacing: -0.01em;
}
.hsb-tagline {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.55);
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hsb-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    margin: 0 0 16px;
}

/* PROGRESS */
.progress-outer {
    padding: 0 36px 20px;
    background: linear-gradient(140deg, #0b2545 0%, #163d6e 50%, #1e5ca8 100%);
    border-radius: 0 0 28px 28px;
    margin-top: -28px;
    padding-top: 28px;
}
.progress-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.progress-label {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.5);
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.progress-count {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.75);
    font-weight: 600;
}
.progress-track {
    background: rgba(255,255,255,0.12);
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
}
.progress-fill {
    background: linear-gradient(90deg, #4fa3e0, #c9a44a);
    border-radius: 99px;
    height: 100%;
    transition: width 0.7s cubic-bezier(.4,0,.2,1);
    box-shadow: 0 0 8px rgba(79,163,224,0.5);
}

/* CHAT */
.chat-area {
    padding: 4px 20px 0;
}

div[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
    border: none !important;
    box-shadow: none !important;
}

/* Assistant */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px 18px 18px 18px !important;
    padding: 14px 18px !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text) !important;
    font-size: 0.915rem !important;
    line-height: 1.72 !important;
    max-width: 90% !important;
}

/* User */
div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: linear-gradient(135deg, var(--navy), var(--navy-mid)) !important;
    border-radius: 18px 6px 18px 18px !important;
    padding: 12px 18px !important;
    color: #ffffff !important;
    font-size: 0.915rem !important;
    line-height: 1.65 !important;
    max-width: 78% !important;
    margin-left: auto !important;
    box-shadow: var(--shadow-md) !important;
}

/* CHAT INPUT */
div[data-testid="stChatInput"] {
    border-radius: 14px !important;
    border: 1.5px solid var(--border) !important;
    box-shadow: var(--shadow-md) !important;
    margin: 14px 20px 22px !important;
    background: var(--white) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: var(--navy-light) !important;
    box-shadow: 0 0 0 3px rgba(30,92,168,0.14), var(--shadow-md) !important;
}
div[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.915rem !important;
    color: var(--text) !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
}

.stSpinner > div { color: var(--navy-light) !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hsb-header">
  <div class="hsb-header-inner">
    <div class="hsb-top-row">
      <div class="hsb-logo-circle">🎓</div>
      <div class="hsb-title-block">
        <p class="hsb-brand">HSB Admission Counselor</p>
        <p class="hsb-tagline">Hệ thống tư vấn tuyển sinh thông minh</p>
      </div>
    </div>
    <div class="hsb-divider"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "messages": [],
    "flow_step": 0,
    "profile": {},
    "done": False,
    "q_count": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# PROGRESS BAR
# =========================================================
pct   = int((st.session_state.q_count / TOTAL_QUESTIONS) * 100) if not st.session_state.done else 100
label = "Hoàn tất ✓" if st.session_state.done else f"Câu {st.session_state.q_count} / {TOTAL_QUESTIONS}"

st.markdown(f"""
<div style="padding: 0 36px 20px; margin-top:-4px;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
    <span style="font-size:0.72rem; color:#6b7280; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;">Tiến trình tư vấn</span>
    <span style="font-size:0.78rem; color:#374151; font-weight:600;">{label}</span>
  </div>
  <div style="background:#e5e9f0; border-radius:99px; height:5px; overflow:hidden;">
    <div style="width:{pct}%; height:100%; background:linear-gradient(90deg,#1e5ca8,#c9a44a); border-radius:99px; transition:width 0.7s;"></div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# AI HELPERS
# =========================================================
def call_groq(system: str, user: str, max_tokens: int = 800, is_json: bool = False) -> str:
    for model in ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"]:
        try:
            kwargs = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user",   "content": user}
                ],
                "temperature": 0.7,
                "max_tokens": max_tokens,
            }
            if is_json:
                kwargs["response_format"] = {"type": "json_object"}

            r = client.chat.completions.create(**kwargs)
            return r.choices[0].message.content
        except Exception as e:
            print(f"Lỗi gọi Groq ({model}):", e)
            continue
    return "⚠️ Lỗi kết nối AI. Vui lòng thử lại."


def generate_checkpoint(template: str, profile: dict) -> str:
    keys = re.findall(r"\{(\w+)\}", template)
    safe = {k: profile.get(k, "chưa có") for k in keys}
    prompt = template.format(**safe)
    return call_groq(
        system="Bạn là cố vấn tuyển sinh ấm áp, nói chuyện tự nhiên như người thật. Tiếng Việt.",
        user=prompt,
        max_tokens=420
    )


def build_profile_text(profile: dict) -> str:
    labels = {
        "intro":       "Băn khoăn ban đầu",
        "academics":   "Học lực & môn mạnh/yếu",
        "strength":    "Điểm mạnh",
        "weakness":    "Điểm yếu",
        "interest":    "Lĩnh vực hứng thú",
        "workstyle":   "Phong cách làm việc",
        "career_goal": "Mục tiêu nghề nghiệp",
        "family":      "Định hướng & nguồn lực gia đình",
        "experience":  "Trải nghiệm thực tế",
    }
    return "\n".join(f"- {labels.get(k, k)}: {v}" for k, v in profile.items())


def generate_final_analysis(profile: dict):
    profile_text = build_profile_text(profile)
    majors_list  = "\n".join(f"- {m}" for m in HSB_MAJORS)

    system = f"""Bạn là CỐ VẤN TUYỂN SINH chuyên nghiệp, sắc bén, ấm áp.

HỒ SƠ HỌC SINH:
{profile_text}

NGÀNH HỢP LỆ:
{majors_list}

NHIỆM VỤ: Trả về ĐÚNG JSON sau, KHÔNG có markdown, KHÔNG có text thêm:
{{
  "personality": "3 câu nhận xét tâm lý sâu, cá nhân hóa cao, không chung chung",
  "personality_tags": ["tag1", "tag2", "tag3"],
  "top_major": "tên ngành phù hợp nhất (đúng tên trong danh sách)",
  "top_reason": "5-6 câu lý giải cụ thể, thuyết phục, liên hệ trực tiếp tính cách/học lực/mục tiêu/gia đình",
  "career_paths": ["công việc 1", "công việc 2", "công việc 3", "công việc 4", "công việc 5"],
  "scores": [
    {{"major": "tên ngành", "score": 8, "comment": "nhận xét 1 câu cụ thể liên quan hồ sơ"}},
    ...đủ 7 ngành...
  ],
  "strengths_match": ["điểm mạnh học sinh phù hợp với ngành 1", "điểm mạnh 2"],
  "watch_out": "1 câu cảnh báo thực tế — điều học sinh cần lưu ý hoặc cải thiện khi theo ngành này",
  "tips": ["lời khuyên cụ thể 1", "lời khuyên cụ thể 2", "lời khuyên cụ thể 3"],
  "followup": "1-2 câu hỏi gợi mở tự nhiên để tiếp tục hội thoại"
}}

QUY TẮC BẮT BUỘC:
- Mảng career_paths BẮT BUỘC phải chứa ĐÚNG 5 gợi ý công việc tương lai chi tiết nhất dựa trên hồ sơ.
- Điểm số PHẢI phân hóa mạnh (có ngành 3-5 điểm, có ngành 8-9 điểm, không dàn đều). Điểm là một số từ 1-10.
- Không bịa ngành mới.
- Chỉ trả về JSON thuần hợp lệ. Tiếng Việt."""

    raw = call_groq(system=system, user="Phân tích hồ sơ và trả về JSON chuẩn.", max_tokens=2000, is_json=True)
    
    try:
        return json.loads(raw)
    except Exception as e:
        print("Lỗi parse từ is_json:", e)
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        return raw


def generate_followup(profile: dict, user_msg: str) -> str:
    profile_text = build_profile_text(profile)
    majors_list  = "\n".join(f"- {m}" for m in HSB_MAJORS)
    system = f"""Bạn là cố vấn tuyển sinh HSB chuyên nghiệp, ấm áp.

Hồ sơ học sinh:
{profile_text}

Ngành hợp lệ: {majors_list}

Trả lời câu hỏi/yêu cầu của học sinh một cách cụ thể, cá nhân hóa dựa trên hồ sơ đã có. Tiếng Việt tự nhiên, không quá ngắn."""
    return call_groq(system=system, user=user_msg, max_tokens=900)


# =========================================================
# RESULT CARD RENDERER
# =========================================================
def render_result_card(data: dict) -> str:
    def safe_escape(val):
        if isinstance(val, list):
            val = " ".join(str(v) for v in val)
        elif val is None or isinstance(val, dict):
            val = ""
        return html_lib.escape(str(val))
    
    e = safe_escape
    
    def ensure_list(val):
        if isinstance(val, list): return val
        if isinstance(val, str): return [val]
        return []

    raw_scores = data.get("scores", [])
    if not isinstance(raw_scores, list):
        raw_scores = [raw_scores] if isinstance(raw_scores, dict) else []

    def parse_score(item):
        try:
            return float(item.get("score", 0)) if isinstance(item, dict) else 0
        except (ValueError, TypeError):
            return 0

    scores = sorted([s for s in raw_scores if isinstance(s, dict)], key=parse_score, reverse=True)
    top_major = data.get("top_major", "")

    tags_html = ""
    for tag in ensure_list(data.get("personality_tags", [])):
        tags_html += f'<span style="display:inline-block;background:#e8f0fb;color:#163d6e;font-size:0.72rem;font-weight:600;padding:3px 10px;border-radius:99px;margin:0 4px 4px 0;letter-spacing:0.03em;">{e(tag)}</span>'

    bars_html = ""
    for item in scores:
        major   = str(item.get("major", ""))
        score   = parse_score(item)
        comment = item.get("comment", "")
        pct     = min(100, max(0, int(score * 10))) 
        display_score = f"{int(score)}" if score.is_integer() else f"{score}"
        icon    = MAJOR_ICONS.get(major, "📌")
        is_top  = (major == top_major)

        if is_top:
            wrap_style  = "background:linear-gradient(135deg,#e8f0fb,#dceaf9);border:1.5px solid #1e5ca8;border-radius:12px;padding:12px 16px;margin-bottom:10px;"
            name_style  = "font-weight:700;color:#0b2545;font-size:0.9rem;"
            bar_color   = "linear-gradient(90deg,#1e5ca8,#4fa3e0)"
            score_style = "font-weight:800;color:#0b2545;font-size:0.88rem;"
            badge       = '<span style="background:#0b2545;color:#fff;font-size:0.62rem;padding:2px 8px;border-radius:99px;margin-left:8px;letter-spacing:0.06em;vertical-align:middle;">✓ TỐT NHẤT</span>'
        else:
            wrap_style  = "background:#fff;border:1px solid #dde3ec;border-radius:12px;padding:12px 16px;margin-bottom:8px;"
            name_style  = "font-weight:500;color:#374151;font-size:0.88rem;"
            bar_color   = "linear-gradient(90deg,#93b8d8,#c9a44a)" if score >= 6 else "linear-gradient(90deg,#c8d4e0,#d4c4a0)"
            score_style = "font-weight:700;color:#6b7280;font-size:0.85rem;"
            badge       = ""

        bars_html += f"""<div style="{wrap_style}">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
<span style="{name_style}">{icon} {e(major)}{badge}</span>
<span style="{score_style}">{display_score}/10</span>
</div>
<div style="background:#e2e8f0;border-radius:99px;height:6px;margin-bottom:6px;overflow:hidden;">
<div style="width:{pct}%;height:100%;background:{bar_color};border-radius:99px;"></div>
</div>
<div style="font-size:0.77rem;color:#6b7280;line-height:1.5;">{e(comment)}</div>
</div>"""

    paths_html = ""
    for cp in ensure_list(data.get("career_paths", [])):
        paths_html += f'<div style="display:flex;align-items:center;gap:8px;padding:7px 0;border-bottom:1px solid #f0f4f8;"><span style="color:#1e5ca8;font-size:0.8rem;">▸</span><span style="font-size:0.86rem;color:#374151;">{e(cp)}</span></div>'

    sm_html = ""
    for sm in ensure_list(data.get("strengths_match", [])):
        sm_html += f'<div style="display:flex;align-items:flex-start;gap:8px;margin-bottom:6px;"><span style="color:#059669;font-size:0.85rem;margin-top:1px;">✓</span><span style="font-size:0.86rem;color:#374151;">{e(sm)}</span></div>'

    tips_html = ""
    for i, tip in enumerate(ensure_list(data.get("tips", [])), 1):
        tips_html += f'<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;"><div style="min-width:22px;height:22px;background:#0b2545;color:#fff;border-radius:50%;font-size:0.72rem;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px;">{i}</div><div style="font-size:0.87rem;color:#374151;line-height:1.6;">{e(tip)}</div></div>'

    watch_out = data.get("watch_out", "")

    card = f"""<div style="font-family:'Inter',Arial,sans-serif;max-width:740px;margin:0 auto;">
<div style="background:linear-gradient(140deg,#0b2545 0%,#163d6e 55%,#1e5ca8 100%);border-radius:18px;padding:26px 28px 22px;margin-bottom:14px;position:relative;overflow:hidden;">
<div style="position:absolute;top:-50px;right:-50px;width:200px;height:200px;background:radial-gradient(circle,rgba(201,164,74,0.18) 0%,transparent 65%);border-radius:50%;"></div>
<div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(255,255,255,0.55);margin-bottom:6px;font-weight:600;">Kết quả phân tích cá nhân</div>
<div style="font-size:1.35rem;font-weight:800;color:#fff;letter-spacing:-0.02em;margin-bottom:10px;">Hồ sơ của bạn đã sẵn sàng ✓</div>
<div style="height:1px;background:linear-gradient(90deg,rgba(255,255,255,0.2),transparent);margin-bottom:14px;"></div>
<div style="font-size:0.88rem;color:rgba(255,255,255,0.85);line-height:1.7;">{e(data.get("personality",""))}</div>
<div style="margin-top:12px;">{tags_html}</div>
</div>

<div style="background:#fff;border:1.5px solid #1e5ca8;border-radius:18px;padding:24px 28px;margin-bottom:14px;position:relative;overflow:hidden;">
<div style="position:absolute;top:0;left:0;width:5px;height:100%;background:linear-gradient(180deg,#0b2545,#1e5ca8);border-radius:18px 0 0 18px;"></div>
<div style="padding-left:8px;">
<div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#1e5ca8;font-weight:700;margin-bottom:6px;">🎯 Ngành phù hợp nhất</div>
<div style="font-size:1.5rem;font-weight:800;color:#0b2545;letter-spacing:-0.02em;margin-bottom:4px;">{MAJOR_ICONS.get(top_major,"📌")} {e(top_major)}</div>
<div style="height:1px;background:#e8f0fb;margin:12px 0;"></div>
<div style="font-size:0.89rem;color:#374151;line-height:1.75;">{e(data.get("top_reason",""))}</div>
</div>
</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
<div style="background:#fff;border:1px solid #dde3ec;border-radius:16px;padding:20px 22px;">
<div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#6b7280;font-weight:700;margin-bottom:12px;">💼 5 Công việc đề xuất</div>
{paths_html}
</div>
<div style="background:#ecfdf5;border:1px solid #a7f3d0;border-radius:16px;padding:20px 22px;">
<div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#059669;font-weight:700;margin-bottom:12px;">✅ Điểm mạnh phù hợp</div>
{sm_html}
</div>
</div>

<div style="background:#fff;border:1px solid #dde3ec;border-radius:18px;padding:22px 24px;margin-bottom:14px;">
<div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#6b7280;font-weight:700;margin-bottom:16px;">📊 Mức độ phù hợp tất cả ngành</div>
{bars_html}
</div>

<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:14px;padding:16px 22px;margin-bottom:14px;display:flex;gap:12px;align-items:flex-start;">
<span style="font-size:1.1rem;margin-top:1px;">⚠️</span>
<div>
<div style="font-size:0.72rem;letter-spacing:0.1em;text-transform:uppercase;color:#92400e;font-weight:700;margin-bottom:4px;">Lưu ý quan trọng</div>
<div style="font-size:0.87rem;color:#78350f;line-height:1.6;">{e(watch_out)}</div>
</div>
</div>

<div style="background:#fff;border:1px solid #dde3ec;border-radius:18px;padding:22px 24px;margin-bottom:14px;">
<div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#6b7280;font-weight:700;margin-bottom:16px;">💡 Lời khuyên thực tế</div>
{tips_html}
</div>

<div style="background:linear-gradient(135deg,#f2f5f9,#e8f0fb);border:1px solid #dde3ec;border-radius:14px;padding:18px 22px;display:flex;gap:12px;align-items:flex-start;">
<span style="font-size:1rem;margin-top:2px;">💬</span>
<div style="font-size:0.88rem;color:#374151;line-height:1.7;">{e(data.get("followup","Bạn muốn tìm hiểu thêm điều gì về ngành này không?"))}</div>
</div>
</div>"""
    return card


# =========================================================
# INIT
# =========================================================
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": FLOW[0]["text"]
    })

# =========================================================
# RENDER CHAT
# =========================================================
st.markdown('<div class="chat-area">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("content") == "__RESULT_CARD__":
            st.markdown(msg["html"], unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# INPUT
# =========================================================
ph = "Nhập câu trả lời của bạn..." if not st.session_state.done else "Hỏi thêm bất cứ điều gì..."
user_input = st.chat_input(ph)

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ── Done → open chat ──
    if st.session_state.done:
        with st.spinner("🔄 Đang xử lý..."):
            reply = generate_followup(st.session_state.profile, user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # ── In flow ──
    else:
        fs   = st.session_state.flow_step
        step = FLOW[fs] if fs < len(FLOW) else None

        if step and step["type"] == "question":
            st.session_state.profile[step["key"]] = user_input
            if step.get("text") is not None:
                st.session_state.q_count += 1
            st.session_state.flow_step += 1

        # advance flow
        while st.session_state.flow_step < len(FLOW):
            nxt = FLOW[st.session_state.flow_step]

            if nxt["type"] == "checkpoint":
                with st.spinner(nxt["spinner"]):
                    cp = generate_checkpoint(nxt["prompt_template"], st.session_state.profile)
                st.session_state.messages.append({"role": "assistant", "content": cp})
                st.session_state.flow_step += 1

                # skip question with text=None (already embedded in checkpoint)
                if st.session_state.flow_step < len(FLOW):
                    after = FLOW[st.session_state.flow_step]
                    if after["type"] == "question" and after["text"] is None:
                        break
                break

            elif nxt["type"] == "final":
                with st.spinner("🧠 Đang phân tích toàn diện hồ sơ của bạn..."):
                    result = generate_final_analysis(st.session_state.profile)

                if isinstance(result, dict):
                    st.session_state.messages.append({
                        "role":    "assistant",
                        "content": "__RESULT_CARD__",
                        "html":    render_result_card(result)
                    })
                else:
                    st.session_state.messages.append({
                        "role":    "assistant",
                        "content": f"## 🎯 Kết quả tư vấn\n\n{result}\n\n---\n*💬 Hỏi thêm bất cứ điều gì bạn muốn.*"
                    })

                st.session_state.done = True
                st.session_state.flow_step += 1
                break

            elif nxt["type"] == "question" and nxt["text"] is not None:
                st.session_state.messages.append({"role": "assistant", "content": nxt["text"]})
                break

            else:
                st.session_state.flow_step += 1

    st.rerun()
