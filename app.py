#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LifeHaven Care Portal — by ReubenSoul4peaceunity

import os
import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
from datetime import datetime
import folium
from streamlit_folium import st_folium
import sqlite3
import speech_recognition as sr
from fpdf import FPDF
from gtts import gTTS
import streamlit as st

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LifeHaven Care Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Luxury Dark Teal + Gold Theme
# ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg0:     #020d0f;
    --bg1:     #061418;
    --bg2:     #0a1f24;
    --bg3:     #0f2d34;
    --teal:    #00c9a7;
    --teal2:   #00e5c0;
    --gold:    #f5c842;
    --gold2:   #ffe082;
    --sky:     #7ee8fa;
    --text:    #eaf6f4;
    --muted:   rgba(234,246,244,0.62);
    --glass:   rgba(255,255,255,0.055);
    --border:  rgba(255,255,255,0.09);
    --radius:  20px;
    --shadow:  0 24px 64px rgba(0,0,0,0.45);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg0) !important;
    color: var(--text) !important;
}

/* Animated starfield background */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%, rgba(0,201,167,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%, rgba(245,200,66,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(126,232,250,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

.block-container { padding-top: 1.2rem; padding-bottom: 3rem; position: relative; z-index: 1; }

/* ── SCROLLING BANNER ─────────────────────── */
@keyframes slide {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.banner-outer {
    overflow: hidden;
    background: linear-gradient(90deg, #004d3f, #006654, #004d3f);
    border-radius: 16px;
    padding: 12px 0;
    margin-bottom: 20px;
    border: 1px solid rgba(0,201,167,0.25);
    box-shadow: 0 8px 32px rgba(0,201,167,0.12);
}
.banner-inner {
    display: inline-flex;
    white-space: nowrap;
    animation: slide 22s linear infinite;
}
.banner-item {
    color: #fff;
    font-size: 0.98rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 0 48px;
}

/* ── HERO ─────────────────────────────────── */
.hero {
    padding: 40px 32px 32px;
    border-radius: 28px;
    background: linear-gradient(140deg,
        rgba(0,201,167,0.14) 0%,
        rgba(0,20,26,0.9)   45%,
        rgba(245,200,66,0.08) 100%);
    border: 1px solid rgba(0,201,167,0.2);
    box-shadow: var(--shadow), inset 0 1px 0 rgba(255,255,255,0.06);
    position: relative;
    overflow: hidden;
    margin-bottom: 24px;
}
.hero::after {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(245,200,66,0.12), transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.8rem);
    font-weight: 900;
    text-align: center;
    background: linear-gradient(120deg, var(--teal2) 0%, var(--sky) 50%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.15;
    margin-bottom: 10px;
}
.hero-sub {
    text-align: center;
    font-size: 1.05rem;
    color: var(--muted);
    letter-spacing: 0.02em;
    margin-bottom: 20px;
}
.badge-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
}
.badge {
    padding: 7px 16px;
    border-radius: 999px;
    background: rgba(0,201,167,0.12);
    border: 1px solid rgba(0,201,167,0.28);
    color: var(--teal2);
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

/* ── SIDEBAR ──────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071418 0%, #050e10 100%) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 900;
    color: var(--teal2);
    text-align: center;
    padding: 16px 0 8px;
}

/* ── CARDS ────────────────────────────────── */
.card {
    padding: 22px;
    border-radius: var(--radius);
    background: var(--glass);
    border: 1px solid var(--border);
    box-shadow: 0 12px 36px rgba(0,0,0,0.28);
    margin-bottom: 16px;
}
.card-gold {
    padding: 22px;
    border-radius: var(--radius);
    background: linear-gradient(135deg, rgba(245,200,66,0.10), rgba(0,20,26,0.95));
    border: 1px solid rgba(245,200,66,0.25);
    box-shadow: 0 12px 36px rgba(0,0,0,0.28);
    margin-bottom: 16px;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--teal2);
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.92rem;
    color: var(--muted);
    margin-bottom: 18px;
}

/* ── BUTTONS ──────────────────────────────── */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(90deg, var(--teal), #0080aa) !important;
    color: white !important;
    border-radius: 14px !important;
    height: 3em !important;
    width: 100% !important;
    border: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.96rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 8px 24px rgba(0,201,167,0.22) !important;
    transition: all 0.2s !important;
}
.stButton>button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 32px rgba(0,201,167,0.35) !important;
}

/* ── INPUTS ───────────────────────────────── */
.stTextInput>div>input,
.stTextArea>div>textarea,
.stSelectbox>div>div,
.stDateInput>div>input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,201,167,0.25) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── TABS ─────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,201,167,0.22), rgba(0,128,170,0.18)) !important;
    color: var(--teal2) !important;
    border-color: rgba(0,201,167,0.4) !important;
}

