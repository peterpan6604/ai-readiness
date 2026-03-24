import streamlit as st
import plotly.graph_objects as go
import smtplib
import io
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF

# --- ODYSSEY BRAND GUIDELINES ---
ODYSSEY_GOLD = "#F1B500"
DEEP_CHARCOAL = "#1A1A1A"
MATTE_BLACK = "#000000"
STARK_WHITE = "#FFFFFF"
SLATE_GREY = "#4A4A4A"

LOGO_URL = "https://raw.githubusercontent.com/peterpan6604/ai-readiness/main/logo.png"

st.set_page_config(page_title="ODYSSEY AI READINESS", layout="centered")

# --- CUSTOM CSS: INDUSTRIAL-TECH UI ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');
    .stApp {{ background-color: {DEEP_CHARCOAL}; color: {STARK_WHITE}; font-family: 'Arial', sans-serif; }}

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
        line-height: 1.6;
    }}

    .progress-bar-container {{
        background-color: {MATTE_BLACK};
        border: 1px solid {SLATE_GREY};
        padding: 10px 15px;
        margin-bottom: 20px;
    }}
    .progress-bar-fill {{
        background-color: {ODYSSEY_GOLD};
        height: 6px;
        transition: width 0.3s ease;
    }}
    .progress-text {{
        color: {ODYSSEY_GOLD};
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
    }}

    div[data-testid="stDownloadButton"] > button {{
        background-color: {ODYSSEY_GOLD};
        color: {MATTE_BLACK};
        border-radius: 0px;
        width: 100%;
        height: 3.5em;
        font-weight: 800;
        border: none;
        text-transform: uppercase;
    }}
    div[data-testid="stDownloadButton"] > button:hover {{
        background-color: {STARK_WHITE};
        color: {MATTE_BLACK};
    }}
