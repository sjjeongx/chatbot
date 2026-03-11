<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>TravelMate · AI 여행 플래너</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet" />
<style>
  :root {
    --sand: #f5efe6;
    --warm: #e8d9c4;
    --terracotta: #c4714a;
    --terra-light: #e8956d;
    --deep: #1a1208;
    --mid: #3d2b1f;
    --muted: #8a7060;
    --accent: #d4a36a;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Jost', sans-serif;
    background: var(--sand);
    color: var(--deep);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ── BACKGROUND TEXTURE ── */
  body::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
      radial-gradient(ellipse 80% 60% at 10% 90%, rgba(196,113,74,.08) 0%, transparent 60%),
      radial-gradient(ellipse 60% 80% at 90% 10%, rgba(212,163,106,.10) 0%, transparent 55%),
      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  /* ── SIDEBAR ── */
  .sidebar {
    position: fixed; left: 0; top: 0; bottom: 0;
    width: 72px;
    background: var(--deep);
    display: flex; flex-direction: column; align-items: center;
    padding: 28px 0 24px;
    gap: 32px;
    z-index: 10;
  }
  .sidebar-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    color: var(--accent);
    writing-mode: vertical-rl;
    text-orientation: mixed;
    letter-spacing: 4px;
    transform: rotate(180deg);
    opacity: .9;
  }
  .sidebar-line {
    width: 1px; flex: 1;
    background: linear-gradient(to bottom, transparent, var(--muted), transparent);
  }
  .sidebar-icon {
    font-size: 1.2rem;
    opacity: .4;
    cursor: pointer;
    transition: opacity .2s;
  }
  .sidebar-icon:hover { opacity: .9; }

  /* ── MAIN LAYOUT ── */
  .main {
    margin-left: 72px;
    display: flex; flex-direction: column;
    height: 100vh;
    position: relative; z-index: 1;
  }

  /* ── HEADER ── */
  .header {
    padding: 28px 48px 20px;
    border-bottom: 1px solid rgba(138,112,96,.15);
    display: flex; align-items: flex-end; justify-content: space-between;
    flex-shrink: 0;
  }
  .header-left h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    line-height: 1;
    color: var(--mid);
    letter-spacing: -0.5px;
  }
  .header-left h1 em {
    font-style: italic;
    color: var(--terracotta);
  }
  .header-left p {
    font-size: .78rem;
    color: var(--muted);
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-top: 6px;
    font-weight: 300;
  }
  .api-pill {
    display: flex; align-items: center; gap: 10px;
  }
  .api-pill input {
    border: 1px solid var(--warm);
    background: white;
    border-radius: 40px;
    padding: 9px 18px;
    font-family: 'Jost', sans-serif;
    font-size: .82rem;
    color: var(--mid);
    outline: none;
    width: 220px;
    transition: border-color .2s, box-shadow .2s;
  }
  .api-pill input:focus {
    border-color: var(--terracotta);
    box-shadow: 0 0 0 3px rgba(196,113,74,.08);
  }
  .api-pill input::placeholder { color: var(--muted); opacity: .7; }
  .api-status {
    width: 8px; height: 8px; border-radius: 50%;
    background: #ccc;
    transition: background .3s;
    flex-shrink: 0;
  }
  .api-status.active { background: #6dbf8a; box-shadow: 0 0 6px rgba(109,191,138,.5); }

  /* ── CHAT AREA ── */
  .chat-wrap {
    flex: 1;
    overflow-y: auto;
    padding: 32px 48px;
    display: flex; flex-direction: column; gap: 20px;
    scroll-behavior: smooth;
  }
  .chat-wrap::-webkit-scrollbar { width: 4px; }
  .chat-wrap::-webkit-scrollbar-thumb { background: var(--warm); border-radius: 4px; }

  /* ── WELCOME / SUGGESTIONS ── */
  .welcome {
    flex: 1;
    display: flex; flex-direction: column;
    justify-content: center;
    padding: 32px 48px 16px;
    animation: fadeUp .6s ease both;
  }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .welcome-eyebrow {
    font-size: .72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--terracotta);
    margin-bottom: 12px;
    font-weight: 500;
  }
  .welcome-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.2rem, 4vw, 3.4rem);
    font-weight: 300;
    color: var(--mid);
    line-height: 1.18;
    margin-bottom: 10px;
  }
  .welcome-title em { font-style: italic; color: var(--terracotta); }
  .welcome-sub {
    font-size: .88rem; color: var(--muted); font-weight: 300; margin-bottom: 36px;
    line-height: 1.7;
    max-width: 460px;
  }

  .suggest-label {
    font-size: .68rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
    font-weight: 500;
  }
  .suggest-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    max-width: 800px;
  }
  .suggest-btn {
    background: white;
    border: 1px solid var(--warm);
    border-radius: 16px;
    padding: 14px 16px;
    cursor: pointer;
    text-align: left;
    transition: all .22s ease;
    position: relative;
    overflow: hidden;
  }
  .suggest-btn::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(196,113,74,.06), transparent);
    opacity: 0;
    transition: opacity .22s;
  }
  .suggest-btn:hover {
    border-color: var(--terracotta);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(196,113,74,.12);
  }
  .suggest-btn:hover::after { opacity: 1; }
  .suggest-btn .icon { font-size: 1.4rem; margin-bottom: 6px; display: block; }
  .suggest-btn .text {
    font-size: .80rem;
    color: var(--mid);
    line-height: 1.4;
    font-weight: 400;
  }

  /* ── MESSAGES ── */
  .msg {
    display: flex; gap: 14px;
    animation: fadeUp .3s ease both;
    max-width: 820px;
  }
  .msg.user { flex-direction: row-reverse; align-self: flex-end; }
  .msg-avatar {
    width: 36px; height: 36px; border-radius: 50%;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: .9rem;
    font-weight: 500;
  }
  .msg.assistant .msg-avatar {
    background: var(--deep); color: var(--accent);
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
  }
  .msg.user .msg-avatar {
    background: var(--terracotta); color: white;
    font-size: .8rem;
  }
  .msg-bubble {
    padding: 14px 18px;
    border-radius: 18px;
    font-size: .88rem;
    line-height: 1.75;
    max-width: 72%;
  }
  .msg.assistant .msg-bubble {
    background: white;
    border: 1px solid var(--warm);
    border-bottom-left-radius: 4px;
    color: var(--mid);
    box-shadow: 0 2px 12px rgba(0,0,0,.04);
  }
  .msg.user .msg-bubble {
    background: var(--terracotta);
    color: white;
    border-bottom-right-radius: 4px;
  }

  /* typing indicator */
  .typing-dots {
    display: flex; gap: 5px; align-items: center; padding: 4px 2px;
  }
  .typing-dots span {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--muted);
    animation: bounce 1.2s infinite ease;
  }
  .typing-dots span:nth-child(2) { animation-delay: .15s; }
  .typing-dots span:nth-child(3) { animation-delay: .3s; }
  @keyframes bounce {
    0%,60%,100% { transform: translateY(0); opacity: .4; }
    30% { transform: translateY(-6px); opacity: 1; }
  }

  /* ── INPUT BAR ── */
  .input-bar {
    padding: 16px 48px 28px;
    flex-shrink: 0;
    border-top: 1px solid rgba(138,112,96,.12);
    background: rgba(245,239,230,.85);
    backdrop-filter: blur(12px);
  }
  .input-inner {
    display: flex; align-items: center; gap: 12px;
    background: white;
    border: 1px solid var(--warm);
    border-radius: 40px;
    padding: 10px 14px 10px 22px;
    transition: border-color .2s, box-shadow .2s;
  }
  .input-inner:focus-within {
    border-color: var(--terracotta);
    box-shadow: 0 0 0 4px rgba(196,113,74,.07);
  }
  .input-inner textarea {
    flex: 1; border: none; outline: none; resize: none;
    font-family: 'Jost', sans-serif;
    font-size: .88rem;
    color: var(--mid);
    background: transparent;
    max-height: 120px;
    line-height: 1.6;
  }
  .input-inner textarea::placeholder { color: var(--muted); opacity: .7; }
  .send-btn {
    width: 40px; height: 40px; border-radius: 50%;
    background: var(--terracotta);
    border: none; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: background .2s, transform .15s;
    color: white;
    font-size: 1rem;
  }
  .send-btn:hover { background: var(--terra-light); transform: scale(1.05); }
  .send-btn:disabled { background: var(--warm); cursor: default; transform: none; }
  .input-hint {
    text-align: center;
    font-size: .72rem;
    color: var(--muted);
    margin-top: 10px;
    opacity: .7;
    letter-spacing: .5px;
  }

  /* responsive */
  @media (max-width: 700px) {
    .sidebar { width: 0; overflow: hidden; }
    .main { margin-left: 0; }
    .header, .welcome, .chat-wrap, .input-bar { padding-left: 20px; padding-right: 20px; }
    .suggest-grid { grid-template-columns: repeat(2, 1fr); }
    .header-left h1 { font-size: 2rem; }
  }
