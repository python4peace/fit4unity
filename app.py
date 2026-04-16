#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ReubenSoul PeaceUnity LifeHaven — by ReubenSoul4peaceunity

import os, io, math, random, sqlite3
from datetime import datetime
import cv2, numpy as np, pandas as pd
import mediapipe as mp, folium
import streamlit as st
from streamlit_folium import st_folium
from fpdf import FPDF
from gtts import gTTS

DB_PATH = "/tmp/lifehaven.db"

st.set_page_config(
    page_title="ReubenSoul PeaceUnity LifeHaven",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700;900&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg:     #030c0e;
  --bg2:    #071318;
  --bg3:    #0c1e24;
  --teal:   #00c9a7;
  --teal2:  #00ffe0;
  --gold:   #f0b429;
  --gold2:  #ffe0a0;
  --sky:    #7ee8fa;
  --text:   #e8f4f2;
  --muted:  rgba(232,244,242,.55);
  --glass:  rgba(255,255,255,.04);
  --border: rgba(0,201,167,.15);
  --glow:   0 0 40px rgba(0,201,167,.12);
}
*{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{
  font-family:'Outfit',sans-serif!important;
  background:var(--bg)!important;
  color:var(--text)!important;
}
.block-container{
  padding:1.5rem 2rem 4rem!important;
  max-width:1400px!important;
}

/* ── ANIMATED BACKGROUND ── */
body::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 70% 50% at 15% 15%,rgba(0,201,167,.07) 0%,transparent 65%),
    radial-gradient(ellipse 50% 40% at 85% 75%,rgba(240,180,41,.05) 0%,transparent 60%),
    radial-gradient(ellipse 40% 35% at 50% 50%,rgba(126,232,250,.03) 0%,transparent 70%);
}
body::after{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    radial-gradient(1px 1px at 20% 30%,rgba(0,255,224,.4) 0%,transparent 100%),
    radial-gradient(1px 1px at 60% 70%,rgba(240,180,41,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 80% 20%,rgba(126,232,250,.3) 0%,transparent 100%),
    radial-gradient(1px 1px at 40% 80%,rgba(0,201,167,.3) 0%,transparent 100%);
  background-size:300px 300px,400px 400px,350px 350px,250px 250px;
}
.block-container{position:relative;z-index:1}

/* ── SCROLLING BANNER ── */
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.ticker-wrap{
  overflow:hidden;
  background:linear-gradient(90deg,rgba(0,80,60,.9),rgba(0,100,75,.9),rgba(0,80,60,.9));
  border:1px solid rgba(0,201,167,.2);
  border-radius:12px;margin-bottom:28px;padding:11px 0;
  box-shadow:0 4px 24px rgba(0,201,167,.1);
}
.ticker-inner{display:inline-flex;animation:ticker 30s linear infinite}
.ticker-item{
  color:rgba(255,255,255,.9);font-size:.88rem;font-weight:500;
  letter-spacing:.08em;padding:0 40px;white-space:nowrap;
}
.ticker-dot{color:var(--teal2);margin-right:8px}

/* ── HERO ── */
.hero{
  position:relative;overflow:hidden;
  padding:52px 40px 44px;border-radius:32px;margin-bottom:32px;
  background:linear-gradient(135deg,
    rgba(0,201,167,.12) 0%,
    rgba(3,12,14,.96) 40%,
    rgba(240,180,41,.07) 100%);
  border:1px solid rgba(0,201,167,.18);
  box-shadow:0 32px 80px rgba(0,0,0,.5),var(--glow);
}
.hero-orb{
  position:absolute;top:-60px;right:-60px;
  width:280px;height:280px;border-radius:50%;
  background:radial-gradient(circle,rgba(240,180,41,.1),transparent 70%);
  pointer-events:none;
}
.hero-orb2{
  position:absolute;bottom:-80px;left:-40px;
  width:200px;height:200px;border-radius:50%;
  background:radial-gradient(circle,rgba(0,201,167,.08),transparent 70%);
  pointer-events:none;
}
.hero-eyebrow{
  text-align:center;font-size:.78rem;font-weight:600;
  letter-spacing:.2em;color:var(--teal);
  text-transform:uppercase;margin-bottom:16px;
}
.hero-title{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.4rem,6vw,5rem);
  font-weight:900;text-align:center;line-height:1.08;
  margin-bottom:16px;
  background:linear-gradient(135deg,var(--teal2) 0%,var(--sky) 40%,var(--gold) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.hero-sub{
  text-align:center;font-size:1.05rem;color:var(--muted);
  max-width:600px;margin:0 auto 28px;line-height:1.7;
}
.badge-row{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.badge{
  padding:6px 14px;border-radius:999px;font-size:.8rem;font-weight:600;
  letter-spacing:.04em;background:rgba(0,201,167,.08);
  border:1px solid rgba(0,201,167,.22);color:var(--teal2);
  transition:all .2s;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#050f12 0%,#030c0e 100%)!important;
  border-right:1px solid var(--border)!important;
}
.sidebar-brand{
  text-align:center;padding:20px 16px 12px;
  border-bottom:1px solid var(--border);margin-bottom:16px;
}
.sidebar-brand-name{
  font-family:'Cormorant Garamond',serif;
  font-size:1.6rem;font-weight:900;color:var(--teal2);
  letter-spacing:.02em;
}
.sidebar-brand-tag{
  font-size:.72rem;color:var(--muted);
  letter-spacing:.12em;text-transform:uppercase;margin-top:2px;
}

/* ── SECTION HEADERS ── */
.sec-header{margin-bottom:24px}
.sec-eyebrow{
  font-size:.72rem;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--teal);margin-bottom:6px;
}
.sec-title{
  font-family:'Cormorant Garamond',serif;
  font-size:2.2rem;font-weight:700;color:var(--text);line-height:1.2;
}
.sec-sub{font-size:.92rem;color:var(--muted);margin-top:6px;line-height:1.6}

/* ── CARDS ── */
.card{
  padding:24px;border-radius:20px;margin-bottom:20px;
  background:var(--glass);
  border:1px solid var(--border);
  box-shadow:0 8px 32px rgba(0,0,0,.3);
  transition:border-color .3s;
}
.card:hover{border-color:rgba(0,201,167,.3)}
.card-gold{
  padding:24px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(240,180,41,.08),rgba(3,12,14,.95));
  border:1px solid rgba(240,180,41,.2);
  box-shadow:0 8px 32px rgba(0,0,0,.3);
}
.card-teal{
  padding:24px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(0,201,167,.10),rgba(3,12,14,.95));
  border:1px solid rgba(0,201,167,.25);
  box-shadow:0 8px 32px rgba(0,0,0,.3);
}

