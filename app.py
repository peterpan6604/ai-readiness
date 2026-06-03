import streamlit as st
import plotly.graph_objects as go
import smtplib
import io
import os
import tempfile
import urllib.request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
from content import QUESTIONS, actions_for_score, get_summary_note

# --- ODYSSEY BRAND GUIDELINES ---
ODYSSEY_GOLD = "#F1B500"
DEEP_CHARCOAL = "#1A1A1A"
MATTE_BLACK = "#000000"
STARK_WHITE = "#FFFFFF"
SLATE_GREY = "#4A4A4A"

LOGO_URL = "https://raw.githubusercontent.com/peterpan6604/ai-readiness/main/Logo.png"

ICON_URL = "https://raw.githubusercontent.com/peterpan6604/ai-readiness/main/Icon.png"

st.set_page_config(page_title="ODYSSEY AI READINESS", layout="centered", page_icon=ICON_URL)


@st.cache_data
def get_logo_path():
    """Download wordmark logo once and cache for PDF embedding."""
    try:
        logo_path = os.path.join(tempfile.gettempdir(), "odyssey_logo.png")
        if not os.path.exists(logo_path):
            urllib.request.urlretrieve(LOGO_URL, logo_path)
        return logo_path
    except Exception:
        return None


@st.cache_data
def get_icon_path():
    """Download AI head icon once and cache for PDF embedding."""
    try:
        icon_path = os.path.join(tempfile.gettempdir(), "odyssey_icon.png")
        if not os.path.exists(icon_path):
            urllib.request.urlretrieve(ICON_URL, icon_path)
        return icon_path
    except Exception:
        return None


