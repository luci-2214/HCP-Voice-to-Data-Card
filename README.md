# Doceree AI Persona Dashboard

> **Voice-to-Segment Architect** — A Command Center for healthcare campaign managers.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red) ![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-orange)

## Features

- 📊 **Real-time KPI metrics** — HCP count, market sentiment, predicted CTR
- 🎙️ **Voice input** — Describe your target persona via microphone
- 🧠 **AI-powered extraction** — Gemini 1.5 Flash extracts specialty, location, prescribing level & campaign focus
- 📈 **Targeting accuracy gauge** — Interactive Plotly visualization
- 📱 **Mobile-responsive** — Works on desktop and mobile browsers

## Quick Start (Local)

```bash
# 1. Clone / navigate to the project
cd doceree_dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Gemini API key
set GEMINI_API_KEY=your-key-here          # Windows CMD
# $env:GEMINI_API_KEY="your-key-here"     # PowerShell
# export GEMINI_API_KEY='your-key-here'   # macOS / Linux

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Deploy on Streamlit Cloud

1. Push this folder to a **GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **"New app"** → select your repo, branch, and `app.py`.
4. In **Advanced settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy**. Done!

> **Note:** On Streamlit Cloud, secrets set via the UI are available as `os.environ` / `st.secrets`.

## Project Structure

```
doceree_dashboard/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .streamlit/
    └── config.toml        # Theme & server config
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ | Google Generative AI API key |

## License

Internal use — Doceree.