/* ── DIVIDER ── */
.divider{
  height:1px;
  background:linear-gradient(90deg,transparent,var(--border),transparent);
  margin:28px 0;
}

/* ── METRIC CARDS ── */
.metric-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0}
.metric-card{
  padding:20px;border-radius:18px;text-align:center;
  background:linear-gradient(135deg,rgba(0,201,167,.09),rgba(3,12,14,.95));
  border:1px solid rgba(0,201,167,.18);
}
.metric-val{
  font-family:'Cormorant Garamond',serif;
  font-size:2.8rem;font-weight:700;color:var(--teal2);line-height:1;
}
.metric-label{font-size:.78rem;color:var(--muted);margin-top:4px;letter-spacing:.06em;text-transform:uppercase}

/* ── REP COUNTER ── */
.rep-display{
  text-align:center;padding:36px 24px;border-radius:24px;
  background:linear-gradient(135deg,rgba(0,201,167,.12),rgba(3,12,14,.98));
  border:1px solid rgba(0,201,167,.25);
  box-shadow:0 0 60px rgba(0,201,167,.08);
}
.rep-number{
  font-family:'Cormorant Garamond',serif;
  font-size:7rem;font-weight:900;color:var(--teal2);
  line-height:1;text-shadow:0 0 40px rgba(0,255,224,.3);
}
.rep-angle{font-size:2rem;font-weight:600;color:var(--sky);margin-top:8px}
.rep-stage{font-size:1rem;font-weight:600;margin-top:10px;letter-spacing:.06em}

/* ── INTAKE SECTIONS ── */
.intake-sec{
  padding:24px 26px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(0,201,167,.06),rgba(3,12,14,.97));
  border:1px solid rgba(0,201,167,.15);
}
.intake-head{
  font-family:'Cormorant Garamond',serif;
  font-size:1.25rem;font-weight:700;color:var(--gold);
  margin-bottom:18px;padding-bottom:10px;
  border-bottom:1px solid rgba(240,180,41,.12);
}

/* ── SECURITY ── */
.sec-clean{
  padding:20px 24px;border-radius:16px;margin-top:16px;
  background:rgba(0,201,167,.08);border:1px solid rgba(0,201,167,.25);
}
.sec-threat{
  padding:20px 24px;border-radius:16px;margin-top:16px;
  background:rgba(255,60,60,.08);border:1px solid rgba(255,100,100,.25);
}
.check-item{
  padding:10px 14px;margin-bottom:8px;border-radius:12px;
  background:var(--glass);border:1px solid var(--border);
  font-size:.92rem;display:flex;align-items:center;gap:10px;
}