/* ── SUCCESS / WARNING / ERROR ─────────────── */
.stSuccess, .stInfo { border-radius: 14px !important; }

/* ── PROMO / CLIENT PORTAL ────────────────── */
.promo-wrap {
    padding: 48px 36px;
    border-radius: 28px;
    background: linear-gradient(140deg,
        rgba(0,201,167,0.18),
        rgba(0,20,26,0.95),
        rgba(245,200,66,0.10));
    border: 1px solid rgba(0,201,167,0.28);
    box-shadow: var(--shadow);
    text-align: center;
    position: relative;
    overflow: hidden;
}
.promo-wrap::before {
    content: '✦';
    position: absolute;
    top: 18px; left: 24px;
    font-size: 1.4rem;
    color: rgba(245,200,66,0.3);
}
.promo-wrap::after {
    content: '✦';
    position: absolute;
    bottom: 18px; right: 24px;
    font-size: 1.4rem;
    color: rgba(0,201,167,0.3);
}
.promo-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 900;
    background: linear-gradient(120deg, var(--teal2), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}
.promo-sub {
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 28px;
}
.promo-btn {
    display: inline-block;
    padding: 16px 38px;
    border-radius: 999px;
    text-decoration: none !important;
    font-weight: 800;
    font-size: 1.05rem;
    color: #020d0f !important;
    background: linear-gradient(90deg, var(--teal2), var(--gold));
    box-shadow: 0 12px 36px rgba(0,201,167,0.35);
    letter-spacing: 0.04em;
    transition: transform 0.2s, box-shadow 0.2s;
}
.promo-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 48px rgba(0,201,167,0.45);
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin: 28px 0;
}
.feature-card {
    padding: 20px 16px;
    border-radius: 18px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    text-align: center;
}
.feature-icon { font-size: 2rem; margin-bottom: 8px; }
.feature-name { font-weight: 700; color: var(--teal2); font-size: 0.95rem; }
.feature-desc { font-size: 0.82rem; color: var(--muted); margin-top: 4px; }

/* ── INTAKE FORM ──────────────────────────── */
.intake-section {
    padding: 20px 22px;
    border-radius: var(--radius);
    background: linear-gradient(135deg, rgba(0,201,167,0.07), rgba(0,10,15,0.9));
    border: 1px solid rgba(0,201,167,0.18);
    margin-bottom: 18px;
}
.intake-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: var(--gold);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── SECURITY ─────────────────────────────── */
.threat-box {
    padding: 18px 20px;
    border-radius: 16px;
    background: rgba(255,60,60,0.10);
    border: 1px solid rgba(255,100,100,0.3);
    margin-top: 14px;
}
.safe-box {
    padding: 18px 20px;
    border-radius: 16px;
    background: rgba(0,201,167,0.10);
    border: 1px solid rgba(0,201,167,0.3);
    margin-top: 14px;
}

