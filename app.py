import streamlit as st
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- THEME & BRANDING ---
BRAND_RED = "#e94560"
BRAND_BLUE = "#0f3460"
BRAND_ORANGE = "#e67e22"
BRAND_GREEN = "#27ae60"
BG_DARK = "#0a0a0a"
CARD_BG = "#141414"

st.set_page_config(page_title="Odyssey AI Readiness", layout="centered")

# Custom CSS for Professional Look
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_DARK}; color: white; }}
    .stButton>button {{ background-color: {BRAND_RED}; color: white; border-radius: 8px; width: 100%; height: 3.5em; font-weight: bold; border: none; }}
    div[data-testid="stExpander"] {{ background-color: {CARD_BG}; border: 1px solid #2a2a2a; border-radius: 12px; margin-bottom: 10px; }}
    .stRadio>label {{ color: #bbb !important; font-size: 14px; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: {CARD_BG}; border-radius: 5px; padding: 10px; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# --- EMAIL FUNCTION ---
def send_email(to_email, user_name, school_name, scores, plan_text):
    try:
        msg = MIMEMultipart()
        # Uses the ALIAS for the display name
        msg['From'] = st.secrets["email_alias"] 
        msg['To'] = f"{to_email}, {st.secrets['admin_email']}"
        msg['Subject'] = f"🛡️ Odyssey AI Action Plan: {school_name}"

        body = f"Hello {user_name},\n\nThank you for completing the Odyssey AI Readiness Assessment for {school_name}.\n\n"
        body += f"YOUR READINESS SCORES (0-3 Scale):\n{scores}\n\n"
        body += f"YOUR 90-DAY ACTION PLAN:\n{plan_text}\n\n"
        body += "Next Steps: Review these actions with your Senior Leadership Team and begin your 90-day implementation cycle.\n\n"
        body += "Best regards,\nOdyssey Learning Solutions"
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(st.secrets["email_host"], st.secrets["email_port"])
        server.starttls()
        # Authenticates with PRIMARY login
        server.login(st.secrets["email_user"], st.secrets["email_password"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

# --- HEADER ---
st.title("🛡️ 90-Day AI Action Plan")
st.caption("Odyssey Learning Solutions | AI Readiness Assessment")

# --- STEP 1: CONTACT DETAILS ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Sarah Johnson")
        school = st.text_input("School / Trust", placeholder="e.g. Wakefield Academy")
    with col2:
        email = st.text_input("Email Address", placeholder="s.johnson@school.org")
        role = st.text_input("Role", placeholder="e.g. Headteacher")

consent = st.checkbox("I consent to receiving my action plan and follow-up AI resources via email.", value=True)

st.divider()

# --- STEP 2: ASSESSMENT (20 Questions) ---
st.subheader("📊 AI Readiness Assessment")
st.write("Rate your progress across the four pillars (0 = Not Started, 3 = Embedded).")

score_map = {
    "No": 0, "In development": 1, "Yes but needs updating": 2, "Yes and current": 3,
    "Not sure": 0, "Partially": 1, "Aware but not done": 1, "In progress": 2, "Complete": 3,
    "No idea": 0, "Some awareness": 1, "Mostly": 2, "Full visibility": 3,
    "Planning one": 1, "Yes, maintained": 3, "None": 0, "Self-directed only": 1,
    "Some formal CPD": 2, "Structured programme": 3, "Definitely not": 0, 
    "Probably not": 1, "Confidently yes": 3, "Informally": 1, "Partially documented": 2, 
    "Fully documented": 3, "A few staff": 1, "Formal group": 3, "Planned": 1, "Active": 3,
    "Ad-hoc": 1, "Systematic": 3, "Some": 2, "Informal": 1, "Formalized": 3, "Always": 3, "Sometimes": 1, "Regularly scheduled": 3, "Embedded": 3, "A few": 1
}

tab1, tab2, tab3, tab4 = st.tabs(["Policy", "Process", "People", "Proof"])

with tab1:
    st.markdown(f"### <span style='color:{BRAND_RED}'>Policy</span>", unsafe_allow_html=True)
    p1 = st.radio("Formal AI use policy established?", ["No", "In development", "Yes but needs updating", "Yes and current"])
    p2 = st.radio("AI explicitly referenced in safeguarding policy?", ["No", "Not sure", "Partially", "Yes"])
    p3 = st.radio("Assessment/Malpractice policy updated for GenAI?", ["No", "Aware but not done", "In progress", "Complete"])
    p4 = st.radio("Parental AI consent process established?", ["No", "Planning one", "Complete"])
    p5 = st.radio("Board/Governor level AI strategy defined?", ["No", "Informal", "Formalized"])
    score_policy = (score_map.get(p1,0)+score_map.get(p2,0)+score_map.get(p3,0)+score_map.get(p4,0)+score_map.get(p5,0))/5

with tab2:
    st.markdown(f"### <span style='color:{BRAND_BLUE}'>Process</span>", unsafe_allow_html=True)
    r1 = st.radio("Visibility of staff AI tool usage?", ["No idea", "Some awareness", "Mostly", "Full visibility"])
    r2 = st.radio("Register of approved AI tools created?", ["No", "Planning one", "Partial", "Yes, maintained"])
    r3 = st.radio("DPIAs completed for current AI tools?", ["No", "Not sure", "For some tools", "Yes, for all"])
    r4 = st.radio("Feedback loops for staff experimenting with AI?", ["No", "Informal", "Regularly scheduled"])
    r5 = st.radio("Procurement process includes AI-specific vetting?", ["No", "Sometimes", "Always"])
    score_process = (score_map.get(r1,0)+score_map.get(r2,0)+score_map.get(r3,0)+score_map.get(r4,0)+score_map.get(r5,0))/5

with tab3:
    st.markdown(f"### <span style='color:{BRAND_ORANGE}'>People</span>", unsafe_allow_html=True)
    l1 = st.radio("Named person leading on AI strategy?", ["No", "Informally", "Yes but unsupported", "Yes with dedicated time"])
    l2 = st.radio("Percentage of staff received formal AI training?", ["None", "Self-directed only", "Some formal CPD", "Structured programme"])
    l3 = st.radio("AI Working Group or Champions established?", ["No", "A few staff", "Informal group", "Formal working group"])
    l4 = st.radio("Parental engagement/comms regarding AI?", ["None", "Planned", "Active"])
    l5 = st.radio("Student AI Literacy lessons integrated?", ["No", "Ad-hoc", "Systematic"])
    score_people = (score_map.get(l1,0)+score_map.get(l2,0)+score_map.get(l3,0)+score_map.get(l4,0)+score_map.get(l5,0))/5

with tab4:
    st.markdown(f"### <span style='color:{BRAND_GREEN}'>Proof</span>", unsafe_allow_html=True)
    v1 = st.radio("Systematic log of AI training completion?", ["No", "Informally", "Partially", "Systematically"])
    v2 = st.radio("Documentation of tool approval/rejection decisions?", ["No", "Informally", "Partially documented", "Fully documented"])
    v3 = st.radio("Ability to evidence AI governance to Governors/Inspectors?", ["Definitely not", "Probably not", "Partially", "Confidently yes"])
    v4 = st.radio("Biannual AI use surveys (Staff & Students)?", ["No", "Planned", "Active"])
    v5 = st.radio("Case studies of AI impact documented?", ["No", "A few", "Embedded"])
    score_proof = (score_map.get(v1,0)+score_map.get(v2,0)+score_map.get(v3,0)+score_map.get(v4,0)+score_map.get(v5,0))/5

# --- GENERATE RESULTS ---
if st.button("GENERATE MY 90-DAY PLAN"):
    if not name or not email or not consent:
        st.error("Please provide your name, email, and consent to proceed.")
    else:
        # Create Spider Chart
        categories = ['Policy', 'Process', 'People', 'Proof']
        scores = [score_policy, score_process, score_people, score_proof]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line_color=BRAND_RED,
            fillcolor='rgba(233, 69, 96, 0.2)'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
            paper_bgcolor=BG_DARK,
            plot_bgcolor=BG_DARK,
            font_color="white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Build Plan Text for UI and Email
        plan_text = ""
        st.header("🎯 Your 90-Day Commitments")
        
        with st.expander("📝 Policy Actions", expanded=(score_policy < 2)):
            txt = "- Draft standalone AI Use Policy\n- Update Safeguarding & Malpractice policies\n- Define parental consent workflows"
            st.write(txt); plan_text += f"\nPOLICY PILLAR:\n{txt}\n"
        
        with st.expander("⚙️ Process Actions", expanded=(score_process < 2)):
            txt = "- Conduct staff AI tool audit\n- Complete DPIAs for core tools\n- Maintain an Approved Tool Register"
            st.write(txt); plan_text += f"\nPROCESS PILLAR:\n{txt}\n"
            
        with st.expander("👥 People Actions", expanded=(score_people < 2)):
            txt = "- Appoint a named AI Lead\n- Establish AI Working Group/Champions\n- Launch structured Staff CPD"
            st.write(txt); plan_text += f"\nPEOPLE PILLAR:\n{txt}\n"
            
        with st.expander("✅ Proof Actions", expanded=(score_proof < 2)):
            txt = "- Log AI training records systematically\n- Document tool approval decisions\n- Prepare Governance evidence report"
            st.write(txt); plan_text += f"\nPROOF PILLAR:\n{txt}\n"

        # Execute Email
        score_summary = f"Policy: {round(score_policy,1)}, Process: {round(score_process,1)}, People: {round(score_people,1)}, Proof: {round(score_proof,1)}"
        if send_email(email, name, school, score_summary, plan_text):
            st.success(f"Excellent, {name}. Your 90-day plan has been sent to {email}!")
            st.balloons()
