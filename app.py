import streamlit as st
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- ODYSSEY BRAND GUIDELINES ---
ODYSSEY_GOLD = "#F1B500"
DEEP_CHARCOAL = "#1A1A1A"
MATTE_BLACK = "#000000"
STARK_WHITE = "#FFFFFF"
SLATE_GREY = "#4A4A4A"

# PASTE YOUR LOGO URL HERE (Link to your GitHub raw image)
LOGO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-readiness/main/logo.png"

st.set_page_config(page_title="ODYSSEY AI READINESS", layout="centered")

# --- CUSTOM CSS: INDUSTRIAL-TECH UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');
    
    .stApp {{ background-color: {DEEP_CHARCOAL}; color: {STARK_WHITE}; font-family: 'Arial', sans-serif; }}
    
    /* Logo Styling */
    .logo-container {{
        text-align: center;
        padding-top: 20px;
        margin-bottom: -10px;
    }}

    h1, h2, h3 {{
        font-family: 'Montserrat', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: {STARK_WHITE};
        border-bottom: 4px solid {ODYSSEY_GOLD};
        display: inline-block;
        margin-bottom: 20px !important;
        padding-bottom: 5px;
    }}
    
    .stCaption {{ color: {ODYSSEY_GOLD}; text-transform: uppercase; font-weight: 800; letter-spacing: 1.5px; }}

    .stButton>button {{
        background-color: {ODYSSEY_GOLD};
        color: {MATTE_BLACK};
        border-radius: 0px; 
        width: 100%;
        height: 3.5em;
        font-weight: 800;
        border: none;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{ background-color: {STARK_WHITE}; color: {MATTE_BLACK}; }}

    div[data-testid="stExpander"] {{
        background-color: {MATTE_BLACK};
        border: 1px solid {SLATE_GREY};
        border-radius: 0px; 
        margin-bottom: 10px;
    }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 5px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: {MATTE_BLACK};
        border-radius: 0px;
        padding: 12px 18px;
        color: {STARK_WHITE};
        font-weight: bold;
        border: 1px solid {SLATE_GREY};
        font-size: 12px;
    }}
    .stTabs [aria-selected="true"] {{ background-color: {ODYSSEY_GOLD} !important; color: {MATTE_BLACK} !important; }}

    .stRadio>label {{
        color: {STARK_WHITE} !important;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 11px;
    }}
    
    .action-item {{
        border-left: 3px solid {ODYSSEY_GOLD};
        padding-left: 15px;
        margin-bottom: 20px;
    }}
    .action-title {{
        color: {ODYSSEY_GOLD};
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
        display: block;
    }}
    .action-desc {{
        color: {STARK_WHITE};
        font-size: 13px;
        display: block;
        margin-top: 5px;
        line-height: 1.4;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- EMAIL FUNCTION ---
def send_email(to_email, user_name, school_name, scores_summary, plan_html_content):
    try:
        msg = MIMEMultipart("alternative")
        friendly_name = "ODYSSEY LEARNING SOLUTIONS"
        msg['From'] = f"{friendly_name} <{st.secrets['email_alias']}>"
        msg['To'] = to_email
        msg['Cc'] = st.secrets['admin_email']
        msg['Reply-To'] = st.secrets['email_alias']
        msg['Subject'] = f"🛡️ STRATEGIC AI ACTION PLAN: {school_name}"

        html_body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: {DEEP_CHARCOAL}; border: 2px solid {ODYSSEY_GOLD}; padding: 40px; color: {STARK_WHITE};">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{LOGO_URL}" width="80" style="margin-bottom: 10px;">
                </div>
                <div style="text-align: left; border-bottom: 6px solid {ODYSSEY_GOLD}; padding-bottom: 10px; margin-bottom: 30px;">
                    <h1 style="color: {STARK_WHITE}; margin: 0; font-size: 28px; letter-spacing: 2px;">ODYSSEY</h1>
                    <p style="color: {ODYSSEY_GOLD}; font-weight: bold; margin: 0; text-transform: uppercase; font-size: 11px;">AI Strategy & Readiness Assessment</p>
                </div>
                
                <p style="font-size: 16px;">Hello <strong>{user_name}</strong>,</p>
                <p style="font-size: 14px; line-height: 1.6;">Below is your high-impact AI Readiness Profile for <strong>{school_name}</strong>. Use these results to drive strategic conversation within your leadership team.</p>
                
                <div style="background-color: {MATTE_BLACK}; padding: 20px; border: 1px solid {SLATE_GREY}; margin: 25px 0;">
                    <h3 style="margin-top: 0; color: {ODYSSEY_GOLD}; font-size: 16px; text-transform: uppercase;">Strategic Scores (0-3)</h3>
                    <p style="font-size: 14px; margin: 0; font-family: 'Courier New', monospace; color: {STARK_WHITE};">{scores_summary}</p>
                </div>

                <h3 style="color: {ODYSSEY_GOLD}; text-transform: uppercase; border-bottom: 2px solid {SLATE_GREY}; padding-bottom: 5px; font-size: 18px;">Your 90-Day Commitments</h3>
                <div style="color: {STARK_WHITE};">
                    {plan_html_content}
                </div>
                
                <div style="margin-top: 30px; padding: 20px; border-left: 4px solid {ODYSSEY_GOLD}; background-color: #222;">
                    <p style="margin: 0; font-size: 14px; line-height: 1.6;">
                        <strong>WHAT'S NEXT?</strong><br>
                        I recommend using this as a starting point when thinking about next steps in your AI readiness journey. If you'd like to discuss this in further detail, please simply reply to this email.
                    </p>
                </div>
                
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid {SLATE_GREY}; text-align: left;">
                    <p style="margin: 0; font-weight: bold; color: {ODYSSEY_GOLD}; font-size: 18px;">PETER</p>
                    <p style="margin: 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Founder | Odyssey Learning Solutions</p>
                </div>
            </div>
          </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        server = smtplib.SMTP(st.secrets["email_host"], st.secrets["email_port"])
        server.starttls()
        server.login(st.secrets["email_user"], st.secrets["email_password"])
        recipients = [to_email, st.secrets['admin_email']]
        server.sendmail(st.secrets["email_user"], recipients, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"SYSTEM ERROR: {e}")
        return False

# --- APP UI ---
# Show Logo at the top
st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" width="120"></div>', unsafe_allow_html=True)
st.caption("AI STRATEGY ENGINE")
st.title("90-DAY ACTION PLAN")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("FULL NAME")
        school = st.text_input("SCHOOL / TRUST")
    with col2:
        email = st.text_input("EMAIL ADDRESS")
        role = st.text_input("ROLE")

consent = st.checkbox("CONSENT TO RECEIVE STRATEGIC AI RESOURCES", value=True)
st.markdown('<div style="width: 100%; height: 2px; background: #F1B500; margin: 20px 0;"></div>', unsafe_allow_html=True)

# --- ASSESSMENT LOGIC (Same as before) ---
score_map = {"No": 0, "In development": 1, "Yes but needs updating": 2, "Yes and current": 3, "Not sure": 0, "Partially": 1, "Aware but not done": 1, "In progress": 2, "Complete": 3, "No idea": 0, "Some awareness": 1, "Mostly": 2, "Full visibility": 3, "Planning one": 1, "Yes, maintained": 3, "None": 0, "Self-directed only": 1, "Some formal CPD": 2, "Structured programme": 3, "Definitely not": 0, "Probably not": 1, "Confidently yes": 3, "Informally": 1, "Partially documented": 2, "Fully documented": 3, "A few staff": 1, "Formal group": 3, "Planned": 1, "Active": 3, "Ad-hoc": 1, "Systematic": 3, "Some": 2, "Informal": 1, "Formalized": 3, "Always": 3, "Embedded": 3}

pillars_data = {
    "POLICY": [("Formal AI use policy established?", ["No", "In development", "Yes and current"]), ("AI referenced in safeguarding?", ["No", "Partially", "Yes"]), ("Malpractice policy updated?", ["No", "In progress", "Complete"]), ("Parental AI consent process?", ["No", "Planning one", "Complete"]), ("Governor level AI strategy?", ["No", "Informal", "Formalized"])],
    "PROCESS": [("Visibility of staff AI tool usage?", ["No idea", "Some awareness", "Full visibility"]), ("Register of approved AI tools?", ["No", "Partial", "Yes, maintained"]), ("DPIAs completed for current tools?", ["No", "For some tools", "Yes, for all"]), ("Feedback loops for staff using AI?", ["No", "Informal", "Regularly scheduled"]), ("Procurement includes AI vetting?", ["No", "Sometimes", "Always"])],
    "PEOPLE": [("Named person leading on AI?", ["No", "Informally", "Yes with dedicated time"]), ("Staff received formal AI training?", ["None", "Some formal CPD", "Structured programme"]), ("AI Working Group established?", ["No", "Informal group", "Formal working group"]), ("Parental engagement on AI?", ["None", "Planned", "Active"]), ("Student AI Literacy integrated?", ["No", "Ad-hoc", "Systematic"])],
    "PROOF": [("Log of AI training completion?", ["No", "Partially", "Systematically"]), ("Log of tool approval decisions?", ["No", "Partially documented", "Fully documented"]), ("Evidence AI governance?", ["Definitely not", "Partially", "Confidently yes"]), ("Biannual AI use surveys?", ["No", "Planned", "Active"]), ("Case studies of AI impact?", ["No", "A few", "Embedded"])]
}

tabs = st.tabs(["POLICY", "PROCESS", "PEOPLE", "PROOF"])
scores = []
for i, (p_name, qs) in enumerate(pillars_data.items()):
    with tabs[i]:
        p_scores = [score_map.get(st.radio(q, o, key=f"{p_name}_{j}"), 0) for j, (q, o) in enumerate(qs)]
        scores.append(sum(p_scores) / 5)

# --- RESULTS ---
if st.button("GENERATE STRATEGIC PLAN"):
    if not name or not email or not consent:
        st.error("REQUIRED FIELDS MISSING")
    else:
        fig = go.Figure(data=[go.Scatterpolar(r=scores + [scores[0]], theta=['POLICY', 'PROCESS', 'PEOPLE', 'PROOF', 'POLICY'], fill='toself', line_color=ODYSSEY_GOLD, fillcolor='rgba(241, 181, 0, 0.2)')])
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 3], color=STARK_WHITE, gridcolor=SLATE_GREY), bgcolor=MATTE_BLACK), paper_bgcolor=DEEP_CHARCOAL, font_color=STARK_WHITE, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("YOUR 90-DAY COMMITMENTS")
        plan_html = ""
        
        detailed_actions = {
            "POLICY": [
                ("Draft a standalone AI Use Policy", "Providing clear guidelines for staff and students ensures consistency and safety across the institution."),
                ("Update Safeguarding & Malpractice policies", "Aligning these core documents with current AI realities (like JCQ guidance) protects the integrity of assessments and student welfare."),
                ("Define parental consent workflows", "Engaging parents early regarding AI tool usage builds trust and ensures legal compliance for student data processing.")
            ],
            "PROCESS": [
                ("Conduct a comprehensive staff AI tool audit", "Mapping out which tools are already in use allows you to manage risks and identify internal 'AI pioneers'."),
                ("Complete DPIAs for core tools", "Data Protection Impact Assessments will support you and the school to confidently implement and utilise AI tools and platforms."),
                ("Maintain an Approved AI Tool Register", "A centralized, vetted list of tools prevents 'shadow AI' and ensures all platforms meet your school's security standards.")
            ],
            "PEOPLE": [
                ("Appoint a named AI Strategic Lead", "Having a single point of accountability ensures that AI integration remains a priority and doesn't get lost in general IT tasks."),
                ("Establish an AI Working Group", "Distributing leadership across departments creates a culture of peer-to-peer support and specialized experimentation."),
                ("Launch a structured Staff CPD programme", "Move beyond 'one-off' sessions to build long-term staff confidence and technical proficiency in prompt engineering and ethics.")
            ],
            "PROOF": [
                ("Log AI training records systematically", "Maintaining evidence of staff professional development is crucial for internal accountability and external inspections."),
                ("Document AI tool approval decisions", "Keeping a clear 'paper trail' of why tools were accepted or blocked demonstrates high-level governance and due diligence."),
                ("Prepare an AI Governance Evidence Report", "Presenting a structured summary of your AI strategy to Governors ensures they can fulfill their oversight role effectively.")
            ]
        }
        
        pillars = ['POLICY', 'PROCESS', 'PEOPLE', 'PROOF']
        for idx, p_name in enumerate(pillars):
            p_score = scores[idx]
            p_actions = detailed_actions[p_name]
            
            with st.expander(f"{p_name} ACTIONS", expanded=(p_score < 2)):
                plan_html += f"<h4 style='color: {ODYSSEY_GOLD}; text-transform: uppercase; margin-bottom: 10px;'>{p_name} STRATEGY:</h4>"
                for title, desc in p_actions:
                    st.markdown(f"""<div class='action-item'><span class='action-title'>{title}</span><span class='action-desc'>{desc}</span></div>""", unsafe_allow_html=True)
                    plan_html += f"<p style='margin-bottom: 15px;'><strong>{title}</strong><br><span style='font-size: 13px; color: #ccc;'>{desc}</span></p>"

        score_sum = f"POLICY: {round(scores[0],1)} | PROCESS: {round(scores[1],1)} | PEOPLE: {round(scores[2],1)} | PROOF: {round(scores[3],1)}"
        if send_email(email, name, school, score_sum, plan_html):
            st.success("STRATEGIC PLAN TRANSMITTED")
            st.balloons()
