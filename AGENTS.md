# AGENTS.md - Advantage Play Intern

## Read first

Before changing code, schemas, prompts, schedules, analytical logic, adapters, catalogs, sources, or evidence contracts, read in this order:

1. `PROJECT_CONTEXT.md`
2. `PROMO_ANALYSIS_PLAYBOOK.md`
3. `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`
4. `SPORT_ADAPTERS/catalog.yaml`
5. `SPORT_ADAPTERS/source_registry.yaml`
6. `SPORT_ADAPTERS/README.md`
7. The selected adapter authority:
   - MLB player hits: Section 6 of `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md`
   - WNBA: `SPORT_ADAPTERS/WNBA.md`
   - NBA: `SPORT_ADAPTERS/NBA.md`
   - NFL: `SPORT_ADAPTERS/NFL.md`
   - Golf: `SPORT_ADAPTERS/GOLF.md`

Read `SPORT_ADAPTERS/ADAPTER_TEMPLATE.md` before changing adapter structure, metadata, profile records, identity fields, sources, materiality, refresh phases, evidence requirements, fixtures, or run contracts. `ROADMAP.md` is non-authoritative future context; it never authorizes work by itself.

Do not run a reusable prompt from `PROMO_ANALYSIS_PLAYBOOK.md` alone. Apply the monitoring playbook, canonical catalog, source registry, and selected adapter together.

## Authority order

- `PROJECT_CONTEXT.md` owns the current product specification, canonical objects, deterministic formulas, human boundary, and broad acceptance requirements.
- `PROMO_ANALYSIS_PLAYBOOK.md` owns promotion intake, analysis workflow, reason codes, QA, and `promotion_decision_brief_v2`.
- `PROMO_PLACEMENT_MONITORING_PLAYBOOK.md` owns global lifecycle-enabled behavior, valuation, consensus, freshness, material-change, candidate-state, and active-scope rules. Its Section 6 remains the MLB player-hits authority.
- `SPORT_ADAPTERS/catalog.yaml` is the canonical `adapter_catalog_v1` record set for adapter identity, profile identity, lifecycle, implementation status, and source readiness.
- `SPORT_ADAPTERS/source_registry.yaml` is the canonical `source_registry_v1` record set for source roles, access policy, jurisdiction/season scope, pricing-origin groups, and review triggers.
- `SPORT_ADAPTERS/README.md` is the human-readable catalog presentation and selection policy; it must agree with the canonical YAML records.
- The selected sport adapter owns only that sport's exact market identity, settlement, signals, source application, cadence, gates, and fixtures. It may narrow global rules but may not weaken them.

When authorities, implementation, source behavior, or provider evidence disagree, stop, fail closed, identify the conflict, and update every affected authority together. Do not rely on undocumented behavior.

## Current readiness and boundaries

This checkout includes a credential-free, manual-input calculator only for `mlb.player_hits` and the three pilot-enabled WNBA full-game profiles. It has no executable retrieval, provider integration, scheduling, polling, alerts, live markets, statistical model, bet tracking, closing-line capture, settlement, sportsbook automation, or certified provider coverage. NBA, NFL, Golf, and unregistered profiles fail before valuation.

Profile lifecycle is policy permission, not proof of implementation or source certification. Implementation status and source readiness are separate canonical fields. Use `SPORT_ADAPTERS/catalog.yaml` for the registered records and derived distribution; do not maintain another numeric total here.

- `mlb.player_hits` is the stable policy-active pregame profile.
- WNBA pregame full-game moneyline, reciprocal half-point spread, and half-point total are policy-`pilot_enabled` for supervised on-demand review only when every per-run evidence gate passes.
- WNBA player points, rebounds, assists, and made threes remain `disabled_provider_validation`.
- Registered NBA full-game moneyline, half-point spread, half-point total, and non-push player points remain `disabled_provider_validation`. NBA rebounds, assists, and made threes are absent.
- Registered NFL full-game moneyline, half-point spread, and half-point total remain `disabled_provider_validation`. NFL player props are absent.
- The six registered Golf profiles remain `disabled_provider_validation`. Their scope is Missouri discovery for individual stroke-play events displayed by FanDuel or DraftKings; a listing is discovery evidence only and never establishes support.
- Soccer, World Cup, NCAAF, NHL, and every other absent profile are unregistered. An absent profile has no lifecycle record and must fail closed; provider exposure cannot register it.

Every disabled or unregistered request remains `BLOCKED` under the applicable existing reason-code and catalog-absence rules. Credential-free fixtures and evidence manifests do not activate a profile, certify a provider, authorize polling, or permit candidate generation.

Statistical/manual probability overrides, Tier D feature use, live betting, recurring schedules, background polling, automatic alerts, bet tracking, closing-line capture, and settlement are not current behavior. They require separately approved work governed by the current documents, not merely a roadmap entry.

AP Frankenstein remains the separate downstream receipt, spreadsheet, tracking, and settlement owner after the user manually places a wager. This project must not call it, edit it, write its spreadsheets, create a bridge, or infer that a researched candidate became a wager.

## Durable orchestration memory

