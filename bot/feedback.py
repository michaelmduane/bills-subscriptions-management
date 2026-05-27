"""
Cycle Bot Feedback & Learning System

Captures feedback in two ways:
1. Explicit feedback — users say "feedback:" or react with specific emojis
2. Implicit learning — tracks unanswered questions, repeated questions, and interaction patterns

Stores everything in a feedback log that the bot reads on startup to improve responses.
"""

import json
import os
from datetime import datetime
from pathlib import Path

FEEDBACK_FILE = Path('/tmp/bills-subscriptions-prd/bot/feedback.json')
LEARNINGS_FILE = Path('/tmp/bills-subscriptions-prd/bot/learnings.md')


def load_feedback():
    """Load existing feedback from disk."""
    if FEEDBACK_FILE.exists():
        return json.loads(FEEDBACK_FILE.read_text())
    return {
        'explicit_feedback': [],
        'unanswered_questions': [],
        'repeated_questions': {},
        'thumbs_down': [],
        'interaction_stats': {
            'total_mentions': 0,
            'total_responses': 0,
            'fallback_responses': 0,
            'decisions_captured': 0,
            'decisions_closed': 0,
        }
    }


def save_feedback(data):
    """Persist feedback to disk."""
    FEEDBACK_FILE.write_text(json.dumps(data, indent=2, default=str))


def log_explicit_feedback(user, text, thread_ts=None, context=None):
    """Log explicit feedback from a user (e.g., 'feedback: the bot should...')."""
    data = load_feedback()
    data['explicit_feedback'].append({
        'timestamp': datetime.now().isoformat(),
        'user': user,
        'feedback': text,
        'thread_ts': thread_ts,
        'context': context,
        'status': 'new',
    })
    save_feedback(data)
    update_learnings(data)
    return len(data['explicit_feedback'])


def log_unanswered(user, question):
    """Log when the bot gives a fallback/default response (couldn't answer)."""
    data = load_feedback()
    data['unanswered_questions'].append({
        'timestamp': datetime.now().isoformat(),
        'user': user,
        'question': question,
    })
    data['interaction_stats']['fallback_responses'] += 1
    save_feedback(data)


def log_repeated_question(question_category):
    """Track how often each question category is asked."""
    data = load_feedback()
    if question_category not in data['repeated_questions']:
        data['repeated_questions'][question_category] = 0
    data['repeated_questions'][question_category] += 1
    save_feedback(data)


def log_thumbs_down(user, message_ts, original_question=None):
    """Log when someone reacts with 👎 to a bot response."""
    data = load_feedback()
    data['thumbs_down'].append({
        'timestamp': datetime.now().isoformat(),
        'user': user,
        'message_ts': message_ts,
        'original_question': original_question,
    })
    save_feedback(data)


def log_interaction(event_type):
    """Increment interaction counters."""
    data = load_feedback()
    if event_type in data['interaction_stats']:
        data['interaction_stats'][event_type] += 1
    save_feedback(data)


def get_feedback_summary():
    """Generate a summary of feedback for reporting."""
    data = load_feedback()
    stats = data['interaction_stats']

    total_feedback = len(data['explicit_feedback'])
    new_feedback = len([f for f in data['explicit_feedback'] if f['status'] == 'new'])
    unanswered = len(data['unanswered_questions'])
    thumbs_down = len(data['thumbs_down'])

    # Top repeated questions
    top_questions = sorted(data['repeated_questions'].items(), key=lambda x: x[1], reverse=True)[:5]

    # Recent unanswered
    recent_unanswered = data['unanswered_questions'][-5:]

    summary = f"*Cycle Bot Feedback Summary*\n\n"
    summary += f"*Interactions:* {stats['total_mentions']} mentions, {stats['total_responses']} responses\n"
    summary += f"*Fallback rate:* {stats['fallback_responses']}/{stats['total_responses']} ({(stats['fallback_responses']/max(stats['total_responses'],1)*100):.0f}% couldn't answer)\n"
    summary += f"*Decisions:* {stats['decisions_captured']} captured, {stats['decisions_closed']} closed\n"
    summary += f"*Feedback:* {total_feedback} total ({new_feedback} new), {thumbs_down} 👎 reactions\n\n"

    if top_questions:
        summary += "*Most asked topics:*\n"
        for topic, count in top_questions:
            summary += f"  • {topic}: {count}x\n"
        summary += "\n"

    if recent_unanswered:
        summary += "*Recent questions I couldn't answer:*\n"
        for q in recent_unanswered:
            summary += f"  • \"{q['question'][:80]}\" ({q['user']}, {q['timestamp'][:10]})\n"
        summary += "\n"

    if new_feedback:
        summary += f"*New feedback ({new_feedback}):*\n"
        for f in data['explicit_feedback']:
            if f['status'] == 'new':
                summary += f"  • \"{f['feedback'][:100]}\" — {f['user']}\n"

    return summary