</style>
""", unsafe_allow_html=True)


# --- PDF TEXT HELPER ---
def clean_text(text):
    """Replace Unicode characters that crash fpdf2's built-in fonts."""
    replacements = {
        '\u2014': '-',   # em dash
        '\u2013': '-',   # en dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote (curly apostrophe)
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2026': '...', # ellipsis
        '\u00a0': ' ',   # non-breaking space
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


# --- PDF GENERATION ---
def generate_pdf(user_name, school_name, scores, detailed_actions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    # Full page dark background
    pdf.set_fill_color(26, 26, 26)
    pdf.rect(0, 0, 210, 297, 'F')

    # Gold top bar
    pdf.set_fill_color(241, 181, 0)
    pdf.rect(0, 0, 210, 8, 'F')

    # Title
    pdf.set_y(20)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, 'ODYSSEY', ln=True)

    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'AI READINESS ASSESSMENT', ln=True)

    # Gold underline
    pdf.set_fill_color(241, 181, 0)
    pdf.rect(10, pdf.get_y() + 2, 60, 2, 'F')
    pdf.ln(10)

    # User details
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, clean_text(f'{user_name}  |  {school_name}'), ln=True)
    pdf.ln(5)

    # Scores box
    pdf.set_fill_color(0, 0, 0)
    pdf.set_draw_color(74, 74, 74)
    box_y = pdf.get_y()
    pdf.rect(10, box_y, 190, 35, 'DF')

    pdf.set_y(box_y + 5)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'YOUR SCORES (0-3)', ln=True)

    pdf.set_x(15)
    pdf.set_font('Courier', 'B', 12)
    pdf.set_text_color(255, 255, 255)
    pillars = ['POLICY', 'PROCESS', 'PEOPLE', 'PROOF']
    score_line = '    '.join([f'{p}: {round(scores[i], 1)}' for i, p in enumerate(pillars)])
    pdf.cell(0, 8, score_line, ln=True)

    avg_score = sum(scores) / 4
    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 6, f'Average: {round(avg_score, 1)}/3', ln=True)

    pdf.set_y(box_y + 40)

    # Intro text
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(220, 220, 220)
    pdf.multi_cell(190, 5, clean_text(
        'None of this is pass or fail. The scores give you a snapshot of where '
        'things stand, and the actions below focus on where the biggest gaps are. '
        'For any pillar scoring below 2, the detail is expanded.'
    ))
    pdf.ln(8)

    # Action plans per pillar
    for idx, p_name in enumerate(pillars):
        p_score = scores[idx]
        p_actions = detailed_actions[p_name]

        if pdf.get_y() > 230:
            pdf.add_page()
            pdf.set_fill_color(26, 26, 26)
            pdf.rect(0, 0, 210, 297, 'F')
            pdf.set_fill_color(241, 181, 0)
            pdf.rect(0, 0, 210, 4, 'F')
            pdf.set_y(15)

        # Pillar header
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(241, 181, 0)
        pdf.cell(0, 8, f'{p_name}  (Score: {round(p_score, 1)}/3)', ln=True)

        pdf.set_fill_color(241, 181, 0)
        pdf.rect(10, pdf.get_y(), 40, 1.5, 'F')
        pdf.ln(5)

        for title, desc in p_actions:
            if pdf.get_y() > 245:
                pdf.add_page()
                pdf.set_fill_color(26, 26, 26)
                pdf.rect(0, 0, 210, 297, 'F')
                pdf.set_fill_color(241, 181, 0)
                pdf.rect(0, 0, 210, 4, 'F')
                pdf.set_y(15)

            # Gold left bar
            bar_y = pdf.get_y()
            pdf.set_fill_color(241, 181, 0)
            pdf.rect(10, bar_y, 2, 3, 'F')

            # Action title
            pdf.set_x(16)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(241, 181, 0)
            pdf.cell(0, 5, clean_text(title.upper()), ln=True)

            # Action description
            pdf.set_x(16)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(200, 200, 200)
            pdf.multi_cell(180, 4.5, clean_text(desc))
            pdf.ln(5)

        pdf.ln(3)

    # CTA box
    if pdf.get_y() > 235:
        pdf.add_page()
        pdf.set_fill_color(26, 26, 26)
        pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_fill_color(241, 181, 0)
        pdf.rect(0, 0, 210, 4, 'F')
        pdf.set_y(15)

    cta_y = pdf.get_y()
    pdf.set_fill_color(34, 34, 34)
    pdf.set_draw_color(241, 181, 0)
    pdf.rect(10, cta_y, 190, 30, 'DF')

    pdf.set_y(cta_y + 5)
    pdf.set_x(15)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, 'WHAT NEXT?', ln=True)

    pdf.set_x(15)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(180, 4.5, clean_text(
        'This is meant to be a conversation starter, not a finished strategy. '
        'If you want to talk through these results or need support putting a plan '
        'together, get in touch: peter@odysseylearningsolutions.com'
    ))

    # Sign-off
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'PETER', ln=True)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(0, 4, 'FOUNDER  |  ODYSSEY LEARNING SOLUTIONS', ln=True)
    pdf.cell(0, 4, 'peter@odysseylearningsolutions.com', ln=True)

    # Bottom gold bar
    pdf.set_fill_color(241, 181, 0)
    pdf.rect(0, 289, 210, 8, 'F')

    return bytes(pdf.output())


