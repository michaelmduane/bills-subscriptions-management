# Project Notes

> Ongoing notes, observations, and discussion points for Bills & Subscription Management.
> Synced from Slack and other coordination tools.

---

## 2026-05-27 — Project Setup

### Context
- PRD drafted based on: Figma designs, design feedback doc (Moneybot transcript analysis), Payment Success doc, customer research (2022), Knot API capabilities
- Key insight from design feedback: empty state is the #1 risk (rated 10/10 criticality) — most customers will see partial or no detection at launch
- Key insight from Payment Success doc: recurring/merchant-initiated transactions have 2x+ higher decline rates — bill-specific auto-reload directly addresses this

### Open Items for Kickoff
- [ ] Decide MVP scope (Option A/B/C)
- [ ] Confirm Knot integration timeline and merchant coverage for our customer base
- [ ] Align on detection strategy: Cash Card transaction patterns vs. Knot-powered vs. both
- [ ] Discuss empty-state design approach
- [ ] Define success metrics targets (recurring GPV per customer baseline + target)
- [ ] Identify any legal/compliance review needs for Knot card-switching

### Design Feedback Highlights (from Moneybot analysis)
1. Empty state will make or break this feature (10/10)
2. Consider hybrid entry: partial detection + prompt to add (8/10)
3. Linking should enhance detection, not gate it (7/10)
4. "Am I covered?" is the strongest unaddressed emotional need (7/10)
5. Connect cancel → save flow; show monthly total (7/10)
6. Be transparent about what Cash App can vs. can't do (6/10)

---

*More notes will be added as the project progresses.*
