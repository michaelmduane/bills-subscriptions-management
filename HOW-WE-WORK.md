# How We Work

> This file explains the project mechanics, workflows, and automation for Bills & Subscription Management.
> If you're new to the project, start here.

---

## Team

| Role | Person | Slack |
|------|--------|-------|
| DRI (overall) | Michael Duane | @michaelduane |
| PM | Trevor Luong | @trevorluong |
| Eng Lead | Megan Tong | @megantong |
| Design Lead | Gustavo | @gbalestraci |

---

## Where Things Live

| What | Where | Purpose |
|------|-------|---------|
| **GitHub repo** | [michaelmduane/bills-subscriptions-management](https://github.com/michaelmduane/bills-subscriptions-management) | Source of truth for all project documentation |
| **Google Doc** | [Bills & Subscription Management PRD](https://docs.google.com/document/d/1HFQI0EEDLRI-xPKDc_L2BPADH1731zPiKELZIw3t790/edit) | Readable companion (5 tabs) |
| **Figma** | [Bills & Subscriptions Manager](https://www.figma.com/design/gSiPlvN2nIjAMVtMysu345/Bills---Subscriptions-Manager?node-id=3-3) | Design source of truth |
| **Slack channel** | [#cycle-2-bills-subscriptions](https://square.enterprise.slack.com/archives/C0B6KN2RPLZ) | Status updates, decisions, discussion |

### GitHub Repo Structure

```
bills-subscriptions-management/
├── README.md              # Project overview and key links
├── PRD.md                 # Product Requirements Document (canonical)
├── DECISIONS.md           # Decision log (open + closed)
├── NOTES.md               # Project notes (synced from Slack)
├── HOW-WE-WORK.md         # This file — project mechanics
└── docs/
    ├── scope-options.md   # Cycle 2 scope options (A/B/C)
    ├── weekly-reviews.md  # Weekly execution review agendas
    └── delivery-review.md # Retro + delivery review structure
```

### Google Doc Tabs

| Tab | Content |
|-----|---------|
| PRD (readable format) | The full PRD, formatted for easy reading |
| Cycle 2 Scope | The three scope options for kickoff |
| Risk Register | All 14 risks with scores and mitigations |
| Weekly Reviews | Execution review agendas for all 6 weeks |
| Delivery Review | Retro questions + org-wide presentation format |

---

## Source of Truth Rules

1. **GitHub is canonical.** If GitHub and the Google Doc conflict, GitHub wins.
2. **Google Doc is for reading and light editing.** Edits made in the Doc are synced to GitHub hourly.
3. **Slack is for discussion.** Decisions and notes from Slack are captured in GitHub automatically.
4. **PRD is updated by closed decisions.** When a decision closes, the PRD is surgically updated to reflect it.

---

## Agent Automation

An AI agent (Goose) runs two scheduled automations for this project:

### 1. Hourly Sync (every hour, on the hour)

**What it does:**
- Reads new messages from the Slack channel (last hour)
- Categorizes them as decisions or notes
- Updates `DECISIONS.md` and `NOTES.md` in GitHub
- Checks the Google Doc for edits and syncs to GitHub
- If a decision is closed, updates `PRD.md` accordingly
- Pushes changes back to the Google Doc

**What triggers a new decision entry:**
- Someone says "decision:", "we need to decide", "open question:", "proposal:"
- Someone raises a question that clearly requires team alignment
- A meeting outcome includes a choice that needs confirmation

**What triggers a decision closing:**
- Michael Duane (@michaelduane) responds with approval language: "approved", "let's go with", "confirmed", "yes ship it", "agreed", "+1 let's do it"
- Michael reacts with ✅ to a decision thread

### 2. Monday Status Check (8am PT, Mondays)

**What it does:**
- Posts a status check message to the Slack channel
- Tags each functional DRI by name: Eng (@megantong), PM (@trevorluong), Design (@gbalestraci)
- Asks each to reply in-thread with green/yellow/red + one sentence update
- Replies are picked up by the hourly sync and captured in NOTES.md

### 3. Daily Decisions Bot (9am PT, weekdays)

**What it does:**
- Reads `DECISIONS.md` for all OPEN decisions
- Posts a summary to the Slack channel listing each open decision
- Flags decisions open 3+ days with a ⚠️ warning
- Reminds the team that @michaelduane confirms to close

**What it looks like in Slack:**
```
🔓 Open Decisions — Bills & Subscription Management

There are 3 decisions waiting for alignment:

1. Cycle 2 MVP Scope (opened May 27)
   > Which option (A/B/C) do we commit to for the 6-week cycle?

2. Detection Strategy for V1 (opened May 27)
   > Transaction patterns vs. Knot-powered vs. hybrid?

3. Empty State Strategy (opened May 27)
   > How do we handle cold start without losing customers on first impression?

---
To close: discuss in thread, then @michaelduane confirms.
```

---

## Decision Lifecycle

```
Slack discussion or meeting
    ↓
Decision identified → DECISIONS.md (🔓 OPEN)
    ↓
Daily bot pings Slack with all open decisions
    ↓
Team discusses in Slack thread
    ↓
DRI (Michael Duane) confirms
    ↓
Hourly sync detects closure → DECISIONS.md (✅ CLOSED)
    ↓
PRD.md auto-updated with decision outcome
    ↓
Google Doc synced from GitHub
```

### Rules

- **Only Michael Duane (DRI) can close decisions.** If someone else says "let's do X" but Michael hasn't confirmed, it stays OPEN.
- **Anyone can open a decision.** Just say "decision:" or "open question:" in Slack.
- **Decisions should be specific and closable.** "What should we do about X?" is good. "We should think about X" is a note, not a decision.

---

## Weekly Execution Reviews

**When:** Every Monday for 6 weeks (June 2 – July 7, 2026)
**Duration:** 30 minutes
**Format:** Status-driven (Red → Yellow → Green)

### Rhythm

| When | Who | What |
|------|-----|------|
| **Monday 8am PT** | Agent | Posts status check, tags each DRI |
| **Monday morning** | Eng, PM, Design | Reply in thread with 🟢/🟡/🔴 + 1 sentence |
| **Monday meeting** | Full squad | Review status, unblock, decide |
| **After meeting** | Anyone | Post notes/decisions to Slack |
| **Hourly** | Agent | Syncs Slack → GitHub → Google Doc |

### Status Definitions

| Status | Meaning |
|--------|---------|
| 🟢 Green | On track to hit the cycle goal |
| 🟡 Yellow | At risk — something is trending wrong |
| 🔴 Red | Blocked — needs leadership intervention |

> Blank = Yellow. When in doubt, show more risk, not less.

### Meeting Tab in Google Doc

Use the "Weekly Reviews" tab to:
- **Before:** Check the agenda for that week's focus areas
- **During:** Take live notes in the Status History table
- **After:** Post decisions/notes in Slack — agent captures them automatically

---

## Delivery Review (End of Cycle)

**When:** Off-week, July 14-17, 2026
**Format:** Two parts

1. **Squad Retro (internal)** — Honest assessment of what worked, what didn't, what to change
2. **Delivery Review (org-wide)** — 5-minute DRI presentation to Eng Staff: outcomes vs. goals, key learnings, what changes next cycle

See `docs/delivery-review.md` for the full structure and templates.

---

## How to Interact with the Agent

The agent monitors the Slack channel passively. You don't need to @mention it or use special commands. Just discuss naturally and:

- **To open a decision:** Say "decision:" or "open question:" or "proposal:" in the channel
- **To close a decision:** Michael responds with "approved" / "confirmed" / "let's go with X" / ✅
- **To add a note:** Just post an update, link, or summary — it'll be captured in NOTES.md
- **To check status:** Look at DECISIONS.md in GitHub or wait for the daily bot post

The agent will never post to Slack on its own except for the daily decisions summary. It operates silently in the background, keeping GitHub in sync.

---

## Quick Reference

| I want to... | Do this |
|--------------|---------|
| Read the PRD | Open the Google Doc (PRD tab) or `PRD.md` in GitHub |
| See open decisions | Check `DECISIONS.md` or wait for the daily Slack post |
| Raise a new decision | Post "decision: [question]" in Slack |
| Close a decision | Michael responds with approval in the Slack thread |
| Add project notes | Post in Slack — agent captures automatically |
| Check weekly agenda | Google Doc (Weekly Reviews tab) or `docs/weekly-reviews.md` |
| See the scope options | Google Doc (Cycle 2 Scope tab) or `docs/scope-options.md` |
| Review risks | Google Doc (Risk Register tab) or the Risks section of `PRD.md` |
| Understand the retro format | `docs/delivery-review.md` |
