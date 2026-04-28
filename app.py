"""
Doceree AI Persona Dashboard
=============================
A Command Center for healthcare campaign managers focusing on
HCP targeting and programmatic advertising insights.

Sections:
  1. Config & Styling
  2. API Setup (Groq FREE tier + Gemini fallback)
  3. UI Layout
  4. Voice Input Handling (Browser-native STT — zero API cost)
  5. AI Processing
  6. Visualization
"""

import os
import json
import streamlit as st
import plotly.graph_objects as go
from streamlit_mic_recorder import speech_to_text

# ──────────────────────────────────────────────
# 1. CONFIG & STYLING
# ──────────────────────────────────────────────

# Page configuration
st.set_page_config(
    page_title="Doceree AI Persona Dashboard",
    page_icon="👨‍⚕️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme constants
PRIMARY = "#00796B"
PRIMARY_LIGHT = "#009688"
PRIMARY_DARK = "#004D40"
BG_COLOR = "#f8fafc"
CARD_BG = "#ffffff"
TEXT_PRIMARY = "#1e293b"
TEXT_SECONDARY = "#64748b"
SUCCESS_GREEN = "#10b981"
ACCENT_AMBER = "#f59e0b"

# Custom CSS injection for a premium analytics feel
st.markdown(f"""
<style>
    /* ── Global ── */
    .stApp {{
        background-color: {BG_COLOR};
    }}
    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY_DARK};
    }}

    /* ── Header banner ── */
    .header-banner {{
        background: linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY} 50%, {PRIMARY_LIGHT} 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 24px rgba(0,121,107,0.25);
        position: relative;
        overflow: hidden;
    }}
    .header-banner::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }}
    .header-banner h1 {{
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }}
    .header-banner p {{
        margin: 0.4rem 0 0 0;
        font-size: 1rem;
        opacity: 0.85;
        font-weight: 400;
    }}

    /* ── Metric cards ── */
    .metric-card {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.5rem 1.25rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }}
    .metric-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }}
    .metric-label {{
        font-size: 0.8rem;
        color: {TEXT_SECONDARY};
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 800;
        color: {TEXT_PRIMARY};
        line-height: 1.1;
    }}
    .metric-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }}
    .metric-delta.positive {{ color: {SUCCESS_GREEN}; }}
    .metric-delta.amber {{ color: {ACCENT_AMBER}; }}

    /* ── Persona card ── */
    .persona-card {{
        background: {CARD_BG};
        border-left: 5px solid {PRIMARY};
        border-radius: 14px;
        padding: 1.75rem 1.5rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.07);
        margin-top: 1rem;
        margin-bottom: 1rem;
    }}
    .persona-card h3 {{
        color: {PRIMARY_DARK} !important;
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 700;
    }}
    .persona-card .persona-content {{
        color: {TEXT_PRIMARY} !important;
        font-size: 1rem !important;
        line-height: 1.9 !important;
    }}
    .persona-card .persona-content strong {{
        color: {PRIMARY_DARK} !important;
        font-weight: 700;
    }}
    .persona-card ul {{
        padding-left: 1.2rem;
        color: {TEXT_PRIMARY} !important;
        line-height: 1.9;
        list-style-type: none;
    }}
    .persona-card li {{
        margin-bottom: 0.5rem;
        color: {TEXT_PRIMARY} !important;
        font-size: 1rem;
    }}
    .persona-card li::before {{
        content: '•';
        color: {PRIMARY};
        font-weight: bold;
        margin-right: 0.5rem;
    }}

    /* ── Section dividers ── */
    .section-divider {{
        border: none;
        border-top: 2px solid #e2e8f0;
        margin: 2rem 0;
    }}
    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* ── Voice recorder area ── */
    .voice-section {{
        background: {CARD_BG};
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px dashed #cbd5e1;
        text-align: center;
    }}

    /* ── Provider badge ── */
    .provider-badge {{
        display: inline-block;
        background: {PRIMARY};
        color: white;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}

    /* ── Misc tweaks ── */
    div[data-testid="stHorizontalBlock"] > div {{
        padding: 0 0.35rem;
    }}

    /* ── Mobile responsive ── */
    @media (max-width: 768px) {{
        .header-banner {{
            padding: 1.5rem 1rem;
        }}
        .header-banner h1 {{
            font-size: 1.4rem;
        }}
        .metric-value {{
            font-size: 1.5rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 2. API SETUP — Groq (free) / Gemini (fallback)
# ──────────────────────────────────────────────

# Helper: read from st.secrets (Streamlit Cloud) or os.environ (local)
def get_secret(key: str) -> str | None:
    """Get a secret from Streamlit Cloud secrets or environment variables."""
    # Streamlit Cloud stores secrets in st.secrets
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        pass
    # Fallback to environment variable (local dev)
    return os.getenv(key)

# Supported AI backends (checked in priority order)
AI_PROVIDER = None  # Will be set below

def setup_groq():
    """Configure Groq client. Returns (client, model_name) or None."""
    api_key = get_secret("GROQ_API_KEY")
    if not api_key:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        return client
    except ImportError:
        return None

def setup_gemini():
    """Configure Gemini. Returns True if ready."""
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        return True
    except Exception:
        return False

def call_groq(client, prompt: str) -> str:
    """Send text prompt to Groq (Llama 3.1 8B — free tier)."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()

def call_gemini(prompt: str) -> str:
    """Send text prompt to Gemini 2.0 Flash."""
    import google.generativeai as genai
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def call_ai(prompt: str) -> str:
    """
    Call the best available AI backend.
    Priority: Groq (free 14.4k req/day) → Gemini → Error
    """
    # Try Groq first (most generous free tier)
    groq_client = setup_groq()
    if groq_client:
        result = call_groq(groq_client, prompt)
        st.session_state["ai_provider"] = "Groq (Llama 3.1)"
        return result

    # Fallback to Gemini
    if setup_gemini():
        result = call_gemini(prompt)
        st.session_state["ai_provider"] = "Google Gemini"
        return result

    return None


# ──────────────────────────────────────────────
# 3. UI LAYOUT (using placeholders for dynamic updates)
# ──────────────────────────────────────────────

# Initialize default metrics in session state
if "metrics" not in st.session_state:
    st.session_state["metrics"] = {
        "hcp_count": "14.2k",
        "hcp_delta": "▲ +5% vs last quarter",
        "sentiment": "Positive",
        "sentiment_detail": "Confidence: High",
        "ctr": "2.4%",
        "ctr_delta": "▲ +0.2% vs benchmark",
        "accuracy": 85,
        "accuracy_ref": 78,
    }

# Header banner
st.markdown("""
<div class="header-banner">
    <h1>👨‍⚕️ HCP Persona Intelligence by Sumit Yadav</h1>
    <p>Voice-to-Segment Architect &nbsp;|&nbsp; Powered by AI Analytics</p>
</div>
""", unsafe_allow_html=True)

# ── Create placeholders for dynamic sections ──
metrics_placeholder = st.empty()
divider1_placeholder = st.empty()

# ──────────────────────────────────────────────
# 4. VOICE INPUT HANDLING (Browser-native STT — FREE)
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">🎙️ Voice Input — Speak Persona Requirements</div>', unsafe_allow_html=True)

st.markdown('<div class="voice-section">', unsafe_allow_html=True)
st.markdown(
    "Press the microphone button below, describe your **target HCP persona**, "
    "then stop recording. Speech is transcribed **locally in your browser** (no API cost)."
)

# speech_to_text uses the browser's built-in Web Speech API (FREE)
transcript = speech_to_text(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=False,
    use_container_width=True,
    language="en",
    key="voice_stt",
)
st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 5. AI PROCESSING
# ──────────────────────────────────────────────

PERSONA_PROMPT = """You are a healthcare advertising strategist working at Doceree.
A campaign manager just described their target HCP persona via voice.

From the transcription below, extract the following details and present
them as clean, professional bullet points:

• **Specialty** – The medical specialty being targeted (e.g., Cardiology, Oncology).
• **Location** – The geographic region or market.
• **Prescribing Level** – High / Medium / Low prescriber tier.
• **Campaign Focus** – The therapeutic area or drug category of interest.

If any detail is ambiguous or missing, make a reasonable inference based on
context and note it as "Inferred".

Transcription:
{transcript}

Respond ONLY with the four bullet points, nothing else."""

METRICS_PROMPT = """Based on this HCP persona, generate realistic healthcare campaign metrics.

Persona:
{persona}

Respond with ONLY valid JSON, no markdown, no explanation, no code blocks:
{{"hcp_count": "8.5k", "hcp_delta": "▲ +3% vs last quarter", "sentiment": "Positive", "sentiment_detail": "Confidence: High", "ctr": "2.1%", "ctr_delta": "▲ +0.3% vs benchmark", "accuracy": 82}}"""

if transcript:
    # Show what was transcribed
    st.info(f"📝 **Transcribed:** {transcript}")

    # Check if any AI backend is available
    has_groq = bool(get_secret("GROQ_API_KEY"))
    has_gemini = bool(get_secret("GEMINI_API_KEY"))

    if not has_groq and not has_gemini:
        st.error(
            "⚠️ **No AI API key found.** Set at least one:\n\n"
            "**Option A — Groq (recommended, free 14.4k req/day):**\n"
            "```bash\nexport GROQ_API_KEY='your-key-here'\n```\n"
            "Get a free key at [console.groq.com](https://console.groq.com)\n\n"
            "**Option B — Google Gemini:**\n"
            "```bash\nexport GEMINI_API_KEY='your-key-here'\n```"
        )
    else:
        with st.spinner("🧠 AI analyzing voice segment..."):
            try:
                # Step 1: Generate persona
                prompt = PERSONA_PROMPT.replace("{transcript}", transcript)
                persona_text = call_ai(prompt)

                if persona_text:
                    st.session_state["persona_result"] = persona_text

                    # Step 2: Generate dynamic metrics based on persona
                    with st.spinner("📊 Generating campaign metrics..."):
                        metrics_prompt = METRICS_PROMPT.replace("{persona}", persona_text)
                        metrics_raw = call_ai(metrics_prompt)

                        if metrics_raw:
                            try:
                                import re as _re
                                # Extract JSON from response
                                json_match = _re.search(r'\{.*\}', metrics_raw, _re.DOTALL)
                                if json_match:
                                    metrics_data = json.loads(json_match.group())
                                    accuracy_val = int(metrics_data.get("accuracy", 85))
                                    st.session_state["metrics"] = {
                                        "hcp_count": str(metrics_data.get("hcp_count", "14.2k")),
                                        "hcp_delta": str(metrics_data.get("hcp_delta", "▲ +5% vs last quarter")),
                                        "sentiment": str(metrics_data.get("sentiment", "Positive")),
                                        "sentiment_detail": str(metrics_data.get("sentiment_detail", "Confidence: High")),
                                        "ctr": str(metrics_data.get("ctr", "2.4%")),
                                        "ctr_delta": str(metrics_data.get("ctr_delta", "▲ +0.2% vs benchmark")),
                                        "accuracy": accuracy_val,
                                        "accuracy_ref": max(accuracy_val - 7, 50),
                                    }
                                    st.success("✅ Dashboard metrics updated!")
                            except (json.JSONDecodeError, ValueError) as e:
                                st.warning(f"Metrics parsing issue, using defaults. ({e})")
                else:
                    st.error("No AI backend available. Please set GROQ_API_KEY or GEMINI_API_KEY.")

            except Exception as exc:
                st.error(f"AI API error: {exc}")

# ── Display Persona Card ──
if "persona_result" in st.session_state and st.session_state["persona_result"]:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧾 Generated Target Persona</div>', unsafe_allow_html=True)

    provider = st.session_state.get("ai_provider", "AI")
    raw_result = st.session_state["persona_result"]

    import re
    persona_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', raw_result)

    lines = persona_html.split("\n")
    list_items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r'^[•\-\*]\s*', '', line)
        if cleaned:
            list_items.append(f'<li>{cleaned}</li>')

    persona_list_html = '<ul>' + ''.join(list_items) + '</ul>' if list_items else persona_html.replace('\n', '<br>')

    st.markdown(f"""
    <div class="persona-card">
        <span class="provider-badge">Powered by {provider}</span>
        <h3>Generated Target Persona</h3>
        <div class="persona-content">{persona_list_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 6. NOW RENDER METRICS & GAUGE (with latest values)
# ──────────────────────────────────────────────

# Read the (potentially updated) metrics
m = st.session_state["metrics"]

# Fill the metrics placeholder at the top of the page
with metrics_placeholder.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Targeted HCPs</div>
            <div class="metric-value">{m["hcp_count"]}</div>
            <div class="metric-delta positive">{m["hcp_delta"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Market Sentiment</div>
            <div class="metric-value">{m["sentiment"]}</div>
            <div class="metric-delta amber">{m["sentiment_detail"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Predicted CTR</div>
            <div class="metric-value">{m["ctr"]}</div>
            <div class="metric-delta positive">{m["ctr_delta"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Fill the divider placeholder
divider1_placeholder.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# Gauge chart with dynamic value
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Targeting Accuracy</div>', unsafe_allow_html=True)

gauge_value = m["accuracy"]
gauge_ref = m["accuracy_ref"]

fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=gauge_value,
    delta={"reference": gauge_ref, "increasing": {"color": SUCCESS_GREEN}},
    number={"suffix": "%", "font": {"size": 48, "color": TEXT_PRIMARY}},
    title={"text": "Targeting Accuracy Score", "font": {"size": 16, "color": TEXT_SECONDARY}},
    gauge={
        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#e2e8f0", "dtick": 20},
        "bar": {"color": PRIMARY, "thickness": 0.75},
        "bgcolor": "#f1f5f9",
        "borderwidth": 0,
        "steps": [
            {"range": [0, 40], "color": "#fecaca"},
            {"range": [40, 70], "color": "#fde68a"},
            {"range": [70, 100], "color": "#a7f3d0"},
        ],
        "threshold": {
            "line": {"color": PRIMARY_DARK, "width": 4},
            "thickness": 0.8,
            "value": gauge_value,
        },
    },
))

fig.update_layout(
    height=320,
    margin=dict(l=30, r=30, t=60, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"family": "Inter, sans-serif"},
)

st.plotly_chart(fig, use_container_width=True)

# ── Footer ──
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align:center; color:{TEXT_SECONDARY}; font-size:0.8rem; padding:1rem 0;">
        Doceree AI Persona Dashboard &nbsp;•&nbsp; Made by Sumit Yadav
    </div>
    """,
    unsafe_allow_html=True,
)
