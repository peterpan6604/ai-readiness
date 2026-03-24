import streamlit as st
import plotly.graph_objects as go

# --- THEME & BRANDING ---
BRAND_RED = "#e94560"
BRAND_BLUE = "#0f3460"
BRAND_ORANGE = "#e67e22"
BRAND_GREEN = "#27ae60"
BG_DARK = "#0a0a0a"
CARD_BG = "#141414"

st.set_page_config(page_title="Odyssey AI Readiness", layout="centered")

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_DARK}; color: white; }}
    .stButton>button {{ background-color: {BRAND_RED}; color: white; border-radius: 8px; width: 100%; height: 3em; font-weight: bold; border: none; }}
    div[data-testid="stExpander"] {{ background-color: {CARD_BG}; border: 1px solid #2a2a2a; border-radius: 12px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ 90-Day AI Action Plan")
st.caption("Odyssey Learning Solutions | AI Readiness Assessment")

# --- STEP 1: CONTACT DETAILS ---
name = st.text_input("Full Name")
school = st.text_input("School / Trust")
email = st.text_input("Email Address")

st.divider()

# --- STEP 2: ASSESSMENT ---
st.subheader("📊 AI Readiness Assessment")
score_map = {"No": 0, "In development": 1, "Yes but needs updating": 2, "Yes and current": 3,
             "Not sure": 0, "Partially": 1, "Aware but not done": 1, "In progress": 2, "Complete": 3,
             "No idea": 0, "Some awareness": 1, "Mostly": 2, "Full visibility": 3,
             "Planning one": 1, "Yes, maintained": 3, "None": 0, "Self-directed only": 1,
             "Some formal CPD": 2, "Structured programme": 3, "Definitely not": 0, 
             "Probably not": 1, "Confidently yes": 3, "Informally": 1, "Partially documented": 2, "Fully documented": 3}

tab1, tab2, tab3, tab4 = st.tabs(["Policy", "Process", "People", "Proof"])

with tab1:
    q1 = st.radio("Formal AI use policy?", ["No", "In development", "Yes and current"], key="q1")
    q2 = st.radio("AI in safeguarding policy?", ["No", "Partially", "Yes"], key="q2")
    score_policy = (score_map.get(q1, 0) + score_map.get(q2, 0)) / 2

with tab2:
    q3 = st.radio("Awareness of staff AI tool use?", ["No idea", "Some awareness", "Full visibility"], key="q3")
    q4 = st.radio("DPIAs completed for AI tools?", ["No", "For some tools", "Yes, for all"], key="q4")
    score_process = (score_map.get(q3, 0) + score_map.get(q4, 0)) / 2

with tab3:
    q5 = st.radio("Named person leading AI?", ["No", "Informally", "Yes with dedicated time"], key="q5")
    q6 = st.radio("Staff AI training status?", ["None", "Some formal CPD", "Structured programme"], key="q6")
    score_people = (score_map.get(q5, 0) + score_map.get(q6, 0)) / 2

with tab4:
    q7 = st.radio("Log of approved tools?", ["No", "Partially", "Fully documented"], key="q7")
    q8 = st.radio("Evidence AI governance to governors?", ["Definitely not", "Partially", "Confidently yes"], key="q8")
    score_proof = (score_map.get(q7, 0) + score_map.get(q8, 0)) / 2

# --- STEP 3: RESULTS ---
if st.button("GENERATE MY 90-DAY PLAN"):
    if not name or not email:
        st.error("Please provide your name and email.")
    else:
        categories = ['Policy', 'Process', 'People', 'Proof']
        scores = [score_policy, score_process, score_people, score_proof]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line_color=BRAND_RED))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), paper_bgcolor=BG_DARK, font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.header("🎯 Your 90-Day Commitments")
        with st.expander("📝 Policy Actions", expanded=(score_policy < 2)):
            st.write("- Draft a standalone AI use policy. \n- Update Safeguarding policy.")
        with st.expander("⚙️ Process Actions", expanded=(score_process < 2)):
            st.write("- Audit current tool use. \n- Create an Approved Tool Register.")
        with st.expander("👥 People Actions", expanded=(score_people < 2)):
            st.write("- Appoint a named AI Lead. \n- Schedule a CPD session.")
        with st.expander("✅ Proof Actions", expanded=(score_proof < 2)):
            st.write("- Start a training log. \n- Prepare a Governor report.")