</style>
</head>
<body>

<!-- SIDEBAR -->
<aside class="sidebar">
  <div class="sidebar-logo">TM</div>
  <div class="sidebar-line"></div>
  <div class="sidebar-icon" title="여행지">🌍</div>
  <div class="sidebar-icon" title="일정">🗓</div>
  <div class="sidebar-icon" title="음식">🍜</div>
  <div class="sidebar-icon" title="숙소">🏨</div>
  <div class="sidebar-line"></div>
</aside>

<!-- MAIN -->
<div class="main">
  <!-- HEADER -->
  <header class="header">
    <div class="header-left">
      <h1>Travel<em>Mate</em></h1>
      <p>AI 여행 플래너 · Your Journey Starts Here</p>
    </div>
    <div class="api-pill">
      <input type="password" id="apiKey" placeholder="OpenAI API Key (sk-…)" />
      <div class="api-status" id="apiStatus"></div>
    </div>
  </header>

  <!-- WELCOME / SUGGESTIONS -->
  <div class="welcome" id="welcome">
    <div class="welcome-eyebrow">✦ AI 여행 컨시어지</div>
    <div class="welcome-title">어디로<br/><em>떠나고</em> 싶으신가요?</div>
    <p class="welcome-sub">
      여행지 추천부터 세부 일정, 현지 음식, 예산까지 —<br/>
      당신만의 완벽한 여행을 함께 설계해드립니다.
    </p>

    <div class="suggest-label">추천 질문</div>
    <div class="suggest-grid" id="suggestGrid">
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🗼</span>
        <span class="text">파리 3박 4일 완벽 여행 일정 짜줘</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🌸</span>
        <span class="text">일본 교토 숨은 명소 추천해줘</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🏖️</span>
        <span class="text">신혼여행지로 어디가 가장 좋을까?</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🌏</span>
        <span class="text">동남아 여행지 TOP 5 추천</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">💰</span>
        <span class="text">유럽 저예산 여행 절약 팁 알려줘</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🍜</span>
        <span class="text">베트남 현지 음식 추천 & 주의사항</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🎒</span>
        <span class="text">배낭여행 필수 준비물 체크리스트</span>
      </button>
      <button class="suggest-btn" onclick="sendSuggestion(this)">
        <span class="icon">🛂</span>
        <span class="text">태국·발리 비자 & 입국 정보</span>
      </button>
    </div>
  </div>

  <!-- CHAT MESSAGES -->
  <div class="chat-wrap" id="chatWrap" style="display:none;"></div>

  <!-- INPUT BAR -->
  <div class="input-bar">
    <div class="input-inner">
      <textarea id="userInput" rows="1"
        placeholder="여행지, 일정, 음식, 비자 등 무엇이든 물어보세요 ✈️"
        onInput="autoResize(this)"
        onKeydown="handleKey(event)"></textarea>
      <button class="send-btn" id="sendBtn" onclick="sendMessage()" disabled>➤</button>
    </div>
    <div class="input-hint">Enter 전송 · Shift+Enter 줄바꿈</div>
  </div>