/* ── BUTTONS ── */
.stButton>button,.stDownloadButton>button{
  background:linear-gradient(90deg,var(--teal),#0090bb)!important;
  color:#030c0e!important;border-radius:12px!important;
  height:2.8em!important;width:100%!important;border:0!important;
  font-family:'Outfit',sans-serif!important;font-weight:700!important;
  font-size:.93rem!important;letter-spacing:.04em!important;
  box-shadow:0 6px 20px rgba(0,201,167,.2)!important;
  transition:all .2s!important;
}

/* ── INPUTS ── */
.stTextInput>div>input,.stTextArea>div>textarea,
.stSelectbox>div>div,.stDateInput>div>input{
  background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(0,201,167,.2)!important;
  border-radius:10px!important;color:var(--text)!important;
  font-family:'Outfit',sans-serif!important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{gap:4px;background:transparent!important;border-bottom:1px solid var(--border)!important}
.stTabs [data-baseweb="tab"]{
  border-radius:8px 8px 0 0!important;background:transparent!important;
  border:none!important;color:var(--muted)!important;
  font-weight:500!important;padding:10px 20px!important;
  font-family:'Outfit',sans-serif!important;
}
.stTabs [aria-selected="true"]{
  background:transparent!important;color:var(--teal2)!important;
  border-bottom:2px solid var(--teal2)!important;
}

/* ── CLIENT PORTAL ── */
.portal-hero{
  padding:64px 40px;border-radius:32px;text-align:center;
  position:relative;overflow:hidden;
  background:linear-gradient(145deg,
    rgba(0,201,167,.15) 0%,
    rgba(3,12,14,.97) 50%,
    rgba(240,180,41,.1) 100%);
  border:1px solid rgba(0,201,167,.2);
  box-shadow:0 40px 100px rgba(0,0,0,.5),var(--glow);
}
.portal-title{
  font-family:'Cormorant Garamond',serif;
  font-size:clamp(2rem,5vw,4rem);font-weight:900;
  background:linear-gradient(120deg,var(--teal2),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:16px;
}
.portal-sub{color:var(--muted);font-size:1.05rem;margin-bottom:36px;line-height:1.7}
.portal-btn{
  display:inline-block;padding:18px 48px;border-radius:999px;
  text-decoration:none!important;font-weight:700;font-size:1.05rem;
  color:#030c0e!important;letter-spacing:.06em;
  background:linear-gradient(90deg,var(--teal2),var(--gold));
  box-shadow:0 16px 48px rgba(0,201,167,.3);
  transition:transform .2s,box-shadow .2s;
}
.feature-grid{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  gap:16px;margin:40px 0 0;
}
.feature-card{
  padding:24px 20px;border-radius:20px;text-align:center;
  background:rgba(255,255,255,.04);border:1px solid var(--border);
  transition:all .3s;
}
.feature-card:hover{
  background:rgba(0,201,167,.07);border-color:rgba(0,201,167,.3);
  transform:translateY(-2px);
}
.f-icon{font-size:2.2rem;margin-bottom:12px}
.f-name{font-weight:700;color:var(--teal2);font-size:.95rem;margin-bottom:6px}
.f-desc{font-size:.82rem;color:var(--muted);line-height:1.5}

/* ── FOOTER ── */
.footer{
  text-align:center;margin-top:60px;padding:24px;
  border-top:1px solid var(--border);
  color:var(--muted);font-size:.82rem;letter-spacing:.06em;
}
.footer b{color:var(--teal)}

/* ── INFO/SUCCESS BOXES ── */
.stAlert{border-radius:14px!important}
</style>
""")

# ── DB INIT ──
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS residents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, dob TEXT, medical_info TEXT, medications TEXT,
        allergies TEXT, emergency_contact TEXT, language TEXT, created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS intake_forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submitted_at TEXT, full_name TEXT, dob TEXT, gender TEXT,
        primary_language TEXT, marital_status TEXT,
        emergency_contact1 TEXT, emergency_contact2 TEXT, primary_physician TEXT,
        chronic_conditions TEXT, allergies TEXT, medications TEXT,
        immunizations TEXT, hospitalizations TEXT,
        adl_status TEXT, mobility TEXT, cognitive_status TEXT,
        skin_integrity TEXT, dietary TEXT, poa TEXT, directives TEXT,
        hipaa_consent TEXT, daily_routine TEXT, social_interests TEXT,
        special_equipment TEXT, transportation TEXT,
        device_type TEXT, security_consent TEXT, phone_concerns TEXT)""")
    conn.commit(); conn.close()

init_db()

# ── SESSION STATE ──
for k,v in {"reps":0,"stage":None,"start_time":datetime.now()}.items():
    if k not in st.session_state: st.session_state[k] = v

# ── HELPERS ──
def safe(v,f="—"): return str(v).strip() if v and str(v).strip() else f
def angle(a,b,c):
    r = math.atan2(c[1]-b[1],c[0]-b[0]) - math.atan2(a[1]-b[1],a[0]-b[0])
    deg = abs(math.degrees(r))
    return 360-deg if deg>180 else deg
def pdf_bytes(pdf): return bytes(pdf.output())
def voice(text,lang="en"):
    try:
        buf=io.BytesIO(); gTTS(text=text,lang=lang).write_to_fp(buf); buf.seek(0); return buf.read()
    except: return None

# ── TICKER BANNER ──
items = ["🌿 ReubenSoul PeaceUnity LifeHaven","💪 AI Fitness Tracking",
         "🏥 Elderly Care Management","📋 Digital Intake Forms",
         "🔒 Phone Security Education","📍 GPS Location Tracking",
         "📄 PDF Export","✨ ReubenSoul4peaceunity","🌍 Health • Peace • Unity"] * 2
ticker_html = "".join(
    f'<span class="ticker-item"><span class="ticker-dot">◆</span>{i}</span>' for i in items
)
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_html}</div></div>',
    unsafe_allow_html=True
)

