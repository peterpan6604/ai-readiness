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

# Custom CSS
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

# --- ENHANCED EMAIL FUNCTION (Deliverability Boosted) ---
def send_email(to_email, user_name, school_name, scores_summary, plan_html_content):
    try:
        msg = MIMEMultipart("alternative")
        
        # Friendly Name helps bypass spam filters
        friendly_name = "Peter - Odyssey Learning Solutions"
        msg['From'] = f"{friendly_name} <{st.secrets['email_alias']}>"
        msg['To'] = to_email
        msg['Cc'] = st.secrets['admin_email']
        msg['Reply-To'] = st.secrets['email_alias']
        msg['Subject'] = f"🛡️ Your 90-Day AI Action Plan: {school_name}"

        # HTML Email Body for Professionalism
        html_body = f"""
        <html>
          <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
            <div style="text-align: center; border-bottom: 2px solid {BRAND_RED}; padding-bottom: 10px; margin-bottom: 20px;">
                <h1 style="color: {BRAND_RED}; margin: 0;">Odyssey Learning Solutions</h1>
                <p style="color: #666; font-style: italic;">AI Readiness Assessment Results</p>
            </div>
            
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>It was a pleasure seeing you at the session today. Based on your assessment for <strong>{school_name}</strong>, here is your current readiness profile and your strategic 90-day plan.</p>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; border-left: 5px solid {BRAND_RED};">
                <h3 style="margin-top: 0; color: {BRAND_RED};">Strategic Readiness Scores (0-3)</h3>
                <p style="font-size: 14px; margin: 0;">{scores_summary}</p>
            </div>

            <h3 style="color: {BRAND_RED}; margin-top: 25px;">Your 90-Day Action Plan</h3>
            <div style="color: #444;">
                {plan_html_content}
            </div>
            
            <p style="margin-top: 30px;"><strong>What's Next?</strong><br>
            I recommend sharing this plan with your Senior Leadership Team to ensure cross-departmental alignment. If you'd like a follow-up conversation regarding staff CPD or policy development, simply reply to this email.</p>
            
            <footer style="margin-top: 40px; padding-top: 10px; border-top: 1px solid #eee; font-size: 11px; color: #999; text-align: center;">
                Odyssey Learning Solutions | 90-Day AI Implementation Framework
            </footer>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        # SMTP Server Connection
        server = smtplib.SMTP(st.secrets["email_host"], st.secrets["email_port"])
        server.starttls()
        server.login(st.secrets["email_user"], st.secrets["email_password"])
        
        # Send to User and Admin
        recipients = [to_email, st.secrets['admin_email']]
        server.sendmail(st.secrets["email_user"], recipients, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email could not be sent: {e}")
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

consent = st.checkbox("I consent to receiving my action plan and follow-up AI resources.", value=True)

st.divider()

# --- STEP 2: ASSESSMENT ---
st.subheader("📊 AI Readiness Assessment")
st.write("Rate your progress (0 = Not Started, 3 = Embedded).")

score_map = {
    "No": 0, "In development": 1, "Yes but needs updating": 2, "Yes and current": 3,
    "Not sure": 0, "Partially": 1, "Aware but not done": 1, "In progress": 2, "Complete": 3,
    "No idea": 0, "Some awareness": 1, "Mostly": 2, "Full visibility": 3,
    "Planning one": 1, "Yes, maintained": 3, "None": 0, "Self-directed only": 1,
    "Some formal CPD": 2, "Structured programme": 3, "Definitely not": 0, 
    "Probably not": 1, "Confidently yes": 3, "Informally": 1, "Partially documented": 2, 
    "Fully documented": 3, "A few staff": 1, "Formal group": 3, "Planned": 1, "Active": 3,
    "Ad-hoc": 1, "Systematic": 3, "Some": 2, "Informal": 1, "Formalized": 3, "Always": 3, 
    "Sometimes": 1, "Regularly scheduled": 3, "Embedded": 3, "A few": 1
}

tab1, tab2, tab3, tab4 = st.tabs(["Policy", "Process", "People", "Proof"])

with tab1:
    st.markdown(f"### <span style='color:{BRAND_RED}'>Policy</span>", unsafe_allow_html=True)
    p1 = st.radio("Formal AI use policy established?", ["No", "In development", "Yes but needs updating", "Yes and current"], key="pol1")
    p2 = st.radio("AI explicitly referenced in safeguarding policy?", ["No", "Not sure", "Partially", "Yes"], key="pol2")
    p3 = st.radio("Assessment/Malpractice policy updated?", ["No", "Aware but not done", "In progress", "Complete"], key="pol3")
    p4 = st.radio("Parental AI consent process established?", ["No", "Planning one", "Complete"], key="pol4")
    p5 = st.radio("Board/Governor level AI strategy defined?", ["No", "Informal", "Formalized"], key="pol5")
    score_policy = (score_map.get(p1,0)+score_map.get(p2,0)+score_map.get(p3,0)+score_map.get(p4,0)+score_map.get(p5,0))/5

with tab2:
    st.markdown(f"### <span style='color:{BRAND_BLUE}'>Process</span>", unsafe_allow_html=True)
    r1 = st.radio("Visibility of staff AI tool usage?", ["No idea", "Some awareness", "Mostly", "Full visibility"], key="pro1")
    r2 = st.radio("Register of approved AI tools created?", ["No", "Planning one", "Partial", "Yes, maintained"], key="pro2")
    r3 = st.radio("DPIAs completed for current AI tools?", ["No", "Not sure", "For some tools", "Yes, for all"], key="pro3")
    r4 = st.radio("Feedback loops for staff using AI?", ["No", "Informal", "Regularly scheduled"], key="pro4")
    r5 = st.radio("Procurement process includes AI-specific vetting?", ["No", "Sometimes", "Always"], key="pro5")
    score_process = (score_map.get(r1,0)+score_map.get(r2,0)+score_map.get(r3,0)+score_map.get(r4,0)+score_map.get(r5,0))/5

with tab3:
    st.markdown(f"### <span style='color:{BRAND_ORANGE}'>People</span>", unsafe_allow_html=True)
    l1 = st.radio("Named person leading on AI strategy?", ["No", "Informally", "Yes but unsupported", "Yes with dedicated time"], key="peo1")
    l2 = st.radio("Staff received formal AI training?", ["None", "Self-directed only", "Some formal CPD", "Structured programme"], key="peo2")
    l3 = st.radio("AI Working Group or Champions established?", ["No", "A few staff", "Informal group", "Formal working group"], key="peo3")
    l4 = st.radio("Parental engagement/comms regarding AI?", ["None", "Planned", "Active"], key="peo4")
    l5 = st.radio("Student AI Literacy lessons integrated?", ["No", "Ad-hoc", "Systematic"], key="peo5")
    score_people = (score_map.get(l1,0)+score_map.get(l2,0)+score_map.get(l3,0)+score_map.get(l4,0)+score_map.get(l5,0))/5

with tab4:
    st.markdown(f"### <span style='color:{BRAND_GREEN}'>Proof</span>", unsafe_allow_html=True)
    v1 = st.radio("Systematic log of AI training completion?", ["No", "Informally", "Partially", "Systematically"], key="pru1")
    v2 = st.radio("Documentation of tool approval decisions?", ["No", "Informally", "Partially documented", "Fully documented"], key="pru2")
    v3 = st.radio("Ability to evidence AI governance?", ["Definitely not", "Probably not", "Partially", "Confidently yes"], key="pru3")
    v4 = st.radio("Biannual AI use surveys (Staff & Students)?", ["No", "Planned", "Active"], key="pru4")
    v5 = st.radio("Case studies of AI impact documented?", ["No", "A few", "Embedded"], key="pru5")
    score_proof = (score_map.get(v1,0)+score_map.get(v2,0)+score_map.get(v3,0)+score_map.get(v4,0)+score_map.get(v5,0))/5

# --- GENERATE RESULTS ---
if st.button("GENERATE MY 90-DAY PLAN"):
    if not name or not email or not consent:
        st.error("Please provide your name, email, and consent to proceed.")
    else:
        # Chart
        categories = ['Policy', 'Process', 'People', 'Proof']
        scores = [score_policy, score_process, score_people, score_proof]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line_color=BRAND_RED, fillcolor='rgba(233, 69, 96, 0.2)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), paper_bgcolor=BG_DARK, font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Build Plan content
        st.header("🎯 Your 90-Day Commitments")
        plan_html = ""
        
        pillars = [
            ("Policy", score_policy, BRAND_RED, "Draft standalone AI Use Policy; Update Safeguarding & Malpractice policies; Define parental consent workflows."),
            ("Process", score_process, BRAND_BLUE, "Conduct staff AI tool audit; Complete DPIAs for core tools; Maintain an Approved Tool Register."),
            ("People", score_people, BRAND_ORANGE, "Appoint a named AI Lead; Establish AI Working Group/Champions; Launch structured Staff CPD."),
            ("Proof", score_proof, BRAND_GREEN, "Log AI training records systematically; Document tool approval decisions; Prepare Governance evidence report.")
        ]
        
        for p_name, p_score, p_color, p_txt in pillars:
            with st.expander(f"{p_name} Actions", expanded=(p_score < 2)):
                st.write(p_txt)
                plan_html += f"<p><strong>{p_name} Pillar:</strong><br>{p_txt}</p>"

        # Format Scores for Email
        score_sum = f"Policy: {round(score_policy,1)}, Process: {round(score_process,1)}, People: {round(score_people,1)}, Proof: {round(score_proof,1)}"
        
        if send_email(email, name, school, score_sum, plan_html):
            st.success(f"Excellent, {name}. Your plan has been sent to {email}!")
            st.balloons()
