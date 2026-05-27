"""
Cycle Bot — Real-time Slack bot for Bills & Subscription Management project coordination.
Uses Slack Socket Mode for instant responses (no polling delay).
"""

import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from feedback import (
    log_explicit_feedback,
    log_unanswered,
    log_repeated_question,
    log_thumbs_down,
    log_interaction,
    get_feedback_summary,
)

# --- Config ---
REPO_PATH = Path('/tmp/bills-subscriptions-prd')
CHANNEL_ID = 'C0B6KN2RPLZ'
BOT_USER_ID = 'U0B6N3EQVHP'
DRI_USER_ID = 'U04V14YS3BH'  # Michael Duane

BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN') or os.environ.get('GOOSE_SLACK_BOT_TOKEN')
APP_TOKEN = os.environ.get('SLACK_APP_TOKEN')

if not BOT_TOKEN or not APP_TOKEN:
    print("ERROR: Missing tokens.")
    print("  SLACK_BOT_TOKEN (xoxb-...): Bot User OAuth Token")
    print("  SLACK_APP_TOKEN (xapp-...): App-Level Token (needs connections:write scope)")
    print("")
    print("To get SLACK_APP_TOKEN:")
    print("  1. Go to https://api.slack.com/apps → Cycle Bot → Basic Information")
    print("  2. Scroll to 'App-Level Tokens' → Generate Token")
    print("  3. Name it 'socket-mode', add scope 'connections:write'")
    print("  4. Copy the xapp-... token")
    exit(1)

app = App(token=BOT_TOKEN)


# --- Helper Functions ---

def read_file(filename):
    """Read a file from the project repo."""
    filepath = REPO_PATH / filename
    try:
        return filepath.read_text()
    except FileNotFoundError:
        return None


def get_open_decisions():
    """Parse DECISIONS.md and return list of open decisions."""
    content = read_file('DECISIONS.md')
    if not content:
        return []

    decisions = []
    open_section = content.split('## Open Decisions')[1].split('## Closed Decisions')[0] if '## Open Decisions' in content else ''

    for match in re.finditer(r'### (DEC-\d+)\s*—\s*(.+?)(?:\n|$)', open_section):
        dec_id = match.group(1)
        title = match.group(2).strip()
        # Find priority
        block = open_section[match.start():]
        next_dec = block.find('### DEC-', 1)
        if next_dec > 0:
            block = block[:next_dec]
        priority_match = re.search(r'\*\*Priority\*\*\s*\|\s*(.+?)\s*\|', block)
        priority = priority_match.group(1).strip() if priority_match else 'Unknown'
        decisions.append({'id': dec_id, 'title': title, 'priority': priority})

    return decisions


def get_next_decision_number():
    """Get the next decision number from DECISIONS.md."""
    content = read_file('DECISIONS.md')
    match = re.search(r'Next decision number: DEC-(\d+)', content or '')
    return int(match.group(1)) if match else 6


def now_et():
    """Get current time formatted in ET."""
    return datetime.now().strftime('%Y-%m-%d %I:%M%p ET')


def git_commit(message):
    """Stage all changes and commit."""
    try:
        subprocess.run(['git', 'add', '-A'], cwd=REPO_PATH, capture_output=True)
        subprocess.run(['git', 'commit', '-m', message], cwd=REPO_PATH, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=REPO_PATH, capture_output=True)
    except Exception as e:
        print(f"Git error: {e}")


def add_decision(title, opened_by, slack_link):
    """Add a new decision to DECISIONS.md."""
    num = get_next_decision_number()
    dec_id = f"DEC-{num:03d}"

    new_entry = f"""### {dec_id} — {title}

| Field | Value |
|-------|-------|
| **Opened** | {now_et()} |
| **Opened by** | {opened_by} |
| **Priority** | TBD — needs assessment |
| **Target close** | TBD |
| **Status** | 🔓 OPEN |

**Context:** Raised in Slack discussion. Needs team alignment.

**Options considered:**
- TBD (to be discussed)

**Decision:** TBD (pending DRI approval)

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| {now_et()} | {opened_by} | Raised decision in Slack | [thread]({slack_link}) |

---

"""

    content = read_file('DECISIONS.md')
    if content:
        # Insert after "## Open Decisions\n\n"
        content = content.replace('## Open Decisions\n\n', f'## Open Decisions\n\n{new_entry}')
        # Update next number
        content = re.sub(r'Next decision number: DEC-\d+', f'Next decision number: DEC-{num + 1}', content)
        (REPO_PATH / 'DECISIONS.md').write_text(content)
        git_commit(f"sync: New decision {dec_id} — {title}")

    return dec_id


# --- Response Generator ---

