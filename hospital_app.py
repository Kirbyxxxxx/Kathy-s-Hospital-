import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

st.set_page_config(
  page_title="Smart Hospital Patient Navigator",
  page_icon="🏥",
  layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html,body. [class"css'] {font-family: 'Inter', sans-serif; }
#mainMenu [ Visisbility: hidden;}
header[data-testid="stHeader"] {display:none;}
.stDeployButtton {display: none }
footer {visibility:hidden;}
.block-container {padding-top:0 !important; padding-bottom 2rem !important; max-width:1100px !important;}
div[data-testid="stform"] {border:none; padding:0;}

div.stButton > button {
    background: linear-gradient(135deg, #1a56db, #1e429f) !important;
    color: white !important; border:none !imortant;
    border-radius: 12px !important; padding : 0.75rem 2rem !imortant;
    font-size: 16px !imortant; font-weight: 600 !important;
    width: 100% !imortant; letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(26,86,219,0,35) !important;
  }
  div.stButton > button:hover {background:linear-gradient(135deg, #1e429f, #1a56db) !important; }

  div[data-testide="stCheckbox"] label{
      font-size: 14 px !important; font-weight: 500 !important; color: #374151 !important;
  }
</style>
""",unsafe_allow_html=True)

@st.cache_resource
def load_model():
  with open('hospital_model.pkl','rb') as f:
    return pickle.load(f)

bundle = load_model()
model = bundle["model"]
scaler = bundle["scaler"]
features = bundle["features"]
cols_to_scale = bundle["cols_to_scale"]
dept_map_inv = bundle["dept_map_inv"]
gender_map = bundle["gender_map"]
temp_map = bundle["temp_map"]
hr_map = bundle["hr_map"]
dur_map = bundle["dur_map"]
cc_map = bundle["cc_map"]

DEPT_INFO = {
  "Respiratory Medicine": {
    'icon':'🫁','color':'#81A6C6','bg':'#4A70A9','border':'#9BB4C0',
    'desc':'Specialises in conditions affecting the lungs and airways.',
    'next':['Visist level 2, Wing B','Estimated wait: 15-25 mins','Please wear a mask']
  },
   "Cardiology": {
    'icon':'❤️','color':'#DCCFC0','bg':'#A77F60','border':'#4B4038',
    'desc':'Specialises in heart and cardiovascular conditions.',
    'next':['Visist level 3, Wing A','Estimated wait: 20-30 mins','Please bring any previous ESG reports']
   },
  "Gastroenterology": {
    'icon':'🫃','color':'#778873','bg':'#607456','border':'#546B41',
    'desc':'Specialises in digestive system and abdominal conditions.',
    'next':['Visist level 1, Wing C','Estimated wait: 20-25 mins','Please Avouid Eating before consultation']
  },
"Neurology": {
    'icon':'🧠','color':'#E2B59A','bg':'#B77466','border':'#957C62',
    'desc':'Specialises in brain, spine, and nervous system conditions.',
    'next':['Visist level 4, Wing A','Estimated wait: 30-40','Please bring a list of current medication']
  },
"General Medicine": {
    'icon':'🩺','color':'#059669','bg':'#dlfae5','border':'#6ee7b7',
    'desc':'Handles general health concerns and non-specialist conditions.',
    'next':['Visist level 1, Wing A','Estimated wait: 18-25 mins','Registration desk is open 24/7']
  },
"Dermatology": {
    'icon':'🔬','color':'#b45309','bg':'#fef9c3','border':'#fde68a',
    'desc':'Specialises in skin, hair, and nail conditions.',
    'next':['Visist level 2, Wing D','Estimated wait: 15-20 mins','Please bring photos of affected areas if possible']
  },
}

#--Hero Profile
st.markdown("""
<div style="background:lenear-gradient(135deg,#1e3a8a 0%, #1a56db 60%, #0ea5e9 100%);
            padding:3rem 2 rem;margin:-1rem 2rem;text-align center;">
        <div style = "font-size:14px;font-weight:599;color:rgba(255,255,255,0.7);
              text-transform:uppercase;letter-spacing:0.1em;margin-bottom:12px;">
              🏥Future Classroom     Machine Learning
        </div>
        <div style="font-size:36px;font-weight:700;color:ffffff;margin-bottom:12px;
                  letter-spacing:-0.02em;">
            Smart Hospital Navigator
      </div>
      <div style = "font-size:18px;color:rgba(255,255,255,0.85);font-weight:499;">
      Find the Right department for your symptoms
      </div>
</div>
""",unsafe_allow_html=True)
#Form
with st.form("triage_form"):

  #Section 1 - Symptoms
  st.markdown("""
  <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:14px;
              padding:20px 24px;margin-bottom20px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                  <span style="background:#0284c7;color:white;border-radius:8px;
                               padding:4px 10px; font-size:12px; font-weight:600;">1</span>
                  <span style="font-size:16px;font-weight:600;color:#0c4a6e;">What are your main symptoms?</span>
                  <span style="font-size:13px;color:#6b7280;font-style:italic;">Select all that apply</span>
          </div>
  </div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
  fever = st.checkbox("Fever")
  cough = st.checkbox("Cough")
  headache = st.checkbox("Headache")
with c2:
  chect_pain = st.checkbox("Chest Pain")
  stomach_pain = st.checkbox("Stomach Pain")
  shortness_breath = st.checkbox("Shortness  of Breath")
with c3:
  nausea_vomiting = st.checkbox("Nausea/Vomiting")
  dizziness = st.checkbox("Dizziness")
  skin_rash = st.checkbox("Skin rash")
#form submission
if submitted:
  patient = pd.DataFrame([{
    'age' : age,
    'gender' : gender_map.get(gender,0),
    'fever' : int(fever),
    'cough' : int(cough),
    'headache' : int(headache),
    'chest_pain' : int(chest_pain),
    'stomach_pain' : int(stomach_pain),
    'shortness_breath' : int(shortness_breath),
    'nausea_vomiting' : int(nausea_vomiting),
    'dizziness' : int(dizziness),
    'skin_rash' : int(skin_rash),
    'tempature_level' : temp_map.get(tempature_level, 1),
    'heart_rate_level' : hr_map.get(heart_rate_level, 1),
    'duration' : dur_map.get(duration, 1),
    'asthma' : int(asthma),
    'hypertension' : int(hypertension),
    'heart_disease' : int(heart_disease),
    'chief_complaint' : cc_map.get(chief_complaint, 9)
  }])

  #2Scale numerical values
  patient_scaled = patient.copy()
  patient_scaled[cols_to_scale] = scaler.transform(patient[cols_to_scale])

  #Make Prediction
  pred = model.predict(patient_scaled[features])[0]
  proba= model.predicct(patient_scaled[features])[0]
  dept_name = dept_map_inv[pred]
  confidence = proba[pred] * 100
  
                  
