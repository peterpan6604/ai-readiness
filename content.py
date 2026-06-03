"""
content.py — Odyssey AI Readiness Assessment
All questions and action-plan content live here so Pete can edit them
without touching the app logic. Two things to know before editing:

1. CONTEXT BRANCHING
   Each question can carry an optional "mat_text" — alternative wording shown
   when someone is completing the assessment at trust/MAT level. If a question
   has no mat_text, the same wording is shown to everyone.
   Some questions are MAT-only or school-only — set "context": "mat" or "school".
   Default (no context key) means the question shows to both.

2. SCORING
   Every question has 4 options scored 0-3. Six questions per pillar.
   Pillar score = sum of the six answers / 6, giving a 0-3 pillar score.

3. ACTION PLAN
   Actions are TIERED. For each pillar, actions are ordered most-urgent first.
   The app shows more actions the lower the score:
     score < 1   -> show first 3 actions (the foundations)
     1 <= score < 2 -> show first 2
     score >= 2  -> show 1 (the next step up)
   Write each action as you'd say it to a head over a coffee. Specific. Plain.
"""

# =============================================================================
#  ASSESSMENT QUESTIONS
#  Format: (question_text, [(option, score), ...], optional_kwargs)
#  optional kwargs dict can contain:
#     "mat_text": "alternative question wording for trust-level"
#     "context":  "mat"  or  "school"   (omit = show to both)
# =============================================================================

