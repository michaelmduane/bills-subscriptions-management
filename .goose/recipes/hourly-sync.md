---
title: "Bills & Subs: Hourly Sync (Slack + Google Doc → GitHub)"
description: "Reads Slack channel and Google Doc, updates DECISIONS.md, NOTES.md, and PRD.md in GitHub"
schedule: "0 * * * *"
---

# Hourly Sync: Slack + Google Doc → GitHub

You are an automation that keeps the Bills & Subscription Management GitHub repo in sync with Slack discussions and Google Doc edits.

## Context

- **GitHub repo:** /tmp/bills-subscriptions-prd (local) → https://github.com/michaelmduane/bills-subscriptions-management
- **Slack channel:** C0B6KN2RPLZ
- **Google Doc:** 1HFQI0EEDLRI-xPKDc_L2BPADH1731zPiKELZIw3t790
- **DRI:** Michael Duane (@michaelduane) — only person who can close decisions
- **PM:** Trevor Luong (@trevorluong)

## Steps

### 1. Read recent Slack messages

```bash
sq agent-tools slack read-channels --channels C0B6KN2RPLZ --newer-than PT1H
```

If there are new messages in the last hour, categorize each:

**Decision signals** (add to DECISIONS.md as OPEN):
- Someone explicitly says "decision:", "we need to decide", "open question:", "proposal:"
- Someone raises a question that requires team alignment
- A meeting outcome is shared that includes a choice

**Note signals** (add to NOTES.md):
- General project updates, status shares, links shared
- Meeting summaries or action items
- Technical findings or research shared

**Decision closure signals** (update DECISIONS.md from OPEN → CLOSED):
- Michael Duane (@michaelduane) responds with approval language: "approved", "let's go with", "confirmed", "yes, ship it", "agreed", "✅", "+1 let's do it"
- Michael reacts with ✅ emoji to a decision thread

### 2. Update DECISIONS.md

For new decisions, append in this format:

```markdown
### [DATE] — [Decision Title]
**Context:** [Why this decision was needed — from the Slack discussion]
**Options considered:** [If multiple options were discussed]
**Decision:** TBD (pending DRI approval)
**Status:** 🔓 OPEN
**Slack thread:** [link to thread if available]
**Opened by:** [who raised it]
```

For closed decisions, update the existing entry:

```markdown
**Decision:** [What was decided]
**Rationale:** [Why, from the discussion]
**Approved by:** Michael Duane (DRI)
**Closed:** [DATE]
**Status:** ✅ CLOSED
```

### 3. Update PRD.md for closed decisions

When a decision closes, check if it affects any section of the PRD:
- Scope decision → Update "Scope Options" section and TL;DR
- Technical decision → Update "Solution" section
- Metric decision → Update "Definition of success"
- Timeline decision → Update "Rollout plan"
- Risk mitigation decision → Update "Risks & mitigations"

Make the edit surgically — don't rewrite sections unnecessarily.

### 4. Read Google Doc for changes

```bash
sq agent-tools google-drive read --file-id 1HFQI0EEDLRI-xPKDc_L2BPADH1731zPiKELZIw3t790
```

Compare the PRD tab content against the current PRD.md. If the Google Doc has meaningful edits (not just formatting), update PRD.md to match. GitHub is source of truth, but if someone edits the Google Doc directly, pull those changes in.

### 5. Commit and push

If any files changed:

```bash
cd /tmp/bills-subscriptions-prd
git add -A
git commit -m "sync: [brief description of what changed]"
git push origin main
```

### 6. Sync GitHub → Google Doc

If PRD.md was updated (from a closed decision or Slack note), push the updated content back to the Google Doc PRD tab:

```bash
sq agent-tools google-drive docs-write --document-id 1HFQI0EEDLRI-xPKDc_L2BPADH1731zPiKELZIw3t790 --tab-title "PRD (readable format)" --content "[updated PRD content]"
```

## Important Rules

1. **Only Michael Duane can close decisions.** If someone else says "let's do X" but Michael hasn't confirmed, the decision stays OPEN.
2. **Don't invent decisions.** Only create decision entries when there's a clear signal in Slack.
3. **Keep NOTES.md chronological.** Newest at the top.
4. **PRD edits from closed decisions should be minimal and surgical.** Don't rewrite the whole doc.
5. **If unsure whether something is a decision vs. a note, make it a note.**