def generate_response(question):
    """Generate a response based on the question and project docs."""
    q = question.lower().strip()

    if not q:
        return "Hey! Ask me anything about the project — decisions, scope, risks, status, agenda, team, metrics, or how things work."

    # Open decisions
    if any(kw in q for kw in ['open decision', 'decisions', 'what decisions', 'pending']):
        decisions = get_open_decisions()
        if not decisions:
            return "No open decisions — we're fully aligned. 🎉"
        lines = [f"There are {len(decisions)} open decisions:\n"]
        for i, d in enumerate(decisions, 1):
            lines.append(f"{i}. *{d['id']} — {d['title']}*\n   Priority: {d['priority']}\n")
        lines.append("\nAll are on the agenda for Monday's kickoff. @michaelduane confirms to close.")
        return '\n'.join(lines)

    # Scope
    if any(kw in q for kw in ['scope', 'option a', 'option b', 'option c', 'options']):
        return ("*Cycle 2 Scope Options:*\n\n"
                "*Option A:* Hub + Knot Linking only (visibility + consolidation) — ~4 weeks eng\n"
                "*Option B:* Hub + Knot Linking + Management Actions (⭐ recommended) — ~5-6 weeks eng\n"
                "*Option C:* Full vision with Bill-Specific Auto-Reload — ~8+ weeks eng\n\n"
                "Recommendation is Option B — ships the most customer value within 6 weeks without taking on auto-reload complexity.\n\n"
                "Full details: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/docs/scope-options.md")

    # Risks
    if 'risk' in q:
        return ("There are 14 identified risks in the PRD. Top ones:\n\n"
                "• *Cold Start / Empty State* (10/10) — Most customers see nothing on day 1\n"
                "• *Knot Merchant Coverage Gaps* (7/10) — Not all billers supported\n"
                "• *Customer Trust with Card-Switching* (7/10) — Handing credentials to a third party\n"
                "• *Recurring Payment Decline Rates* (6/10) — 2x higher than one-time transactions\n"
                "• *Auto-Reload Cannibalization* (5/10) — New feature may confuse existing users\n\n"
                "Full risk register: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/PRD.md")

    # Agenda / Monday / Kickoff
    if any(kw in q for kw in ['agenda', 'monday', 'kickoff', 'meeting']):
        return ("*Monday's kickoff agenda (June 2):*\n\n"
                "1. Scope decision — which option (A/B/C) do we commit to? (15 min)\n"
                "2. Staffing — confirm the squad, identify gaps (5 min)\n"
                "3. Detection strategy — transaction patterns vs. Knot vs. hybrid\n"
                "4. Empty state — what do customers see on day 1?\n"
                "5. Confidence check — rate 1-5 on hitting the cycle goal\n\n"
                "Full agenda: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/docs/weekly-reviews.md")

    # Status
    if any(kw in q for kw in ['status', 'how are we', 'where are we', 'update']):
        return ("We're in pre-kickoff mode. Cycle 2 starts Monday June 2.\n\n"
                "• 4 open decisions pending Monday's kickoff\n"
                "• PRD, scope options, and risk register are complete\n"
                "• Team: Michael (DRI), Trevor (PM), Megan (Eng), Gustavo (Design)\n"
                "• Designs in Figma, ready for review\n\n"
                "First status check goes out Monday at 6am ET.")

    # Team
    if any(kw in q for kw in ['team', 'who is', 'who owns', 'who\'s']):
        return ("*Bills & Subscription Management — Team:*\n\n"
                "• *Michael Duane* — DRI (overall)\n"
                "• *Trevor Luong* — PM\n"
                "• *Megan Tong* — Eng Lead\n"
                "• *Gustavo* — Design Lead\n\n"
                "Full details: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/README.md")

    # Metrics
    if any(kw in q for kw in ['metric', 'success', 'kpi', 'measure', 'goal']):
        return ("*North star metric:* Recurring card GPV per customer\n\n"
                "*Leading indicators:*\n"
                "• Number of bills/subscriptions linked via Knot\n"
                "• Card-switch completion rate\n"
                "• Recurring payment success rate (currently ~2x higher decline rate vs. one-time)\n"
                "• Auto-reload adoption for bills (future)\n\n"
                "Specific targets TBD after kickoff scope decision.")

    # Competitors
    if any(kw in q for kw in ['competitor', 'competition', 'market']):
        return ("*Key competitors:*\n\n"
                "• *Rocket Money* — Bill tracking + cancellation (standalone app)\n"
                "• *Apple Wallet* — Recurring transaction visibility (passive)\n"
                "• *Chime* — Some bill pay features (limited management)\n"
                "• *Traditional banks* — Bill pay but no card-switching\n\n"
                "Our edge: Knot-powered card-switching + management actions + auto-reload, all inside Cash App where the money already lives.")

    # How things work / process
    if any(kw in q for kw in ['how do', 'how does', 'process', 'workflow']):
        return ("Here's how the project coordination works:\n\n"
                "• *Slack* — Day-to-day discussion. Say \"decision:\" to open a decision.\n"
                "• *GitHub* — Source of truth (PRD, decisions, notes, status)\n"
                "• *Google Doc* — Readable companion (5 tabs)\n"
                "• *Me (Cycle Bot)* — I sync everything hourly, post status checks Mondays, and track decisions\n\n"
                "Full details: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/HOW-WE-WORK.md")

    # Problem / why
    if any(kw in q for kw in ['problem', 'why are we', 'what are we solving', 'pain point']):
        return ("*The problem we're solving:*\n\n"
                "Cash App Card customers lack visibility into their recurring charges. They:\n"
                "• Track bills offline (spreadsheets, notes, memory)\n"
                "• Get surprised by subscription renewals\n"
                "• Miss payments because they don't sequence bills properly (pay Netflix before rent)\n"
                "• Don't have enough funds when recurring charges hit\n\n"
                "Recurring/merchant-initiated transactions have 2x+ higher decline rates than one-time purchases. "
                "This feature consolidates bills onto Cash App Card, improves funding, and reduces declines — "
                "making Cash App the primary bank for recurring spend.")

    # Timeline
    if any(kw in q for kw in ['timeline', 'when', 'deadline', 'ship', 'launch']):
        return ("*Cycle 2 Timeline:*\n\n"
                "• *June 2* — Kickoff (scope decision)\n"
                "• *June 9-16* — Build phase (Knot integration, Hub UI)\n"
                "• *June 23* — Integration testing\n"
                "• *June 30* — Internal dogfood target\n"
                "• *July 7* — Final week, delivery assessment\n"
                "• *July 14-17* — Off-week: retro + delivery review\n\n"
                "Gated pilot to real customers planned for Cycle 3.")

    # Knot
    if 'knot' in q:
        return ("*Knot (knotapi.com):*\n\n"
                "Knot powers the card-switching and subscription management capabilities:\n"
                "• *Card-on-file switching* — Changes payment method to Cash App Card with a few clicks\n"
                "• *Subscription management* — Cancel, pause, update subscriptions\n"
                "• *15,000+ merchant coverage*\n"
                "• No one has built robust subscription management on top of Knot yet — we'd be first\n\n"
                "More: https://www.knotapi.com/subscription-manager/")

    # Default — log as unanswered for learning
    return None  # Signal that we couldn't answer


