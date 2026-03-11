import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

* { font-family: 'Outfit', sans-serif !important; }

/* BACKGROUND */
.stApp {
    background: #0d1117;
}

/* HEADER */
.tm-header {
    padding: 48px 0 32px;
    text-align: center;
}
.tm-badge {
    display: inline-block;
    background: rgba(56,189,148,0.12);
    border: 1px solid rgba(56,189,148,0.25);
    color: #38bd94;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 40px;
    margin-bottom: 20px;
}
.tm-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #f0f4f8;
    line-height: 1.15;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}
.tm-title span {
    background: linear-gradient(90deg, #38bd94, #5eead4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.tm-sub {
    font-size: 0.92rem;
    color: #6b7a8d;
    font-weight: 300;
}

/* API INPUT */
.stTextInput > label {
    color: #4a5568 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 12px !important;
    color: #e6edf3 !important;
    padding: 0.65rem 1.1rem !important;
    font-size: 0.87rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #38bd94 !important;
    box-shadow: 0 0 0 3px rgba(56,189,148,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #3d4a5c !important; }

/* SUGGEST LABEL */
.suggest-head {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #38bd94;
    margin: 36px 0 14px;
}

/* SUGGEST BUTTONS */
div[data-testid="column"] .stButton > button {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 14px !important;
    color: #c9d1d9 !important;
    font-size: 0.81rem !important;
    font-weight: 400 !important;
    padding: 14px !important;
    text-align: left !important;
    line-height: 1.5 !important;
    height: auto !important;
    min-height: 76px !important;
    width: 100% !important;
    white-space: normal !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #1c2330 !important;
    border-color: #38bd94 !important;
    color: #f0f4f8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
}

/* DIVIDER */
hr {
    border: none !important;
    border-top: 1px solid #21262d !important;
    margin: 28px 0 !important;
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatMessage"] p {
    color: #c9d1d9 !important;
    font-size: 0.9rem !important;
    line-height: 1.75 !important;
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #38bd94 !important;
    box-shadow: 0 0 0 3px rgba(56,189,148,0.08) !important;
}
[data-testid="stChatInputTextArea"] {
    color: #e6edf3 !important;
    font-size: 0.88rem !important;
}
[data-testid="stChatInputTextArea"]::placeholder { color: #3d4a5c !important; }
[data-testid="stChatInputSubmitButton"] > button {
    background: #38bd94 !important;
    border-radius: 10px !important;
}
[data-testid="stChatInputSubmitButton"] > button:hover {
    background: #5eead4 !important;
}

/* FIX: Hide broken Material Icon text in avatars */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    font-size: 0 !important;
    overflow: hidden !important;
}
[data-testid="chatAvatarIcon-assistant"] *,
[data-testid="chatAvatarIcon-user"] * {
    font-size: 0 !important;
    visibility: hidden !important;
}

/* Replace with clean colored dot avatars */
[data-testid="chatAvatarIcon-assistant"] {
    background: #38bd94 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    flex-shrink: 0 !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #6366f1 !important;
    border-radius: 50% !important;
    width: 32px !important; height: 32px !important;
    flex-shrink: 0 !important;
}

/* CHAT MESSAGE ACCENT LINE */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-left: 3px solid #38bd94 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-left: 3px solid #6366f1 !important;
}

/* INFO BOX */
[data-testid="stAlert"] {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 14px !important;
    color: #6b7a8d !important;
}

/* HIDE STREAMLIT UI */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are TravelMate, a world-class AI travel concierge. Your mission: help users plan unforgettable trips.

Expertise:
- Destination recommendations with rich detail (must-see spots, hidden gems, culture, best season)
- Day-by-day itinerary building with optimized routing
- Flight, accommodation and local transport tips
- Food guides from street food to fine dining
- Budget planning and cost-saving strategies
- Visa, entry requirements and safety info
- Packing lists tailored to destination and duration
- Local customs, etiquette and cultural tips

Tone: Enthusiastic, knowledgeable, concise. Use emojis naturally. Always respond in Korean."""

SUGGESTIONS = [
    ("✈️", "파리 3박 4일 완벽 여행 일정"),
    ("🌸", "일본 교토 숨은 명소 추천"),
    ("🏝️", "신혼여행지 베스트 5"),
    ("🌏", "동남아 여행지 TOP 추천"),
    ("💸", "유럽 저예산 절약 꿀팁"),
    ("🍜", "베트남 현지 음식 가이드"),
    ("🎒", "배낭여행 준비물 리스트"),
    ("🛂", "태국·발리 비자 입국 정보"),
]

# HEADER
st.markdown("""
<div class="tm-header">
    <div class="tm-badge">✦ AI Travel Concierge</div>
    <div class="tm-title">여행을 <span>더 쉽게</span>,<br>더 특별하게.</div>
    <div class="tm-sub">목적지부터 일정, 음식, 예산까지 &mdash; 당신만의 여행을 설계해드립니다</div>
</div>
""", unsafe_allow_html=True)

# API KEY
openai_api_key = st.text_input("OPENAI API KEY", type="password", placeholder="sk-...")

if not openai_api_key:
    st.info("🔑  API 키를 입력하면 TravelMate가 시작됩니다.")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending" not in st.session_state:
        st.session_state.pending = None

    # SUGGESTIONS
    if not st.session_state.messages:
        st.markdown('<div class="suggest-head">추천 질문</div>', unsafe_allow_html=True)
        for row_start in range(0, len(SUGGESTIONS), 4):
            row = SUGGESTIONS[row_start:row_start + 4]
            cols = st.columns(4)
            for col, (icon, text) in zip(cols, row):
                with col:
                    if st.button(f"{icon}  {text}", key=f"sq_{text}", use_container_width=True):
                        st.session_state.pending = f"{icon} {text}"
        st.markdown("<hr/>", unsafe_allow_html=True)

    # CHAT HISTORY
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # PENDING SUGGESTION
    if st.session_state.pending:
        prompt = st.session_state.pending
        st.session_state.pending = None
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # CHAT INPUT
    if prompt := st.chat_input("여행지, 일정, 음식, 비자 등 무엇이든 물어보세요 ✈️"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})