# --- EMAIL FUNCTION ---
def send_email(to_email, user_name, school_name, scores_summary, plan_html_content):
    try:
        msg = MIMEMultipart("alternative")
        friendly_name = "Peter | Odyssey Learning Solutions"
        msg['From'] = f"{friendly_name} <{st.secrets['email_alias']}>"
        msg['To'] = to_email
        msg['Cc'] = st.secrets['admin_email']
        msg['Reply-To'] = st.secrets['email_alias']
        msg['Subject'] = f"Your AI Readiness Results — {school_name}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: {DEEP_CHARCOAL}; border: 2px solid {ODYSSEY_GOLD}; padding: 40px; color: {STARK_WHITE};">

                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{LOGO_URL}" width="80" style="margin-bottom: 10px;" alt="Odyssey Learning Solutions">
                </div>

                <div style="text-align: left; border-bottom: 6px solid {ODYSSEY_GOLD}; padding-bottom: 10px; margin-bottom: 30px;">
                    <h1 style="color: {STARK_WHITE}; margin: 0; font-size: 28px; letter-spacing: 2px;">ODYSSEY</h1>
                    <p style="color: {ODYSSEY_GOLD}; font-weight: bold; margin: 0; text-transform: uppercase; font-size: 11px;">AI Readiness Assessment</p>
                </div>

                <p style="font-size: 16px;">Hi {user_name},</p>

                <p style="font-size: 14px; line-height: 1.6;">Here are the results from your AI Readiness Assessment for <strong>{school_name}</strong>. The scores below give you a snapshot of where things stand across four areas — Policy, Process, People and Proof.</p>

                <p style="font-size: 14px; line-height: 1.6;">None of this is pass or fail. It's a starting point for working out where to focus first.</p>

                <div style="background-color: {MATTE_BLACK}; padding: 20px; border: 1px solid {SLATE_GREY}; margin: 25px 0;">
                    <h3 style="margin-top: 0; color: {ODYSSEY_GOLD}; font-size: 16px; text-transform: uppercase;">Your Scores (0-3)</h3>
                    <p style="font-size: 14px; margin: 0; font-family: 'Courier New', monospace; color: {STARK_WHITE};">{scores_summary}</p>
                </div>

                <h3 style="color: {ODYSSEY_GOLD}; text-transform: uppercase; border-bottom: 2px solid {SLATE_GREY}; padding-bottom: 5px; font-size: 18px;">90-Day Actions</h3>

                <p style="font-size: 14px; line-height: 1.6; margin-bottom: 20px;">The actions below are tailored to where your scores suggest the biggest gaps. For any pillar scoring below 2, I've expanded the detail — these are the areas worth prioritising in the next term.</p>

                <div style="color: {STARK_WHITE};">
                    {plan_html_content}
                </div>

                <div style="margin-top: 30px; padding: 20px; border-left: 4px solid {ODYSSEY_GOLD}; background-color: #222;">
                    <p style="margin: 0; font-size: 14px; line-height: 1.6;">
                        <strong>WHAT NEXT?</strong><br>
                        This is meant to be a conversation starter, not a finished strategy. If you'd like to talk through these results or want support putting a plan together, just reply to this email. Happy to help.
                    </p>
                </div>

                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid {SLATE_GREY}; text-align: left;">
                    <p style="margin: 0; font-weight: bold; color: {ODYSSEY_GOLD}; font-size: 18px;">PETER</p>
                    <p style="margin: 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Founder | Odyssey Learning Solutions</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: {SLATE_GREY};">peter@odysseylearningsolutions.com</p>
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
        st.error(f"Email couldn't be sent — but your PDF download is ready below. ({e})")
        return False


# --- APP UI ---
st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" width="120"></div>', unsafe_allow_html=True)
st.caption("AI READINESS TOOL")
st.title("WHERE DOES YOUR SCHOOL STAND?")

st.markdown(
    f'<p style="font-size: 14px; line-height: 1.6; color: {STARK_WHITE}; margin-bottom: 25px;">'
    'Answer 20 questions across four areas — Policy, Process, People and Proof — '
    'and get a personalised action plan you can download straight away.</p>',
    unsafe_allow_html=True
)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("YOUR NAME")
        school = st.text_input("SCHOOL / TRUST")
    with col2:
        email = st.text_input("EMAIL ADDRESS")
        role = st.text_input("YOUR ROLE")

    consent = st.checkbox("I'm happy to receive my results and occasional AI resources from Odyssey Learning Solutions", value=True)

st.markdown(f'<div style="width: 100%; height: 2px; background: {ODYSSEY_GOLD}; margin: 20px 0;"></div>', unsafe_allow_html=True)