# --- Slack Event Handlers ---

@app.event("app_mention")
def handle_mention(event, say):
    """Respond to @Cycle Bot mentions."""
    ts = datetime.now().strftime('%H:%M:%S')
    user = event.get('user', 'unknown')
    text = event.get('text', '')
    print(f"[{ts}] @mention from {user}: {text}")

    # Track interaction
    log_interaction('total_mentions')

    # Strip the bot mention
    question = re.sub(f'<@{BOT_USER_ID}>', '', text).strip()

    # Check for explicit feedback
    feedback_signals = ['feedback:', 'suggestion:', 'you should', 'it would be better if', 'can you improve']
    if any(signal in question.lower() for signal in feedback_signals):
        feedback_text = re.sub(r'(feedback:|suggestion:)', '', question, flags=re.IGNORECASE).strip()
        count = log_explicit_feedback(user, feedback_text, thread_ts=event['ts'])
        say(
            text=f"🙏 Thanks for the feedback — logged as item #{count}. I'll use this to improve.\n\n"
                 f"_You can always give me feedback by saying \"feedback: [your thought]\"_",
            thread_ts=event['ts'],
        )
        log_interaction('total_responses')
        return

    # Check for feedback summary request (DRI only)
    if 'feedback summary' in question.lower() or 'how are you doing' in question.lower():
        summary = get_feedback_summary()
        say(text=summary, thread_ts=event['ts'])
        log_interaction('total_responses')
        return

    # Generate response
    response = generate_response(question)

    if response is None:
        # Couldn't answer — log it and give fallback
        log_unanswered(user, question)
        response = (
            "I'm not sure I have a specific answer for that, but I've logged it so I can learn.\n\n"
            "Here's where to find things:\n"
            "• *PRD:* https://github.com/michaelmduane/bills-subscriptions-management/blob/main/PRD.md\n"
            "• *Decisions:* https://github.com/michaelmduane/bills-subscriptions-management/blob/main/DECISIONS.md\n"
            "• *How we work:* https://github.com/michaelmduane/bills-subscriptions-management/blob/main/HOW-WE-WORK.md\n\n"
            "Ask me something more specific and I'll dig in! Or say \"feedback: [suggestion]\" to help me improve."
        )
    else:
        # Track which category was asked about
        q = question.lower()
        if 'decision' in q: log_repeated_question('decisions')
        elif 'scope' in q or 'option' in q: log_repeated_question('scope')
        elif 'risk' in q: log_repeated_question('risks')
        elif 'agenda' in q or 'monday' in q: log_repeated_question('agenda')
        elif 'status' in q: log_repeated_question('status')
        elif 'team' in q or 'who' in q: log_repeated_question('team')
        elif 'metric' in q or 'kpi' in q: log_repeated_question('metrics')
        elif 'competitor' in q: log_repeated_question('competitors')
        elif 'timeline' in q or 'when' in q: log_repeated_question('timeline')
        elif 'knot' in q: log_repeated_question('knot')
        elif 'problem' in q or 'why' in q: log_repeated_question('problem')
        elif 'how' in q and 'work' in q: log_repeated_question('process')
        else: log_repeated_question('other')

    say(text=response, thread_ts=event['ts'])
    log_interaction('total_responses')