</div>

<script>
const SYSTEM_PROMPT = `당신은 전문 여행 컨시어지 AI 'TravelMate'입니다. 사용자가 꿈꾸는 여행을 현실로 만들어드립니다.

역할:
- 여행지 추천 & 상세 정보 (명소, 음식, 문화, 날씨, 최적 시기)
- 여행 일정 계획 (일별 코스, 동선 최적화)
- 항공권·숙소·교통 팁
- 현지 음식 & 레스토랑 추천
- 예산 계획 & 절약 팁
- 비자·여행 서류·안전 정보
- 짐 싸기 & 준비물 가이드
- 현지 문화·예절·주의사항

스타일: 친근하고 열정적으로, 구체적·실용적 정보를 이모지와 함께 제공합니다. 한국어로 답변합니다.`;

let messages = [];
let isLoading = false;

const apiKeyInput = document.getElementById('apiKey');
const apiStatus = document.getElementById('apiStatus');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const welcome = document.getElementById('welcome');
const chatWrap = document.getElementById('chatWrap');

apiKeyInput.addEventListener('input', () => {
  const hasKey = apiKeyInput.value.trim().length > 10;
  apiStatus.className = 'api-status' + (hasKey ? ' active' : '');
  updateSendBtn();
});

userInput.addEventListener('input', updateSendBtn);