# --- ASSESSMENT QUESTIONS & SCORING ---
pillars_data = {
    "POLICY": [
        (
            "Does your school have a standalone AI use policy?",
            [("No — not started", 0), ("We've discussed it but nothing written", 1), ("Draft exists but not approved", 2), ("Yes — approved and shared with staff", 3)]
        ),
        (
            "Has your safeguarding policy been updated to reference AI?",
            [("No", 0), ("It's on the list but not done yet", 1), ("Partially — some references added", 2), ("Yes — reviewed and updated", 3)]
        ),
        (
            "Has your malpractice or academic integrity policy been updated for AI?",
            [("No", 0), ("We're aware of JCQ updates but haven't acted", 1), ("In progress", 2), ("Yes — aligned with current JCQ guidance", 3)]
        ),
        (
            "Do you have a process for parental consent around student AI use?",
            [("No — not considered yet", 0), ("We've discussed it internally", 1), ("Draft process exists", 2), ("Yes — in place and communicated to parents", 3)]
        ),
        (
            "Is AI part of your governance strategy at board or governor level?",
            [("No — governors haven't discussed AI", 0), ("Mentioned informally but no formal agenda item", 1), ("Governors have been briefed", 2), ("Yes — AI is a standing item with clear oversight", 3)]
        ),
    ],
    "PROCESS": [
        (
            "Do you know which AI tools your staff are currently using?",
            [("No idea", 0), ("We have a rough sense but nothing documented", 1), ("Mostly — some tools are tracked", 2), ("Yes — we have full visibility", 3)]
        ),
        (
            "Do you maintain a register of approved AI tools?",
            [("No", 0), ("We've started listing some tools informally", 1), ("Partial register exists", 2), ("Yes — maintained and regularly reviewed", 3)]
        ),
        (
            "Have you completed Data Protection Impact Assessments for AI tools in use?",
            [("No — not started", 0), ("For one or two tools only", 1), ("For most tools", 2), ("Yes — completed for all tools in use", 3)]
        ),
        (
            "Is there a feedback loop for staff to report on how AI tools are working?",
            [("No", 0), ("Informal — staff chat about it in passing", 1), ("Some structured opportunities exist", 2), ("Yes — regular and scheduled", 3)]
        ),
        (
            "Does your procurement process include AI-specific vetting?",
            [("No — we haven't thought about this", 0), ("Sometimes — depends who's buying", 1), ("Mostly — there's an informal checklist", 2), ("Yes — all new tools are vetted for AI considerations", 3)]
        ),
    ],
    "PEOPLE": [
        (
            "Is there a named person in your school leading on AI?",
            [("No", 0), ("Informally — someone's taken an interest", 1), ("Yes — but it sits alongside their other responsibilities", 2), ("Yes — with dedicated time and clear accountability", 3)]
        ),
        (
            "What AI training have your staff received?",
            [("None", 0), ("Self-directed only — people finding their own way", 1), ("Some formal CPD has been delivered", 2), ("A structured ongoing programme is in place", 3)]
        ),
        (
            "Do you have an AI working group or champions network?",
            [("No", 0), ("A few interested staff but nothing formal", 1), ("An informal group meets occasionally", 2), ("Yes — a formal working group with regular meetings", 3)]
        ),
        (
            "Have you engaged parents on the school's approach to AI?",
            [("No — not yet", 0), ("We're planning to", 1), ("Some communication has gone out", 2), ("Yes — parents have been informed and consulted", 3)]
        ),
        (
            "Is AI literacy being taught to students?",
            [("No", 0), ("Ad hoc — some teachers cover it when relevant", 1), ("In certain subjects or year groups", 2), ("Yes — integrated across the curriculum", 3)]
        ),
    ],
    "PROOF": [
        (
            "Are you logging which staff have completed AI training?",
            [("No", 0), ("Partially — some records exist", 1), ("Mostly — we track it but not systematically", 2), ("Yes — all training is logged and tracked", 3)]
        ),
        (
            "Are AI tool approval decisions documented?",
            [("No", 0), ("Some decisions are noted informally", 1), ("Mostly documented", 2), ("Yes — a clear record of all decisions and rationale", 3)]
        ),
        (
            "Could you confidently present your AI governance approach to governors or inspectors?",
            [("Definitely not", 0), ("We'd struggle to pull it together", 1), ("We could put something together fairly quickly", 2), ("Yes — evidence is organised and ready", 3)]
        ),
        (
            "Do you run surveys on AI use among staff or students?",
            [("No", 0), ("We've discussed doing this", 1), ("We've run one", 2), ("Yes — regular surveys are scheduled", 3)]
        ),
        (
            "Do you have case studies or examples of AI impact in your school?",
            [("No", 0), ("Anecdotal — staff share stories informally", 1), ("A few documented examples", 2), ("Yes — case studies are collected and shared", 3)]
        ),
    ],
}


# --- RENDER ASSESSMENT ---
tabs = st.tabs(["POLICY", "PROCESS", "PEOPLE", "PROOF"])
scores = []
total_answered = 0

for i, (p_name, qs) in enumerate(pillars_data.items()):
    with tabs[i]:
        p_scores = []
        for j, (question, options) in enumerate(qs):
            option_labels = [opt[0] for opt in options]
            selected = st.radio(question, option_labels, key=f"{p_name}_{j}")
            score = next(opt[1] for opt in options if opt[0] == selected)
            p_scores.append(score)
            if selected != option_labels[0]:
                total_answered += 1
        scores.append(sum(p_scores) / 5)