# --- CUSTOM CSS: INDUSTRIAL-TECH UI ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&display=swap');
    .stApp {{ background-color: {DEEP_CHARCOAL}; color: {STARK_WHITE}; font-family: 'Arial', sans-serif; }}

    /* --- MOTION --- */
    @keyframes odyFadeUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes odyFadeIn {{
        from {{ opacity: 0; }}
        to   {{ opacity: 1; }}
    }}
    @keyframes odyGoldSweep {{
        from {{ width: 0; }}
        to   {{ width: 60px; }}
    }}
    /* Respect users who prefer no motion */
    @media (prefers-reduced-motion: reduce) {{
        *, *::before, *::after {{ animation: none !important; transition: none !important; }}
    }}

    .logo-container {{
        text-align: center;
        padding-top: 20px;
        margin-bottom: -10px;
        animation: odyFadeUp 0.7s ease both;
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
        transition: transform 0.15s ease, background-color 0.2s ease, box-shadow 0.2s ease;
    }}
    .stButton>button:hover {{
        background-color: {STARK_WHITE};
        color: {MATTE_BLACK};
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(241, 181, 0, 0.25);
    }}

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
        animation: odyFadeUp 0.5s ease both;
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
    """Replace Unicode characters that crash fpdf2 built-in fonts."""
    replacements = {
        '\u2014': '-', '\u2013': '-',
        '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u00a0': ' ',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


# --- PDF GENERATION ---
def generate_pdf(user_name, school_name, scores, detailed_actions):
    logo_path = get_logo_path()
    icon_path = get_icon_path()
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=30)

    def draw_page_bg(first_page=False):
        pdf.set_fill_color(26, 26, 26)
        pdf.rect(0, 0, 210, 297, 'F')
        pdf.set_fill_color(241, 181, 0)
        pdf.rect(0, 0, 210, 8 if first_page else 4, 'F')
        pdf.set_fill_color(241, 181, 0)
        pdf.rect(0, 289, 210, 8, 'F')

    def draw_continuation_header():
        if icon_path:
            pdf.image(icon_path, x=180, y=6, w=12)
        pdf.set_font('Helvetica', 'B', 7)
        pdf.set_text_color(100, 100, 100)
        saved_y = pdf.get_y()
        pdf.set_xy(140, 9)
        pdf.cell(35, 4, 'ODYSSEY  |  AI READINESS', align='R')
        pdf.set_y(saved_y)

    def new_page():
        pdf.add_page()
        draw_page_bg(first_page=False)
        draw_continuation_header()
        pdf.set_y(20)

    # === PAGE 1 ===
    pdf.add_page()
    draw_page_bg(first_page=True)

    # Logo centred
    if logo_path:
        pdf.image(logo_path, x=82, y=15, w=46)
        pdf.set_y(65)
    else:
        pdf.set_y(25)

    # Title
    pdf.set_font('Helvetica', 'B', 32)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 14, 'ODYSSEY', ln=True, align='C')

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'AI READINESS ASSESSMENT', ln=True, align='C')

    # Gold rule centred
    pdf.set_fill_color(241, 181, 0)
    pdf.rect(75, pdf.get_y() + 3, 60, 2, 'F')
    pdf.ln(14)

    # User details
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, clean_text(user_name), ln=True, align='C')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, 6, clean_text(school_name), ln=True, align='C')
    pdf.ln(12)

    # === SCORES BOX ===
    pdf.set_fill_color(0, 0, 0)
    pdf.set_draw_color(241, 181, 0)
    box_y = pdf.get_y()
    pdf.rect(15, box_y, 180, 45, 'DF')

    pdf.set_y(box_y + 6)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'YOUR SCORES (0-3)', ln=True, align='C')

    pillars = ['POLICY', 'PROCESS', 'PEOPLE', 'PROOF']
    col_w = 45
    start_x = 15

    # Pillar labels
    pdf.set_y(box_y + 16)
    for i, p in enumerate(pillars):
        pdf.set_x(start_x + (i * col_w))
        pdf.set_font('Helvetica', '', 8)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(col_w, 4, p, align='C')
    pdf.ln(5)

    # Pillar scores (big gold numbers)
    for i in range(4):
        pdf.set_x(start_x + (i * col_w))
        pdf.set_font('Courier', 'B', 20)
        pdf.set_text_color(241, 181, 0)
        pdf.cell(col_w, 10, str(round(scores[i], 1)), align='C')

    avg_score = sum(scores) / 4
    pdf.ln(12)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 5, f'Average: {round(avg_score, 1)} / 3', ln=True, align='C')

    pdf.set_y(box_y + 52)

    # Intro text
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(210, 210, 210)
    pdf.set_x(20)
    pdf.multi_cell(170, 5, clean_text(
        'None of this is pass or fail. The scores give you a snapshot of where '
        'things stand, and the actions below focus on where the biggest gaps are. '
        'For any pillar scoring below 2, the detail is expanded.'
    ), align='C')
    pdf.ln(10)

    # === ACTION PLANS ===
    for idx, p_name in enumerate(pillars):
        p_score = scores[idx]
        p_actions = detailed_actions[p_name]

        if pdf.get_y() > 215:
            new_page()

        # Pillar header — gold left bar + name + score right-aligned
        header_y = pdf.get_y()
        pdf.set_fill_color(241, 181, 0)
        pdf.rect(15, header_y, 3, 10, 'F')

        pdf.set_x(22)
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(120, 10, p_name)
        pdf.set_font('Helvetica', 'B', 13)
        pdf.set_text_color(241, 181, 0)
        pdf.cell(0, 10, f'{round(p_score, 1)} / 3', ln=True, align='R')

        # Gold rule
        pdf.set_fill_color(241, 181, 0)
        pdf.rect(15, pdf.get_y(), 180, 0.8, 'F')
        pdf.ln(5)

        for title, desc in p_actions:
            if pdf.get_y() > 240:
                new_page()

            pdf.set_x(20)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(241, 181, 0)
            pdf.cell(0, 5, clean_text(title.upper()), ln=True)

            pdf.set_x(20)
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(195, 195, 195)
            pdf.multi_cell(170, 4.5, clean_text(desc))
            pdf.ln(4)

        pdf.ln(4)

    # === CTA BOX ===
    if pdf.get_y() > 220:
        new_page()

    cta_y = pdf.get_y()
    pdf.set_fill_color(34, 34, 34)
    pdf.set_draw_color(241, 181, 0)
    pdf.rect(15, cta_y, 180, 32, 'DF')

    pdf.set_y(cta_y + 6)
    pdf.set_x(20)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 5, 'WHAT NEXT?', ln=True)

    pdf.set_x(20)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(195, 195, 195)
    pdf.multi_cell(170, 4.5, clean_text(
        'This is meant to be a conversation starter, not a finished strategy. '
        'If you want to talk through these results or need support putting a plan '
        'together, get in touch: peter@odysseylearningsolutions.com'
    ))

    # === SIGN-OFF ===
    pdf.ln(12)
    signoff_y = pdf.get_y()

    if icon_path:
        pdf.image(icon_path, x=15, y=signoff_y, w=18)
        text_x = 38
    else:
        text_x = 15

    pdf.set_x(text_x)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(241, 181, 0)
    pdf.cell(0, 6, 'PETER', ln=True)
    pdf.set_x(text_x)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(160, 160, 160)
    pdf.cell(0, 4, 'FOUNDER  |  ODYSSEY LEARNING SOLUTIONS', ln=True)
    pdf.set_x(text_x)
    pdf.cell(0, 4, 'peter@odysseylearningsolutions.com', ln=True)

    return bytes(pdf.output())


