import streamlit as st
from openai import OpenAI

# --- Page Config ---
st.set_page_config(
    page_title="✈️ TravelMate AI",
    page_icon="✈️",
    layout="centered",
)

# --- Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    min-height: 100vh;
}

/* Title */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.6rem !important;
    background: linear-gradient(90deg, #f7c59f, #f9e4b7, #ffe0ac);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: 1px;
    padding-top: 0.5rem;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #a8c8d8;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    font-weight: 300;
    letter-spacing: 0.5px;
}

/* API key input */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 12px !important;
    color: #f0f4f8 !important;
    padding: 0.6rem 1rem !important;
}

/* Suggested question section title */
.suggest-title {
    font-family: 'Playfair Display', serif;
    color: #f7c59f;
    font-size: 1.05rem;
    margin-bottom: 0.3rem;
}

.suggest-subtitle {
    color: #7fa8be;
    font-size: 0.82rem;
    margin-bottom: 0.8rem;
    font-weight: 300;
}

/* Suggested buttons */
.stButton > button {
    background: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(247, 197, 159, 0.3) !important;
    border-radius: 14px !important;
    color: #e8d5b7 !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 0.8rem !important;
    transition: all 0.25s ease !important;
    text-align: left !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    line-height: 1.4 !important;
    backdrop-filter: blur(6px) !important;
}
.stButton > button:hover {
    background: rgba(247, 197, 159, 0.18) !important;
    border-color: #f7c59f !important;
    color: #fff7ed !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(247, 197, 159, 0.15) !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 1.2rem 0 !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.5rem !important;
    backdrop-filter: blur(8px) !important;
}

/* Chat input */
[data-testid="stChatInput"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(247, 197, 159, 0.25) !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"] textarea {
    color: #f0f4f8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Info box */
.stAlert {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(247,197,159,0.2) !important;
    border-radius: 12px !important;
    color: #c9dde8 !important;
}

/* Caption */
.stCaption {
    color: #7fa8be !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(247,197,159,0.3); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- System Prompt ---
SYSTEM_PROMPT = """당신은 전문 여행 도우미 AI 'TravelMate'입니다.
사용자가 여행을 계획하고 즐길 수 있도록 도와주는 친절하고 박식한 어시스턴트입니다.

다음 역할을 수행합니다:
- 여행지 추천 및 상세 정보 제공 (명소, 음식, 문화, 날씨, 최적 방문 시기 등)
- 여행 일정 계획 도움 (일별 코스, 동선 최적화)
- 항공권, 숙소, 교통 이용 팁 제공
- 현지 음식 및 레스토랑 추천
- 여행 예산 계획 조언
- 비자, 여행 서류, 안전 정보 안내
- 짐 싸기 팁 및 여행 준비물 안내
- 현지 문화, 예절, 주의사항 설명

응답 스타일:
- 친근하고 열정적인 톤으로 답변
- 구체적이고 실용적인 정보 제공
- 이모지를 적절히 사용해 읽기 쉽게 구성
- 필요하면 리스트나 단계별 설명 활용
- 한국어로 답변 (사용자가 다른 언어 사용 시 해당 언어로)
"""

# --- Header ---
st.markdown("<h1>✈️ TravelMate AI</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">당신의 완벽한 여행을 함께 설계합니다 · Your AI Travel Companion</p>', unsafe_allow_html=True)

# --- API Key ---
openai_api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

if not openai_api_key:
    st.info("🗝️  OpenAI API 키를 입력하면 여행 플래너가 시작됩니다.", icon="✈️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None

    # --- Suggested Questions (only when no messages) ---
    SUGGESTED_QUESTIONS = [
        "🗼 파리 3박 4일 여행 일정 짜줘",
        "🌏 동남아 여행지 추천해줘",
        "🎌 일본 교토 볼거리 알려줘",
        "🏖️ 신혼여행지로 어디가 좋을까?",
        "🎒 유럽 배낭여행 준비물 체크리스트",
        "💰 저예산 해외여행 절약 팁",
        "🍜 베트남 꼭 먹어야 할 음식은?",
        "🛂 태국 여행 비자 정보 알려줘",
    ]

    if not st.session_state.messages:
        st.markdown('<p class="suggest-title">🌐 어디로 떠나고 싶으신가요?</p>', unsafe_allow_html=True)
        st.markdown('<p class="suggest-subtitle">추천 질문을 선택하거나 직접 입력하세요</p>', unsafe_allow_html=True)

        cols = st.columns(2)
        for i, question in enumerate(SUGGESTED_QUESTIONS):
            with cols[i % 2]:
                if st.button(question, key=f"suggested_{i}", use_container_width=True):
                    st.session_state.pending_prompt = question

        st.divider()

    # --- Display chat history ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Handle suggested question click ---
    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # --- Chat input ---
    if prompt := st.chat_input("여행지, 일정, 준비물 등 무엇이든 물어보세요! 🌍"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
