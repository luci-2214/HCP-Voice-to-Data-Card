"""
Doceree AI Persona Dashboard
=============================
A Command Center for healthcare campaign managers focusing on
HCP targeting and programmatic advertising insights.

Sections:
  1. Config & Styling
  2. API Setup
  3. UI Layout
  4. Voice Input Handling
  5. AI Processing
  6. Visualization
"""

import os
import io
import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

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
        color: {PRIMARY_DARK};
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 700;
    }}
    .persona-card ul {{
        padding-left: 1.2rem;
        color: {TEXT_PRIMARY};
        line-height: 1.8;
    }}
    .persona-card li {{
        margin-bottom: 0.3rem;
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
# 2. API SETUP
# ──────────────────────────────────────────────

def configure_gemini() -> bool:
    """
    Configure Google Generative AI with the API key from the environment.
    Returns True if configuration succeeds.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True


def get_gemini_model():
    """Return a Gemini 1.5 Flash model instance."""
    return genai.GenerativeModel("gemini-2.0-flash-lite")


# ──────────────────────────────────────────────
# 3. UI LAYOUT
# ──────────────────────────────────────────────

# Header banner
st.markdown("""
<div class="header-banner">
    <h1>👨‍⚕️ HCP Persona Intelligence</h1>
    <p>Voice-to-Segment Architect &nbsp;|&nbsp; Powered by AI Analytics</p>
</div>
""", unsafe_allow_html=True)

# ── Top Metrics Row ──
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Targeted HCPs</div>
        <div class="metric-value">14.2k</div>
        <div class="metric-delta positive">▲ +5% vs last quarter</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Market Sentiment</div>
        <div class="metric-value">Positive</div>
        <div class="metric-delta amber">Confidence: High</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Predicted CTR</div>
        <div class="metric-value">2.4%</div>
        <div class="metric-delta positive">▲ +0.2% vs benchmark</div>
    </div>
    """, unsafe_allow_html=True)

# Divider
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 4. VOICE INPUT HANDLING
# ──────────────────────────────────────────────

st.markdown('<div class="section-title">🎙️ Voice Input — Speak Persona Requirements</div>', unsafe_allow_html=True)

st.markdown('<div class="voice-section">', unsafe_allow_html=True)
st.markdown("Press the microphone button below, describe your **target HCP persona**, then stop recording.")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹️ Stop Recording",
    just_once=False,
    use_container_width=True,
    key="voice_recorder",
)
st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 5. AI PROCESSING
# ──────────────────────────────────────────────

PERSONA_PROMPT = """
You are a healthcare advertising strategist working at Doceree.
A campaign manager just described their target HCP persona via voice.

From the audio transcription below, extract the following details and present
them as clean, professional bullet points:

• **Specialty** – The medical specialty being targeted (e.g., Cardiology, Oncology).
• **Location** – The geographic region or market.
• **Prescribing Level** – High / Medium / Low prescriber tier.
• **Campaign Focus** – The therapeutic area or drug category of interest.

If any detail is ambiguous or missing, make a reasonable inference based on
context and note it as "Inferred".

Audio transcription / content:
{audio_content}

Respond ONLY with the four bullet points, nothing else.
"""

if audio and audio.get("bytes"):
    gemini_ready = configure_gemini()

    if not gemini_ready:
        st.error(
            "⚠️ **GEMINI_API_KEY not found.** "
            "Set the `GEMINI_API_KEY` environment variable before running the app.\n\n"
            "```bash\nexport GEMINI_API_KEY='your-key-here'\n```"
        )
    else:
        with st.spinner("🧠 AI analyzing voice segment..."):
            try:
                model = get_gemini_model()

                # Upload audio bytes to Gemini for multimodal processing
                audio_bytes = audio["bytes"]
                audio_part = {
                    "mime_type": "audio/wav",
                    "data": audio_bytes,
                }

                response = model.generate_content(
                    [
                        PERSONA_PROMPT.replace("{audio_content}", "(see attached audio)"),
                        audio_part,
                    ]
                )

                persona_text = response.text.strip()

                # Store in session state so it persists across reruns
                st.session_state["persona_result"] = persona_text

            except Exception as exc:
                st.error(f"Gemini API error: {exc}")

# ── Display Persona Card ──
if "persona_result" in st.session_state and st.session_state["persona_result"]:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧾 Generated Target Persona</div>', unsafe_allow_html=True)

    persona_html = st.session_state["persona_result"].replace("\n", "<br>")
    st.markdown(f"""
    <div class="persona-card">
        <h3>Generated Target Persona</h3>
        <div>{persona_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 6. VISUALIZATION
# ──────────────────────────────────────────────

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Targeting Accuracy</div>', unsafe_allow_html=True)

# Plotly Gauge Chart
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=85,
    delta={"reference": 78, "increasing": {"color": SUCCESS_GREEN}},
    number={"suffix": "%", "font": {"size": 48, "color": TEXT_PRIMARY}},
    title={"text": "Targeting Accuracy Score", "font": {"size": 16, "color": TEXT_SECONDARY}},
    gauge={
        "axis": {
            "range": [0, 100],
            "tickwidth": 1,
            "tickcolor": "#e2e8f0",
            "dtick": 20,
        },
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
            "value": 85,
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
        Doceree AI Persona Dashboard &nbsp;•&nbsp; Built with Streamlit &amp; Gemini AI
    </div>
    """,
    unsafe_allow_html=True,
)
