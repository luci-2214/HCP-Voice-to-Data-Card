# HCP AI Persona Dashboard

> **Voice-to-Segment Architect** — A Command Center for healthcare campaign managers.

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red) ![Gemini](https://img.shields.io/badge/Gemini-2.0--Flash-orange) ![Groq](https://img.shields.io/badge/Groq-0.4.0--yellow)

## Features

- 📊 **Real-time KPI metrics** — HCP count, market sentiment, predicted CTR
- 🎙️ **Voice input** — Describe your target persona via microphone
- 🧠 **AI-powered extraction** — Gemini 1.5 Flash extracts specialty, location, prescribing level & campaign focus
- 📈 **Targeting accuracy gauge** — Interactive Plotly visualization
- 📱 **Mobile-responsive** — Works on desktop and mobile browsers

## Quick Start (Local)

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
