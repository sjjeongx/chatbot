import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=Jost:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif !important;
}

.stApp {
    background: #f5efe6;
}

/* Header */
.travel-header {
    text-align: center;
    padding: 2rem 0 1rem;
}
.travel-header h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: #3d2b1f;
    margin: 0;
    line-height: 1;
}
.travel-header h1 span { color: #c4714a; font-style: italic; }
.travel-header p {
    font-size: 0.78rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8a7060;
    margin-top: 8px;
    font-weight: 300;
}
.divider {
    width: 60px; height: 1px;
    background: linear-gradient(to right, transparent, #c4714a, transparent);
    margin: 12px auto 0;
}

/* API input */
.stTextInput > label { color: #8a7060 !important; font-size: 0.8rem !important; letter-spacing: 1px; }
.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid #e8d9c4 !important;
    border-radius: 40px !important;
    color: #3d2b1f !important;
    padding: 0.55rem 1.2rem !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #c4714a !important;
    box-shadow: 0 0 0 3px rgba(196,113,74,0.08) !important;
}

/* Suggest section */
.suggest-label {
    font-size: 0.7rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #8a7060;
    margin-bottom: 12px;
    margin-top: 28px;
    font-weight: 500;
}

/* Suggest buttons */
div[data-testid="column"] .stButton > button {
    background: white !important;
    border: 1px solid #e8d9c4 !important;
    border-radius: 16px !important;
    color: #3d2b1f !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    padding: 0.85rem 1rem !important;
    text-align: left !important;
    line-height: 1.45 !important;
    transition: all 0.2s ease !important;
    height: auto !important;
    min-height: 72px !important;
    width: 100% !important;
    white-space: normal !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: #c4714a !important;
    box-shadow: 0 6px 20px rgba(196,113,74,0.12) !important;
    transform: translateY(-2px) !important;
    color: #c4714a !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: white !important;
    border: 1px solid #e8d9c4 !important;
    border-radius: 18px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
}

/* Chat input */
[data-testid="stChatInputTextArea"] {
    font-family: 'Jost', sans-serif !important;
    color: #3d2b1f !important;
}
[data-testid="stChatInput"] {
    border: 1px solid #e8d9c4 !important;
    border-radius: 40px !important;
    background: white !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #c4714a !important;
    box-shadow: 0 0 0 3px rgba(196,113,74,0.08) !important;
}

/* Info box */
[data-testid="stAlert"] {
    background: white !important;
    border: 1px solid #e8d9c4 !important;
    border-radius: 14px !important;
    color: #8a7060 !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

SYSTEM_PROMPT = """You are TravelMate, a professional AI travel concierge. Help users plan perfect trips.

Your expertise:
- Destination recommendations with detailed info (attractions, food, culture, weather, best time to visit)
- Day-by-day itinerary planning and route optimization  
- Flight, accommodation, and transportation tips
- Local food and restaurant recommendations
- Budget planning and money-saving tips
- Visa, travel documents, and safety information
- Packing lists and travel preparation guides
- Local culture, etiquette, and customs

Style: Be warm, enthusiastic, and practical. Use emojis naturally. Respond in Korean by default."""

SUGGESTED = [
    ("🗼", "파리 3박 4일 완벽 일정 짜줘"),
    ("🌸", "일본 교토 숨은 명소 추천"),
    ("🏖️", "신혼여행지 베스트 추천"),
    ("🌏", "동남아 여행지 TOP 5"),
    ("💰", "유럽 저예산 여행 절약 팁"),
    ("🍜", "베트남 현지 음식 가이드"),
    ("🎒", "배낭여행 필수 준비물 리스트"),
    ("🛂", "태국·발리 비자 입국 정보"),
]

# Header
st.markdown("""
<div class="travel-header">
  <h1>Travel<span>Mate</span></h1>
  <p>AI 여행 플래너 &middot; Your Journey Starts Here</p>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)

# API Key
openai_api_key = st.text_input("OPENAI API KEY", type="password", placeholder="sk-...")

if not openai_api_key:
    st.info("✈️  API 키를 입력하면 여행 플래너가 시작됩니다.")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending" not in st.session_state:
        st.session_state.pending = None

    # Suggested questions (only when no messages)
    if not st.session_state.messages:
        st.markdown('<div class="suggest-label">✦ 추천 질문</div>', unsafe_allow_html=True)
        rows = [SUGGESTED[:4], SUGGESTED[4:]]
        for row in rows:
            cols = st.columns(4)
            for col, (icon, text) in zip(cols, row):
                with col:
                    if st.button(f"{icon}\n{text}", key=f"s_{text}", use_container_width=True):
                        st.session_state.pending = f"{icon} {text}"
        st.markdown("<br/>", unsafe_allow_html=True)

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Handle suggested question
    if st.session_state.pending:
        prompt = st.session_state.pending
        st.session_state.pending = None
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Chat input
    if prompt := st.chat_input("여행지, 일정, 음식, 비자 등 무엇이든 물어보세요 ✈️"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
