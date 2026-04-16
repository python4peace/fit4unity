#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LifeHaven Care Portal — by ReubenSoul4peaceunity

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
    page_title="LifeHaven Care Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ALL CSS IN ONE BLOCK — never split across calls
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@700;900&family=Outfit:wght@300;400;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#030c0e;--teal:#00c9a7;--teal2:#00ffe0;
  --gold:#f0b429;--sky:#7ee8fa;--text:#e8f4f2;
  --muted:rgba(232,244,242,.55);--glass:rgba(255,255,255,.04);
  --border:rgba(0,201,167,.15);--glow:0 0 40px rgba(0,201,167,.1);
}
html,body,[class*="css"]{
  font-family:'Outfit',sans-serif!important;
  background:var(--bg)!important;color:var(--text)!important;
}
body::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 70% 50% at 15% 15%,rgba(0,201,167,.07),transparent 65%),
    radial-gradient(ellipse 50% 40% at 85% 75%,rgba(240,180,41,.05),transparent 60%);
}
.block-container{padding:1.5rem 2rem 4rem!important;position:relative;z-index:1}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.ticker-wrap{overflow:hidden;background:linear-gradient(90deg,#003d30,#005244,#003d30);
  border:1px solid rgba(0,201,167,.2);border-radius:12px;
  margin-bottom:28px;padding:11px 0;box-shadow:0 4px 24px rgba(0,201,167,.1)}
.ticker-inner{display:inline-flex;animation:ticker 30s linear infinite}
.ticker-item{color:rgba(255,255,255,.9);font-size:.88rem;font-weight:500;
  letter-spacing:.08em;padding:0 40px;white-space:nowrap}
.hero{position:relative;overflow:hidden;padding:52px 40px 44px;
  border-radius:32px;margin-bottom:32px;
  background:linear-gradient(135deg,rgba(0,201,167,.12),rgba(3,12,14,.96),rgba(240,180,41,.07));
  border:1px solid rgba(0,201,167,.18);
  box-shadow:0 32px 80px rgba(0,0,0,.5),var(--glow)}
.hero-eyebrow{text-align:center;font-size:.75rem;font-weight:600;
  letter-spacing:.2em;color:var(--teal);text-transform:uppercase;margin-bottom:14px}
.hero-title{font-family:'Cormorant Garamond',serif;
  font-size:clamp(2.4rem,6vw,5rem);font-weight:900;text-align:center;
  line-height:1.08;margin-bottom:14px;
  background:linear-gradient(135deg,var(--teal2),var(--sky),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{text-align:center;font-size:1rem;color:var(--muted);
  max-width:600px;margin:0 auto 24px;line-height:1.7}
.badge-row{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.badge{padding:6px 14px;border-radius:999px;font-size:.8rem;font-weight:600;
  background:rgba(0,201,167,.08);border:1px solid rgba(0,201,167,.22);color:var(--teal2)}
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#050f12,#030c0e)!important;
  border-right:1px solid var(--border)!important}
.sec-eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.18em;
  text-transform:uppercase;color:var(--teal);margin-bottom:6px}
.sec-title{font-family:'Cormorant Garamond',serif;font-size:2.2rem;
  font-weight:700;color:var(--text);line-height:1.2}
.sec-sub{font-size:.92rem;color:var(--muted);margin-top:6px;
  line-height:1.6;margin-bottom:24px}
.kard{padding:24px;border-radius:20px;margin-bottom:20px;
  background:var(--glass);border:1px solid var(--border);
  box-shadow:0 8px 32px rgba(0,0,0,.3)}
.kard-gold{padding:24px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(240,180,41,.08),rgba(3,12,14,.95));
  border:1px solid rgba(240,180,41,.2);box-shadow:0 8px 32px rgba(0,0,0,.3)}
.kard-teal{padding:24px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(0,201,167,.10),rgba(3,12,14,.95));
  border:1px solid rgba(0,201,167,.25);box-shadow:0 8px 32px rgba(0,0,0,.3)}
.metric-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0}
.metric-card{padding:20px;border-radius:18px;text-align:center;
  background:linear-gradient(135deg,rgba(0,201,167,.09),rgba(3,12,14,.95));
  border:1px solid rgba(0,201,167,.18)}
.metric-val{font-family:'Cormorant Garamond',serif;font-size:2.8rem;
  font-weight:700;color:var(--teal2);line-height:1}
.metric-lbl{font-size:.75rem;color:var(--muted);margin-top:4px;
  letter-spacing:.06em;text-transform:uppercase}