# --- EMAIL FUNCTION ---
def send_email(to_email, user_name, school_name, scores_summary, plan_html_content):
    try:
        import requests
        api_key = st.secrets["brevo_api_key"]

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: {DEEP_CHARCOAL}; border: 2px solid {ODYSSEY_GOLD}; padding: 40px; color: {STARK_WHITE};">
                <div style="text-align: center; margin-bottom: 20px;">
                    <img src="{ICON_URL}" width="50" style="margin-bottom: 8px;"><br>
                    <img src="{LOGO_URL}" width="180" alt="Odyssey Learning Solutions">
                </div>
                <div style="text-align: left; border-bottom: 6px solid {ODYSSEY_GOLD}; padding-bottom: 10px; margin-bottom: 30px;">
                    <h1 style="color: {STARK_WHITE}; margin: 0; font-size: 28px; letter-spacing: 2px;">ODYSSEY</h1>
                    <p style="color: {ODYSSEY_GOLD}; font-weight: bold; margin: 0; text-transform: uppercase; font-size: 11px;">AI Readiness Assessment</p>
                </div>
                <p style="font-size: 16px;">Hi {user_name},</p>
                <p style="font-size: 14px; line-height: 1.6;">Here are the results from your AI Readiness Assessment for <strong>{school_name}</strong>. The scores below give you a snapshot of where things stand across four areas - Policy, Process, People and Proof.</p>
                <p style="font-size: 14px; line-height: 1.6;">None of this is pass or fail. It's a starting point for working out where to focus first.</p>
                <div style="background-color: {MATTE_BLACK}; padding: 20px; border: 1px solid {SLATE_GREY}; margin: 25px 0;">
                    <h3 style="margin-top: 0; color: {ODYSSEY_GOLD}; font-size: 16px; text-transform: uppercase;">Your Scores (0-3)</h3>
                    <p style="font-size: 14px; margin: 0; font-family: 'Courier New', monospace; color: {STARK_WHITE};">{scores_summary}</p>
                </div>
                <h3 style="color: {ODYSSEY_GOLD}; text-transform: uppercase; border-bottom: 2px solid {SLATE_GREY}; padding-bottom: 5px; font-size: 18px;">90-Day Actions</h3>
                <p style="font-size: 14px; line-height: 1.6; margin-bottom: 20px;">The actions below are tailored to where your scores suggest the biggest gaps.</p>
                <div style="color: {STARK_WHITE};">{plan_html_content}</div>
                <div style="margin-top: 30px; padding: 20px; border-left: 4px solid {ODYSSEY_GOLD}; background-color: #222;">
                    <p style="margin: 0; font-size: 14px; line-height: 1.6;">
                        <strong>WHAT NEXT?</strong><br>
                        This is meant to be a conversation starter, not a finished strategy. If you would like to talk through these results or want support putting a plan together, just reply to this email.
                    </p>
                </div>
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid {SLATE_GREY};">
                    <p style="margin: 0; font-weight: bold; color: {ODYSSEY_GOLD}; font-size: 18px;">PETER</p>
                    <p style="margin: 0; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Founder | Odyssey Learning Solutions</p>
                    <p style="margin: 5px 0 0 0; font-size: 12px; color: {SLATE_GREY};">peter@odysseylearningsolutions.com</p>
                </div>
            </div>
        </body>
        </html>
        """

        payload = {
            "sender": {"name": "Peter | Odyssey Learning Solutions", "email": "peter@odysseylearningsolutions.com"},
            "to": [{"email": to_email}],
            "cc": [{"email": st.secrets["admin_email"]}],
            "replyTo": {"email": "peter@odysseylearningsolutions.com"},
            "subject": f"Your AI Readiness Results - {school_name}",
            "htmlContent": html_body
        }

        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": api_key, "Content-Type": "application/json"},
            json=payload
        )

        if response.status_code == 201:
            return True
        else:
            st.error(f"Email could not be sent. ({response.text})")
            return False

    except Exception as e:
        st.error(f"Email could not be sent. ({e})")
        return False


# --- APP UI ---
st.markdown(f"""
<div class="logo-container">
    <img src="{ICON_URL}" width="200" style="margin-bottom: 8px;"><br>
    <img src="{LOGO_URL}" width="400">
