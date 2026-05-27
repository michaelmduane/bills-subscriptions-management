# Bills & Subscription Management: Scope Options

> For Cycle 2 Kickoff Discussion
> Team: Michael Duane (PM), Megan Tong (Eng), Gustavo (Design)

---

## Context

We have 6 weeks in Cycle 2 (June 1 – Jul 10) to build and internally test the Bills & Subscription Management feature. The full vision has three layers. We need to decide which layers ship in Cycle 2 vs. later cycles.

**North star metric:** Recurring card GPV per customer

**Strategic goal:** Make Cash App the place customers consolidate their recurring payments, driving funding and primary bank behavior.

---

## Option A: Hub + Knot Linking

*Visibility + Consolidation Only*

### What ships:
- Bills hub UI (accessible from Card tab + Money tab)
- Detection of recurring charges from Cash Card transaction history
- Knot CardSwitcher integration — move bills from other cards to Cash App Card
- Basic actions: view details, dismiss, add manually

### What does NOT ship:
- No management actions (no pause/cancel/change plan)
- No bill-specific auto-reload
- No post-cancellation monitoring

### Pros:
- Smallest scope — highest confidence of shipping in 6 weeks
- Proves the consolidation thesis (do customers switch bills to Cash App Card?)
- Knot CardSwitcher is their most mature product

### Cons:
- Read-only dashboard risk — customers can see bills but cannot act on them
- Design feedback explicitly warns against this (empty/passive experience)
- May not generate enough engagement to measure impact on recurring GPV

### Effort estimate: ~4 weeks build + 2 weeks QA/dogfood

---

## Option B: Hub + Knot Linking + Management Actions ⭐ RECOMMENDED

*Visibility + Consolidation + Control*

### What ships:
- Everything in Option A, plus:
- Knot SubscriptionManager integration — pause, cancel, change plan in-app
- Post-cancellation monitoring (alert if merchant charges again after cancel)
- Detail pages with full management UI
- Clear distinction between Knot-supported (full management) vs. other merchants (limited)

### What does NOT ship:
- No bill-specific auto-reload (Cycle 3)
- No coverage check / "Am I covered?" (Cycle 3)
- No proactive notifications (Cycle 3)

### Pros:
- Customers can act, not just observe — addresses the #1 design feedback concern
- Differentiates from Apple Wallet (visibility only) and matches Rocket Money (management)
- Card-switching + management = complete consolidation story
- Management actions build trust and engagement

### Cons:
- Broader Knot integration surface (SubscriptionManager + CardSwitcher)
- More edge cases: failed cancellations, partial support, merchant-specific quirks
- 6 weeks is tight for both integrations + hub UI + QA

### Effort estimate: ~5 weeks build + 1 week QA/dogfood (tight)

### Key question for eng: Is the Knot SubscriptionManager integration feasible in this timeline alongside CardSwitcher?

---

## Option C: Hub + Knot + Management + Bill-Specific Auto-Reload

*Full Vision — Visibility + Consolidation + Control + Funding*

### What ships:
- Everything in Option B, plus:
- Bill-specific auto-reload (per-bill funding triggers from linked debit)
- Coverage check: "You have 3 bills totaling $47 due this week. Balance: $62. ✅ You're covered."
- Proactive push notifications (low balance warning before bill)

### What does NOT ship:
- Moneybot integration
- Savings connection (cancel → save flow)
- Lending layer

### Pros:
- Complete value loop: see → manage → fund → succeed
- Directly addresses the 2x decline rate problem for recurring charges
- "Am I covered?" is the strongest unaddressed emotional need (design feedback 7/10)
- Maximum impact on recurring GPV and payment success

### Cons:
- Very large scope for 6 weeks — high risk of not shipping
- Bill-specific auto-reload is a new funding primitive (payments infra dependency)
- Interactions with existing auto-reload need careful design
- More QA surface, more edge cases, more support scenarios

### Effort estimate: ~7-8 weeks (exceeds Cycle 2)

---

## Recommendation

**Ship Option B in Cycle 2. Ship Option C's auto-reload as the first Cycle 3 deliverable.**

Rationale:
1. Option A is too passive — design feedback explicitly warns that a read-only dashboard will fail
2. Option B gives customers a reason to engage (management actions) and a reason to consolidate (card-switching)
3. Option C is the right end-state but exceeds 6 weeks; auto-reload is a clean Cycle 3 addition
4. Option B can ship to internal dogfood by week 5, giving 1 week for iteration before Cycle 2 ends

---

## Decision Needed at Kickoff

1. Which option do we commit to for Cycle 2?
2. If Option B: Is the Knot SubscriptionManager integration timeline feasible?
3. What is our detection strategy for V1? (Cash Card patterns vs. Knot-powered vs. both)
4. What does "done" look like at the end of Cycle 2? (Internal dogfood? Gated pilot? Broader?)
5. Who owns the Knot partnership relationship and integration timeline?
