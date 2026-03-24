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

# Custom CSS for Mobile Optimization
st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_DARK}; color: white; }}
    .stButton>button {{ background-color: {BRAND_RED}; color: white; border-radius: 8px; width: 100%; height: 3.5em; font-weight: bold; border: none; }}
    div[data-testid="stExpander"] {{ background-color: {CARD_BG}; border: 1px solid #2a2a2a; border-radius: 12px; margin-bottom: 10px; }}
    .stRadio>label {{ color: #bbb !important; font-size: 14px; padding-bottom: 10px; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: {CARD_BG}; border-radius: 5px; padding: 10px; color: white; font-size: 12px; }}
    li {{ margin-bottom: 8px; font-size: 14px; color: #ddd; list-style-type: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- ENHANCED EMAIL FUNCTION ---
def send_email(to_email, user_name, school_name, scores_summary, plan_html_content):
    try:
        msg = MIMEMultipart("alternative")
        
        # Professional Friendly Name and Alias
        friendly_name = "Peter | Odyssey Learning Solutions"
        msg['From'] = f"{friendly_name} <{st.secrets['email_alias']}>"
        msg['To'] = to_email
        msg['Cc'] = st.secrets['admin_email']
        msg['Reply-To'] = st.secrets['email_alias']
        msg['Subject'] = f"🛡️ Your AI Action Plan: {school_name}"

        # HTML Email Body
        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: auto; border: 1px solid #eee; padding: 25px; border-radius: 10px;">
            <div style="text-align: center; border-bottom: 3px solid {BRAND_RED}; padding-bottom: 15px; margin-bottom: 25px;">
                <h1 style="color: {BRAND_RED}; margin: 0; font-size: 24px;">ODYSSEY LEARNING SOLUTIONS</h1>
                <p style="color: #666; font-style: italic; margin: 5px 0 0 0;">AI Strategy & Readiness Assessment</p>
            </div>
            
            <p>Hello <strong>{user_name}</strong>,</p>
            <p>It was a pleasure seeing you at the session today. Based on your assessment for <strong>{school_name}</strong>, here is your readiness profile and your targeted 90-day plan.</p>
            
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; border-left: 5px solid {BRAND_RED}; margin: 20px 0;">
                <h3 style="margin-top: 0; color: {BRAND_RED}; font-size: 18px;">Readiness Scores (0-3)</h3>
                <p style="font-size: 14px; margin: 0; font-family: monospace;">{scores_summary}</p>
            </div>

            <h3 style="color: {BRAND_RED}; border-bottom: 1px solid #eee; padding-bottom: 5px;">Your 90-Day Action Plan</h3>
            <div style="color: #444;">
                {plan_html_content}
            </div>
            
            <p style="margin-top: 30px; padding: 15px; background-color: #f0f7ff; border-radius: 8px; font-size: 15px; border: 1px solid #d0e3ff;">
                <strong>What's Next?</strong><br>
                I recommend using this as a starting point when thinking about next steps in your AI readiness journey. If you'd like to discuss this in further detail, please simply reply to this email.
            </p>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #eee; text-align: left;">
                <p style="margin: 0; font-weight: bold; color: {BRAND_RED};">Peter</p>
                <p style="margin: 0; font-size: 14px; color: #555;">Founder | Odyssey Learning Solutions</p>
                <p style="margin: 5px 0 0 0; font-size: 11px; color: #999;"><em>Helping school leaders navigate the AI frontier with confidence.</em></p>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(st.secrets["email_host"], st.secrets["email_port"])
        server.starttls()
        # Authenticates with PRIMARY login, but sends as ALIAS
        server.login(st.secrets["email_user"], st.secrets["email_password"])
        
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

# PILLAR QUESTIONS
pillars_data = {
    "Policy": [
        ("Formal AI use policy established?", ["No", "In development", "Yes but needs updating", "Yes and current"]),
        ("AI explicitly referenced in safeguarding policy?", ["No", "Not sure", "Partially", "Yes"]),
        ("Assessment/Malpractice policy updated?", ["No", "Aware but not done", "In progress", "Complete"]),
        ("Parental AI consent process established?", ["No", "Planning one", "Complete"]),
        ("Board/Governor level AI strategy defined?", ["No", "Informal", "Formalized"])
    ],
    "Process": [
        ("Visibility of staff AI tool usage?", ["No idea", "Some awareness", "Mostly", "Full visibility"]),
        ("Register of approved AI tools created?", ["No", "Planning one", "Partial", "Yes, maintained"]),
        ("DPIAs completed for current AI tools?", ["No", "Not sure", "For some tools", "Yes, for all"]),
        ("Feedback loops for staff using AI?", ["No", "Informal", "Regularly scheduled"]),
        ("Procurement process includes AI-specific vetting?", ["No", "Sometimes", "Always"])
    ],
    "People": [
        ("Named person leading on AI strategy?", ["No", "Informally", "Yes but unsupported", "Yes with dedicated time"]),
        ("Percentage of staff received formal AI training?", ["None", "Self-directed only", "Some formal CPD", "Structured programme"]),
        ("AI Working Group or Champions established?", ["No", "A few staff", "Informal group", "Formal working group"]),
        ("Parental engagement/comms regarding AI?", ["None", "Planned", "Active"]),
        ("Student AI Literacy lessons integrated?", ["No", "Ad-hoc", "Systematic"])
    ],
    "Proof": [
        ("Systematic log of AI training completion?", ["No", "Informally", "Partially", "Systematically"]),
        ("Documentation of tool approval decisions?", ["No", "Informally", "Partially documented", "Fully documented"]),
        ("Ability to evidence AI governance?", ["Definitely not", "Probably not", "Partially", "Confidently yes"]),
        ("Biannual AI use surveys (Staff & Students)?", ["No", "Planned", "Active"]),
        ("Case studies of AI impact documented?", ["No", "A few", "Embedded"])
    ]
}

tab1, tab2, tab3, tab4 = st.tabs(["Policy", "Process", "People", "Proof"])
tabs = [tab1, tab2, tab3, tab4]
scores = []

for i, (p_name, qs) in enumerate(pillars_data.items()):
    with tabs[i]:
        st.markdown(f"### {p_name}")
        p_scores = []
        for j, (q_text, opts) in enumerate(qs):
            ans = st.radio(q_text, opts, key=f"{p_name}_{j}")
            p_scores.append(score_map.get(ans, 0))
        scores.append(sum(p_scores) / 5)

score_policy, score_process, score_people, score_proof = scores

# --- GENERATE RESULTS ---
if st.button("GENERATE MY 90-DAY PLAN"):
    if not name or not email or not consent:
        st.error("Please provide your name, email, and consent to proceed.")
    else:
        # Chart
        categories = ['Policy', 'Process', 'People', 'Proof']
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=scores + [scores[0]], theta=categories + [categories[0]], fill='toself', line_color=BRAND_RED, fillcolor='rgba(233, 69, 96, 0.2)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3])), paper_bgcolor=BG_DARK, font_color="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Build Plan content
        st.header("🎯 Your 90-Day Commitments")
        plan_html = ""
        
        actions = {
            "Policy": ["Draft standalone AI Use Policy", "Update Safeguarding & Malpractice policies", "Define parental consent workflows"],
            "Process": ["Conduct staff AI tool audit", "Complete DPIAs for core tools", "Maintain an Approved Tool Register"],
            "People": ["Appoint a named AI Lead", "Establish AI Working Group/Champions", "Launch structured Staff CPD"],
            "Proof": ["Log AI training records systematically", "Document tool approval decisions", "Prepare Governance evidence report"]
        }
        
        colors = [BRAND_RED, BRAND_BLUE, BRAND_ORANGE, BRAND_GREEN]
        for idx, p_name in enumerate(categories):
            p_score = scores[idx]
            p_actions = actions[p_name]
            
            with st.expander(f"{p_name} Pillar Actions", expanded=(p_score < 2)):
                for a in p_actions:
                    st.write(f"✅ {a}")
                
                # HTML for Email
                plan_html += f"<h4 style='color: {colors[idx]}; margin-bottom: 5px;'>{p_name} Actions:</h4><ul style='margin-top: 0; padding-left: 20px;'>"
                for a in p_actions:
                    plan_html += f"<li style='margin-bottom: 5px;'>{a}</li>"
                plan_html += "</ul>"

        # Format Scores summary string
        score_sum = f"Policy: {round(score_policy,1)} | Process: {round(score_process,1)} | People: {round(score_people,1)} | Proof: {round(score_proof,1)}"
        
        if send_email(email, name, school, score_sum, plan_html):
            st.success(f"Success! Your plan has been sent to {email}!")
            st.balloons()