- Decide automatically at task startup whether durable memory is needed. It applies to multi-phase/session work, role-based review, durable product/adapter/architecture/data decisions, release or validation gates, recovery/external-service dependencies, relevant branch/worktree ambiguity, and major strategy changes or rejected approaches.
- Use `docs/handoffs/PROJECT_CONTEXT.md` for stable decision memory and `docs/handoffs/CURRENT_STATUS.md` for current verified posture when the protocol is triggered. The root `PROJECT_CONTEXT.md` is the authoritative product requirements document and must not be repurposed, renamed, or treated as either handoff file.
- The coordinator owns these handoffs, verifies them against live Git/source/tests/current instructions, gives helpers only role-relevant excerpts, and records helper findings only after synthesis. Current evidence overrides stale handoff prose, and handoffs never authorize polling, provider calls, activation, deployment, or live betting behavior.
- Update stable memory only for durable decisions. Update current status after material phases, strategy changes, significant blockers, useful checkpoints, validation/release results, interruptions, or pauses likely to resume.
- Skip handoff creation for a narrow single-session task with no durable consequence. Under read-only/no-edit scope, report the deferred handoff delta in chat rather than writing files.

## Non-negotiable analysis rules

1. **Human control:** Never place, submit, confirm, or pretend to place a wager. Never automate sportsbook account actions or handle sportsbook credentials.
2. **Deterministic numbers:** When an implementation exists, tested deterministic code owns odds conversion, boost application, de-vigging, probability aggregation, EV, expected dollars, staking, timestamps, freshness, normalization, ranking, and grading. The LLM may parse, map, summarize, and explain; it must not invent numerical inputs or perform recommendation-grade arithmetic free-form.
3. **Exact identity:** Preserve raw labels and require exact event, participant, period, line, side, overtime, participation, push, void, stat-counting, and settlement equivalence. Never substitute a nearby market.
4. **Consensus:** Exclude the target sportsbook. Require complete method-specific outcome sets from at least two non-target comparison books assigned to two resolved independent pricing-origin groups. De-vig each book separately; never synthesize opposing sides across books.
5. **Freshness:** Every material fact and quote needs provenance and a UTC capture time. Enforce the governing profile's maximum ages and collection skew. A material context fact newer than prices invalidates the batch and requires synchronized refetch; it does not create a manual probability adjustment.
6. **Missing data:** Keep missing, stale, conflicting, suspended, unreadable, or unverified facts explicit. Do not impute them. Use the governing `WATCH`, `BLOCKED`, or `INELIGIBLE` outcome and reason codes.
7. **Context boundary:** Sport context protects identity and freshness. Tier A/C facts may gate or invalidate; they may not add narrative points or change numeric rank. Tier D and Tier X material remains unavailable unless separately activated under the governing contracts.
8. **Auditability:** Every material fact must retain source identity, jurisdiction, capture time, event/market identifiers, relevant version, and safe snapshot hash or manifest reference.

Use the exact formulas, report fields, candidate states, reason codes, freshness gates, and validation outcomes in the governing documents. Do not restate or fork them here.

## Sources, evidence, and access

- Follow `SPORT_ADAPTERS/source_registry.yaml` and the selected adapter. Prefer official league/team/organizer and government sources for event facts, then licensed/documented providers, then sportsbook-originated evidence, then approved specialist sources, with screenshots or structured manual entry as the explicit fallback.
- A provider marketing page or exposed field is not coverage evidence. Validate the exact sportsbook, Missouri jurisdiction where applicable, market, line, settlement, timing, source permission, and pricing-origin relationship.
- Never bypass authentication, geolocation, age/jurisdiction controls, CAPTCHAs, anti-bot measures, paywalls, rate limits, or source terms. Do not automate authenticated sportsbook pages or store sportsbook login credentials.
- NFL.com, NBA/WNBA, PGA TOUR, sportsbook, and other restricted sources remain manual/on-demand unless the source registry records a permitted licensed path. Official NBA/WNBA statistics must not be used for gambling-related modeling contrary to their terms.
- NWS data may be used only under its documented access requirements and for registered operational-weather facts.
- Golf requires an event-specific organizer/competition/market/settlement source pack. FanDuel or DraftKings availability in Missouri remains discovery-only.
- Repository evidence must use the credential-free safe manifests under `evidence/templates/`. Do not commit raw screenshots, account or personal data, credentials, session material, private paths, raw sportsbook payloads, or generated decision briefs.

## Practical working instructions

- Inspect the repository and working tree before proposing or changing anything. Preserve unrelated user changes.
- Keep changes small, reversible, provider-agnostic, and within the exact approved profile and files.
- Update canonical YAML truth before or atomically with generated/human-readable catalog text. Never hand-maintain competing adapter counts, lifecycle totals, source permissions, or pricing-origin records.
- Update documentation and implementation together when behavior changes. Documentation-only work must not imply that a runtime, provider, or activation exists.
- Use recorded credential-free fixtures and offline tests by default. Do not make paid API calls, provider calls, sportsbook access, deployments, schedules, or other external mutations without explicit approval.
- Never commit secrets or personal/account data. Keep local raw evidence and generated briefs in ignored paths.
- Run the relevant repository validation, link checks, and tests after changes; report actual results and unresolved blockers.
- Preserve `adapter_contract_v1`, `promotion_decision_brief_v2`, lifecycle/freshness gates, human control, and the AP Frankenstein boundary unless an explicitly approved migration says otherwise.
- Use bounded parallel workers only when the user requests them or independent review materially improves reliability. Give each worker non-overlapping ownership and have a coordinator review the combined diff.

If required evidence, authority, permission, identity, or scope remains unclear, stop and ask for direction rather than broadening the task.