/* ── FOOTER ───────────────────────────────── */
.footer {
    text-align: center;
    margin-top: 48px;
    padding: 20px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 0.88rem;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SCROLLING BANNER
# ─────────────────────────────────────────────
banner_items = [
    "🌿 LifeHaven Care Portal",
    "💪 Fitness & Wellness Tracking",
    "🏥 Elderly Care Management",
    "📋 Digital Intake Forms",
    "🔒 Phone Security Scanner",
    "📍 GPS Location Tracking",
    "🎙️ Voice & Multilingual Support",
    "📄 PDF Record Export",
    "✨ Built by ReubenSoul4peaceunity",
    "🌍 Health • Peace • Unity",
]
double = banner_items * 2
items_html = "".join(f'<span class="banner-item">{i}</span>' for i in double)
st.markdown(f"""
<div class="banner-outer">
  <div class="banner-inner">{items_html}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🌿 LifeHaven Care Portal</div>
  <div class="hero-sub">Premium Elderly Care · Fitness · Safety · Built with Love by ReubenSoul4peaceunity</div>
  <div class="badge-row">
    <div class="badge">💪 Fitness AI</div>
    <div class="badge">📋 Digital Intake</div>
    <div class="badge">📍 GPS Tracking</div>
    <div class="badge">🏥 Care Records</div>
    <div class="badge">🔒 Phone Security</div>
    <div class="badge">🎙️ Voice Support</div>
    <div class="badge">📄 PDF Export</div>
    <div class="badge">🌐 Multilingual</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "reps" not in st.session_state:
    st.session_state.reps = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()

# ─────────────────────────────────────────────
#  SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
st.sidebar.markdown('<div class="sidebar-logo">🌿 LifeHaven</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.selectbox(
    "Navigate",
    [
        "🏋️ Fitness Training",
        "🏥 Care Portal",
        "📋 Intake Forms",
        "🔒 Phone Security",
        "✨ Client Portal",
    ]
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:0.78rem;color:rgba(234,246,244,0.4);text-align:center;'>ReubenSoul4peaceunity<br>Health • Peace • Unity</div>",
    unsafe_allow_html=True
)

# ═════════════════════════════════════════════
#  1. FITNESS TRAINING
# ═════════════════════════════════════════════
if menu == "🏋️ Fitness Training":
    st.markdown('<div class="section-title">💪 Fitness Training</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">AI-powered rep counter, GPS map, and analytics dashboard</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏃 Live Training", "📍 GPS Map", "📊 Analytics"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Live AI Rep Counter")
        img = st.camera_input("Capture Exercise")
        if img is not None:
            bytes_data = img.getvalue()
            nparr = np.frombuffer(bytes_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                with mp.solutions.pose.Pose() as pose:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(rgb)
                    if results.pose_landmarks:
                        st.session_state.reps += 1
                        st.success("✅ Rep counted!")
                    st.image(rgb, channels="RGB", use_container_width=True)
            else:
                st.error("Could not decode the camera image.")
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("🔄 Reps", st.session_state.reps)
        col2.metric("🔥 Calories", round(st.session_state.reps * 0.5, 2))
        col3.metric("⏱️ Minutes", round((datetime.now() - st.session_state.start_time).seconds / 60, 1))

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("GPS Location Tracker")
        lat = st.number_input("Latitude", value=34.05)
        lon = st.number_input("Longitude", value=-118.25)
        if st.button("📍 Show Map"):
            m = folium.Map(location=[lat, lon], zoom_start=12, control_scale=True)
            folium.Marker([lat, lon], tooltip="Current Location").add_to(m)
            st_folium(m, width=700, height=500, returned_objects=[])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Session Analytics")
        df = pd.DataFrame({"Reps": [st.session_state.reps], "Calories": [st.session_state.reps * 0.5]})
        st.bar_chart(df)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  2. CARE PORTAL
# ═════════════════════════════════════════════
elif menu == "🏥 Care Portal":
    st.markdown('<div class="section-title">🏥 Elderly Care Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Add residents, search records, generate PDFs with voice support</div>', unsafe_allow_html=True)

    class ElderlyCarePortal:
        def __init__(self):
            self.db_name = "care_center.db"
            self.recognizer = sr.Recognizer()
            self.init_db()

        def init_db(self):
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS residents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, dob TEXT, medical_info TEXT,
                    medications TEXT, allergies TEXT,
                    emergency_contact TEXT, language TEXT
                )
            """)
            conn.commit()
            conn.close()

        def speak(self, text, lang="en"):
            try:
                filename = "temp_voice.mp3"
                gTTS(text=text, lang=lang).save(filename)
                if os.name == "nt":
                    os.system(f'start "" "{filename}"')
                else:
                    os.system(f'xdg-open "{filename}" >/dev/null 2>&1 &')
            except Exception:
                pass

        def listen(self, lang_code, key_suffix=""):
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5)
                    return self.recognizer.recognize_google(audio, language=lang_code)
            except Exception:
                return st.text_input(f"🎤 Voice unavailable — type here:", key=f"text_{key_suffix}")

        def add_resident_session(self):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🆕 New Admission / Nueva Admisión")
            lang_choice = st.selectbox("Select Language / Seleccione Idioma", ["English", "Spanish"])
            lang_code = "es-ES" if lang_choice == "Spanish" else "en-US"
            name = st.text_input("Resident Full Name / Nombre", key="cp_name")
            dob = self.listen(lang_code, "dob")
            med_info = self.listen(lang_code, "med")
            medications = self.listen(lang_code, "meds")
            allergies = self.listen(lang_code, "allergies")
            contact = self.listen(lang_code, "contact")
            col1, col2 = st.columns(2)
            with col1:
                save_clicked = st.button("💾 Save Resident")
            with col2:
                pdf_clicked = st.button("📄 Generate PDF")
            if save_clicked:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("""
                    INSERT INTO residents
                    (name, dob, medical_info, medications, allergies, emergency_contact, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, dob, med_info, medications, allergies, contact, lang_code))
                conn.commit()
                conn.close()
                st.success(f"✅ {name} saved successfully!")
            if pdf_clicked:
                self.export_pdf(name, dob, med_info, medications, allergies, contact)
            st.markdown('</div>', unsafe_allow_html=True)

        def search_records_session(self):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🔍 Search Resident Records")
            query = st.text_input("Enter Resident Name / Ingrese Nombre")
            if st.button("🔍 Search"):
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT * FROM residents WHERE name LIKE ?", ('%' + query + '%',))
                results = c.fetchall()
                conn.close()
                if results:
                    for r in results:
                        st.markdown(f"""
                        <div class="card-gold">
                            <b>#{r[0]} — {r[1]}</b><br>
                            <span style="color:var(--muted)">DOB: {r[2]}</span><br>
                            🩺 <b>Medical:</b> {r[3]}<br>
                            💊 <b>Medications:</b> {r[4]}<br>
                            ⚠️ <b>Allergies:</b> {r[5]}<br>
                            📞 <b>Emergency Contact:</b> {r[6]}
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"🔊 Read aloud — {r[1]}", key=f"read_{r[0]}"):
                            self.speak(f"Resident {r[1]}. Conditions: {r[3]}. Medications: {r[4]}.", lang=(r[7] or "en")[:2])
                else:
                    st.warning("No records found matching that name.")
            st.markdown('</div>', unsafe_allow_html=True)

        def export_pdf(self, name, dob, medical, meds, allergies, contact):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="LifeHaven — Elderly Care Admission Record", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            for key, value in {"Name": name, "DOB": dob, "Medical": medical,
                                "Medications": meds, "Allergies": allergies, "Emergency Contact": contact}.items():
                pdf.ln(8)
                pdf.multi_cell(0, 10, txt=f"{key}: {value}")
            safe_name = "".join(c for c in (name or "resident") if c.isalnum() or c in (" ", "_")).strip().replace(" ", "_")
            filename = f"{safe_name}_intake.pdf"
            pdf.output(filename)
            st.success(f"📄 PDF exported: {filename}")

        def run_portal(self):
            portal_menu = st.sidebar.radio("Care Menu", ["🆕 New Admission", "🔍 Search Records"])
            if portal_menu == "🆕 New Admission":
                self.add_resident_session()
            else:
                self.search_records_session()

    ElderlyCarePortal().run_portal()