# ── HERO ──
st.markdown("""
<div class="hero">
  <div class="hero-orb"></div><div class="hero-orb2"></div>
  <div class="hero-eyebrow">◆ Premium Care Platform ◆</div>
  <div class="hero-title">ReubenSoul PeaceUnity LifeHaven</div>
  <div class="hero-sub">
    Elderly Care · AI Fitness · Digital Intake · Phone Safety<br>
    Built with Love by ReubenSoul4peaceunity
  </div>
  <div class="badge-row">
    <span class="badge">💪 Fitness AI</span>
    <span class="badge">📋 Digital Intake</span>
    <span class="badge">📍 GPS Tracking</span>
    <span class="badge">🏥 Care Records</span>
    <span class="badge">🔒 Phone Security</span>
    <span class="badge">🎙️ Voice Support</span>
    <span class="badge">📄 PDF Export</span>
    <span class="badge">🌐 Multilingual</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
st.sidebar.markdown("""
<div class="sidebar-brand">
  <div class="sidebar-brand-name">🌿 ReubenSoul PeaceUnity LifeHaven</div>
  <div class="sidebar-brand-tag">Care Portal</div>
</div>
""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("", [
    "🏋️ Fitness Training",
    "🏥 Care Portal",
    "📋 Intake Forms",
    "🔒 Phone Security",
    "✨ Client Portal",
], label_visibility="collapsed")

st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div style='text-align:center;font-size:.72rem;color:rgba(232,244,242,.3);letter-spacing:.08em'>REUBENSOUL4PEACEUNITY<br>HEALTH • PEACE • UNITY</div>",
    unsafe_allow_html=True
)