# --- PROGRESS INDICATOR ---
progress_pct = min(int((total_answered / 20) * 100), 100)
st.markdown(f"""
<div class="progress-bar-container">
    <div style="background-color: {SLATE_GREY}; height: 6px; width: 100%;">
        <div class="progress-bar-fill" style="width: {progress_pct}%;"></div>
    </div>
    <div class="progress-text">{total_answered} of 20 questions answered</div>
</div>
""", unsafe_allow_html=True)


# --- ACTION PLAN CONTENT ---
detailed_actions = {
    "POLICY": [
        (
            "Write a standalone AI Use Policy",
            "Most schools don't have one yet. You don't need to start from scratch — "
            "the DfE guidance gives you a solid starting point. The important thing is "
            "getting something written down that staff can actually refer to. It doesn't "
            "have to be perfect first time. Get a draft to governors by the end of term "
            "and plan to review it termly, because this area moves fast."
        ),
        (
            "Update your safeguarding and academic integrity policies",
            "AI changes the risk picture for both of these. JCQ updated their guidance "
            "on AI and malpractice — make sure your policies reflect that. On safeguarding, "
            "the question is straightforward: what happens if a student uses an AI tool "
            "and something concerning comes up? If your policy doesn't cover it, it needs to."
        ),
        (
            "Get AI onto the governor agenda",
            "Governors need to understand what AI means for your school — not the technical "
            "detail, but the strategic picture. What tools are being used, what the risks are, "
            "and what the plan is. A 15-minute briefing at the next meeting is a good start. "
            "They can't provide oversight on something they haven't been told about."
        ),
    ],
    "PROCESS": [
        (
            "Find out what tools staff are already using",
            "There's a good chance staff are using AI tools you don't know about. "
            "A quick, anonymous survey will give you the picture. This isn't about catching "
            "people out — it's about understanding what's happening so you can support it "
            "properly. The BCS found 36% of teachers using AI hadn't told their leadership team."
        ),
        (
            "Complete DPIAs for your most-used AI tools",
            "Data Protection Impact Assessments sound more complicated than they are. "
            "Start with the tools staff use most. What data goes in? Where does it go? "
            "Who processes it? Your DPO can help with this. Getting these done means you "
            "can confidently say yes or no to tools rather than guessing."
        ),
        (
            "Create and maintain an approved tool register",
            "A simple, shared list of which AI tools are approved, which aren't, and why. "
            "Keep it somewhere staff can find it easily. Update it when new tools come "
            "along or when existing ones change their terms. This prevents the situation "
            "where everyone's using different tools with nobody knowing what's been vetted."
        ),
    ],
    "PEOPLE": [
        (
            "Appoint someone to lead on AI",
            "This doesn't need to be a new role or a huge time commitment. But somebody "
            "needs to own it. Without a named person, AI stays in the 'everyone's problem "
            "and nobody's responsibility' space. Pick someone with genuine interest and "
            "give them time to do it properly — even half a day a fortnight makes a difference."
        ),
        (
            "Set up an AI working group",
            "Get a small group together from different departments — teaching staff, admin, "
            "IT, safeguarding. Meet half-termly. Share what's working, flag what isn't, "
            "and feed into policy decisions. The schools doing this well have found it creates "
            "a culture where people feel comfortable experimenting rather than hiding what they're doing."
        ),
        (
            "Start structured AI CPD",
            "Move beyond the one-off twilight session. Staff need practical, hands-on training "
            "that's relevant to their specific role. Admin staff see admin examples. Teachers "
            "see teaching examples. Build confidence through doing, not just talking about it. "
            "The DfE and Chartered College now offer free training materials — use them."
        ),
    ],
    "PROOF": [
        (
            "Start logging AI training",
            "Keep a record of who's been trained, when, and on what. This is basic "
            "accountability — if Ofsted ask what you've done to support staff with AI, "
            "you need something to show them. A shared spreadsheet is fine. It doesn't "
            "need to be complicated."
        ),
        (
            "Document your tool approval decisions",
            "When you approve or reject an AI tool, write down why. This creates a "
            "paper trail that shows you're making considered decisions rather than "
            "reacting on the fly. It also helps when the next person asks about a "
            "similar tool — you've already done the thinking."
        ),
        (
            "Put together a governance evidence pack",
            "Pull your policy, training records, tool register, and DPIA outcomes into "
            "one place. This isn't about creating extra work — it's about being able "
            "to show governors and inspectors that you've got a grip on AI in your school. "
            "Ofsted aren't inspecting AI specifically yet, but they will look at how well "
            "you manage risk and support staff."
        ),
    ],
}