QUESTIONS = {
    "POLICY": [
        ("Does your school have a standalone AI use policy?",
         [("No - not started", 0),
          ("We've discussed it but nothing written", 1),
          ("Draft exists but not approved", 2),
          ("Yes - approved and shared with staff", 3)],
         {"mat_text": "Does your trust have a standard AI use policy that schools work from?"}),

        ("Has your safeguarding policy been updated to reference AI?",
         [("No", 0),
          ("It's on the list but not done yet", 1),
          ("Partially - some references added", 2),
          ("Yes - reviewed and updated", 3)],
         {}),

        ("Has your malpractice or academic integrity policy been updated for AI?",
         [("No", 0),
          ("We're aware of JCQ updates but haven't acted", 1),
          ("In progress", 2),
          ("Yes - aligned with current JCQ guidance", 3)],
         {}),

        ("Do you have a process for parental consent around student AI use?",
         [("No - not considered yet", 0),
          ("We've discussed it internally", 1),
          ("Draft process exists", 2),
          ("Yes - in place and communicated to parents", 3)],
         {}),

        ("Is AI part of your governance strategy at board or governor level?",
         [("No - governors haven't discussed AI", 0),
          ("Mentioned informally but no formal agenda item", 1),
          ("Governors have been briefed", 2),
          ("Yes - AI is a standing item with clear oversight", 3)],
         {"mat_text": "Is AI a standing item for your board of trustees?"}),

        # NEW (6th question)
        ("Is your AI policy consistent across the organisation, or does each part do its own thing?",
         [("Every school / department sets its own approach", 0),
          ("Some alignment but a lot of variation", 1),
          ("Broadly consistent with local flexibility", 2),
          ("Clear central standard that everyone works to", 3)],
         {"context": "mat",
          "mat_text": "Is your AI policy consistent across schools in the trust, or does each set its own?"}),

        # school-level alternative for the 6th slot
        ("Does your AI policy actually reflect what staff are doing day to day?",
         [("No - the policy and reality don't match", 0),
          ("Roughly, but it's out of date", 1),
          ("Mostly - reviewed in the last year", 2),
          ("Yes - written with staff input and kept current", 3)],
         {"context": "school"}),
    ],

    "PROCESS": [
        ("Do you know which AI tools your staff are currently using?",
         [("No idea", 0),
          ("We have a rough sense but nothing documented", 1),
          ("Mostly - some tools are tracked", 2),
          ("Yes - we have full visibility", 3)],
         {}),

        ("Do you maintain a register of approved AI tools?",
         [("No", 0),
          ("We've started listing some tools informally", 1),
          ("Partial register exists", 2),
          ("Yes - maintained and regularly reviewed", 3)],
         {"mat_text": "Is there a trust-wide register of approved AI tools schools can draw from?"}),

        ("Have you completed Data Protection Impact Assessments for AI tools in use?",
         [("No - not started", 0),
          ("For one or two tools only", 1),
          ("For most tools", 2),
          ("Yes - completed for all tools in use", 3)],
         {}),

        ("Is there a feedback loop for staff to report on how AI tools are working?",
         [("No", 0),
          ("Informal - staff chat about it in passing", 1),
          ("Some structured opportunities exist", 2),
          ("Yes - regular and scheduled", 3)],
         {}),

        ("Does your procurement process include AI-specific vetting?",
         [("No - we haven't thought about this", 0),
          ("Sometimes - depends who's buying", 1),
          ("Mostly - there's an informal checklist", 2),
          ("Yes - all new tools are vetted for AI considerations", 3)],
         {"mat_text": "Does trust-level procurement vet tools for AI and data considerations before schools adopt them?"}),

        # NEW (6th question)
        ("When a useful AI approach is found in one place, does it spread to others?",
         [("No - good practice stays where it started", 0),
          ("Occasionally, through word of mouth", 1),
          ("Sometimes shared through meetings or networks", 2),
          ("Yes - there's a deliberate way of sharing what works", 3)],
         {"mat_text": "When one school finds an AI approach that works, is there a way it reaches the others?"}),
    ],

    "PEOPLE": [
        ("Is there a named person leading on AI?",
         [("No", 0),
          ("Informally - someone's taken an interest", 1),
          ("Yes - but it sits alongside their other responsibilities", 2),
          ("Yes - with dedicated time and clear accountability", 3)],
         {"mat_text": "Is there a named person leading on AI at trust level - not just in individual schools?"}),

        ("What AI training have your staff received?",
         [("None", 0),
          ("Self-directed only - people finding their own way", 1),
          ("Some formal CPD has been delivered", 2),
          ("A structured ongoing programme is in place", 3)],
         {}),

        ("Do you have an AI working group or champions network?",
         [("No", 0),
          ("A few interested staff but nothing formal", 1),
          ("An informal group meets occasionally", 2),
          ("Yes - a formal working group with regular meetings", 3)],
         {"mat_text": "Is there a cross-school AI working group or champions network across the trust?"}),

        ("Have you engaged parents on the school's approach to AI?",
         [("No - not yet", 0),
          ("We're planning to", 1),
          ("Some communication has gone out", 2),
          ("Yes - parents have been informed and consulted", 3)],
         {}),

        ("Is AI literacy being taught to students?",
         [("No", 0),
          ("Ad hoc - some teachers cover it when relevant", 1),
          ("In certain subjects or year groups", 2),
          ("Yes - integrated across the curriculum", 3)],
         {}),

        # NEW (6th question)
        ("How confident are your staff using AI in their day-to-day work?",
         [("Most are anxious or avoiding it", 0),
          ("A keen few are confident, the rest aren't", 1),
          ("A reasonable spread - growing steadily", 2),
          ("Broadly confident across the team", 3)],
         {}),
    ],

    "PROOF": [
        ("Are you logging which staff have completed AI training?",
         [("No", 0),
          ("Partially - some records exist", 1),
          ("Mostly - we track it but not systematically", 2),
          ("Yes - all training is logged and tracked", 3)],
         {}),

        ("Are AI tool approval decisions documented?",
         [("No", 0),
          ("Some decisions are noted informally", 1),
          ("Mostly documented", 2),
          ("Yes - a clear record of all decisions and rationale", 3)],
         {}),

        ("Could you confidently present your AI governance approach to governors or inspectors?",
         [("Definitely not", 0),
          ("We'd struggle to pull it together", 1),
          ("We could put something together fairly quickly", 2),
          ("Yes - evidence is organised and ready", 3)],
         {"mat_text": "Could you present a clear trust-wide AI governance picture to trustees or inspectors?"}),

        ("Do you run surveys on AI use among staff or students?",
         [("No", 0),
          ("We've discussed doing this", 1),
          ("We've run one", 2),
          ("Yes - regular surveys are scheduled", 3)],
         {}),

        ("Do you have case studies or examples of AI impact?",
         [("No", 0),
          ("Anecdotal - staff share stories informally", 1),
          ("A few documented examples", 2),
          ("Yes - case studies are collected and shared", 3)],
         {}),

        # NEW (6th question)
        ("Can you see how AI readiness is changing over time, or only where it stands today?",
         [("We've never measured it", 0),
          ("We have a one-off snapshot", 1),
          ("We've measured it more than once", 2),
          ("Yes - we track it on a regular cycle", 3)],
         {"mat_text": "Can you compare AI readiness across schools and see how it's moving over time?"}),
    ],
}


# =============================================================================
#  ACTION PLAN — tiered, most urgent first.
#  Each pillar holds a list of (title, description). The app shows more of them
#  the lower the score. Write in Pete's voice. Reference real guidance.
# =============================================================================

