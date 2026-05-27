# Key Decisions Log

> This file tracks key decisions for the Bills & Subscription Management project.
> Decisions flow through a lifecycle: **OPEN → discussed in Slack → DRI approves → CLOSED → PRD updated.**
>
> - 🔓 OPEN = Needs team discussion and DRI (Michael Duane) approval
> - ✅ CLOSED = Decided, reflected in PRD
>
> The daily Slack bot posts all OPEN decisions every weekday at 9am for follow-up.
> Only Michael Duane (@michaelduane) can close a decision.

---

## Open Decisions

### 2026-05-27 — Cycle 2 MVP Scope

**Context:** The full vision has three layers (Hub + Knot Linking, Management Actions, Bill-Specific Auto-Reload). We need to decide what ships in Cycle 2's 6-week window.

**Options considered:**
- Option A: Hub + Knot Linking only (visibility + consolidation)
- Option B: Hub + Knot Linking + Management Actions (recommended)
- Option C: Hub + Knot + Management + Bill-Specific Auto-Reload (full vision)

**Decision:** TBD (pending kickoff discussion Monday)

**Opened by:** Michael Duane, Trevor Luong

**Status:** 🔓 OPEN

---

### 2026-05-27 — Detection Strategy for V1

**Context:** How do we identify a customer's recurring bills at launch? Options range from analyzing Cash Card transaction patterns (limited to what's already on the card) to Knot-powered detection (broader but requires linking) to a hybrid approach.

**Options considered:**
- Cash Card transaction pattern matching only
- Knot-powered detection (requires customer to link accounts)
- Hybrid: pattern matching + Knot enhancement + manual add

**Decision:** TBD

**Opened by:** Michael Duane

**Status:** 🔓 OPEN

---

### 2026-05-27 — Empty State Strategy

**Context:** Design feedback rated the empty/cold-start problem as 10/10 criticality. Most customers will see partial or no detection at launch. How do we handle this without losing them on first impression?

**Options considered:**
- Lead with Knot linking as primary path (requires action before value)
- Show partial detection + "add more" prompt (lower friction)
- Common subscription logos as quick-add buttons (visual, fast)
- Combination approach

**Decision:** TBD

**Opened by:** Michael Duane (from design feedback review)

**Status:** 🔓 OPEN

---

## Closed Decisions

### 2026-05-27 — PRD Structure and Roles

**Context:** Needed to establish project roles and PRD format before kickoff.

**Decision:** Michael Duane is overall DRI. Trevor Luong is PM DRI. PRD lives in GitHub as source of truth with Google Doc as readable companion. Three scope options presented for kickoff.

**Rationale:** Clear ownership separation — Michael owns strategy and final decisions, Trevor owns day-to-day product execution.

**Approved by:** Michael Duane (DRI)

**Closed:** 2026-05-27

**Status:** ✅ CLOSED

---

*Decisions are added automatically from Slack discussions. The daily bot will ping open decisions every weekday at 9am.*