@app.event("message")
def handle_message(event, say):
    """Watch for decision signals and DRI closures."""
    # Skip bot messages, message_changed events, etc.
    if event.get('bot_id') or event.get('subtype'):
        return
    if event.get('channel') != CHANNEL_ID:
        return

    text = (event.get('text') or '').lower()
    user = event.get('user', '')
    thread_ts = event.get('thread_ts')
    message_ts = event.get('ts')

    # Decision signals (top-level messages only)
    if not thread_ts:
        decision_signals = ['decision:', 'open question:', 'proposal:', 'we need to decide']
        if any(signal in text for signal in decision_signals):
            # Extract title
            raw_text = event.get('text', '')
            title = re.sub(r'(decision:|open question:|proposal:|we need to decide)', '', raw_text, flags=re.IGNORECASE).strip()
            title = title[:100]

            # Get user info for "opened by"
            try:
                user_info = app.client.users_info(user=user)
                display_name = user_info['user']['real_name']
            except:
                display_name = f"<@{user}>"

            slack_link = f"https://sq-block.slack.com/archives/{CHANNEL_ID}/p{message_ts.replace('.', '')}"
            dec_id = add_decision(title, display_name, slack_link)

            ts_str = datetime.now().strftime('%H:%M:%S')
            print(f"[{ts_str}] Decision captured: {dec_id} — {title}")

            say(
                text=(f"📝 Got it — logged as *{dec_id}*.\n\n"
                      f"I've added this to the decisions log. Discuss in this thread, then @michaelduane confirms to close.\n\n"
                      f"_Tracked in: https://github.com/michaelmduane/bills-subscriptions-management/blob/main/DECISIONS.md_"),
                thread_ts=message_ts,
            )

    # Decision closure by DRI (in threads)
    if thread_ts and user == DRI_USER_ID:
        closure_signals = ['approved', "let's go with", 'confirmed', 'yes ship it', 'agreed', "+1 let's do it", 'decision: closed']
        if any(signal in text for signal in closure_signals):
            ts_str = datetime.now().strftime('%H:%M:%S')
            print(f"[{ts_str}] Decision closure detected by DRI in thread {thread_ts}")

            say(
                text="✅ Decision closed by @michaelduane. Updating DECISIONS.md and PRD.\n\n_Syncing to GitHub..._",
                thread_ts=thread_ts,
            )
            # The hourly sync will handle the actual file updates


# Handle emoji reactions (👎 = bad response, 👍 = good response)
@app.event("reaction_added")
def handle_reaction(event, say):
    """Track reactions to bot messages for feedback."""
    reaction = event.get('reaction', '')
    user = event.get('user', '')
    item = event.get('item', {})

    # Only care about reactions to messages in our channel
    if item.get('channel') != CHANNEL_ID:
        return

    if reaction in ['-1', 'thumbsdown']:
        log_thumbs_down(user, item.get('ts', ''))
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 👎 reaction from {user} on {item.get('ts')}")

    elif reaction in ['+1', 'thumbsup', 'white_check_mark']:
        # Positive signal — no action needed but could track later
        pass


# --- Start ---

if __name__ == '__main__':
    print("⚡️ Cycle Bot starting in Socket Mode...")
    print(f"   Channel: {CHANNEL_ID}")
    print(f"   Bot User: {BOT_USER_ID}")
    print(f"   Repo: {REPO_PATH}")
    print("")

    handler = SocketModeHandler(app, APP_TOKEN)
    handler.start()
