# Cycle Bot

Real-time Slack bot for Bills & Subscription Management project coordination.

## Setup

1. **Install dependencies:**
   ```
   pip3 install -r requirements.txt
   ```

2. **Get tokens:**
   - `SLACK_BOT_TOKEN` (xoxb-...): From Slack App → OAuth & Permissions → Bot User OAuth Token
   - `SLACK_APP_TOKEN` (xapp-...): From Slack App → Basic Information → App-Level Tokens
     - Generate one with `connections:write` scope

3. **Enable Socket Mode:**
   - Go to Slack App → Socket Mode → Toggle ON

4. **Enable Event Subscriptions:**
   - Go to Slack App → Event Subscriptions → Toggle ON
   - Subscribe to bot events: `app_mention`, `message.channels`, `reaction_added`

5. **Run:**
   ```
   export SLACK_BOT_TOKEN="xoxb-..."
   export SLACK_APP_TOKEN="xapp-..."
   python3 cycle_bot.py
   ```

## What it does

- **Instant responses** to @Cycle Bot mentions (decisions, scope, risks, status, team, etc.)
- **Decision capture** — detects "decision:" messages, logs to DECISIONS.md, confirms in-thread
- **Decision closure** — detects DRI approval in threads, updates docs
- **Full project context** — reads from all GitHub repo files to answer questions
- **Feedback & learning** — tracks unanswered questions, explicit feedback, and 👎 reactions

## Feedback system

Cycle Bot learns from interactions:

- **Explicit feedback:** Say "feedback: [your thought]" to tell the bot what to improve
- **Thumbs down:** React 👎 to a bad response — it's logged for review
- **Knowledge gaps:** Questions the bot can't answer are tracked in `learnings.md`
- **Weekly digest:** Every Friday, the bot posts a self-assessment with stats and gaps
- **Feedback summary:** Ask "@Cycle Bot feedback summary" to see the full report anytime

## Running as a background service

```
nohup python3 cycle_bot.py > /tmp/cycle-bot.log 2>&1 &
```

Or use launchd for persistence across reboots (see bot/com.cyclebot.plist).