def update_learnings(data):
    """Update the learnings markdown file with patterns and improvements needed."""
    learnings = "# Cycle Bot Learnings\n\n"
    learnings += f"> Last updated: {datetime.now().strftime('%Y-%m-%d %I:%M%p ET')}\n\n"
    learnings += "This file tracks what Cycle Bot is learning from team interactions.\n"
    learnings += "Use this to improve responses and add new capabilities.\n\n"
    learnings += "---\n\n"

    # Explicit feedback
    learnings += "## Explicit Feedback\n\n"
    if data['explicit_feedback']:
        for f in data['explicit_feedback'][-20:]:  # Last 20
            status_icon = "🆕" if f['status'] == 'new' else "✅"
            learnings += f"- {status_icon} [{f['timestamp'][:10]}] {f['user']}: \"{f['feedback']}\"\n"
    else:
        learnings += "_No feedback yet._\n"
    learnings += "\n"

    # Unanswered questions (gaps in knowledge)
    learnings += "## Knowledge Gaps (Questions I Couldn't Answer)\n\n"
    if data['unanswered_questions']:
        for q in data['unanswered_questions'][-15:]:
            learnings += f"- [{q['timestamp'][:10]}] {q['user']}: \"{q['question'][:100]}\"\n"
    else:
        learnings += "_None yet — answering everything so far._\n"
    learnings += "\n"

    # Repeated questions (popular topics)
    learnings += "## Popular Topics (Most Asked)\n\n"
    top = sorted(data['repeated_questions'].items(), key=lambda x: x[1], reverse=True)
    if top:
        for topic, count in top[:10]:
            learnings += f"- **{topic}**: asked {count}x\n"
    else:
        learnings += "_No patterns yet._\n"
    learnings += "\n"

    # Thumbs down (bad responses)
    learnings += "## Responses That Missed (👎 Reactions)\n\n"
    if data['thumbs_down']:
        for td in data['thumbs_down'][-10:]:
            q = td.get('original_question', 'unknown')
            learnings += f"- [{td['timestamp'][:10]}] {td['user']} — question: \"{q[:80]}\"\n"
    else:
        learnings += "_No negative reactions yet._\n"
    learnings += "\n"

    # Stats
    learnings += "## Stats\n\n"
    stats = data['interaction_stats']
    learnings += f"| Metric | Value |\n|--------|-------|\n"
    learnings += f"| Total mentions | {stats['total_mentions']} |\n"
    learnings += f"| Total responses | {stats['total_responses']} |\n"
    learnings += f"| Fallback (couldn't answer) | {stats['fallback_responses']} |\n"
    learnings += f"| Fallback rate | {(stats['fallback_responses']/max(stats['total_responses'],1)*100):.0f}% |\n"
    learnings += f"| Decisions captured | {stats['decisions_captured']} |\n"
    learnings += f"| Decisions closed | {stats['decisions_closed']} |\n"

    LEARNINGS_FILE.write_text(learnings)


def mark_feedback_addressed(index):
    """Mark a piece of feedback as addressed."""
    data = load_feedback()
    if 0 <= index < len(data['explicit_feedback']):
        data['explicit_feedback'][index]['status'] = 'addressed'
        save_feedback(data)
        update_learnings(data)
