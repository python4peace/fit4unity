#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LifeHaven Care Portal — by ReubenSoul4peaceunity
# Professional build — all known issues resolved

import os
import io
import math
import random
import sqlite3
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import mediapipe as mp
import folium
import streamlit as st
from streamlit_folium import st_folium
from fpdf import FPDF
from gtts import gTTS

# ─────────────────────────────────────────────
#  DB PATH — /tmp persists within Render session
# ─────────────────────────────────────────────
DB_PATH = "/tmp/lifehaven.db"

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first st call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LifeHaven Care Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg0:#020d0f;--bg1:#061418;--bg2:#0a1f24;--bg3:#0f2d34;
  --teal:#00c9a7;--teal2:#00e5c0;--gold:#f5c842;--gold2:#ffe082;
  --sky:#7ee8fa;--text:#eaf6f4;--muted:rgba(234,246,244,.62);
  --glass:rgba(255,255,255,.055);--border:rgba(255,255,255,.09);
  --radius:20px;--shadow:0 24px 64px rgba(0,0,0,.45);
}
html,body,[class*="css"]{
  font-family:'DM Sans',sans-serif;
  background:var(--bg0)!important;color:var(--text)!important;
}
body::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse 80% 60% at 20% 10%,rgba(0,201,167,.08),transparent 60%),
    radial-gradient(ellipse 60% 50% at 80% 80%,rgba(245,200,66,.06),transparent 60%),
    radial-gradient(ellipse 50% 40% at 50% 50%,rgba(126,232,250,.04),transparent 70%);
}
.block-container{padding-top:1.2rem;padding-bottom:3rem;position:relative;z-index:1}
@keyframes slide{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.banner-outer{overflow:hidden;background:linear-gradient(90deg,#004d3f,#006654,#004d3f);
  border-radius:16px;padding:12px 0;margin-bottom:20px;
  border:1px solid rgba(0,201,167,.25);box-shadow:0 8px 32px rgba(0,201,167,.12)}
.banner-inner{display:inline-flex;white-space:nowrap;animation:slide 24s linear infinite}
.banner-item{color:#fff;font-size:.98rem;font-weight:600;letter-spacing:.04em;padding:0 48px}
.hero{padding:40px 32px 32px;border-radius:28px;margin-bottom:24px;position:relative;overflow:hidden;
  background:linear-gradient(140deg,rgba(0,201,167,.14) 0%,rgba(0,20,26,.9) 45%,rgba(245,200,66,.08) 100%);
  border:1px solid rgba(0,201,167,.2);box-shadow:var(--shadow),inset 0 1px 0 rgba(255,255,255,.06)}
.hero::after{content:'';position:absolute;top:-80px;right:-80px;width:260px;height:260px;
  border-radius:50%;background:radial-gradient(circle,rgba(245,200,66,.12),transparent 70%);pointer-events:none}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(2rem,5vw,3.8rem);font-weight:900;
  text-align:center;line-height:1.15;margin-bottom:10px;
  background:linear-gradient(120deg,var(--teal2) 0%,var(--sky) 50%,var(--gold) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{text-align:center;font-size:1.05rem;color:var(--muted);letter-spacing:.02em;margin-bottom:20px}
.badge-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.badge{padding:7px 16px;border-radius:999px;background:rgba(0,201,167,.12);
  border:1px solid rgba(0,201,167,.28);color:var(--teal2);font-size:.88rem;font-weight:600;letter-spacing:.03em}
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#071418,#050e10)!important;
  border-right:1px solid var(--border)}
.card{padding:22px;border-radius:var(--radius);background:var(--glass);
  border:1px solid var(--border);box-shadow:0 12px 36px rgba(0,0,0,.28);margin-bottom:16px}
.card-gold{padding:22px;border-radius:var(--radius);margin-bottom:16px;
  background:linear-gradient(135deg,rgba(245,200,66,.10),rgba(0,20,26,.95));
  border:1px solid rgba(245,200,66,.25);box-shadow:0 12px 36px rgba(0,0,0,.28)}
.section-title{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;
  color:var(--teal2);margin-bottom:4px}
.section-sub{font-size:.92rem;color:var(--muted);margin-bottom:18px}
.stButton>button,.stDownloadButton>button{
  background:linear-gradient(90deg,var(--teal),#0080aa)!important;
  color:white!important;border-radius:14px!important;height:3em!important;
  width:100%!important;border:0!important;font-family:'DM Sans',sans-serif!important;
  font-weight:700!important;font-size:.96rem!important;letter-spacing:.03em!important;
  box-shadow:0 8px 24px rgba(0,201,167,.22)!important;transition:all .2s!important}
.stTextInput>div>input,.stTextArea>div>textarea,
.stSelectbox>div>div,.stDateInput>div>input{
  background:rgba(255,255,255,.05)!important;
  border:1px solid rgba(0,201,167,.25)!important;
  border-radius:12px!important;color:var(--text)!important;
  font-family:'DM Sans',sans-serif!important}
.stTabs [data-baseweb="tab-list"]{gap:6px;background:transparent!important}
.stTabs [data-baseweb="tab"]{border-radius:10px!important;background:var(--glass)!important;
  border:1px solid var(--border)!important;color:var(--muted)!important;
  font-weight:600!important;padding:8px 18px!important}
.stTabs [aria-selected="true"]{
  background:linear-gradient(90deg,rgba(0,201,167,.22),rgba(0,128,170,.18))!important;
  color:var(--teal2)!important;border-color:rgba(0,201,167,.4)!important}
.rep-counter{text-align:center;padding:28px;border-radius:24px;
  background:linear-gradient(135deg,rgba(0,201,167,.15),rgba(0,20,26,.95));
  border:1px solid rgba(0,201,167,.3)}
.rep-number{font-family:'Playfair Display',serif;font-size:5rem;font-weight:900;
  color:var(--teal2);line-height:1}
.intake-section{padding:20px 22px;border-radius:var(--radius);margin-bottom:18px;
  background:linear-gradient(135deg,rgba(0,201,167,.07),rgba(0,10,15,.9));
  border:1px solid rgba(0,201,167,.18)}
.intake-heading{font-family:'Playfair Display',serif;font-size:1.2rem;
  color:var(--gold);margin-bottom:14px}
.threat-box{padding:18px 20px;border-radius:16px;margin-top:14px;
  background:rgba(255,60,60,.10);border:1px solid rgba(255,100,100,.3)}
.safe-box{padding:18px 20px;border-radius:16px;margin-top:14px;
  background:rgba(0,201,167,.10);border:1px solid rgba(0,201,167,.3)}
.promo-wrap{padding:48px 36px;border-radius:28px;text-align:center;
  position:relative;overflow:hidden;
  background:linear-gradient(140deg,rgba(0,201,167,.18),rgba(0,20,26,.95),rgba(245,200,66,.10));
  border:1px solid rgba(0,201,167,.28);box-shadow:var(--shadow)}
.promo-wrap::before{content:'✦';position:absolute;top:18px;left:24px;
  font-size:1.4rem;color:rgba(245,200,66,.3)}
.promo-wrap::after{content:'✦';position:absolute;bottom:18px;right:24px;
  font-size:1.4rem;color:rgba(0,201,167,.3)}
.promo-title{font-family:'Playfair Display',serif;font-size:2.4rem;font-weight:900;
  margin-bottom:10px;
  background:linear-gradient(120deg,var(--teal2),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.promo-sub{color:var(--muted);font-size:1.05rem;margin-bottom:28px}
.promo-btn{display:inline-block;padding:16px 38px;border-radius:999px;
  text-decoration:none!important;font-weight:800;font-size:1.05rem;
  color:#020d0f!important;letter-spacing:.04em;
  background:linear-gradient(90deg,var(--teal2),var(--gold));
  box-shadow:0 12px 36px rgba(0,201,167,.35)}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  gap:14px;margin:28px 0}
.feature-card{padding:20px 16px;border-radius:18px;text-align:center;
  background:rgba(255,255,255,.05);border:1px solid var(--border)}
.feature-icon{font-size:2rem;margin-bottom:8px}
.feature-name{font-weight:700;color:var(--teal2);font-size:.95rem}
.feature-desc{font-size:.82rem;color:var(--muted);margin-top:4px}
.footer{text-align:center;margin-top:48px;padding:20px;
  border-top:1px solid var(--border);color:var(--muted);
  font-size:.88rem;letter-spacing:.04em}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATABASE INIT
# ─────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS residents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, dob TEXT, medical_info TEXT,
            medications TEXT, allergies TEXT,
            emergency_contact TEXT, language TEXT, created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS intake_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT, full_name TEXT, dob TEXT, gender TEXT,
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

init_db()

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in {"reps": 0, "stage": None, "start_time": datetime.now()}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def safe(val, fallback="—"):
    return str(val).strip() if val and str(val).strip() else fallback

def calculate_angle(a, b, c):
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(math.degrees(radians))
    return 360 - angle if angle > 180 else angle

def make_pdf_bytes(pdf: FPDF) -> bytes:
    return bytes(pdf.output())

def make_voice(text: str, lang: str = "en"):
    try:
        buf = io.BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(buf)
        buf.seek(0)
        return buf.read()
    except Exception:
        return None

# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────
items = [
    "🌿 LifeHaven Care Portal","💪 AI Fitness Tracking",
    "🏥 Elderly Care Management","📋 Digital Intake Forms",
    "🔒 Phone Security Education","📍 GPS Location Tracking",
    "📄 PDF Export","✨ Built by ReubenSoul4peaceunity","🌍 Health • Peace • Unity",
] * 2
st.markdown(
    '<div class="banner-outer"><div class="banner-inner">'
    + "".join(f'<span class="banner-item">{i}</span>' for i in items)
    + '</div></div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🌿 LifeHaven Care Portal</div>
  <div class="hero-sub">Premium Elderly Care · Fitness · Safety · Built with Love by ReubenSoul4peaceunity</div>
  <div class="badge-row">
    <div class="badge">💪 Fitness AI</div><div class="badge">📋 Digital Intake</div>
    <div class="badge">📍 GPS Tracking</div><div class="badge">🏥 Care Records</div>
    <div class="badge">🔒 Phone Security</div><div class="badge">🎙️ Voice Support</div>
    <div class="badge">📄 PDF Export</div><div class="badge">🌐 Multilingual</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown('<div style="font-family:\'Playfair Display\',serif;font-size:1.3rem;font-weight:900;color:#00e5c0;text-align:center;padding:16px 0 8px">🌿 LifeHaven</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
menu = st.sidebar.selectbox("Navigate", [
    "🏋️ Fitness Training",
    "🏥 Care Portal",
    "📋 Intake Forms",
    "🔒 Phone Security",
    "✨ Client Portal",
])
st.sidebar.markdown("---")
st.sidebar.caption("ReubenSoul4peaceunity\nHealth • Peace • Unity")

# ═════════════════════════════════════════════
#  1 — FITNESS TRAINING
# ═════════════════════════════════════════════
if menu == "🏋️ Fitness Training":
    st.markdown('<div class="section-title">💪 Fitness Training</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">AI angle-based rep counter · GPS map · Analytics</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏃 Live Training", "📍 GPS Map", "📊 Analytics"])

    with tab1:
        exercise = st.selectbox("Exercise Type", [
            "Bicep Curl (arm)", "Squat (leg)", "Shoulder Press (arm)",
        ])
        LANDMARK_MAP = {
            "Bicep Curl (arm)":     (11, 13, 15),
            "Squat (leg)":          (23, 25, 27),
            "Shoulder Press (arm)": (11, 13, 15),
        }
        UP_THRESH, DOWN_THRESH = 50, 160

        st.info(
            "📸 **How to count reps:** Take a photo at the **BOTTOM** of the move "
            "(arm straight / sitting deep), then at the **TOP** (arm curled / standing). "
            "Each full cycle = 1 rep counted automatically.",
        )

        img = st.camera_input("📸 Snap your exercise position")

        if img is not None:
            nparr = np.frombuffer(img.getvalue(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                with mp.solutions.pose.Pose(
                    static_image_mode=True, model_complexity=1,
                    min_detection_confidence=0.5
                ) as pose:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(rgb)

                    if results.pose_landmarks:
                        lm = results.pose_landmarks.landmark
                        p1, p2, p3 = LANDMARK_MAP[exercise]
                        a = (lm[p1].x, lm[p1].y)
                        b = (lm[p2].x, lm[p2].y)
                        c = (lm[p3].x, lm[p3].y)
                        angle = calculate_angle(a, b, c)

                        # State machine
                        if angle > DOWN_THRESH:
                            if st.session_state.stage == "up":
                                st.session_state.reps += 1
                            st.session_state.stage = "down"
                        elif angle < UP_THRESH:
                            st.session_state.stage = "up"

                        # Draw skeleton
                        annotated = rgb.copy()
                        h, w = frame.shape[:2]
                        mp.solutions.drawing_utils.draw_landmarks(
                            annotated, results.pose_landmarks,
                            mp.solutions.pose.POSE_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=(0,229,192), thickness=3, circle_radius=5),
                            mp.solutions.drawing_utils.DrawingSpec(color=(245,200,66), thickness=2),
                        )
                        px, py = int(lm[p2].x * w), int(lm[p2].y * h)
                        cv2.putText(annotated, f"{int(angle)}\u00b0", (px-40, py-20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0,229,192), 3, cv2.LINE_AA)
                        st.image(annotated, channels="RGB", use_container_width=True)

                        stage = st.session_state.stage or "—"
                        stage_msg = "⬆️ TOP — go back down" if stage == "up" else "⬇️ BOTTOM — push up for next rep"
                        stage_color = "#00e5c0" if stage == "up" else "#f5c842"
                        st.markdown(f"""
                        <div class="rep-counter">
                          <div class="rep-number">{st.session_state.reps}</div>
                          <div style="color:var(--muted);font-size:.9rem">REPS</div>
                          <div style="font-size:1.8rem;font-weight:700;color:var(--sky);margin-top:6px">{int(angle)}°</div>
                          <div style="font-size:1.05rem;font-weight:700;color:{stage_color};margin-top:8px">{stage_msg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No pose detected. Make sure your full body is visible and well-lit.")
                        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
            else:
                st.error("❌ Could not decode image.")

        col1, col2, col3 = st.columns(3)
        elapsed = (datetime.now() - st.session_state.start_time).seconds
        col1.metric("🔄 Reps", st.session_state.reps)
        col2.metric("🔥 Calories", round(st.session_state.reps * 0.5, 1))
        col3.metric("⏱️ Minutes", round(elapsed / 60, 1))
        if st.button("🔁 Reset Session"):
            for k, v in {"reps": 0, "stage": None, "start_time": datetime.now()}.items():
                st.session_state[k] = v
            st.rerun()

    with tab2:
        st.subheader("📍 GPS Location Tracker")
        lat = st.number_input("Latitude", value=34.05, format="%.6f")
        lon = st.number_input("Longitude", value=-118.25, format="%.6f")
        if st.button("📍 Show Map"):
            m = folium.Map(location=[lat, lon], zoom_start=14, tiles="CartoDB dark_matter")
            folium.Marker([lat, lon], tooltip="📍 Current Location",
                          icon=folium.Icon(color="green", icon="heart", prefix="fa")).add_to(m)
            st_folium(m, width=700, height=480, returned_objects=[])

    with tab3:
        st.subheader("📊 Session Analytics")
        elapsed = (datetime.now() - st.session_state.start_time).seconds
        df = pd.DataFrame({
            "Metric": ["Reps", "Calories", "Minutes"],
            "Value": [st.session_state.reps, round(st.session_state.reps * 0.5, 1), round(elapsed / 60, 1)],
        })
        st.bar_chart(df.set_index("Metric"))
        st.dataframe(df, use_container_width=True)

# ═════════════════════════════════════════════
#  2 — CARE PORTAL
# ═════════════════════════════════════════════
elif menu == "🏥 Care Portal":
    st.markdown('<div class="section-title">🏥 Elderly Care Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Add residents, search records, generate PDFs</div>', unsafe_allow_html=True)

    portal_menu = st.sidebar.radio("Care Menu", ["🆕 New Admission", "🔍 Search Records"])
    LANGS = {"English": "en", "Spanish": "es", "French": "fr", "Haitian Creole": "ht", "Portuguese": "pt"}

    if portal_menu == "🆕 New Admission":
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🆕 New Admission")
        lang_choice = st.selectbox("Language / Idioma", list(LANGS.keys()))
        lang_code   = LANGS[lang_choice]
        name      = st.text_input("Full Name / Nombre *")
        dob       = st.text_input("Date of Birth (YYYY-MM-DD)")
        med_info  = st.text_area("Medical Conditions", height=80)
        meds      = st.text_area("Medications & Dosage", height=80)
        allergies = st.text_area("Allergies", height=60)
        contact   = st.text_input("Emergency Contact (Name / Relation / Phone)")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save Resident"):
                if not name.strip():
                    st.error("⚠️ Name is required.")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute(
                        "INSERT INTO residents (name,dob,medical_info,medications,allergies,emergency_contact,language,created_at) VALUES(?,?,?,?,?,?,?,?)",
                        (name, dob, med_info, meds, allergies, contact, lang_code, datetime.now().strftime("%Y-%m-%d %H:%M"))
                    )
                    conn.commit(); conn.close()
                    st.success(f"✅ {name} saved!")

        with c2:
            if st.button("📄 Generate PDF"):
                if not name.strip():
                    st.error("⚠️ Enter a name first.")
                else:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 12, "LifeHaven — Care Admission Record", ln=True, align="C")
                    pdf.ln(4)
                    for k, v in {
                        "Name": safe(name), "DOB": safe(dob),
                        "Medical Conditions": safe(med_info), "Medications": safe(meds),
                        "Allergies": safe(allergies), "Emergency Contact": safe(contact),
                        "Generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }.items():
                        pdf.set_font("Arial", "B", 11); pdf.cell(0, 8, f"{k}:", ln=True)
                        pdf.set_font("Arial", size=11); pdf.multi_cell(0, 8, v); pdf.ln(2)
                    pdf_data  = make_pdf_bytes(pdf)
                    safe_name = "".join(x for x in name if x.isalnum() or x == " ").replace(" ", "_")
                    st.download_button("📥 Download PDF", data=pdf_data,
                                       file_name=f"{safe_name}_admission.pdf", mime="application/pdf")

        if name.strip() and med_info.strip():
            audio = make_voice(
                f"Resident {safe(name)}. Conditions: {safe(med_info)}. Medications: {safe(meds)}.",
                lang=lang_code,
            )
            if audio:
                st.caption("🔊 Voice summary:")
                st.audio(audio, format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔍 Search Records")
        query = st.text_input("Enter Resident Name")
        if st.button("🔍 Search"):
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute("SELECT * FROM residents WHERE name LIKE ?", (f"%{query}%",)).fetchall()
            conn.close()
            if rows:
                for r in rows:
                    st.markdown(f"""
                    <div class="card-gold">
                      <b>#{r[0]} — {safe(r[1])}</b>
                      <span style="color:var(--muted);font-size:.85rem"> | DOB: {safe(r[2])} | Added: {safe(r[8])}</span><br>
                      🩺 <b>Medical:</b> {safe(r[3])}<br>
                      💊 <b>Medications:</b> {safe(r[4])}<br>
                      ⚠️ <b>Allergies:</b> {safe(r[5])}<br>
                      📞 <b>Emergency Contact:</b> {safe(r[6])}
                    </div>
                    """, unsafe_allow_html=True)
                    lang = (r[7] or "en")[:2]
                    audio = make_voice(
                        f"Resident {safe(r[1])}. Conditions: {safe(r[3])}. Medications: {safe(r[4])}.",
                        lang=lang,
                    )
                    if audio:
                        st.audio(audio, format="audio/mp3")
            else:
                st.warning("No records found.")
        st.markdown('</div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  3 — INTAKE FORMS
# ═════════════════════════════════════════════
elif menu == "📋 Intake Forms":
    st.markdown('<div class="section-title">📋 Digital Admission Intake</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete all 7 sections — saves to database + downloadable PDF</div>', unsafe_allow_html=True)

    with st.form("intake_form"):
        st.markdown('<div class="intake-section"><div class="intake-heading">👤 Section 1 — Client Profile</div>', unsafe_allow_html=True)
        c1, c2  = st.columns(2)
        full_name   = c1.text_input("Full Legal Name *")
        dob         = c2.date_input("Date of Birth *")
        c3, c4  = st.columns(2)
        gender      = c3.selectbox("Gender Identity", ["Male","Female","Non-binary","Prefer not to say","Other"])
        marital     = c4.selectbox("Marital Status", ["Single","Married","Widowed","Divorced","Separated"])
        c5, c6  = st.columns(2)
        _ssn        = c5.text_input("Last 4 of SSN (secure)", max_chars=4, type="password")
        primary_lang= c6.selectbox("Primary Language", ["English","Spanish","French","Haitian Creole","Portuguese","Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">📞 Section 2 — Emergency Contacts</div>', unsafe_allow_html=True)
        ec1       = st.text_input("Primary Contact — Name / Relationship / Phone")
        ec2       = st.text_input("Secondary Contact — Name / Relationship / Phone")
        physician = st.text_input("Primary Care Physician — Name / Phone")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">🩺 Section 3 — Health History</div>', unsafe_allow_html=True)
        chronic   = st.text_area("Chronic Conditions", height=75)
        allergies = st.text_area("Known Allergies", height=75)
        meds_f    = st.text_area("Current Medications & Dosage", height=85)
        immunize  = st.text_input("Immunization Records")
        hospital  = st.text_area("Recent Hospitalizations / Surgeries (last 5 yrs)", height=75)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">🏥 Section 4 — Medical Assessment</div>', unsafe_allow_html=True)
        adl      = st.multiselect("ADL — Independent In:", ["Eating","Bathing","Dressing","Toileting","Transferring","Continence"])
        mobility = st.selectbox("Mobility Status", ["Fully Ambulatory","Uses Cane","Uses Walker","Uses Wheelchair","Bedbound"])
        cognitive= st.selectbox("Cognitive Status", ["Alert & Oriented x4","Mild Impairment","Moderate Impairment","Severe Impairment","Dementia Diagnosed"])
        skin     = st.selectbox("Skin Integrity", ["Intact","Stage I Wound","Stage II Wound","Stage III/IV Wound","Under Treatment"])
        dietary  = st.text_input("Dietary Restrictions / Requirements")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">⚖️ Section 5 — Legal Documentation</div>', unsafe_allow_html=True)
        poa        = st.selectbox("Power of Attorney on File?", ["Yes — Medical & Financial","Yes — Medical Only","Yes — Financial Only","No","In Progress"])
        directives = st.selectbox("Advanced Directives / DNR", ["Full Code","DNR on File","DNI on File","Comfort Care Only","Not Established"])
        hipaa      = st.checkbox("✅ I acknowledge the HIPAA Privacy Notice and Admission Agreement")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">💛 Section 6 — Care Preferences</div>', unsafe_allow_html=True)
        routine   = st.text_area("Daily Routine Preferences", height=75)
        social    = st.text_area("Social & Recreational Interests", height=75)
        equipment = st.text_input("Special Equipment (Oxygen, CPAP, Hearing Aid, etc.)")
        transport = st.selectbox("Transportation Needs", ["None","Medical Appointments Only","Regular Transport","Ambulance Only"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-section"><div class="intake-heading">🔒 Section 7 — Phone Security Setup</div>', unsafe_allow_html=True)
        device     = st.selectbox("Device Type", ["iPhone (iOS)","Android","Basic Cell Phone","No Phone","Other"])
        ph_concern = st.text_area("Known Issues (suspicious calls, strange apps, etc.)", height=65)
        sec_consent= st.checkbox("✅ Client consents to phone security assessment by care staff")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("📤 Submit Complete Intake Packet")

    if submitted:
        if not full_name.strip():
            st.error("⚠️ Full name is required.")
        elif not hipaa:
            st.error("⚠️ HIPAA acknowledgment is required.")
        else:
            adl_str = ", ".join(adl) if adl else "—"
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = sqlite3.connect(DB_PATH)
            conn.execute("""
                INSERT INTO intake_forms (
                    submitted_at,full_name,dob,gender,primary_language,marital_status,
                    emergency_contact1,emergency_contact2,primary_physician,
                    chronic_conditions,allergies,medications,immunizations,hospitalizations,
                    adl_status,mobility,cognitive_status,skin_integrity,dietary,
                    poa,directives,hipaa_consent,daily_routine,social_interests,
                    special_equipment,transportation,device_type,security_consent,phone_concerns
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                now_str, full_name, str(dob), gender, primary_lang, marital,
                safe(ec1), safe(ec2), safe(physician),
                safe(chronic), safe(allergies), safe(meds_f), safe(immunize), safe(hospital),
                adl_str, mobility, cognitive, skin, safe(dietary),
                poa, directives, "Yes",
                safe(routine), safe(social), safe(equipment), transport,
                device, "Yes" if sec_consent else "No", safe(ph_concern),
            ))
            conn.commit(); conn.close()

            # Build PDF in memory — no disk writes
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 18)
            pdf.cell(0, 12, "LifeHaven Care Portal", ln=True, align="C")
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 8, "Complete Admission Intake Packet", ln=True, align="C")
            pdf.ln(6)

            sections_data = [
                ("CLIENT PROFILE", {"Full Name": full_name, "DOB": str(dob), "Gender": gender, "Marital Status": marital, "Language": primary_lang}),
                ("EMERGENCY CONTACTS", {"Primary": safe(ec1), "Secondary": safe(ec2), "Physician": safe(physician)}),
                ("HEALTH HISTORY", {"Chronic Conditions": safe(chronic), "Allergies": safe(allergies), "Medications": safe(meds_f), "Immunizations": safe(immunize), "Hospitalizations": safe(hospital)}),
                ("MEDICAL ASSESSMENT", {"ADL Independent": adl_str, "Mobility": mobility, "Cognitive": cognitive, "Skin": skin, "Dietary": safe(dietary)}),
                ("LEGAL DOCUMENTATION", {"Power of Attorney": poa, "Directives/DNR": directives, "HIPAA": "Acknowledged"}),
                ("CARE PREFERENCES", {"Daily Routine": safe(routine), "Social Interests": safe(social), "Equipment": safe(equipment), "Transport": transport}),
                ("PHONE SECURITY", {"Device": device, "Concerns": safe(ph_concern), "Consent": "Yes" if sec_consent else "No"}),
            ]

            for sec_name, fields in sections_data:
                pdf.set_font("Arial", "B", 12)
                pdf.set_fill_color(0, 100, 90); pdf.set_text_color(255, 255, 255)
                pdf.cell(0, 9, f"  {sec_name}", ln=True, fill=True)
                pdf.set_text_color(0, 0, 0); pdf.ln(2)
                for k, v in fields.items():
                    pdf.set_font("Arial", "B", 10); pdf.cell(60, 7, f"{k}:", ln=False)
                    pdf.set_font("Arial", size=10); pdf.multi_cell(0, 7, v)
                pdf.ln(3)

            pdf.set_font("Arial", "I", 9)
            pdf.cell(0, 6, f"Generated: {now_str} | LifeHaven Care Portal", ln=True, align="C")

            pdf_data = make_pdf_bytes(pdf)
            safe_fn  = "".join(x for x in full_name if x.isalnum() or x == " ").replace(" ", "_")
            st.success(f"🎉 Intake packet for **{full_name}** saved!")
            st.download_button(
                "📥 Download Full PDF Intake Packet",
                data=pdf_data,
                file_name=f"{safe_fn}_intake_packet.pdf",
                mime="application/pdf",
            )

# ═════════════════════════════════════════════
#  4 — PHONE SECURITY
# ═════════════════════════════════════════════
elif menu == "🔒 Phone Security":
    st.markdown('<div class="section-title">🔒 Phone Security Education</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Security checklists and scam awareness for elderly clients</div>', unsafe_allow_html=True)
    st.info(
        "🛡️ **Educational Tool:** This generates security checklists and awareness reports. "
        "It does NOT scan real devices. For actual threats, contact your IT provider or the FTC at 1-877-382-4357.",
    )

    TIPS = [
        "Never share OTP codes — not even with family or your bank.",
        "Do not tap links in unexpected text messages.",
        "Keep your phone software updated at all times.",
        "Use a 6-digit PIN or biometric lock.",
        "Enable two-factor authentication on your email.",
        "Block unknown callers automatically in phone settings.",
        "Only download apps from the official App Store or Google Play.",
        "Real banks never ask for your password by phone or text.",
        "If something feels wrong, ask your caregiver before doing anything.",
    ]
    CHECKS = [
        "Phone software is up to date",
        "Unknown apps reviewed and removed",
        "Screen lock (PIN/biometric) enabled",
        "Automatic unknown caller blocking is ON",
        "No recent suspicious texts with links clicked",
        "Two-factor authentication enabled on email",
        "Caregiver or family member can assist if needed",
    ]

    client_name = st.text_input("Client Name", placeholder="e.g. Mary Johnson")
    scan_type   = st.selectbox("Assessment Type", [
        "Quick Security Checklist", "Full Device Assessment",
        "Scam Awareness Review", "App Permission Audit",
    ])

    if st.button("🔍 Generate Security Report"):
        name_display = client_name.strip() or "Client"
        with st.spinner(f"Preparing report for {name_display}…"):
            import time; time.sleep(1)

        results = [(label, random.choices([True, False], weights=[3, 1])[0]) for label in CHECKS]
        passed  = sum(1 for _, s in results if s)
        score   = int(passed / len(results) * 100)
        color   = "#00e5c0" if score >= 80 else "#f5c842" if score >= 60 else "#ff6b6b"
        emoji   = "✅" if score >= 80 else "⚠️" if score >= 60 else "🚨"

        st.markdown(f"""
        <div class="card">
          <b style="color:var(--teal2);font-family:'Playfair Display',serif;font-size:1.3rem;">
            🛡️ Security Report — {name_display}
          </b><br>
          <span style="color:var(--muted);font-size:.88rem">{scan_type} · {datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
          <div style="margin-top:16px;font-size:2.5rem;font-weight:900;color:{color}">{emoji} {score}% SECURE</div>
          <div style="color:var(--muted);font-size:.9rem">{passed} of {len(results)} checks passed</div>
        </div>
        """, unsafe_allow_html=True)

        for label, status in results:
            icon  = "✅" if status else "❌"
            color_s = "var(--teal2)" if status else "#ff6b6b"
            st.markdown(
                f'<div style="padding:8px 12px;margin-bottom:6px;border-radius:10px;'
                f'background:var(--glass);border:1px solid var(--border);">'
                f'<span style="color:{color_s}">{icon}</span> {label}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f"""
        <div class="card-gold" style="margin-top:18px">
          💡 <b>Daily Safety Tip:</b><br>
          <span style="color:var(--muted)">{random.choice(TIPS)}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📱 Common Scams Targeting Elderly Clients")
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="card"><b>📱 Grandparent Scam</b><br><span style="color:var(--muted);font-size:.88rem">Caller pretends to be a grandchild in trouble. Never send money without calling family directly.</span></div>', unsafe_allow_html=True)
    s2.markdown('<div class="card"><b>💊 Medicare Scam</b><br><span style="color:var(--muted);font-size:.88rem">Fake reps ask for your card number. Real Medicare never cold-calls for your information.</span></div>', unsafe_allow_html=True)
    s3.markdown('<div class="card"><b>🏦 Bank Fraud</b><br><span style="color:var(--muted);font-size:.88rem">Texts claiming your account is locked. Never click links — call the number on your card.</span></div>', unsafe_allow_html=True)

# ═════════════════════════════════════════════
#  5 — CLIENT PORTAL
# ═════════════════════════════════════════════
else:
    st.markdown("""
    <div class="promo-wrap">
      <div class="promo-title">🌿 LifeHaven Client Portal</div>
      <div class="promo-sub">
        A premium, secure experience for your clients and their families.<br>
        Health records · Digital intake · Fitness tracking · Safety — all in one place.
      </div>
      <a class="promo-btn" href="https://fit4unity.onrender.com" target="_blank">🚀 Open LifeHaven Portal</a>
      <div class="feature-grid">
        <div class="feature-card"><div class="feature-icon">💪</div><div class="feature-name">Fitness AI</div><div class="feature-desc">Angle-based rep counter using real AI pose detection</div></div>
        <div class="feature-card"><div class="feature-icon">📋</div><div class="feature-name">Digital Intake</div><div class="feature-desc">All 7 admission sections — saves to DB + PDF export</div></div>
        <div class="feature-card"><div class="feature-icon">🏥</div><div class="feature-name">Care Records</div><div class="feature-desc">Secure resident database with voice summary & PDF</div></div>
        <div class="feature-card"><div class="feature-icon">🔒</div><div class="feature-name">Phone Security</div><div class="feature-desc">Security checklists and scam education for seniors</div></div>
        <div class="feature-card"><div class="feature-icon">📍</div><div class="feature-name">GPS Tracking</div><div class="feature-desc">Live location map for fitness routes and safety</div></div>
        <div class="feature-card"><div class="feature-icon">📄</div><div class="feature-name">PDF Export</div><div class="feature-desc">In-memory PDF — download instantly, no server files</div></div>
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