</div>
""", unsafe_allow_html=True)
st.caption("AI READINESS TOOL")
st.title("WHERE DOES YOUR SCHOOL STAND?")

st.markdown(
    f'<p style="font-size: 14px; line-height: 1.6; color: {STARK_WHITE}; margin-bottom: 25px;">'
    'Answer 20 questions across four areas - Policy, Process, People and Proof - '
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

# --- CONTEXT BRANCHING ---
st.markdown(
    f'<p style="font-size: 13px; color: {ODYSSEY_GOLD}; text-transform: uppercase; '
    f'letter-spacing: 1px; font-weight: bold; margin-bottom: 8px;">FIRST, THE CONTEXT</p>',
    unsafe_allow_html=True
)
context_choice = st.radio(
    "Are you completing this for a single school, or across a trust?",
    ["A single school", "A multi-academy trust (MAT)"],
    key="context_choice",
    horizontal=True,
)
CONTEXT = "mat" if context_choice.startswith("A multi") else "school"

st.markdown(f'<div style="width: 100%; height: 2px; background: {ODYSSEY_GOLD}; margin: 20px 0;"></div>', unsafe_allow_html=True)


# --- ASSESSMENT QUESTIONS now live in content.py ---
# --- RENDER ASSESSMENT ---
tabs = st.tabs(["POLICY", "PROCESS", "PEOPLE", "PROOF"])
scores = []
total_answered = 0
total_questions = 0

for i, (p_name, qs) in enumerate(QUESTIONS.items()):
    with tabs[i]:
        p_scores = []
        for j, item in enumerate(qs):
            question, options = item[0], item[1]
            meta = item[2] if len(item) > 2 else {}

            # Skip questions that don't apply to this context
            q_context = meta.get("context")
            if q_context and q_context != CONTEXT:
                continue

            # Use MAT wording if we're in trust mode and it's provided
            display_q = question
            if CONTEXT == "mat" and meta.get("mat_text"):
                display_q = meta["mat_text"]

            option_labels = [opt[0] for opt in options]
            selected = st.radio(display_q, option_labels, key=f"{p_name}_{j}")
            score = next(opt[1] for opt in options if opt[0] == selected)
            p_scores.append(score)
            total_questions += 1
            if selected != option_labels[0]:
                total_answered += 1
        # Pillar score normalised to 0-3 regardless of how many questions applied
        scores.append(sum(p_scores) / len(p_scores) if p_scores else 0)

# Progress
progress_pct = min(int((total_answered / total_questions) * 100), 100) if total_questions else 0
st.markdown(f"""
<div class="progress-bar-container">
    <div style="background-color: {SLATE_GREY}; height: 6px; width: 100%;">
        <div class="progress-bar-fill" style="width: {progress_pct}%;"></div>
    </div>
    <div class="progress-text">{total_answered} of {total_questions} questions answered</div>
</div>
""", unsafe_allow_html=True)


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

        avg_score = sum(scores) / 4
        summary_note = get_summary_note(avg_score)

        st.markdown(
            f'<p style="font-size: 14px; line-height: 1.6; color: {STARK_WHITE}; '
            f'padding: 15px; background-color: {MATTE_BLACK}; border-left: 3px solid {ODYSSEY_GOLD}; '
            f'animation: odyFadeUp 0.6s ease both;">'
            f'{summary_note}</p>',
            unsafe_allow_html=True
        )

        st.subheader("YOUR 90-DAY ACTIONS")

        plan_html = ""
        pillars = ['POLICY', 'PROCESS', 'PEOPLE', 'PROOF']

        # Build the actions actually shown, tiered by each pillar's score.
        # This same dict feeds the PDF so screen and download always match.
        shown_actions = {}

        for idx, p_name in enumerate(pillars):
            p_score = scores[idx]
            p_actions = actions_for_score(p_name, p_score)
            shown_actions[p_name] = p_actions
            with st.expander(f"{p_name} - SCORE: {round(p_score, 1)}/3", expanded=(p_score < 2)):
                plan_html += f"<h4 style='color: {ODYSSEY_GOLD}; text-transform: uppercase; margin-bottom: 10px;'>{p_name} (Score: {round(p_score, 1)}/3)</h4>"
                for ai, (title, desc) in enumerate(p_actions):
                    delay = round(ai * 0.08, 2)
                    st.markdown(
                        f"""<div class='action-item' style='animation-delay: {delay}s;'>
                            <span class='action-title'>{title}</span>
                            <span class='action-desc'>{desc}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    plan_html += f"<p style='margin-bottom: 15px;'><strong>{title}</strong><br><span style='font-size: 13px; color: #ccc; line-height: 1.6;'>{desc}</span></p>"

        score_sum = f"POLICY: {round(scores[0], 1)} | PROCESS: {round(scores[1], 1)} | PEOPLE: {round(scores[2], 1)} | PROOF: {round(scores[3], 1)}"

        # --- PDF DOWNLOAD ---
        st.markdown(f'<div style="width: 100%; height: 2px; background: {ODYSSEY_GOLD}; margin: 25px 0 15px 0;"></div>', unsafe_allow_html=True)

        pdf_bytes = generate_pdf(name, school if school else "your school", scores, shown_actions)
        school_slug = (school or "school").lower().replace(" ", "-").replace("/", "-")

        st.download_button(
            label="DOWNLOAD YOUR ACTION PLAN (PDF)",
            data=pdf_bytes,
            file_name=f"ai-readiness-{school_slug}.pdf",
            mime="application/pdf"
        )

        # --- EMAIL (backup) ---
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
            st.info("Your PDF is ready above. The email didn't go through - likely a firewall issue - but you've got everything you need.")
        st.balloons()