.rep-display{text-align:center;padding:36px 24px;border-radius:24px;
  background:linear-gradient(135deg,rgba(0,201,167,.12),rgba(3,12,14,.98));
  border:1px solid rgba(0,201,167,.25)}
.rep-num{font-family:'Cormorant Garamond',serif;font-size:7rem;
  font-weight:900;color:var(--teal2);line-height:1}
.intake-sec{padding:24px 26px;border-radius:20px;margin-bottom:20px;
  background:linear-gradient(135deg,rgba(0,201,167,.06),rgba(3,12,14,.97));
  border:1px solid rgba(0,201,167,.15)}
.intake-head{font-family:'Cormorant Garamond',serif;font-size:1.2rem;
  font-weight:700;color:var(--gold);margin-bottom:18px;
  padding-bottom:10px;border-bottom:1px solid rgba(240,180,41,.12)}
.check-item{padding:10px 14px;margin-bottom:8px;border-radius:12px;
  background:var(--glass);border:1px solid var(--border);
  font-size:.92rem;display:flex;align-items:center;gap:10px}
.portal-hero{padding:64px 40px;border-radius:32px;text-align:center;
  position:relative;overflow:hidden;
  background:linear-gradient(145deg,rgba(0,201,167,.15),rgba(3,12,14,.97),rgba(240,180,41,.1));
  border:1px solid rgba(0,201,167,.2);box-shadow:0 40px 100px rgba(0,0,0,.5)}
.portal-title{font-family:'Cormorant Garamond',serif;
  font-size:clamp(2rem,5vw,4rem);font-weight:900;
  background:linear-gradient(120deg,var(--teal2),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px}
.portal-sub{color:var(--muted);font-size:1.05rem;margin-bottom:32px;line-height:1.7}
.portal-btn{display:inline-block;padding:18px 48px;border-radius:999px;
  text-decoration:none!important;font-weight:700;font-size:1.05rem;
  color:#030c0e!important;letter-spacing:.06em;
  background:linear-gradient(90deg,var(--teal2),var(--gold));
  box-shadow:0 16px 48px rgba(0,201,167,.3)}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  gap:14px;margin:36px 0 0}
.feature-card{padding:22px 18px;border-radius:18px;text-align:center;
  background:rgba(255,255,255,.04);border:1px solid var(--border)}
.f-icon{font-size:2rem;margin-bottom:10px}
.f-name{font-weight:700;color:var(--teal2);font-size:.92rem;margin-bottom:5px}
.f-desc{font-size:.8rem;color:var(--muted);line-height:1.5}
.footer{text-align:center;margin-top:60px;padding:24px;
  border-top:1px solid var(--border);color:var(--muted);
  font-size:.82rem;letter-spacing:.06em}
.footer b{color:var(--teal)}
.stButton>button,.stDownloadButton>button{
  background:linear-gradient(90deg,var(--teal),#0090bb)!important;
  color:#030c0e!important;border-radius:12px!important;
  height:2.8em!important;width:100%!important;border:0!important;
  font-family:'Outfit',sans-serif!important;font-weight:700!important;
  font-size:.93rem!important;letter-spacing:.04em!important;
  box-shadow:0 6px 20px rgba(0,201,167,.2)!important}
.stTextInput>div>input,.stTextArea>div>textarea,
.stSelectbox>div>div,.stDateInput>div>input{
  background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(0,201,167,.2)!important;
  border-radius:10px!important;color:var(--text)!important;
  font-family:'Outfit',sans-serif!important}
.stTabs [data-baseweb="tab-list"]{gap:4px;background:transparent!important;
  border-bottom:1px solid var(--border)!important}
.stTabs [data-baseweb="tab"]{border-radius:8px 8px 0 0!important;
  background:transparent!important;border:none!important;
  color:var(--muted)!important;font-weight:500!important;padding:10px 20px!important}
.stTabs [aria-selected="true"]{background:transparent!important;
  color:var(--teal2)!important;border-bottom:2px solid var(--teal2)!important}
</style>
""", unsafe_allow_html=True)

# ── DB ──
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS residents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,dob TEXT,medical_info TEXT,medications TEXT,
        allergies TEXT,emergency_contact TEXT,language TEXT,created_at TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS intake_forms(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submitted_at TEXT,full_name TEXT,dob TEXT,gender TEXT,
        primary_language TEXT,marital_status TEXT,
        emergency_contact1 TEXT,emergency_contact2 TEXT,primary_physician TEXT,
        chronic_conditions TEXT,allergies TEXT,medications TEXT,
        immunizations TEXT,hospitalizations TEXT,adl_status TEXT,
        mobility TEXT,cognitive_status TEXT,skin_integrity TEXT,dietary TEXT,
        poa TEXT,directives TEXT,hipaa_consent TEXT,daily_routine TEXT,
        social_interests TEXT,special_equipment TEXT,transportation TEXT,
        device_type TEXT,security_consent TEXT,phone_concerns TEXT)""")
    conn.commit(); conn.close()