function updateSendBtn() {
  sendBtn.disabled = !apiKeyInput.value.trim() || !userInput.value.trim() || isLoading;
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) sendMessage();
  }
}

function sendSuggestion(btn) {
  const text = btn.querySelector('.text').textContent.trim();
  userInput.value = text;
  sendMessage();
}

function showChat() {
  welcome.style.display = 'none';
  chatWrap.style.display = 'flex';
  chatWrap.style.flexDirection = 'column';
}

function appendMsg(role, content) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = role === 'assistant' ? 'TM' : 'ME';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = content.replace(/\n/g, '<br/>');

  div.appendChild(avatar);
  div.appendChild(bubble);
  chatWrap.appendChild(div);
  chatWrap.scrollTop = chatWrap.scrollHeight;
  return bubble;
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'msg assistant';
  div.id = 'typing';
  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = 'TM';
  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
  div.appendChild(avatar);
  div.appendChild(bubble);
  chatWrap.appendChild(div);
  chatWrap.scrollTop = chatWrap.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

async function sendMessage() {
  const key = apiKeyInput.value.trim();
  const text = userInput.value.trim();
  if (!key || !text || isLoading) return;

  showChat();
  appendMsg('user', text);
  messages.push({ role: 'user', content: text });

  userInput.value = '';
  userInput.style.height = 'auto';
  isLoading = true;
  updateSendBtn();
  showTyping();

  try {
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${key}`
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          ...messages
        ],
        stream: true
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.error?.message || 'API 오류');
    }

    removeTyping();
    const bubble = appendMsg('assistant', '');
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let full = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n').filter(l => l.startsWith('data: '));
      for (const line of lines) {
        const data = line.slice(6);
        if (data === '[DONE]') break;
        try {
          const json = JSON.parse(data);
          const delta = json.choices?.[0]?.delta?.content || '';
          full += delta;
          bubble.innerHTML = full.replace(/\n/g, '<br/>');
          chatWrap.scrollTop = chatWrap.scrollHeight;
        } catch {}
      }
    }
    messages.push({ role: 'assistant', content: full });

  } catch (err) {
    removeTyping();
    appendMsg('assistant', `⚠️ 오류가 발생했습니다: ${err.message}`);
  } finally {
    isLoading = false;
    updateSendBtn();
  }
}
</script>
</body>
</html>