# --- RESULTS ---
if st.button("GENERATE MY ACTION PLAN"):
    if not name or not email:
        st.error("Please enter your name and email address to continue.")
    elif not consent:
        st.error("Please tick the consent box to receive your results.")
    else:
        # Radar Chart
        fig = go.Figure(data=[go.Scatterpolar(
            r=scores + [scores[0]],
            theta=['POLICY', 'PROCESS', 'PEOPLE', 'PROOF', 'POLICY'],
            fill='toself',
            line_color=ODYSSEY_GOLD,
            fillcolor='rgba(241, 181, 0, 0.2)'
        )])
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 3], color=STARK_WHITE, gridcolor=SLATE_GREY),
                bgcolor=MATTE_BLACK
            ),
            paper_bgcolor=DEEP_CHARCOAL,
            font_color=STARK_WHITE,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # Score context
        avg_score = sum(scores) / 4
        if avg_score < 1:
            summary_note = "You're at the early stages — but that's exactly why this matters. Most schools are in a similar position."
        elif avg_score < 2:
            summary_note = "You've made a start in some areas. The actions below will help you build on that and close the gaps."
        else:
            summary_note = "You're further ahead than most. The focus now is on formalising what you've started and building the evidence base."

        st.markdown(
            f'<p style="font-size: 14px; line-height: 1.6; color: {STARK_WHITE}; '
            f'padding: 15px; background-color: {MATTE_BLACK}; border-left: 3px solid {ODYSSEY_GOLD};">'
            f'{summary_note}</p>',
            unsafe_allow_html=True
        )

        st.subheader("YOUR 90-DAY ACTIONS")

        plan_html = ""
        pillars = ['POLICY', 'PROCESS', 'PEOPLE', 'PROOF']

        for idx, p_name in enumerate(pillars):
            p_score = scores[idx]
            p_actions = detailed_actions[p_name]

            with st.expander(f"{p_name} — SCORE: {round(p_score, 1)}/3", expanded=(p_score < 2)):
                plan_html += f"<h4 style='color: {ODYSSEY_GOLD}; text-transform: uppercase; margin-bottom: 10px;'>{p_name} (Score: {round(p_score, 1)}/3)</h4>"

                for title, desc in p_actions:
                    st.markdown(
                        f"""<div class='action-item'>
                            <span class='action-title'>{title}</span>
                            <span class='action-desc'>{desc}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    plan_html += f"<p style='margin-bottom: 15px;'><strong>{title}</strong><br><span style='font-size: 13px; color: #ccc; line-height: 1.6;'>{desc}</span></p>"

        score_sum = f"POLICY: {round(scores[0], 1)} | PROCESS: {round(scores[1], 1)} | PEOPLE: {round(scores[2], 1)} | PROOF: {round(scores[3], 1)}"

        # --- PDF DOWNLOAD (always works, no firewall issues) ---
        st.markdown(f'<div style="width: 100%; height: 2px; background: {ODYSSEY_GOLD}; margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        pdf_bytes = generate_pdf(
            name,
            school if school else "your school",
            scores,
            detailed_actions
        )

        school_slug = (school or "school").lower().replace(" ", "-").replace("/", "-")
        filename = f"ai-readiness-{school_slug}.pdf"

        st.download_button(
            label="DOWNLOAD YOUR ACTION PLAN (PDF)",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )

        # --- EMAIL (attempt — graceful failure if firewall blocks it) ---
        st.markdown(
            f'<p style="font-size: 12px; color: {SLATE_GREY}; margin-top: 10px;">'
            'We\'ll also try to send a copy to your email. If it doesn\'t arrive '
            '(school firewalls can be strict), the PDF above has everything you need.</p>',
            unsafe_allow_html=True
        )

        email_sent = send_email(email, name, school if school else "your school", score_sum, plan_html)

        if email_sent:
            st.success("Done. Your PDF is ready and a copy has been sent to your inbox.")
        else:
            st.info("Your PDF is ready above. The email didn't go through — likely a firewall issue — but you've got everything you need.")

        st.balloons()