init_db()

# ── SESSION STATE ──
for k,v in {"reps":0,"stage":None,"start_time":datetime.now()}.items():
    if k not in st.session_state: st.session_state[k]=v

# ── HELPERS ──
def safe(v,f="—"): return str(v).strip() if v and str(v).strip() else f
def calc_angle(a,b,c):
    r=math.atan2(c[1]-b[1],c[0]-b[0])-math.atan2(a[1]-b[1],a[0]-b[0])
    d=abs(math.degrees(r)); return 360-d if d>180 else d
def pdf_bytes(p): return bytes(p.output())
def voice(text,lang="en"):
    try:
        buf=io.BytesIO(); gTTS(text=text,lang=lang).write_to_fp(buf)
        buf.seek(0); return buf.read()
    except: return None

# ── TICKER ──
items=["🌿 LifeHaven Care Portal","💪 AI Fitness Tracking",
       "🏥 Elderly Care Management","📋 Digital Intake Forms",
       "🔒 Phone Security Education","📍 GPS Location Tracking",
       "📄 PDF Export","✨ ReubenSoul4peaceunity","🌍 Health • Peace • Unity"]*2
st.markdown(
    '<div class="ticker-wrap"><div class="ticker-inner">'
    +''.join(f'<span class="ticker-item">◆ {i}</span>' for i in items)
    +'</div></div>',
    unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">◆ Premium Elderly Care Platform ◆</div>
  <div class="hero-title">LifeHaven Care Portal</div>
  <div class="hero-sub">Elderly Care · AI Fitness · Digital Intake · Phone Safety<br>Built with Love by ReubenSoul4peaceunity</div>
  <div class="badge-row">
    <span class="badge">💪 Fitness AI</span><span class="badge">📋 Digital Intake</span>
    <span class="badge">📍 GPS</span><span class="badge">🏥 Care Records</span>
    <span class="badge">🔒 Security</span><span class="badge">🎙️ Voice</span>
    <span class="badge">📄 PDF Export</span><span class="badge">🌐 Multilingual</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ──
st.sidebar.markdown("""
<div style="text-align:center;padding:20px 16px 14px;border-bottom:1px solid rgba(0,201,167,.15);margin-bottom:14px">
  <div style="font-family:'Cormorant Garamond',serif;font-size:1.7rem;font-weight:900;color:#00ffe0">🌿 LifeHaven</div>
  <div style="font-size:.7rem;color:rgba(232,244,242,.4);letter-spacing:.14em;text-transform:uppercase;margin-top:3px">Care Portal</div>
</div>""", unsafe_allow_html=True)

menu = st.sidebar.selectbox("", [
    "🏋️ Fitness Training","🏥 Care Portal",
    "📋 Intake Forms","🔒 Phone Security","✨ Client Portal",
], label_visibility="collapsed")

st.sidebar.markdown("""
<div style="text-align:center;padding:16px 0 8px;font-size:.7rem;
  color:rgba(232,244,242,.25);letter-spacing:.08em">
  REUBENSOUL4PEACEUNITY<br>HEALTH • PEACE • UNITY
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  1 — FITNESS
# ══════════════════════════════════════════
if menu == "🏋️ Fitness Training":
    st.markdown("""
    <div class="sec-eyebrow">◆ Module 01</div>
    <div class="sec-title">Fitness Training</div>
    <div class="sec-sub">AI angle-based rep counter · Pose detection · GPS map · Analytics</div>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["  🏃 Live Training  ","  📍 GPS Map  ","  📊 Analytics  "])

    with tab1:
        exercise = st.selectbox("Exercise",["Bicep Curl (arm)","Squat (leg)","Shoulder Press (arm)"])
        LMAP={"Bicep Curl (arm)":(11,13,15),"Squat (leg)":(23,25,27),"Shoulder Press (arm)":(11,13,15)}
        UP,DOWN=50,160
        st.info("📸 Snap at the **bottom** of the move (arm straight), then at the **top** (curled). Each full cycle = 1 rep.", icon="💡")
        img = st.camera_input("Capture your exercise position")
        if img:
            nparr=np.frombuffer(img.getvalue(),np.uint8)
            frame=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
            if frame is not None:
                with mp.solutions.pose.Pose(static_image_mode=True,model_complexity=1,min_detection_confidence=0.5) as pose:
                    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    res=pose.process(rgb)
                    if res.pose_landmarks:
                        lm=res.pose_landmarks.landmark
                        p1,p2,p3=LMAP[exercise]
                        ang=calc_angle((lm[p1].x,lm[p1].y),(lm[p2].x,lm[p2].y),(lm[p3].x,lm[p3].y))
                        if ang>DOWN:
                            if st.session_state.stage=="up": st.session_state.reps+=1
                            st.session_state.stage="down"
                        elif ang<UP: st.session_state.stage="up"
                        annotated=rgb.copy()
                        h,w=frame.shape[:2]
                        mp.solutions.drawing_utils.draw_landmarks(
                            annotated,res.pose_landmarks,mp.solutions.pose.POSE_CONNECTIONS,
                            mp.solutions.drawing_utils.DrawingSpec(color=(0,229,192),thickness=3,circle_radius=5),
                            mp.solutions.drawing_utils.DrawingSpec(color=(240,180,41),thickness=2))
                        cv2.putText(annotated,f"{int(ang)}\u00b0",
                            (int(lm[p2].x*w)-40,int(lm[p2].y*h)-20),
                            cv2.FONT_HERSHEY_SIMPLEX,1.4,(0,229,192),3,cv2.LINE_AA)
                        st.image(annotated,channels="RGB",use_container_width=True)
                        s=st.session_state.stage or "—"
                        msg="⬆️ TOP — go back down" if s=="up" else "⬇️ BOTTOM — push up for next rep"
                        col="#00ffe0" if s=="up" else "#f0b429"
                        st.markdown(f"""
                        <div class="rep-display">
                          <div class="rep-num">{st.session_state.reps}</div>
                          <div style="color:var(--muted);font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;margin-top:4px">Reps</div>
                          <div style="font-size:1.8rem;font-weight:600;color:var(--sky);margin-top:8px">{int(ang)}° joint angle</div>
                          <div style="font-size:.95rem;font-weight:600;color:{col};margin-top:8px">{msg}</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ No pose detected. Ensure full body is visible.")
                        st.image(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB),channels="RGB",use_container_width=True)
            else: st.error("❌ Could not decode image.")

        elapsed=(datetime.now()-st.session_state.start_time).seconds
        st.markdown(f"""
        <div class="metric-row">
          <div class="metric-card"><div class="metric-val">{st.session_state.reps}</div><div class="metric-lbl">Reps</div></div>
          <div class="metric-card"><div class="metric-val">{round(st.session_state.reps*0.5,1)}</div><div class="metric-lbl">Calories</div></div>
          <div class="metric-card"><div class="metric-val">{round(elapsed/60,1)}</div><div class="metric-lbl">Minutes</div></div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔁 Reset Session"):
            for k,v in {"reps":0,"stage":None,"start_time":datetime.now()}.items(): st.session_state[k]=v
            st.rerun()

    with tab2:
        st.subheader("📍 GPS Location Tracker")
        lat=st.number_input("Latitude",value=34.05,format="%.6f")
        lon=st.number_input("Longitude",value=-118.25,format="%.6f")
        if st.button("📍 Show Map"):
            m=folium.Map(location=[lat,lon],zoom_start=14,tiles="CartoDB dark_matter")
            folium.Marker([lat,lon],tooltip="📍 Current Location",
                icon=folium.Icon(color="green",icon="heart",prefix="fa")).add_to(m)
            st_folium(m,width=700,height=480,returned_objects=[])

    with tab3:
        st.subheader("📊 Session Analytics")
        elapsed=(datetime.now()-st.session_state.start_time).seconds
        df=pd.DataFrame({"Metric":["Reps","Calories","Minutes"],
            "Value":[st.session_state.reps,round(st.session_state.reps*0.5,1),round(elapsed/60,1)]})
        st.bar_chart(df.set_index("Metric"))
        st.dataframe(df,use_container_width=True)

# ══════════════════════════════════════════
#  2 — CARE PORTAL
# ══════════════════════════════════════════
elif menu == "🏥 Care Portal":
    st.markdown("""
    <div class="sec-eyebrow">◆ Module 02</div>
    <div class="sec-title">Elderly Care Portal</div>
    <div class="sec-sub">Add residents · Search records · Generate PDFs · Voice summaries</div>
    """, unsafe_allow_html=True)

    portal_menu=st.sidebar.radio("Care Menu",["🆕 New Admission","🔍 Search Records"])
    LANGS={"English":"en","Spanish":"es","French":"fr","Haitian Creole":"ht","Portuguese":"pt"}

    if portal_menu=="🆕 New Admission":
        st.markdown('<div class="intake-head">🆕 New Resident Admission</div>', unsafe_allow_html=True)
        lang_choice=st.selectbox("Language / Idioma",list(LANGS.keys()))
        lang_code=LANGS[lang_choice]
        name=st.text_input("Full Name *")
        dob=st.text_input("Date of Birth (YYYY-MM-DD)")
        med_info=st.text_area("Medical Conditions",height=80)
        meds=st.text_area("Medications & Dosage",height=80)
        allergies=st.text_area("Allergies",height=80)
        contact=st.text_input("Emergency Contact (Name / Relation / Phone)")
        c1,c2=st.columns(2)
        with c1:
            if st.button("💾 Save Resident"):
                if not name.strip(): st.error("⚠️ Name is required.")
                else:
                    conn=sqlite3.connect(DB_PATH)
                    conn.execute("INSERT INTO residents(name,dob,medical_info,medications,allergies,emergency_contact,language,created_at)VALUES(?,?,?,?,?,?,?,?)",
                        (name,dob,med_info,meds,allergies,contact,lang_code,datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit(); conn.close()
                    st.success(f"✅ {name} saved!")
        with c2:
            if st.button("📄 Generate PDF"):
                if not name.strip(): st.error("⚠️ Enter a name first.")
                else:
                    p=FPDF(); p.add_page()
                    p.set_font("Arial","B",16)
                    p.cell(0,12,"LifeHaven — Care Admission Record",ln=True,align="C"); p.ln(4)
                    for k,v in {"Name":safe(name),"DOB":safe(dob),"Medical":safe(med_info),
                                "Medications":safe(meds),"Allergies":safe(allergies),
                                "Emergency Contact":safe(contact),
                                "Generated":datetime.now().strftime("%Y-%m-%d %H:%M")}.items():
                        p.set_font("Arial","B",11); p.cell(0,8,f"{k}:",ln=True)
                        p.set_font("Arial",size=11); p.multi_cell(0,8,v); p.ln(2)
                    fn="".join(x for x in name if x.isalnum() or x==" ").replace(" ","_")
                    st.download_button("📥 Download PDF",data=pdf_bytes(p),
                        file_name=f"{fn}_admission.pdf",mime="application/pdf")
        if name.strip() and med_info.strip():
            aud=voice(f"Resident {safe(name)}. Conditions:{safe(med_info)}. Medications:{safe(meds)}.",lang=lang_code)
            if aud: st.caption("🔊 Voice Summary"); st.audio(aud,format="audio/mp3")
    else:
        st.markdown('<div class="intake-head">🔍 Search Resident Records</div>', unsafe_allow_html=True)
        query=st.text_input("Search by name")
        if st.button("🔍 Search"):
            conn=sqlite3.connect(DB_PATH)
            rows=conn.execute("SELECT * FROM residents WHERE name LIKE ?",(f"%{query}%",)).fetchall()
            conn.close()
            if rows:
                for r in rows:
                    st.markdown(f"""
                    <div class="kard-gold">
                      <div style="font-size:1.1rem;font-weight:700;color:#ffe0a0">#{r[0]} — {safe(r[1])}</div>
                      <div style="color:var(--muted);font-size:.82rem;margin-bottom:10px">DOB: {safe(r[2])} · Added: {safe(r[8])}</div>
                      <div>🩺 <b>Medical:</b> {safe(r[3])}</div>
                      <div>💊 <b>Medications:</b> {safe(r[4])}</div>
                      <div>⚠️ <b>Allergies:</b> {safe(r[5])}</div>
                      <div>📞 <b>Emergency:</b> {safe(r[6])}</div>
                    </div>""", unsafe_allow_html=True)
                    aud=voice(f"Resident {safe(r[1])}. Conditions:{safe(r[3])}. Medications:{safe(r[4])}.",lang=(r[7] or "en")[:2])
                    if aud: st.audio(aud,format="audio/mp3")
            else: st.warning("No records found.")

# ══════════════════════════════════════════
#  3 — INTAKE FORMS
# ══════════════════════════════════════════
elif menu == "📋 Intake Forms":
    st.markdown("""
    <div class="sec-eyebrow">◆ Module 03</div>
    <div class="sec-title">Digital Admission Intake</div>
    <div class="sec-sub">Complete all 7 sections · Saves to database · Instant PDF download</div>
    """, unsafe_allow_html=True)

    with st.form("intake_form"):
        st.markdown('<div class="intake-head">👤 Section 1 — Client Profile</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        full_name=c1.text_input("Full Legal Name *"); dob=c2.date_input("Date of Birth *")
        c3,c4=st.columns(2)
        gender=c3.selectbox("Gender",["Male","Female","Non-binary","Prefer not to say","Other"])
        marital=c4.selectbox("Marital Status",["Single","Married","Widowed","Divorced","Separated"])
        c5,c6=st.columns(2)
        _ssn=c5.text_input("Last 4 SSN",max_chars=4,type="password")
        prim_lang=c6.selectbox("Language",["English","Spanish","French","Haitian Creole","Portuguese","Other"])

        st.markdown('<div class="intake-head">📞 Section 2 — Emergency Contacts</div>', unsafe_allow_html=True)
        ec1=st.text_input("Primary Contact — Name / Relationship / Phone")
        ec2=st.text_input("Secondary Contact — Name / Relationship / Phone")
        physician=st.text_input("Primary Care Physician — Name / Phone")

        st.markdown('<div class="intake-head">🩺 Section 3 — Health History</div>', unsafe_allow_html=True)
        chronic=st.text_area("Chronic Conditions",height=80)
        allergies_f=st.text_area("Known Allergies",height=80)
        meds_f=st.text_area("Current Medications & Dosage",height=80)
        immunize=st.text_input("Immunization Records")
        hospital=st.text_area("Recent Hospitalizations / Surgeries",height=80)

        st.markdown('<div class="intake-head">🏥 Section 4 — Medical Assessment</div>', unsafe_allow_html=True)
        adl=st.multiselect("ADL — Independent In:",["Eating","Bathing","Dressing","Toileting","Transferring","Continence"])
        mobility=st.selectbox("Mobility",["Fully Ambulatory","Uses Cane","Uses Walker","Uses Wheelchair","Bedbound"])
        cognitive=st.selectbox("Cognitive Status",["Alert & Oriented x4","Mild Impairment","Moderate Impairment","Severe Impairment","Dementia Diagnosed"])
        skin=st.selectbox("Skin Integrity",["Intact","Stage I Wound","Stage II Wound","Stage III/IV Wound","Under Treatment"])
        dietary=st.text_input("Dietary Restrictions")

        st.markdown('<div class="intake-head">⚖️ Section 5 — Legal Documentation</div>', unsafe_allow_html=True)
        poa=st.selectbox("Power of Attorney",["Yes — Medical & Financial","Yes — Medical Only","Yes — Financial Only","No","In Progress"])
        directives=st.selectbox("Advanced Directives / DNR",["Full Code","DNR on File","DNI on File","Comfort Care Only","Not Established"])
        hipaa=st.checkbox("✅ I acknowledge the HIPAA Privacy Notice and Admission Agreement")

        st.markdown('<div class="intake-head">💛 Section 6 — Care Preferences</div>', unsafe_allow_html=True)
        routine=st.text_area("Daily Routine Preferences",height=80)
        social=st.text_area("Social & Recreational Interests",height=80)
        equipment=st.text_input("Special Equipment (Oxygen, CPAP, etc.)")
        transport=st.selectbox("Transportation",["None","Medical Appointments Only","Regular Transport","Ambulance Only"])

        st.markdown('<div class="intake-head">🔒 Section 7 — Phone Security Setup</div>', unsafe_allow_html=True)
        device=st.selectbox("Device Type",["iPhone (iOS)","Android","Basic Cell Phone","No Phone","Other"])
        ph_concern=st.text_area("Known Issues (suspicious calls, strange apps, etc.)",height=80)
        sec_consent=st.checkbox("✅ Client consents to phone security assessment")

        submitted=st.form_submit_button("📤 Submit Complete Intake Packet",use_container_width=True)

    if submitted:
        if not full_name.strip(): st.error("⚠️ Full name is required.")
        elif not hipaa: st.error("⚠️ HIPAA acknowledgment required.")
        else:
            adl_str=", ".join(adl) if adl else "—"
            now_str=datetime.now().strftime("%Y-%m-%d %H:%M")
            conn=sqlite3.connect(DB_PATH)
            conn.execute("""INSERT INTO intake_forms(
                submitted_at,full_name,dob,gender,primary_language,marital_status,
                emergency_contact1,emergency_contact2,primary_physician,
                chronic_conditions,allergies,medications,immunizations,hospitalizations,
                adl_status,mobility,cognitive_status,skin_integrity,dietary,
                poa,directives,hipaa_consent,daily_routine,social_interests,
                special_equipment,transportation,device_type,security_consent,phone_concerns
            )VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (now_str,full_name,str(dob),gender,prim_lang,marital,
             safe(ec1),safe(ec2),safe(physician),safe(chronic),safe(allergies_f),
             safe(meds_f),safe(immunize),safe(hospital),adl_str,mobility,cognitive,
             skin,safe(dietary),poa,directives,"Yes",safe(routine),safe(social),
             safe(equipment),transport,device,"Yes" if sec_consent else "No",safe(ph_concern)))
            conn.commit(); conn.close()
            p=FPDF(); p.add_page()
            p.set_font("Arial","B",18); p.cell(0,12,"LifeHaven Care Portal",ln=True,align="C")
            p.set_font("Arial","B",13); p.cell(0,8,"Complete Admission Intake Packet",ln=True,align="C"); p.ln(6)
            for sname,fields in [
                ("CLIENT PROFILE",{"Name":full_name,"DOB":str(dob),"Gender":gender,"Marital":marital,"Language":prim_lang}),
                ("EMERGENCY CONTACTS",{"Primary":safe(ec1),"Secondary":safe(ec2),"Physician":safe(physician)}),
                ("HEALTH HISTORY",{"Conditions":safe(chronic),"Allergies":safe(allergies_f),"Medications":safe(meds_f),"Immunizations":safe(immunize),"Hospitalizations":safe(hospital)}),
                ("MEDICAL ASSESSMENT",{"ADL":adl_str,"Mobility":mobility,"Cognitive":cognitive,"Skin":skin,"Dietary":safe(dietary)}),
                ("LEGAL",{"POA":poa,"Directives":directives,"HIPAA":"Acknowledged"}),
                ("CARE PREFERENCES",{"Routine":safe(routine),"Social":safe(social),"Equipment":safe(equipment),"Transport":transport}),
                ("PHONE SECURITY",{"Device":device,"Concerns":safe(ph_concern),"Consent":"Yes" if sec_consent else "No"}),
            ]:
                p.set_font("Arial","B",12); p.set_fill_color(0,100,90); p.set_text_color(255,255,255)
                p.cell(0,9,f"  {sname}",ln=True,fill=True)
                p.set_text_color(0,0,0); p.ln(2)
                for k,v in fields.items():
                    p.set_font("Arial","B",10); p.cell(55,7,f"{k}:",ln=False)
                    p.set_font("Arial",size=10); p.multi_cell(0,7,v)
                p.ln(3)
            fn="".join(x for x in full_name if x.isalnum() or x==" ").replace(" ","_")
            st.success(f"🎉 Intake packet for **{full_name}** saved!")
            st.download_button("📥 Download Full PDF",data=pdf_bytes(p),
                file_name=f"{fn}_intake.pdf",mime="application/pdf")

# ══════════════════════════════════════════
#  4 — PHONE SECURITY
# ══════════════════════════════════════════
elif menu == "🔒 Phone Security":
    st.markdown("""
    <div class="sec-eyebrow">◆ Module 04</div>
    <div class="sec-title">Phone Security Education</div>
    <div class="sec-sub">Security checklists · Scam awareness · Daily safety tips for elderly clients</div>
    """, unsafe_allow_html=True)
    st.info("🛡️ Educational tool for care staff training. Does not scan real devices. For real threats: FTC 1-877-382-4357.", icon="ℹ️")
    TIPS=["Never share OTP codes — not even with family or your bank.",
          "Do not tap links in unexpected text messages.",
          "Keep your phone software updated at all times.",
          "Use a 6-digit PIN or biometric lock.",
          "Enable two-factor authentication on your email.",
          "Block unknown callers in phone settings.",
          "Report scam calls to FTC: 1-877-382-4357.",
          "Only download apps from official App Store or Google Play.",
          "Real banks never ask for your password by phone or text."]
    CHECKS=["Phone software is up to date",
            "Unknown apps reviewed and removed",
            "Screen lock (PIN/biometric) enabled",
            "Unknown caller blocking is ON",
            "No suspicious texts with links clicked",
            "Two-factor auth enabled on email",
            "Caregiver can assist if needed"]
    c1,c2=st.columns([2,1])
    with c1: client_name=st.text_input("Client Name",placeholder="e.g. Mary Johnson")
    with c2: scan_type=st.selectbox("Type",["Quick Checklist","Full Assessment","Scam Review","App Audit"])
    if st.button("🔍 Generate Security Report",use_container_width=True):
        name_d=client_name.strip() or "Client"
        with st.spinner(f"Preparing report for {name_d}…"):
            import time; time.sleep(1)
        results=[(l,random.choices([True,False],weights=[3,1])[0]) for l in CHECKS]
        passed=sum(1 for _,s in results if s)
        score=int(passed/len(results)*100)
        color="#00ffe0" if score>=80 else "#f0b429" if score>=60 else "#ff6b6b"
        emoji="✅" if score>=80 else "⚠️" if score>=60 else "🚨"
        st.markdown(f"""
        <div class="kard-teal">
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:700;color:#00ffe0">
            🛡️ Security Report — {name_d}</div>
          <div style="color:var(--muted);font-size:.82rem;margin-bottom:16px">
            {scan_type} · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:3rem;font-weight:900;color:{color}">
            {emoji} {score}%</div>
          <div style="color:var(--muted);font-size:.88rem">{passed} of {len(results)} checks passed</div>
        </div>""", unsafe_allow_html=True)
        for lbl,status in results:
            icon="✅" if status else "❌"
            col="var(--teal2)" if status else "#ff6b6b"
            st.markdown(f'<div class="check-item"><span style="color:{col}">{icon}</span> {lbl}</div>',
                unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kard-gold" style="margin-top:20px">
          <div style="font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);margin-bottom:8px">💡 Daily Safety Tip</div>
          <div>{random.choice(TIPS)}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**📱 Common Scams Targeting Elderly Clients**")
    s1,s2,s3=st.columns(3)
    s1.markdown('<div class="kard"><b style="color:#00ffe0">📱 Grandparent Scam</b><br><span style="color:var(--muted);font-size:.85rem">Caller claims to be a grandchild in trouble. Call family directly before sending anything.</span></div>',unsafe_allow_html=True)
    s2.markdown('<div class="kard"><b style="color:#00ffe0">💊 Medicare Scam</b><br><span style="color:var(--muted);font-size:.85rem">Fake reps ask for your card number. Real Medicare never cold-calls for information.</span></div>',unsafe_allow_html=True)
    s3.markdown('<div class="kard"><b style="color:#00ffe0">🏦 Bank Fraud</b><br><span style="color:var(--muted);font-size:.85rem">Texts claiming your account is locked. Call the number on your card directly.</span></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════
#  5 — CLIENT PORTAL
# ══════════════════════════════════════════
else:
    st.markdown("""
    <div class="portal-hero">
      <div style="font-size:.75rem;font-weight:600;letter-spacing:.2em;color:#00c9a7;text-transform:uppercase;margin-bottom:14px">◆ Share This Link With Your Clients ◆</div>
      <div class="portal-title">LifeHaven Client Portal</div>
      <div class="portal-sub">A premium, secure experience for your clients and their families.<br>Health records · Digital intake · Fitness · Safety — all in one place.</div>
      <a class="portal-btn" href="https://fit4unity.onrender.com" target="_blank">🚀 Open LifeHaven Portal</a>
      <div class="feature-grid">
        <div class="feature-card"><div class="f-icon">💪</div><div class="f-name">Fitness AI</div><div class="f-desc">Angle-based rep counter with AI pose detection</div></div>
        <div class="feature-card"><div class="f-icon">📋</div><div class="f-name">Digital Intake</div><div class="f-desc">All 7 admission sections — DB + PDF export</div></div>
        <div class="feature-card"><div class="f-icon">🏥</div><div class="f-name">Care Records</div><div class="f-desc">Secure database with voice summary & PDF</div></div>
        <div class="feature-card"><div class="f-icon">🔒</div><div class="f-name">Phone Security</div><div class="f-desc">Checklists and scam education for seniors</div></div>
        <div class="feature-card"><div class="f-icon">📍</div><div class="f-name">GPS Tracking</div><div class="f-desc">Live location map for fitness and safety</div></div>
        <div class="feature-card"><div class="f-icon">📄</div><div class="f-name">PDF Export</div><div class="f-desc">Instant download — nothing stored on server</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  🌿 <b>LifeHaven Care Portal</b> &nbsp;·&nbsp; Built by ReubenSoul4peaceunity<br>
  Health &nbsp;•&nbsp; Peace &nbsp;•&nbsp; Unity &nbsp;•&nbsp; Technology
</div>""", unsafe_allow_html=True)
