---
title: Bills & Subscription Management
status: draft
author: "@trevorluong"
dri: "@michaelduane"
reviewers:
  - Megan Tong (Eng lead)
  - Gustavo (Design lead)
  - TBD Data lead
  - TBD Legal/Compliance lead
created: 2026-05-27
updated: 2026-05-27
linear: TBD
blueprint: TBD
target_launch: Cycle 2 pilot (June 1 – Jul 10, 2026)
tags: [cash-app-card, bills, subscriptions, recurring, knot, auto-reload, consolidation, primary-bank]
---

# Bills & Subscription Management PRD

## TL;DR

Build a bills and subscription management hub inside Cash App that gives Card customers a single place to see, consolidate, and manage all their recurring card-based payments. The feature uses Knot-powered card-switching to let customers move existing subscriptions and bills onto their Cash App Card with a few taps, and offers management actions (pause, cancel, change plan) directly inside the app. A new bill-specific auto-reload capability ensures customers always have enough funds to cover upcoming charges, reducing declines and building trust that Cash App is their primary account.

The strategic thesis is straightforward: customers who consolidate recurring payments onto Cash App Card will fund their accounts more consistently, experience fewer declines, and generate meaningfully higher recurring card GPV — the strongest leading indicator of primary bank behavior.

The MVP scope is TBD pending the Cycle 2 kickoff (see [Scope Options](#scope-options) below). This PRD outlines the full vision and proposes three phased scope options for team alignment.

## Problem

Cash App Card customers lack a unified view of their recurring financial obligations. Today:

- **No visibility into upcoming charges.** Without explicit linking, customers have no definitive view of upcoming bills inside Cash App or any financial institution. They're forced to check each biller's website/app and often track recurring transactions offline through notes, spreadsheets, or mental accounting.

- **High recurring payment failure rates.** Merchant-initiated and recurring transactions have 2x+ higher decline rates than customer-initiated purchases. Across the Cash App Card portfolio, recurring/subscription declines represent a significant share of total declined volume — driven by insufficient funds, card expiration, and timing mismatches between bill dates and funding events.

- **Poor payment sequencing.** Customers pay for low-priority subscriptions (e.g., Netflix at $17.99) and then lack funds for high-priority bills (e.g., rent at $1,700). Without a tool that shows what's coming and when, customers can't sequence their spending intelligently.

- **No consolidation path.** Customers who want to move spending to Cash App Card must manually update their payment method with each biller — a high-friction process that most abandon partway through. The average US consumer has 6-12 recurring subscriptions across different providers.

- **Existing workarounds signal unmet need.** Customer research shows users locking/unlocking their cards to prevent unexpected charges, using third-party tools like Privacy.com for subscription control, and manually tracking bills in notes apps. Moneybot transcript analysis (May 2026) shows customers asking about subscriptions and recurring charges regularly, with most sessions ending in dead ends ("No recurring outflows detected").

## Users

- **Primary customer:** US Cash App Card holders with 2+ recurring card-based payments, particularly those with direct deposit or regular funding patterns who are on the path to using Cash App as a primary account.

- **Primary job-to-be-done:** "Help me see everything I'm paying for on a recurring basis, make sure I don't miss a payment, and give me control to change or cancel things I don't need anymore — all without leaving Cash App."

- **Secondary user segments:**
  - **New Card activators** who need a reason to move spending from their existing bank card
  - **Direct deposit customers** who already fund Cash App but still pay most bills from another account
  - **Cost-conscious customers** who want to identify and eliminate unnecessary subscriptions

- **Internal users:** Card product (PM: Trevor Luong), engineering, design, data, partnerships (Knot), and support teams.

## Hypothesis

We believe Cash App Card customers will consolidate recurring payments onto their Card if we reduce the friction of switching (via Knot) and provide ongoing value through visibility, management tools, and funding assurance (bill-specific auto-reload). We believe this consolidation will drive measurably higher recurring card GPV per customer, increased account funding, and improved payment success rates — reinforcing primary bank behavior.

## Solution

### Overview

A bills and subscription management hub accessible from the Card tab (Spend surface) and Money tab, with three core capabilities:

1. **Bills Hub** — A unified view of all detected and linked recurring payments, showing upcoming charges, amounts, due dates, payment history, and monthly totals.

2. **Knot-powered consolidation** — Card-switching integration that lets customers move existing subscriptions and bills from other payment methods to their Cash App Card, plus management actions (pause, cancel, change plan, update payment info) executed directly through Knot's merchant integrations.

3. **Bill-specific auto-reload** — A new auto-reload variant that triggers funding from a linked debit card specifically when an upcoming bill would exceed the customer's available balance, ensuring recurring payments succeed.

### Key flows

**Entry points:**
- Card tab → Spend surface (NUX prompt for new users, persistent hub for active users)
- Money tab → Bills section
- Push notifications (upcoming bill, low balance warning, price change alert)

**Hub states:**
- Empty (no bills detected) → Prompt to link via Knot or add manually
- Partial detection (1-3 found) → Show detected + prompt to add more
- Populated → Upcoming this month, paid this month, monthly total, manage section

**Detail page:**
- Individual bill/subscription view with: merchant, amount, frequency, next charge date, charge history, and available actions (manage via Knot, set up auto-reload, block, dismiss)

**Management actions (Knot-powered):**
- Switch payment method to Cash App Card
- Change subscription plan/tier
- Pause subscription
- Cancel subscription
- Post-cancellation monitoring (alert if merchant charges again)

**Bill-specific auto-reload:**
- Per-bill funding rules: "Auto-reload $X from [linked debit] 2 days before [bill] is due"
- Distinct from existing balance-based auto-reload (which remains unchanged)
- Coverage check: "You have 3 charges totaling $47 due this week. Your balance is $62. ✅ You're covered."

### Scope Options

Three options for Cycle 2 MVP, to be decided at kickoff:

**Option A: Hub + Knot Linking (Visibility + Consolidation)**
- Bills hub with detection from Cash Card transaction history
- Knot card-switching to move bills onto Cash App Card
- Basic management actions (view, dismiss)
- *Value:* Proves consolidation thesis, measures card-switching adoption
- *Risk:* Without management tools, may feel like a read-only dashboard

**Option B: Hub + Knot Linking + Management Actions**
- Everything in Option A, plus:
- Knot-powered pause/cancel/change plan
- Post-cancellation monitoring
- *Value:* Full utility — customers can act, not just see
- *Risk:* Broader Knot integration surface, more edge cases to handle

**Option C: Hub + Knot Linking + Management + Bill-Specific Auto-Reload**
- Everything in Option B, plus:
- Per-bill auto-reload from linked debit
- Coverage check ("Am I covered?") with proactive notifications
- *Value:* Complete value loop — see bills, manage them, never miss one
- *Risk:* Largest scope; auto-reload is a new funding primitive that touches payments infrastructure

**Recommendation:** Start with Option B for Cycle 2 build, with Option C's auto-reload as a fast-follow in Cycle 3. Option A alone risks the "read-only dashboard" problem identified in design feedback — customers need to be able to act, not just observe.

## Key value props

- **One place for all your bills** — See every recurring charge in one view, whether it's already on your Cash App Card or linked from another account via Knot.
- **Switch payments in a few taps** — Move subscriptions and bills from other cards to Cash App Card without visiting each biller's website. Knot handles the update.
- **Take action without leaving Cash App** — Pause, cancel, or change your subscription plan directly from the bills hub. No more navigating biller websites or sitting on hold.
- **Never miss a bill** — Set up auto-reload specifically for upcoming bills so your balance is always ready when charges hit. Know you're covered before the bill arrives.
- **Spot what you don't need** — See your total monthly recurring spend, catch price increases, identify duplicates, and free up money you didn't know you were losing.

## Competitor analysis

| Capability | Cash App (today) | Proposed | Rocket Money | Apple Wallet | Chime | Traditional Banks |
| --- | --- | --- | --- | --- | --- | --- |
| View recurring charges | Partial (transaction history only) | Yes — dedicated hub with detection + Knot linking | Yes — auto-detected from linked accounts | Yes — recurring transaction grouping in Wallet | No dedicated view | Partial — some show "recurring" tag |
| Switch payment method to your card | No | Yes — Knot CardSwitcher™ in-app | No (visibility only) | No | No | No |
| Cancel/pause/change subscriptions | No | Yes — Knot SubscriptionManager™ | Yes — concierge cancellation service | No | No | No |
| Bill-specific auto-funding | No (only balance-based auto-reload) | Yes — per-bill reload triggers | No | No | Partial (SpotMe covers small overages) | No (bill pay is push-based) |
| Upcoming bill alerts + coverage check | No | Yes — "Am I covered?" with proactive notifications | Yes — bill reminders | Yes — upcoming payment notifications | No | Yes — bill pay reminders |
| Price change detection | No | Yes — alert when charge amount changes | Yes | No | No | No |
| Monthly total / spending insight | No (requires manual review) | Yes — monthly recurring total on hub | Yes — monthly subscription total | Partial | No | Partial |

**Strategic positioning:** Rocket Money is the closest competitor in subscription management but operates as a standalone app — it can see and cancel, but it can't fund. Apple Wallet shows recurring charges but offers no actions. Chime's SpotMe covers small overages but isn't bill-aware. Traditional banks have bill pay but it's push-based and disconnected from card spending.

Cash App's unique advantage is the combination of: (1) Knot-powered card-switching and management actions, (2) bill-specific auto-reload from linked funding sources, and (3) integration with the broader Cash App ecosystem (direct deposit, Boost, savings). No competitor offers all three in one place. The strategic wedge is not just visibility — it's the closed loop of consolidate → manage → fund → succeed.

## Definition of success

**North star metric:** Recurring card GPV per customer (monthly)

**How we get there:**
- More recurring transactions on Cash App Card (consolidation via Knot)
- Higher payment success rate on recurring charges (bill-specific auto-reload)
- Increased account funding (customers fund ahead of known bills)

**Leading metrics:**
| Metric | What it measures | Target |
| --- | --- | --- |
| Bills linked via Knot (card-switches) | Consolidation adoption | TBD at kickoff |
| Recurring transactions per customer | Depth of consolidation | TBD |
| Recurring payment success rate | Funding + timing effectiveness | Improve vs. baseline |
| Auto-reload adoption (bill-specific) | Funding assurance uptake | TBD |
| Hub engagement (WAU) | Feature stickiness | TBD |
| Account funding events post-linking | Behavioral shift toward primary bank | TBD |

**Guardrail metrics:**
- Support contact rate (should not spike)
- Knot action failure rate (card-switch, cancel, pause)
- False detection rate (bills shown that aren't real recurring charges)
- Auto-reload failure rate
- Customer complaints about unauthorized actions

**Non-goals for Cycle 2:**
- Lending/credit layering on top of bills
- Non-US launch
- Recurring P2P payment management (future consideration)
- Moneybot integration (future consideration, per design feedback)
- Savings goal connection ("you freed up $15/month — save it?")

## Rollout plan

### Cycle 2 (June 1 – Jul 10, 2026): Build + Internal Testing

- **Week 1-2:** Finalize MVP scope at kickoff, Knot integration planning, detection logic design
- **Week 3-4:** Hub UI build, Knot card-switching integration, detection from Cash Card transaction history
- **Week 5-6:** Management actions (if Option B+), internal dogfooding, QA, edge case handling

### Cycle 3: Gated Pilot

- Bill-specific auto-reload (if not in Cycle 2)
- Gated rollout to eligible Card customers (criteria TBD — likely DD users with 3+ recurring charges)
- Holdout group for measurement
- Weekly readouts on adoption, payment success, and support contacts

### Cycle 4+: Expansion

- Broader rollout based on pilot results
- Coverage check + proactive notifications
- Price change detection and duplicate subscription alerts
- Moneybot integration (conversational bills management)
- Savings connection (cancel → save flow)
- Lending consideration (cover a bill now, pay back later)

## Risks & mitigations

| # | Risk | Description | Mitigation | Score |
| --- | --- | --- | --- | --- |
| 1 | **Cold start / empty state** | Customers open the hub and see nothing — detection from Cash Card transactions alone may miss most bills, especially if bills are paid from other cards. First impression failure means customers never return. Design feedback rated this 10/10 criticality. | Lead with Knot linking as enhancement (not gate); design three distinct empty/near-empty states; show partial detection + "add more" prompt; use common subscription logos as quick-add buttons. | 8/10 |
| 2 | **Knot merchant coverage gaps** | Knot doesn't support every merchant. Customers will encounter billers where card-switching or management actions aren't available, creating inconsistent experience. | Show clear distinction between full-management (Knot-supported) and limited-management merchants; offer "block merchant" as universal fallback; be transparent about what Cash App can vs. can't do for each biller. | 6/10 |
| 3 | **Knot action reliability** | Card-switch, cancel, or pause actions may fail silently or partially. Customer thinks they cancelled but gets charged. Trust destruction. | Implement confirmation + post-action monitoring; alert if charge reappears after cancellation; graceful fallback with deep link to biller's site if Knot fails; track failure rates by merchant. | 7/10 |
| 4 | **Detection accuracy (false positives/negatives)** | Pattern-based detection from transaction history may surface non-recurring charges or miss actual subscriptions. Wrong information is worse than no information. | Start conservative (high-confidence detections only); let customers dismiss false positives and add missed bills manually; improve detection model over time with user corrections. | 6/10 |
| 5 | **Customer trust with card-switching** | Customers may be uncomfortable with Cash App changing their payment method at merchants. Feels invasive or risky. "What if something goes wrong?" | Frame as customer-initiated action with clear confirmation; show exactly what will change; provide undo/revert path; build trust incrementally (start with low-stakes subscriptions like streaming). | 5/10 |
| 6 | **Bill-specific auto-reload complexity** | New funding primitive that interacts with existing auto-reload, balance, and payment timing. Edge cases: multiple bills same day, reload amount exceeds linked debit balance, reload timing vs. merchant charge timing. | Design clear priority rules; cap per-bill reload amounts; handle conflicts gracefully; extensive testing before pilot; keep existing auto-reload unchanged. | 7/10 |
| 7 | **Cannibalization of existing auto-reload** | Bill-specific reload may confuse customers who already use balance-based auto-reload. Two reload systems = cognitive overhead. | Position bill-specific reload as complementary ("your auto-reload keeps your balance healthy; bill reload makes sure specific bills are covered"); consider unified reload settings page. | 4/10 |
| 8 | **Management actions reduce card GPV** | If customers primarily use management tools to cancel subscriptions, net effect could be lower GPV, not higher. Feature helps customers spend less. | Acceptable tradeoff — customers who feel in control of their money trust Cash App more and consolidate more spending long-term. Track net GPV including new bills added via Knot vs. cancelled. Cancellation = trust building. | 3/10 |
| 9 | **Regulatory / compliance risk** | Switching payment methods on behalf of customers, or facilitating cancellations, may have regulatory implications depending on how actions are framed and disclosed. | Legal review before launch; ensure all actions are clearly customer-initiated with explicit confirmation; maintain audit trail of all Knot actions; review state-by-state requirements. | 5/10 |
| 10 | **Merchant pushback** | Merchants may object to a feature that makes it easy to cancel their subscriptions or switch payment methods away from their preferred card. | Knot handles merchant relationships; Cash App is the card issuer acting on behalf of the cardholder; frame as customer empowerment, not anti-merchant. | 3/10 |
| 11 | **Linked merchant frustration** | Showing charges from merchants where management isn't available (no Knot support) may frustrate customers who can see but can't act. Design feedback rated this 5/10. | Offer baseline actions for all merchants (block, set reminder, view history); clearly distinguish "full management" vs. "limited" merchants; use limitation as motivation to request Knot coverage expansion. | 4/10 |
| 12 | **NUX sets wrong expectations** | If onboarding oversells capabilities ("manage all your bills!") but detection/coverage is limited at launch, customers feel misled. | Set honest expectations in NUX; show what was found + invite customers to add more; frame partial detection as starting point, not failure; avoid claiming comprehensive coverage until it's real. | 5/10 |
| 13 | **Support volume spike** | New feature with Knot-powered actions will generate support contacts — failed cancellations, unexpected charges, confusion about what Cash App did vs. what the merchant did. | Pre-build support macros and FAQ; clear in-app status for all actions; post-action confirmation with "something wrong?" path; monitor support volume weekly during pilot. | 5/10 |
| 14 | **Timing dependency on Knot integration** | Knot integration timeline may not align with Cycle 2 build schedule. API changes, merchant coverage updates, or reliability issues could delay launch. | Identify Knot integration milestones early; build hub UI independently of Knot (detection + manual add can work without Knot); have fallback scope that ships without full Knot management. | 6/10 |

## Appendix

### Open questions

- What is the exact MVP scope for Cycle 2? (Decision needed at Monday kickoff)
- What detection method ships first — Cash Card transaction pattern matching, Knot-powered detection, or both?
- How does bill-specific auto-reload interact with existing auto-reload settings? Can a customer have both?
- Should recurring P2P payments (rent to a $cashtag, monthly to family) appear in the bills hub?
- What is the right empty-state strategy given detection quality at launch?
- How should Moneybot surface this feature in conversation? (Design feedback item #12)
- What is the Knot merchant coverage for Cash App's customer base? (% of common billers supported)
- Should we show a monthly total on the hub home view? (Design feedback strongly recommends yes)

### Design references

- Figma: [Bills & Subscriptions Manager](https://www.figma.com/design/gSiPlvN2nIjAMVtMysu345/Bills---Subscriptions-Manager?node-id=3-3)
- Design feedback (Moneybot transcript analysis): [Subscription Management: Design Feedback](https://docs.google.com/document/d/1QwftardXlA1e8wWiMuyWfhvZu9uyc4JuupCVGDwAbWE/edit)

### Research links

- Customer research (2022): [Bills & Subscriptions Research](https://docs.google.com/presentation/d/1-wuqTiH45wJk0QT9laiGvF0ixmR-QU6vswdPuuegj0s/edit)
- Payment Success analysis: [Payment Success & Failure Rates](https://docs.google.com/document/d/1LD13fZQwDnpa3CY3pyTzVMJOIISTFhsF4VPn5O-A580/edit)
- Knot API documentation: [knotapi.com](https://www.knotapi.com/subscription-manager/)

### Partner: Knot API

Knot provides the infrastructure for card-switching and subscription management:
- **CardSwitcher™** — Switch saved payment methods on behalf of users at 10,000+ merchants
- **SubscriptionManager™** — View, manage, pause, cancel, and upgrade subscription plans in-app
- **TransactionLink™** — SKU-level transaction details for better detection
- SOC 2 Type II, PCI DSS compliant
- Trusted by Visa, Mastercard, American Express, PayPal, Plaid

### Methodology notes

- Design feedback was generated by analyzing 25,000 Moneybot sessions (May 3-7, 2026), identifying 29 user-initiated subscription sessions and 565 proactive nudge sessions
- Payment success data from internal Cash App Card analysis (see Payment Success doc)
- Competitor analysis based on publicly available product documentation and features as of May 2026