ACTIONS = {
    "POLICY": [
        ("Write a standalone AI use policy",
         "Most schools still don't have one. You don't need to start from scratch - the DfE's product safety expectations and generative AI guidance give you a workable starting point. The thing that matters is getting something written that staff can actually refer to. It doesn't have to be perfect first time. Get a draft to governors this term and review it termly, because this area moves fast."),

        ("Update safeguarding and academic integrity policies for AI",
         "AI shifts the risk picture for both. JCQ has updated its guidance on AI use and malpractice - your assessment and integrity policies need to reflect that. On safeguarding, the question is simple: what happens if a student uses an AI tool and something concerning surfaces? If your policy is silent on it, that's the gap to close first."),

        ("Get AI onto the governor agenda",
         "Governors need the strategic picture, not the technical detail. What's being used, what the risks are, what the plan is. A fifteen-minute briefing at the next meeting is enough to start. They can't provide oversight on something nobody has told them about - and that's increasingly what inspectors will expect to see."),

        ("Pin down parental consent and communication",
         "Parents will ask how AI is being used with their children. Having a clear position - what tools, what data, what choice they have - turns an awkward conversation into a confident one. A short, plain statement to parents does more than a long policy nobody reads."),
    ],

    "PROCESS": [
        ("Find out what tools staff are already using",
         "There's a good chance staff are using tools you don't know about. A quick anonymous survey gives you the picture. This isn't about catching anyone out - it's about understanding what's happening so you can support it properly rather than driving it underground. You can't govern what you can't see."),

        ("Complete DPIAs for your most-used tools",
         "Data Protection Impact Assessments sound heavier than they are. Start with the tools staff use most. What data goes in, where it goes, who processes it. Your DPO can help. Once these are done you can say a clear yes or no to a tool rather than guessing - and you're meeting your UK GDPR obligations while you're at it."),

        ("Build and maintain an approved tool register",
         "A simple shared list: what's approved, what isn't, and why. Keep it somewhere staff can find it. Update it when new tools appear or existing ones change their terms. This is what stops everyone using a different tool with nobody knowing what's been checked."),

        ("Create a way to share what works",
         "Good practice tends to stay stuck where it started. A standing slot in a meeting, a shared space, an occasional showcase - any of these moves a useful approach from one classroom to the rest. The schools doing this well treat it as deliberate, not accidental."),
    ],

    "PEOPLE": [
        ("Give one person clear responsibility for AI",
         "This doesn't need to be a new role or a big time commitment. But someone has to own it. Without a named lead, AI sits in the everyone's-problem-and-nobody's-responsibility space. Pick someone with genuine interest and give them real time to do it - even half a day a fortnight changes things."),

        ("Move from one-off training to something structured",
         "The single twilight session rarely sticks. Staff need practical, hands-on training relevant to their actual role - admin staff seeing admin examples, teachers seeing teaching ones. Confidence comes from doing, not from being talked at. There are free DfE and Chartered College materials you can build on rather than starting cold."),

        ("Set up an AI working group",
         "Get a small group together from across the school - teaching, admin, IT, safeguarding. Meet half-termly. Share what's working, flag what isn't, feed into policy. Done well, it builds a culture where people experiment openly instead of quietly hiding what they're doing."),

        ("Bring students and parents into the picture",
         "Staff readiness is only part of it. Students need AI literacy taught, not assumed, and parents need to understand the school's approach. Neither has to be elaborate. A clear position and a few well-placed lessons do more than a glossy strategy."),
    ],

    "PROOF": [
        ("Start logging AI training",
         "Keep a record of who's been trained, when, and on what. This is basic accountability - if an inspector asks what you've done to support staff with AI, you need something to show. A shared spreadsheet is fine. It doesn't need to be clever."),

        ("Document your tool approval decisions",
         "When you approve or reject a tool, write down why. That gives you a paper trail showing considered decisions rather than reactions on the fly. It also saves time the next time someone asks about a similar tool - you've already done the thinking."),

        ("Pull together a governance evidence pack",
         "Bring your policy, training records, tool register and DPIA outcomes into one place. This isn't extra work for its own sake - it's being able to show governors and inspectors you've got a grip on AI. Ofsted aren't inspecting AI directly yet, but they will look at how well you manage risk and support staff."),

        ("Measure readiness more than once",
         "A single snapshot tells you where you are. Measuring again tells you whether anything's actually changing. Re-running an assessment like this one each term turns a gut feeling into something you can show - and shows staff the effort is going somewhere."),
    ],
}


def get_summary_note(avg_score):
    """One-line framing based on overall average. Pete's voice - no hype."""
    if avg_score < 1:
        return ("You're at the early stages - and that's exactly why this matters. "
                "Most schools are in a similar position. The point isn't where you "
                "are now, it's having a clear next step.")
    elif avg_score < 2:
        return ("You've made a start in some areas. The actions below are about "
                "building on that and closing the gaps that are holding the rest back.")
    else:
        return ("You're further ahead than most. The focus now is formalising what "
                "you've already started and building the evidence to prove it - the "
                "bit schools most often skip.")


def actions_for_score(pillar, score):
    """Return the actions to show for a pillar, tiered by how low the score is."""
    all_actions = ACTIONS[pillar]
    if score < 1:
        return all_actions[:3]
    elif score < 2:
        return all_actions[:2]
    else:
        return all_actions[:1]