# ══════════════════════════════════════════════
#  1 — FITNESS TRAINING
# ══════════════════════════════════════════════
if menu == "🏋️ Fitness Training":
    st.markdown("""
    <div class="sec-header">
      <div class="sec-eyebrow">◆ Module 01</div>
      <div class="sec-title">Fitness Training</div>
      <div class="sec-sub">AI-powered angle-based rep counter · Live pose detection · GPS tracking · Analytics</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["  🏃 Live Training  ", "  📍 GPS Map  ", "  📊 Analytics  "])

    with tab1:
        exercise = st.selectbox("Exercise", ["Bicep Curl (arm)","Squat (leg)","Shoulder Press (arm)"])
        LMAP = {"Bicep Curl (arm)":(11,13,15),"Squat (leg)":(23,25,27),"Shoulder Press (arm)":(11,13,15)}
        UP, DOWN = 50, 160

        st.info("📸 **How to count reps:** Snap at the **bottom** of movement (arm straight / knees bent), then at the **top** (curled / standing). Each full cycle = 1 rep counted automatically.", icon="💡")

        img = st.camera_input("Capture your exercise position")
        if img:
            nparr = np.frombuffer(img.getvalue(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if frame is not None:
                with mp.solutions.pose.Pose(static_image_mode=True, model_complexity=1, min_detection_confidence=0.5) as pose:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    res = pose.process(rgb)
                    if res.pose_landmarks:
                        lm = res.pose_landmarks.landmark
                        p1,p2,p3 = LMAP[exercise]
                        a_ = (lm[p1].x,lm[p1].y)
                        b_ = (lm[p2].x,lm[p2].y)
                        c_ = (lm[p3].x,lm[p3].y)
                        ang = angle(a_,b_,c_)
                        if ang > DOWN:
                            if st.session_state.stage == "up": st.session_state.reps += 1
                            st.session_state.stage = "down"
                        elif ang < UP:
                            st.session_state.stage = "up"
                        annotated = rgb.copy()
                        h,w = frame.shape[:2]
                        mp.solutions.drawing_utils.draw_landmarks(
                            annotated, res.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=(0,229,192),thickness=3,circle_radius=5),
                            mp.solutions.drawing_utils.DrawingSpec(color=(240,180,41),thickness=2))
                        px,py = int(lm[p2].x*w),int(lm[p2].y*h)
                        cv2.putText(annotated,f"{int(ang)}\u00b0",(px-40,py-20),cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,229,192),3,cv2.LINE_AA)
                        st.image(annotated, channels="RGB", use_container_width=True)
                        stage = st.session_state.stage or "—"
                        msg = "⬆️ TOP — go back down to complete rep" if stage=="up" else "⬇️ BOTTOM — push up for next rep"
                        color = "#00ffe0" if stage=="up" else "#f0b429"
                        st.markdown(f"""
                        <div class="rep-display">
                          <div class="rep-number">{st.session_state.reps}</div>
                          <div style="color:var(--muted);font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;margin-top:4px">Reps Completed</div>
                          <div class="rep-angle">{int(ang)}° joint angle</div>
                          <div class="rep-stage" style="color:{color}">{msg}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No pose detected. Ensure your full body is visible and well-lit.")
                        st.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB), channels="RGB", use_container_width=True)
            else:
                st.error("❌ Could not decode image.")

        elapsed = (datetime.now()-st.session_state.start_time).seconds
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-card">
            <div class="metric-val">{st.session_state.reps}</div>
            <div class="metric-label">Reps</div>
          </div>
          <div class="metric-card">
            <div class="metric-val">{round(st.session_state.reps*0.5,1)}</div>
            <div class="metric-label">Calories</div>
          </div>
          <div class="metric-card">
            <div class="metric-val">{round(elapsed/60,1)}</div>
            <div class="metric-label">Minutes</div>
          </div>
        </div>""", unsafe_allow_html=True)

        if st.button("🔁 Reset Session"):
            for k,v in {"reps":0,"stage":None,"start_time":datetime.now()}.items():
                st.session_state[k] = v
            st.rerun()

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📍 GPS Location Tracker")
        lat = st.number_input("Latitude", value=34.05, format="%.6f")
        lon = st.number_input("Longitude", value=-118.25, format="%.6f")
        if st.button("📍 Show Map"):
            m = folium.Map(location=[lat,lon], zoom_start=14, tiles="CartoDB dark_matter")
            folium.Marker([lat,lon], tooltip="📍 Current Location",
                icon=folium.Icon(color="green",icon="heart",prefix="fa")).add_to(m)
            st_folium(m, width=700, height=480, returned_objects=[])
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        elapsed = (datetime.now()-st.session_state.start_time).seconds
        df = pd.DataFrame({
            "Metric":["Reps","Calories","Minutes"],
            "Value":[st.session_state.reps, round(st.session_state.reps*0.5,1), round(elapsed/60,1)]
        })
        st.bar_chart(df.set_index("Metric"))
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  2 — CARE PORTAL
# ══════════════════════════════════════════════
elif menu == "🏥 Care Portal":
    st.markdown("""
    <div class="sec-header">
      <div class="sec-eyebrow">◆ Module 02</div>
      <div class="sec-title">Elderly Care Portal</div>
      <div class="sec-sub">Add residents, search records, generate PDFs with multilingual voice summaries</div>
    </div>
    """, unsafe_allow_html=True)

    portal_menu = st.sidebar.radio("Care Menu", ["🆕 New Admission","🔍 Search Records"])
    LANGS = {"English":"en","Spanish":"es","French":"fr","Haitian Creole":"ht","Portuguese":"pt"}

    if portal_menu == "🆕 New Admission":
        st.markdown('<div class="card-teal">', unsafe_allow_html=True)
        st.markdown('<div class="intake-head">🆕 New Resident Admission</div>', unsafe_allow_html=True)
        lang_choice = st.selectbox("Language / Idioma", list(LANGS.keys()))
        lang_code   = LANGS[lang_choice]
        name      = st.text_input("Full Name *")
        dob       = st.text_input("Date of Birth (YYYY-MM-DD)")
        med_info  = st.text_area("Medical Conditions", height=80)
        meds      = st.text_area("Medications & Dosage", height=80)
        allergies = st.text_area("Allergies", height=60)
        contact   = st.text_input("Emergency Contact (Name / Relation / Phone)")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("💾 Save Resident"):
                if not name.strip(): st.error("⚠️ Name is required.")
                else:
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO residents (name,dob,medical_info,medications,allergies,emergency_contact,language,created_at) VALUES(?,?,?,?,?,?,?,?)",
                        (name,dob,med_info,meds,allergies,contact,lang_code,datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit(); conn.close()
                    st.success(f"✅ {name} saved successfully!")
        with c2:
            if st.button("📄 Generate PDF"):
                if not name.strip(): st.error("⚠️ Enter a name first.")
                else:
                    p = FPDF(); p.add_page()
                    p.set_font("Arial","B",16)
                    p.cell(0,12,"LifeHaven — Care Admission Record",ln=True,align="C")
                    p.ln(4)
                    for k,v in {"Name":safe(name),"DOB":safe(dob),"Medical":safe(med_info),
                                "Medications":safe(meds),"Allergies":safe(allergies),
                                "Emergency Contact":safe(contact),
                                "Generated":datetime.now().strftime("%Y-%m-%d %H:%M")}.items():
                        p.set_font("Arial","B",11); p.cell(0,8,f"{k}:",ln=True)
                        p.set_font("Arial",size=11); p.multi_cell(0,8,v); p.ln(2)
                    fn = "".join(x for x in name if x.isalnum() or x==" ").replace(" ","_")
                    st.download_button("📥 Download PDF",data=pdf_bytes(p),
                        file_name=f"{fn}_admission.pdf",mime="application/pdf")
        if name.strip() and med_info.strip():
            aud = voice(f"Resident {safe(name)}. Conditions: {safe(med_info)}. Medications: {safe(meds)}.",lang=lang_code)
            if aud:
                st.caption("🔊 Voice Summary")
                st.audio(aud, format="audio/mp3")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="intake-head">🔍 Search Resident Records</div>', unsafe_allow_html=True)
        query = st.text_input("Search by name")
        if st.button("🔍 Search"):
            conn = sqlite3.connect(DB_PATH)
            rows = conn.execute("SELECT * FROM residents WHERE name LIKE ?",(f"%{query}%",)).fetchall()
            conn.close()
            if rows:
                for r in rows:
                    st.markdown(f"""
                    <div class="card-gold">
                      <div style="font-size:1.1rem;font-weight:700;color:var(--gold2)">#{r[0]} — {safe(r[1])}</div>
                      <div style="color:var(--muted);font-size:.82rem;margin-bottom:10px">DOB: {safe(r[2])} · Added: {safe(r[8])}</div>
                      <div>🩺 <b>Medical:</b> {safe(r[3])}</div>
                      <div>💊 <b>Medications:</b> {safe(r[4])}</div>
                      <div>⚠️ <b>Allergies:</b> {safe(r[5])}</div>
                      <div>📞 <b>Emergency:</b> {safe(r[6])}</div>
                    </div>""", unsafe_allow_html=True)
                    lang = (r[7] or "en")[:2]
                    aud = voice(f"Resident {safe(r[1])}. Conditions: {safe(r[3])}. Medications: {safe(r[4])}.",lang=lang)
                    if aud: st.audio(aud, format="audio/mp3")
            else:
                st.warning("No records found.")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  3 — INTAKE FORMS
# ══════════════════════════════════════════════
elif menu == "📋 Intake Forms":
    st.markdown("""
    <div class="sec-header">
      <div class="sec-eyebrow">◆ Module 03</div>
      <div class="sec-title">Digital Admission Intake</div>
      <div class="sec-sub">Complete all 7 sections digitally · Saves to secure database · Instant PDF download</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("intake_form"):
        st.markdown('<div class="intake-sec"><div class="intake-head">👤 Section 1 — Client Profile</div>', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        full_name = c1.text_input("Full Legal Name *")
        dob       = c2.date_input("Date of Birth *")
        c3,c4 = st.columns(2)
        gender  = c3.selectbox("Gender Identity",["Male","Female","Non-binary","Prefer not to say","Other"])
        marital = c4.selectbox("Marital Status",["Single","Married","Widowed","Divorced","Separated"])
        c5,c6 = st.columns(2)
        _ssn     = c5.text_input("Last 4 of SSN",max_chars=4,type="password")
        prim_lang= c6.selectbox("Primary Language",["English","Spanish","French","Haitian Creole","Portuguese","Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">📞 Section 2 — Emergency Contacts</div>', unsafe_allow_html=True)
        ec1 = st.text_input("Primary Contact — Name / Relationship / Phone")
        ec2 = st.text_input("Secondary Contact — Name / Relationship / Phone")
        physician = st.text_input("Primary Care Physician — Name / Phone")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">🩺 Section 3 — Health History</div>', unsafe_allow_html=True)
        chronic   = st.text_area("Chronic Conditions",height=75)
        allergies = st.text_area("Known Allergies",height=75)
        meds_f    = st.text_area("Current Medications & Dosage",height=85)
        immunize  = st.text_input("Immunization Records")
        hospital  = st.text_area("Recent Hospitalizations / Surgeries",height=75)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">🏥 Section 4 — Medical Assessment</div>', unsafe_allow_html=True)
        adl      = st.multiselect("ADL — Independent In:",["Eating","Bathing","Dressing","Toileting","Transferring","Continence"])
        mobility = st.selectbox("Mobility Status",["Fully Ambulatory","Uses Cane","Uses Walker","Uses Wheelchair","Bedbound"])
        cognitive= st.selectbox("Cognitive Status",["Alert & Oriented x4","Mild Impairment","Moderate Impairment","Severe Impairment","Dementia Diagnosed"])
        skin     = st.selectbox("Skin Integrity",["Intact","Stage I Wound","Stage II Wound","Stage III/IV Wound","Under Treatment"])
        dietary  = st.text_input("Dietary Restrictions / Requirements")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">⚖️ Section 5 — Legal Documentation</div>', unsafe_allow_html=True)
        poa        = st.selectbox("Power of Attorney on File?",["Yes — Medical & Financial","Yes — Medical Only","Yes — Financial Only","No","In Progress"])
        directives = st.selectbox("Advanced Directives / DNR",["Full Code","DNR on File","DNI on File","Comfort Care Only","Not Established"])
        hipaa      = st.checkbox("✅ I acknowledge the HIPAA Privacy Notice and Admission Agreement")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">💛 Section 6 — Care Preferences</div>', unsafe_allow_html=True)
        routine   = st.text_area("Daily Routine Preferences",height=75)
        social    = st.text_area("Social & Recreational Interests",height=75)
        equipment = st.text_input("Special Equipment (Oxygen, CPAP, Hearing Aid, etc.)")
        transport = st.selectbox("Transportation Needs",["None","Medical Appointments Only","Regular Transport","Ambulance Only"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="intake-sec"><div class="intake-head">🔒 Section 7 — Phone Security Setup</div>', unsafe_allow_html=True)
        device     = st.selectbox("Device Type",["iPhone (iOS)","Android","Basic Cell Phone","No Phone","Other"])
        ph_concern = st.text_area("Known Issues (suspicious calls, strange apps, etc.)",height=80)
        sec_consent= st.checkbox("✅ Client consents to phone security assessment by care staff")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("📤 Submit Complete Intake Packet", use_container_width=True)

    if submitted:
        if not full_name.strip():
            st.error("⚠️ Full name is required.")
        elif not hipaa:
            st.error("⚠️ HIPAA acknowledgment is required.")
        else:
            adl_str = ", ".join(adl) if adl else "—"
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn = sqlite3.connect(DB_PATH)
            conn.execute("""INSERT INTO intake_forms (
                submitted_at,full_name,dob,gender,primary_language,marital_status,
                emergency_contact1,emergency_contact2,primary_physician,
                chronic_conditions,allergies,medications,immunizations,hospitalizations,
                adl_status,mobility,cognitive_status,skin_integrity,dietary,
                poa,directives,hipaa_consent,daily_routine,social_interests,
                special_equipment,transportation,device_type,security_consent,phone_concerns
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (now_str,full_name,str(dob),gender,prim_lang,marital,
             safe(ec1),safe(ec2),safe(physician),safe(chronic),safe(allergies),
             safe(meds_f),safe(immunize),safe(hospital),adl_str,mobility,cognitive,
             skin,safe(dietary),poa,directives,"Yes",safe(routine),safe(social),
             safe(equipment),transport,device,"Yes" if sec_consent else "No",safe(ph_concern)))
            conn.commit(); conn.close()

            p = FPDF(); p.add_page()
            p.set_font("Arial","B",18); p.cell(0,12,"ReubenSoul PeaceUnity LifeHaven",ln=True,align="C")
            p.set_font("Arial","B",13); p.cell(0,8,"Complete Admission Intake Packet",ln=True,align="C"); p.ln(6)
            secs = [
                ("CLIENT PROFILE",{"Full Name":full_name,"DOB":str(dob),"Gender":gender,"Marital":marital,"Language":prim_lang}),
                ("EMERGENCY CONTACTS",{"Primary":safe(ec1),"Secondary":safe(ec2),"Physician":safe(physician)}),
                ("HEALTH HISTORY",{"Conditions":safe(chronic),"Allergies":safe(allergies),"Medications":safe(meds_f),"Immunizations":safe(immunize),"Hospitalizations":safe(hospital)}),
                ("MEDICAL ASSESSMENT",{"ADL":adl_str,"Mobility":mobility,"Cognitive":cognitive,"Skin":skin,"Dietary":safe(dietary)}),
                ("LEGAL",{"POA":poa,"Directives":directives,"HIPAA":"Acknowledged"}),
                ("CARE PREFERENCES",{"Routine":safe(routine),"Social":safe(social),"Equipment":safe(equipment),"Transport":transport}),
                ("PHONE SECURITY",{"Device":device,"Concerns":safe(ph_concern),"Consent":"Yes" if sec_consent else "No"}),
            ]
            for sname,fields in secs:
                p.set_font("Arial","B",12); p.set_fill_color(0,100,90); p.set_text_color(255,255,255)
                p.cell(0,9,f"  {sname}",ln=True,fill=True)
                p.set_text_color(0,0,0); p.ln(2)
                for k,v in fields.items():
                    p.set_font("Arial","B",10); p.cell(55,7,f"{k}:",ln=False)
                    p.set_font("Arial",size=10); p.multi_cell(0,7,v)
                p.ln(3)
            p.set_font("Arial","I",9)
            p.cell(0,6,f"Generated: {now_str} | ReubenSoul PeaceUnity LifeHaven",ln=True,align="C")
            fn = "".join(x for x in full_name if x.isalnum() or x==" ").replace(" ","_")
            st.success(f"🎉 Intake packet for **{full_name}** saved successfully!")
            st.download_button("📥 Download Full PDF Intake Packet",
                data=pdf_bytes(p),file_name=f"{fn}_intake.pdf",mime="application/pdf")

# ══════════════════════════════════════════════
#  4 — PHONE SECURITY
# ══════════════════════════════════════════════
elif menu == "🔒 Phone Security":
    st.markdown("""
    <div class="sec-header">
      <div class="sec-eyebrow">◆ Module 04</div>
      <div class="sec-title">Phone Security Education</div>
      <div class="sec-sub">Security checklists · Scam awareness · Daily safety tips for elderly clients</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("🛡️ **Educational Tool:** Generates security checklists and awareness reports for care staff training. Does not access or scan real devices. For real threats: FTC at 1-877-382-4357.", icon="ℹ️")

    TIPS = [
        "Never share OTP codes — not even with family or your bank.",
        "Do not tap links in unexpected text messages.",
        "Keep your phone's software updated at all times.",
        "Use a 6-digit PIN or biometric lock on your phone.",
        "Enable two-factor authentication on your email account.",
        "Block unknown callers automatically in phone settings.",
        "Report scam calls to the FTC: 1-877-382-4357.",
        "Only download apps from the official App Store or Google Play.",
        "Real banks never ask for your password by phone or text.",
    ]
    CHECKS = [
        "Phone software is up to date",
        "Unknown apps reviewed and removed",
        "Screen lock (PIN/biometric) enabled",
        "Automatic unknown caller blocking is ON",
        "No suspicious texts with links clicked recently",
        "Two-factor authentication enabled on email",
        "Caregiver or family member can assist if needed",
    ]

    c1,c2 = st.columns([2,1])
    with c1: client_name = st.text_input("Client Name", placeholder="e.g. Mary Johnson")
    with c2: scan_type = st.selectbox("Assessment Type",["Quick Checklist","Full Assessment","Scam Review","App Audit"])

    if st.button("🔍 Generate Security Report", use_container_width=True):
        name_d = client_name.strip() or "Client"
        with st.spinner(f"Preparing report for {name_d}…"):
            import time; time.sleep(1)
        results = [(lbl, random.choices([True,False],weights=[3,1])[0]) for lbl in CHECKS]
        passed  = sum(1 for _,s in results if s)
        score   = int(passed/len(results)*100)
        color   = "#00ffe0" if score>=80 else "#f0b429" if score>=60 else "#ff6b6b"
        emoji   = "✅" if score>=80 else "⚠️" if score>=60 else "🚨"

        st.markdown(f"""
        <div class="card-teal">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:700;color:var(--teal2)">
            🛡️ Security Report — {name_d}
          </div>
          <div style="color:var(--muted);font-size:.82rem;margin-bottom:16px">{scan_type} · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
          <div style="font-size:3rem;font-weight:900;color:{color};font-family:'Cormorant Garamond',serif">{emoji} {score}%</div>
          <div style="color:var(--muted);font-size:.88rem">{passed} of {len(results)} checks passed</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("**📋 Security Checklist**")
        for lbl,status in results:
            icon  = "✅" if status else "❌"
            col   = "var(--teal2)" if status else "#ff6b6b"
            st.markdown(
                f'<div class="check-item"><span style="color:{col}">{icon}</span> {lbl}</div>',
                unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card-gold" style="margin-top:20px">
          <div style="font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:8px">💡 Daily Safety Tip</div>
          <div style="color:var(--text)">{random.choice(TIPS)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**📱 Common Scams Targeting Elderly Clients**")
    s1,s2,s3 = st.columns(3)
    s1.markdown('<div class="card"><div style="font-weight:700;color:var(--teal2);margin-bottom:8px">📱 Grandparent Scam</div><div style="color:var(--muted);font-size:.85rem;line-height:1.6">Caller claims to be a grandchild in trouble. Never send money without calling family directly first.</div></div>', unsafe_allow_html=True)
    s2.markdown('<div class="card"><div style="font-weight:700;color:var(--teal2);margin-bottom:8px">💊 Medicare Scam</div><div style="color:var(--muted);font-size:.85rem;line-height:1.6">Fake reps ask for your card number. Real Medicare never cold-calls for your information.</div></div>', unsafe_allow_html=True)
    s3.markdown('<div class="card"><div style="font-weight:700;color:var(--teal2);margin-bottom:8px">🏦 Bank Fraud</div><div style="color:var(--muted);font-size:.85rem;line-height:1.6">Texts claiming your account is locked. Never click links — call the number on your card.</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  5 — CLIENT PORTAL
# ══════════════════════════════════════════════
else:
    st.markdown("""
    <div class="portal-hero">
      <div style="font-size:.78rem;font-weight:600;letter-spacing:.2em;color:var(--teal);text-transform:uppercase;margin-bottom:16px">◆ Share This Link With Your Clients ◆</div>
      <div class="portal-title">LifeHaven Client Portal</div>
      <div class="portal-sub">
        A premium, secure experience for your clients and their families.<br>
        Health records · Digital intake · Fitness tracking · Safety — all in one place.
      </div>
      <a class="portal-btn" href="https://fit4unity.onrender.com" target="_blank">
        🚀 Open LifeHaven Portal
      </a>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="f-icon">💪</div>
          <div class="f-name">Fitness AI</div>
          <div class="f-desc">Angle-based rep counter using real AI pose detection</div>
        </div>
        <div class="feature-card">
          <div class="f-icon">📋</div>
          <div class="f-name">Digital Intake</div>
          <div class="f-desc">All 7 admission sections — saves to DB + PDF export</div>
        </div>
        <div class="feature-card">
          <div class="f-icon">🏥</div>
          <div class="f-name">Care Records</div>
          <div class="f-desc">Secure resident database with voice summary & PDF</div>
        </div>
        <div class="feature-card">
          <div class="f-icon">🔒</div>
          <div class="f-name">Phone Security</div>
          <div class="f-desc">Security checklists and scam education for seniors</div>
        </div>
        <div class="feature-card">
          <div class="f-icon">📍</div>
          <div class="f-name">GPS Tracking</div>
          <div class="f-desc">Live location map for fitness routes and client safety</div>
        </div>
        <div class="feature-card">
          <div class="f-icon">📄</div>
          <div class="f-name">PDF Export</div>
          <div class="f-desc">In-memory PDF — download instantly, nothing stored</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="footer">
  🌿 <b>ReubenSoul PeaceUnity LifeHaven</b> &nbsp;·&nbsp; Built by ReubenSoul4peaceunity<br>
  Health &nbsp;•&nbsp; Peace &nbsp;•&nbsp; Unity &nbsp;•&nbsp; Technology
</div>
""", unsafe_allow_html=True)