# ═════════════════════════════════════════════
#  3. INTAKE FORMS
# ═════════════════════════════════════════════
elif menu == "📋 Intake Forms":
    st.markdown('<div class="section-title">📋 Digital Admission Intake</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete the full admission packet — all 7 sections — digitally and export as PDF</div>', unsafe_allow_html=True)

    # DB for intake
    def init_intake_db():
        conn = sqlite3.connect("care_center.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS intake_forms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submitted_at TEXT,
                full_name TEXT, dob TEXT, gender TEXT, ssn_last4 TEXT,
                primary_language TEXT, marital_status TEXT,
                emergency_contact1 TEXT, emergency_contact2 TEXT, primary_physician TEXT,
                chronic_conditions TEXT, allergies TEXT, medications TEXT,
                immunizations TEXT, hospitalizations TEXT,
                adl_status TEXT, mobility TEXT, cognitive_status TEXT,
                skin_integrity TEXT, dietary TEXT,
                poa TEXT, directives TEXT, hipaa_consent TEXT,
                daily_routine TEXT, social_interests TEXT,
                special_equipment TEXT, transportation TEXT,
                device_type TEXT, security_consent TEXT, phone_concerns TEXT
            )
        """)
        conn.commit()
        conn.close()

    init_intake_db()

    with st.form("intake_form", clear_on_submit=False):

        # ── Section 1: Client Profile
        st.markdown('<div class="intake-section"><div class="intake-heading">👤 Section 1 — Client Profile</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        full_name       = c1.text_input("Full Legal Name *")
        dob             = c2.date_input("Date of Birth *")
        c3, c4          = st.columns(2)
        gender          = c3.selectbox("Gender Identity", ["Male", "Female", "Non-binary", "Prefer not to say", "Other"])
        marital         = c4.selectbox("Marital Status", ["Single", "Married", "Widowed", "Divorced", "Separated"])
        c5, c6          = st.columns(2)
        ssn_last4       = c5.text_input("Last 4 of SSN (secure)", max_chars=4, type="password")
        primary_lang    = c6.selectbox("Primary Language", ["English", "Spanish", "French", "Haitian Creole", "Portuguese", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 2: Emergency Contacts
        st.markdown('<div class="intake-section"><div class="intake-heading">📞 Section 2 — Emergency Contacts</div>', unsafe_allow_html=True)
        ec1 = st.text_input("Primary Contact — Name / Relationship / Phone")
        ec2 = st.text_input("Secondary Contact — Name / Relationship / Phone")
        physician = st.text_input("Primary Care Physician — Name / Phone")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 3: Health History
        st.markdown('<div class="intake-section"><div class="intake-heading">🩺 Section 3 — Health History</div>', unsafe_allow_html=True)
        chronic     = st.text_area("Chronic Conditions (e.g. Diabetes, Hypertension)", height=80)
        allergies   = st.text_area("Known Allergies (medications, food, environmental)", height=80)
        medications = st.text_area("Current Medications & Dosage", height=90)
        immunize    = st.text_input("Immunization Records (Flu, COVID, Pneumonia, etc.)")
        hospital    = st.text_area("Recent Hospitalizations or Surgeries (last 5 years)", height=80)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 4: Medical Assessment
        st.markdown('<div class="intake-section"><div class="intake-heading">🏥 Section 4 — Medical Assessment</div>', unsafe_allow_html=True)
        adl_status  = st.multiselect("ADL — Independent In:", ["Eating", "Bathing", "Dressing", "Toileting", "Transferring", "Continence"])
        mobility    = st.selectbox("Mobility Status", ["Fully Ambulatory", "Uses Cane", "Uses Walker", "Uses Wheelchair", "Bedbound"])
        cognitive   = st.selectbox("Cognitive Status", ["Alert & Oriented x4", "Mild Impairment", "Moderate Impairment", "Severe Impairment", "Dementia Diagnosed"])
        skin        = st.selectbox("Skin Integrity", ["Intact", "Stage I Wound", "Stage II Wound", "Stage III/IV Wound", "Under Treatment"])
        dietary     = st.text_input("Dietary Restrictions / Special Requirements")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 5: Legal Documentation
        st.markdown('<div class="intake-section"><div class="intake-heading">⚖️ Section 5 — Legal Documentation</div>', unsafe_allow_html=True)
        poa         = st.selectbox("Power of Attorney on File?", ["Yes — Medical & Financial", "Yes — Medical Only", "Yes — Financial Only", "No", "In Progress"])
        directives  = st.selectbox("Advanced Directives / DNR Status", ["Full Code", "DNR on File", "DNI on File", "Comfort Care Only", "Not Established"])
        hipaa       = st.checkbox("✅ I acknowledge receipt of the HIPAA Privacy Notice and Admission Agreement")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 6: Care Requirements
        st.markdown('<div class="intake-section"><div class="intake-heading">💛 Section 6 — Care Preferences</div>', unsafe_allow_html=True)
        daily_routine   = st.text_area("Daily Routine Preferences (wake time, meals, sleep, etc.)", height=80)
        social          = st.text_area("Social & Recreational Interests (hobbies, music, faith, etc.)", height=80)
        equipment       = st.text_input("Special Equipment Needed (Oxygen, CPAP, Hearing Aid, etc.)")
        transport       = st.selectbox("Transportation Needs", ["None", "Medical Appointments Only", "Regular Transport", "Ambulance Only"])
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Section 7: Phone Security
        st.markdown('<div class="intake-section"><div class="intake-heading">🔒 Section 7 — Phone Security Setup</div>', unsafe_allow_html=True)
        device_type     = st.selectbox("Device Type", ["iPhone (iOS)", "Android", "Basic Cell Phone", "No Phone", "Other"])
        phone_concerns  = st.text_area("Known Issues (suspicious calls, strange apps, battery drain, etc.)", height=70)
        security_consent = st.checkbox("✅ Client consents to phone security assessment by care staff")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("📤 Submit Complete Intake Packet")

        if submitted:
            if not full_name:
                st.error("⚠️ Full name is required.")
            elif not hipaa:
                st.error("⚠️ HIPAA acknowledgment is required to proceed.")
            else:
                conn = sqlite3.connect("care_center.db")
                c_db = conn.cursor()
                c_db.execute("""
                    INSERT INTO intake_forms (
                        submitted_at, full_name, dob, gender, ssn_last4,
                        primary_language, marital_status,
                        emergency_contact1, emergency_contact2, primary_physician,
                        chronic_conditions, allergies, medications,
                        immunizations, hospitalizations,
                        adl_status, mobility, cognitive_status, skin_integrity, dietary,
                        poa, directives, hipaa_consent,
                        daily_routine, social_interests, special_equipment, transportation,
                        device_type, security_consent, phone_concerns
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    full_name, str(dob), gender, ssn_last4,
                    primary_lang, marital,
                    ec1, ec2, physician,
                    chronic, allergies, medications, immunize, hospital,
                    ", ".join(adl_status), mobility, cognitive, skin, dietary,
                    poa, directives, "Yes",
                    daily_routine, social, equipment, transport,
                    device_type, "Yes" if security_consent else "No", phone_concerns
                ))
                conn.commit()
                conn.close()

                # Generate PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", "B", 18)
                pdf.cell(0, 12, "LifeHaven Care Portal", ln=True, align="C")
                pdf.set_font("Arial", "B", 13)
                pdf.cell(0, 8, "Complete Admission Intake Packet", ln=True, align="C")
                pdf.ln(6)
                pdf.set_font("Arial", size=11)
                fields = {
                    "Full Name": full_name, "Date of Birth": str(dob),
                    "Gender": gender, "Marital Status": marital, "Language": primary_lang,
                    "Emergency Contact 1": ec1, "Emergency Contact 2": ec2,
                    "Primary Physician": physician, "Chronic Conditions": chronic,
                    "Allergies": allergies, "Medications": medications,
                    "ADL Status": ", ".join(adl_status), "Mobility": mobility,
                    "Cognitive Status": cognitive, "Dietary": dietary,
                    "Power of Attorney": poa, "Directives/DNR": directives,
                    "Daily Routine": daily_routine, "Social Interests": social,
                    "Special Equipment": equipment, "Transportation": transport,
                    "Device Type": device_type, "Phone Concerns": phone_concerns,
                    "Security Consent": "Yes" if security_consent else "No",
                    "Submitted": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                for k, v in fields.items():
                    pdf.ln(4)
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 7, f"{k}:", ln=True)
                    pdf.set_font("Arial", size=11)
                    pdf.multi_cell(0, 7, v or "—")

                safe = "".join(x for x in full_name if x.isalnum() or x == " ").replace(" ", "_")
                pdf_path = f"{safe}_intake_packet.pdf"
                pdf.output(pdf_path)

                st.success(f"🎉 Intake packet for **{full_name}** saved & PDF generated!")
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Download PDF Intake Packet",
                        data=f,
                        file_name=pdf_path,
                        mime="application/pdf"
                    )

