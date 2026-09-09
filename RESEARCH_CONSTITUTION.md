# Research constitution

Established: 2026-09-08. Status: governing instructions; the initial research specification remains provisional.

## Purpose

Build an auditable, educational research laboratory that can eventually be shared publicly. Investigate whether a daily ranking of a fixed group of liquid U.S. stocks helps identify which stocks outperform SPY over 10 trading days. The purpose is learning and agency, not manufacturing a profitable strategy.

The process is: idea → ask a better question → build an experiment → form a hypothesis → test it → try to break it → learn from failure → build again → create a repeatable system.

## Governing rules

1. Never use information that would not have been available on the signal date.
2. Explicitly protect against lookahead bias.
3. Identify survivorship bias or universe-selection bias whenever relevant.
4. Never optimize parameters unless the user explicitly authorizes optimization.
5. Never silently change an agreed methodology.
6. Record failed hypotheses as carefully as successful ones.
7. Never discard unattractive results.
8. Prefer simple, economically explainable hypotheses over complicated ones.
9. Never modify the research simply because we dislike a backtest result.
10. Separate evidence from interpretation.
11. Maintain an auditable research log documenting important decisions, changes, failures, and results.
12. Stop after each major stage so the user makes the next major research decision.
13. Prefer the simplest implementation capable of answering the research question.
14. Do not introduce new packages, data vendors, APIs, or frameworks without explaining why they are necessary. Obtain explicit approval for additional complexity.
15. Treat failure as information. The goal is to learn, not to force a successful result.

## Fixed starting constraints

- Horizon: 10 trading days.
- Universe: approximately 50 liquid U.S. stocks, supplied by the user later and held fixed.
- Benchmark: SPY.
- Evaluation: only the most recent 12 months; older observations may support historical inputs but are not additional evaluation results.
- Expected data source: Yahoo Finance through yfinance, subject to a later data-quality review.
- Eventual output: daily rankings, not simply BUY/SELL signals.
- Preferred implementation: Python, yfinance, pandas, and numpy.
- No machine learning, optimization frameworks, databases, VectorBT, TA-Lib, or other added complexity without explicit approval.

## Public record

Maintain RESEARCH_CONSTITUTION.md, RESEARCH_LOG.md, and PROMPTS.md from the start. Record methodology versions, material decisions, hypothesis definitions, results, failed attempts, and limitations. Distinguish user-approved rules from provisional proposals. Amendments must be dated and explained rather than silently replacing the historical record.

Keep public files free of credentials, API keys, private information, and machine-specific paths. Create README.md, START_HERE.md, and SOCRATES_MODE.md later when needed. The eventual viewer experience should support: “Don't copy my treasure hunt. Start your own.”

## Current stage boundary

Stage 1 is specification only. No implementation code, data pipeline, data acquisition, GitHub research, feature selection, signal construction, backtesting, or search for a profitable strategy is authorized at this stage. Stop after documenting the specification and wait for the user's next instruction.
