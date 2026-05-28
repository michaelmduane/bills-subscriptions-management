# Key Decisions Log

> This file is the comprehensive source of truth for all decisions on the Bills & Subscription Management project.
> Every decision includes full context, timestamps, conversation references, and resolution history.
>
> **Lifecycle:** OPEN → discussed in Slack → DRI approves → CLOSED → PRD updated
>
> - 🔓 OPEN = Needs team discussion and DRI (Michael Duane) approval
> - ✅ CLOSED = Decided, reflected in PRD
>
> **Rules:**
> - Only Michael Duane (@michaelduane) can close a decision
> - Every decision must link back to the Slack thread(s) where it was discussed
> - Timestamps use ET and follow ISO format where possible
> - The daily Slack bot posts all OPEN decisions every weekday at 9am PT

---

## Open Decisions

### DEC-005 — Feature Access: Card Customers Only or Broader?

| Field | Value |
|-------|-------|
| **Opened** | 2026-05-27 5:16pm ET |
| **Opened by** | Michael Duane (DRI) |
| **Priority** | High — affects addressable market and eng scope |
| **Target close** | Monday June 2 (kickoff) |
| **Status** | 🔓 OPEN |

**Context:** Bills & Subscription Management could be scoped to Cash App Card customers only (since it's a Card feature managing card-based payments), or it could be made available to a broader set of Cash App users (e.g., anyone with a linked debit or direct deposit). This affects addressable market, complexity, and positioning.

**Options considered:**
- Card customers only (tightest scope, clearest value prop)
- Card + Direct Deposit customers (broader, but still funded accounts)
- All Cash App users (broadest reach, but may not have card-based payments to manage)

**Decision:** TBD (pending DRI approval)

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 5:16pm ET | Michael Duane | Raised decision in Slack | [thread](https://sq-block.slack.com/archives/C0B6KN2RPLZ/p1779916566268059) |
| 2026-05-27 5:17pm ET | Cycle Bot | Acknowledged, logged to DECISIONS.md | [reply](https://sq-block.slack.com/archives/C0B6KN2RPLZ/p1779916566268059) |

---

### DEC-004 — Cycle 2 MVP Scope

| Field | Value |
|-------|-------|
| **Opened** | 2026-05-27 12:00pm ET |
| **Opened by** | Michael Duane (DRI), Trevor Luong (PM) |
| **Priority** | Critical — defines the entire cycle's deliverable |
| **Target close** | Monday June 2 (kickoff) |
| **Status** | 🔓 OPEN |

**Context:** The full vision has three layers (Hub + Knot Linking, Management Actions, Bill-Specific Auto-Reload). We need to decide what ships in Cycle 2's 6-week window.

**Options considered:**
- Option A: Hub + Knot Linking only (visibility + consolidation) — ~4 weeks eng
- Option B: Hub + Knot Linking + Management Actions (recommended) — ~5-6 weeks eng
- Option C: Hub + Knot + Management + Bill-Specific Auto-Reload (full vision) — ~8+ weeks eng

**Decision:** TBD (pending kickoff discussion Monday)

**Related docs:**
- [Scope Options doc](https://github.com/michaelmduane/bills-subscriptions-management/blob/main/docs/scope-options.md)
- [Google Doc — Cycle 2 Scope tab](https://docs.google.com/document/d/1HFQI0EEDLRI-xPKDc_L2BPADH1731zPiKELZIw3t790/edit)

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 12:00pm ET | Michael Duane | Created scope options during PRD build | — |
| 2026-05-27 5:16pm ET | Cycle Bot | Posted to Slack channel with pre-read links | [welcome post](https://sq-block.slack.com/archives/C0B6KN2RPLZ/p1779918677471129) |

---

### DEC-003 — Detection Strategy for V1

| Field | Value |
|-------|-------|
| **Opened** | 2026-05-27 12:00pm ET |
| **Opened by** | Michael Duane (DRI) |
| **Priority** | High — determines technical architecture |
| **Target close** | Monday June 2 or Week 2 (June 9) |
| **Status** | 🔓 OPEN |

**Context:** How do we identify a customer's recurring bills at launch? Options range from analyzing Cash Card transaction patterns (limited to what's already on the card) to Knot-powered detection (broader but requires linking) to a hybrid approach.

**Options considered:**
- Cash Card transaction pattern matching only (fast, limited coverage)
- Knot-powered detection (requires customer to link, broader coverage)
- Hybrid: pattern matching + Knot enhancement + manual add (most complete, most complex)

**Decision:** TBD

**Key considerations:**
- Transaction pattern matching can identify ~60-70% of recurring charges already on the card
- Knot covers 15,000+ merchants but requires customer action to link
- Hybrid gives best UX but highest eng complexity
- This decision is tightly coupled to the empty state decision (DEC-002)

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 12:00pm ET | Michael Duane | Identified during PRD creation | — |

---

### DEC-002 — Empty State Strategy

| Field | Value |
|-------|-------|
| **Opened** | 2026-05-27 12:00pm ET |
| **Opened by** | Michael Duane (DRI), from design feedback review |
| **Priority** | Critical — rated 10/10 by design review |
| **Target close** | Monday June 2 or Week 2 (June 9) |
| **Status** | 🔓 OPEN |

**Context:** Design feedback rated the empty/cold-start problem as 10/10 criticality. Most customers will see partial or no detection at launch. How do we handle this without losing them on first impression?

**Options considered:**
- Lead with Knot linking as primary path (requires action before value)
- Show partial detection + "add more" prompt (lower friction)
- Common subscription logos as quick-add buttons (visual, fast)
- Combination approach

**Decision:** TBD

**Key considerations:**
- First impression determines whether customers engage or bounce
- Research shows customers track bills offline (spreadsheets, notes) — any visibility is better than none
- Knot linking requires trust; customers may not want to card-switch immediately
- The NUX screenshots show several approaches (see Figma)

**Related docs:**
- [Figma — NUX states](https://www.figma.com/design/gSiPlvN2nIjAMVtMysu345/Bills---Subscriptions-Manager?node-id=3-3)
- [Design feedback doc](https://docs.google.com/document/d/1QwftardXlA1e8wWiMuyWfhvZu9uyc4JuupCVGDwAbWE/edit)

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 12:00pm ET | Michael Duane | Identified from design feedback review | — |

---

## Closed Decisions

### DEC-001 — PRD Structure and Roles

| Field | Value |
|-------|-------|
| **Opened** | 2026-05-27 10:00am ET |
| **Closed** | 2026-05-27 12:00pm ET |
| **Opened by** | Michael Duane (DRI) |
| **Approved by** | Michael Duane (DRI) |
| **Status** | ✅ CLOSED |

**Context:** Needed to establish project roles and PRD format before kickoff.

**Decision:** Michael Duane is overall DRI. Trevor Luong is PM DRI. PRD lives in GitHub as source of truth with Google Doc as readable companion. Three scope options presented for kickoff.

**Rationale:** Clear ownership separation — Michael owns strategy and final decisions, Trevor owns day-to-day product execution.

**Impact on PRD:** Updated frontmatter with roles, established repo structure, created all project docs.

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 10:00am ET | Michael Duane | Discussed roles and structure in Goose session | — |
| 2026-05-27 12:00pm ET | Michael Duane | Confirmed structure and roles | — |

---

## Decision Template

When adding a new decision, use this format:

```markdown
### DEC-[NNN] — [Decision Title]

| Field | Value |
|-------|-------|
| **Opened** | [YYYY-MM-DD H:MMam/pm ET] |
| **Opened by** | [Name (role)] |
| **Priority** | [Critical / High / Medium / Low] — [one line why] |
| **Target close** | [Date or meeting] |
| **Status** | 🔓 OPEN |

**Context:** [Why this decision is needed — 2-3 sentences]

**Options considered:**
- [Option 1]
- [Option 2]
- [Option 3]

**Decision:** TBD

**Key considerations:**
- [Important factor 1]
- [Important factor 2]

**Related docs:**
- [Link to relevant doc/design/data]

**Conversation history:**
| When | Who | What | Link |
|------|-----|------|------|
| [timestamp] | [person] | [what happened] | [slack link] |
```

---

*Decisions are captured automatically from Slack by Cycle Bot. The daily bot posts open decisions every weekday at 9am PT.*
### DEC-006 — North Star Metric for Bills & Subscription Management

| Field | Value |
|-------|-------|
| Opened | 2026-05-27 |
| Closed | 2026-05-28 |
| Owner | Michael Duane (DRI) |
| Priority | High |
| Status | ✅ CLOSED |

**Context:** We needed to confirm the primary success metric for this workstream to ensure all feature decisions align.

**Options considered:**
- Recurring card GPV per customer (monthly)
- Number of bills consolidated
- Payment success rate improvement
- Customer retention / churn reduction

**Decision:** Recurring card GPV per customer (monthly) is the north star.

**Rationale:** This is the most comprehensive metric — it captures both consolidation (more recurring txns on Card) and funding success (fewer declines). Every feature lever (Knot linking, auto-reload, hub visibility) flows through this single metric.

**Baseline:** $38.94/mo per recurring-active customer (1.3 settled recurring txns/mo)

**Conversation history:**

| Date | Who | What | Link |
|------|-----|------|------|
| 2026-05-27 | Michael Duane | Raised metric goals as open decision | Slack |
| 2026-05-28 | Michael Duane | "Let's use recurring GPV as the primary goal" | [Thread](https://sq-block.slack.com/archives/C0B6KN2RPLZ/p1779983264686979) |

---

*Next decision number: DEC-007*