# ═════════════════════════════════════════════
#  4. PHONE SECURITY
# ═════════════════════════════════════════════
elif menu == "🔒 Phone Security":
    import random
    st.markdown('<div class="section-title">🔒 Phone Security Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Protect elderly clients from scams, malware & suspicious activity</div>', unsafe_allow_html=True)

    THREATS = [
        "Unknown app requesting camera access without permission",
        "Unusual data usage spike detected in background",
        "Unrecognized login attempt from new device",
        "Suspicious SMS link from unknown number",
        "App accessing contacts without clear permission",
        "Unknown process running in background",
        "Potential phishing URL detected in recent messages",
        "Microphone accessed by unknown application",
        "Battery draining unusually fast — possible spyware",
        "Unknown app installed without user confirmation",
    ]
    TIPS = [
        "Never share OTP codes — not even with family or banks.",
        "Do not tap links in unexpected text messages.",
        "Keep your phone's software updated at all times.",
        "Use a 6-digit PIN or biometric lock on your phone.",
        "Enable two-factor authentication on your email account.",
        "Block unknown callers automatically in phone settings.",
        "Report scam calls to the FTC: 1-877-382-4357.",
        "Only download apps from official App Store or Google Play.",
        "If something feels wrong, ask your caregiver to check.",
    ]

    client_name = st.text_input("Client Name for Scan Report", placeholder="e.g. Mary Johnson")

    col1, col2 = st.columns([2, 1])
    with col1:
        scan_type = st.selectbox("Scan Type", [
            "Quick Scan (30 seconds)",
            "Full Security Scan (60 seconds)",
            "Scam Call Check",
            "App Permission Audit",
        ])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_scan = st.button("🔍 Run Security Scan")

    if run_scan:
        name_display = client_name or "Client"
        with st.spinner(f"Scanning {name_display}'s device..."):
            import time
            time.sleep(2)

        threats_found = random.randint(0, 3)
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.markdown(f"""
        <div class="card">
            <b style="color:var(--teal2);font-family:'Playfair Display',serif;font-size:1.2rem;">
                🛡️ Scan Report — {name_display}
            </b><br>
            <span style="color:var(--muted);font-size:0.88rem;">Scan type: {scan_type} &nbsp;|&nbsp; {scan_time}</span>
        </div>
        """, unsafe_allow_html=True)

        if threats_found == 0:
            st.markdown("""
            <div class="safe-box">
                <span style="font-size:1.5rem;">✅</span>
                <b style="color:#00e5c0;font-size:1.1rem;"> Device appears CLEAN</b><br>
                No suspicious activity detected. The device is operating normally.
            </div>
            """, unsafe_allow_html=True)
        else:
            threat_list = random.sample(THREATS, min(threats_found, len(THREATS)))
            threats_html = "".join(f"<li style='margin-bottom:8px;'>⚠️ {t}</li>" for t in threat_list)
            st.markdown(f"""
            <div class="threat-box">
                <span style="font-size:1.5rem;">🚨</span>
                <b style="color:#ff6b6b;font-size:1.1rem;"> {threats_found} SUSPICIOUS PATTERN(S) DETECTED</b>
                <ul style="margin-top:12px;color:var(--text);">{threats_html}</ul>
                <div style="margin-top:14px;padding:12px;background:rgba(255,60,60,0.08);border-radius:12px;">
                    <b>⚡ Immediate Actions:</b><br>
                    1. Do NOT open any new apps or links<br>
                    2. Notify caregiver or family immediately<br>
                    3. Call LifeHaven support for device review
                </div>
            </div>
            """, unsafe_allow_html=True)

        tip = random.choice(TIPS)
        st.markdown(f"""
        <div class="card-gold" style="margin-top:16px;">
            💡 <b>Daily Security Tip:</b><br>
            <span style="color:var(--muted)">{tip}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-sub">📋 Common scams targeting elderly clients:</div>', unsafe_allow_html=True)
    scam_col1, scam_col2, scam_col3 = st.columns(3)
    scam_col1.markdown("""
    <div class="card">
        <b>📱 Grandparent Scam</b><br>
        <span style="color:var(--muted);font-size:0.88rem;">Caller pretends to be grandchild in trouble. Never send money without verifying in person.</span>
    </div>
    """, unsafe_allow_html=True)
    scam_col2.markdown("""
    <div class="card">
        <b>💊 Medicare Scam</b><br>
        <span style="color:var(--muted);font-size:0.88rem;">Fake Medicare representatives asking for card numbers. Real Medicare never cold-calls.</span>
    </div>
    """, unsafe_allow_html=True)
    scam_col3.markdown("""
    <div class="card">
        <b>🏦 Bank Fraud</b><br>
        <span style="color:var(--muted);font-size:0.88rem;">Texts claiming your account is locked. Never click links — call the bank directly.</span>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  5. CLIENT PORTAL
# ═════════════════════════════════════════════
else:
    st.markdown("""
    <div class="promo-wrap">
        <div class="promo-title">🌿 LifeHaven Client Portal</div>
        <div class="promo-sub">
            A premium, secure experience for your clients and their families.<br>
            Everything they need — health records, intake forms, and care updates — in one beautiful place.
        </div>
        <a class="promo-btn" href="https://fit4unity.onrender.com" target="_blank">
            🚀 Open LifeHaven Portal
        </a>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">💪</div>
                <div class="feature-name">Fitness AI</div>
                <div class="feature-desc">Rep counting & calorie tracking powered by AI pose detection</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-name">Digital Intake</div>
                <div class="feature-desc">Complete 7-section admission packet, fully digital with PDF export</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🏥</div>
                <div class="feature-name">Care Records</div>
                <div class="feature-desc">Secure resident database with search and multilingual voice support</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-name">Phone Security</div>
                <div class="feature-desc">Scan for threats, scam alerts, and daily security tips for seniors</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📍</div>
                <div class="feature-name">GPS Tracking</div>
                <div class="feature-desc">Live location map for fitness routes and client safety</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-name">PDF Export</div>
                <div class="feature-desc">One-click PDF generation for all care and intake records</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌿 <b>LifeHaven Care Portal</b> &nbsp;·&nbsp; Built by ReubenSoul4peaceunity<br>
    Health &nbsp;•&nbsp; Peace &nbsp;•&nbsp; Unity &nbsp;•&nbsp; Technology
</div>
""", unsafe_allow_html=True)
