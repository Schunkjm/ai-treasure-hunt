# ALL 14 PROMPTS — EXACTLY AS USED

Complete original research prompts in chronological order. Restored and verified against authoritative sources on 2026-09-09.

Seven prompts were recovered from their original submitted text attachments; seven from original user-message records in this project's conversation. Attachment bodies are the submitted prompt; the application's generated attachment/path wrapper is not part of that body. No assistant responses, system instructions or tool output are represented as user prompts.

Each FULL ORIGINAL PROMPT — VERBATIM block preserves the source wording, punctuation, capitalization, Markdown, whitespace and line endings. The surrounding headings, source metadata, code fences and RESULT / DECISION are editorial framing, not part of the original prompt. SHA-256 and UTF-8 byte counts refer only to the original text inside each block. Original mixed line endings are intentionally retained; do not normalize this file if checking these hashes.

The former edited-summary entries have been replaced, not passed off as originals. Earlier audit findings remain in RESEARCH_LOG.md and PUBLIC_RELEASE_AUDIT.md. No original prompt was reconstructed from memory. No privacy redactions were required. Publication-maintenance instructions are unnumbered and are not Prompt 15.

## Navigation

- [Prompt 1 — Research laboratory](#prompt-1)
- [Prompt 2 — GitHub treasure hunt](#prompt-2)
- [Prompt 3 — Human override / V0](#prompt-3)
- [Prompt 4 — Preregistration](#prompt-4)
- [Prompt 5 — Infrastructure](#prompt-5)
- [Prompt 6 — Freeze](#prompt-6)
- [Prompt 7 — First performance comparison](#prompt-7)
- [Prompt 8 — Robustness](#prompt-8)
- [Prompt 9 — Long-term trend diagnostic](#prompt-9)
- [Prompt 10 — Decision gate](#prompt-10)
- [Prompt 11 — Chapter 7 / system build](#prompt-11)
- [Prompt 12 — First live run](#prompt-12)
- [Prompt 13 — Public educational release](#prompt-13)
- [Prompt 14 — Socrates Mode](#prompt-14)

## Prompt 1

**PROMPT NUMBER:** 1

**CHAPTER / STAGE:** Research laboratory

**PURPOSE:** Define a falsifiable question

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 6065

**ORIGINAL SHA-256:** `077d06bda0bf957c6e3ae13682dcde6b555d0251b970d32d495ab4ed4a2b2287`

### FULL ORIGINAL PROMPT — VERBATIM

````text
I want you to collaborate with me on an investment research experiment that I will later present in an educational video.

This project will ultimately be published as a public GitHub repository so viewers can clone the entire research laboratory, inspect the work, and use it as the starting point for their own experiments.

The purpose is NOT to manufacture a profitable trading strategy.

The purpose is to demonstrate how someone can:

IDEA
→ ASK A BETTER QUESTION
→ BUILD AN EXPERIMENT
→ FORM A HYPOTHESIS
→ TEST IT
→ TRY TO BREAK IT
→ LEARN FROM FAILURE
→ BUILD AGAIN
→ CREATE A REPEATABLE SYSTEM

The larger lesson is empowerment and agency: AI can help an individual move from:

“I don't know how to do that.”

to:

“I can figure this out.”

to:

“I can actually build it.”

--------------------------------------------------
MY STARTING IDEA
--------------------------------------------------

I want to investigate whether we can rank a fixed group of liquid U.S. stocks in a way that helps identify which stocks may outperform SPY over approximately the next two weeks.

For now:

- Define “two weeks” as 10 trading days.
- Use a fixed universe of approximately 50 liquid U.S. stocks that I will provide later.
- Use SPY as the benchmark.
- Use only the most recent 12 months as the evaluation period.
- We expect to use Yahoo Finance for market data.
- The eventual output should be a daily ranking rather than simply BUY/SELL signals.

Keep the implementation deliberately simple.

Prefer:
- Python
- yfinance
- pandas
- numpy

Do not introduce machine learning, optimization frameworks, databases, VectorBT, TA-Lib, or additional complexity unless I explicitly approve it later.

--------------------------------------------------
RESEARCH CONSTITUTION
--------------------------------------------------

Throughout this entire project:

1. Never use information that would not have been available on the signal date.

2. Explicitly protect against lookahead bias.

3. Identify survivorship bias or universe-selection bias whenever relevant.

4. Never optimize parameters unless I explicitly authorize optimization.

5. Never silently change an agreed methodology.

6. Record failed hypotheses as carefully as successful ones.

7. Never discard unattractive results.

8. Prefer simple, economically explainable hypotheses over complicated ones.

9. Never modify the research simply because we dislike a backtest result.

10. Separate evidence from interpretation.

11. Maintain an auditable research log documenting important decisions, changes, failures, and results.

12. Stop after each major stage so that I—not you—make the next major research decision.

13. Prefer the simplest implementation capable of answering the research question.

14. Do not introduce new packages, data vendors, APIs, or frameworks without explaining why they are necessary.

15. Treat failure as information. The goal is to learn, not to force a successful result.

--------------------------------------------------
PUBLIC / EDUCATIONAL PROJECT
--------------------------------------------------

Because this project will eventually be shared publicly on GitHub, begin maintaining these files from the start:

RESEARCH_CONSTITUTION.md
RESEARCH_LOG.md
PROMPTS.md

PROMPTS.md should become a clean chronological record of the major instructions used to build the project so viewers can understand the process later.

Do not include machine-specific paths, credentials, API keys, private information, or anything else that should not appear in a public repository.

Later we will also create:

README.md
START_HERE.md
SOCRATES_MODE.md

Do NOT create those three files yet unless they are needed now.

SOCRATES_MODE.md will eventually allow a viewer to clone this repository, open it in their own AI coding environment, and have the AI interview them about what THEY are curious about rather than simply reproducing my trading signal.

The philosophy will be:

“Don't copy my treasure hunt. Start your own.”

--------------------------------------------------
YOUR FIRST TASK
--------------------------------------------------

DO NOT WRITE CODE YET.

DO NOT BUILD THE DATA PIPELINE.

DO NOT PROPOSE A TRADING SIGNAL.

DO NOT SEARCH FOR A PROFITABLE STRATEGY.

Your only job at this stage is to turn my vague idea into a precise research specification.

Define:

- the exact research question
- the prediction target
- benchmark
- holding horizon
- universe assumptions
- evaluation period
- required historical data
- how daily rankings will ultimately be evaluated
- the basic performance metrics that would be informative
- the most important potential biases
- what a successful experiment would mean
- what it would NOT mean
- the major stages required to move from this idea to a repeatable daily ranking system

If something is ambiguous, make the simplest reasonable provisional assumption, identify it clearly, and tell me whether it requires a decision from me later.

Create/update:

RESEARCH_CONSTITUTION.md
RESEARCH_LOG.md
PROMPTS.md

Then STOP.

Do not proceed to GitHub research, data acquisition, feature selection, signal construction, or backtesting.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

When finished, end your response with a concise section titled:

VIDEO SUMMARY

Use exactly this structure:

THE QUESTION:
What were we trying to accomplish at this stage?

WHAT WE DID:
3-5 short bullets.

WHAT WE NOW KNOW:
The most important definitions and decisions.

WHAT COULD FOOL US:
The most important caveats, biases, or unresolved assumptions.

THE NEXT CLUE:
The single most important question we should investigate next.

Keep the entire VIDEO SUMMARY short enough to display clearly on one screen.

Then STOP and wait for my next instruction.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Initial specification; implementation deferred.

## Prompt 2

**PROMPT NUMBER:** 2

**CHAPTER / STAGE:** GitHub treasure hunt

**PURPOSE:** Find understandable building blocks

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 3372

**ORIGINAL SHA-256:** `847811eae5b51090135e30a3a6327c1ffe4050af7d5f5a690500f1aeab1a0ace`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have completed Stage 1 and now have a defined research question.

Before building any signal, I want to follow the principle:

“Don’t reinvent the wheel.”

Our next task is to search GitHub for simple, understandable, open-source stock-trading signal ideas that we can potentially use as the starting point for this experiment.

IMPORTANT:
Do NOT implement anything yet.
Do NOT optimize anything.
Do NOT search for “the most profitable strategy.”
Do NOT assume GitHub popularity proves trading profitability.

We are looking for established building blocks and signal concepts.

---

## TIMING DECISION

For this project, use this timing convention going forward unless I explicitly change it:

- Signal is calculated using information available at the market close.
- Entry is assumed at the next trading day’s open.
- Forward performance is measured over the next 10 trading days from that entry.
- SPY is measured over the identical period.

Document this in the research log.

---

## GITHUB TREASURE HUNT

Search GitHub for simple Python stock-trading signal repositories that:

- use daily OHLCV data
- can work with Yahoo Finance / yfinance or can easily be adapted to it
- are easy for a non-programmer to understand conceptually
- have clear code and documentation
- have meaningful adoption, stars, forks, or community use where possible
- have a license appropriate for us to inspect and reuse or adapt
- avoid machine learning and black-box methods
- can plausibly be adapted to a roughly 10-trading-day horizon

Prioritize signal families such as:

- moving-average crossover
- momentum / relative strength
- RSI
- Bollinger Bands
- ATR / volatility contraction or expansion
- simple breakout signals

For each candidate, report:

1. Repository name and GitHub URL
2. Approximate stars / popularity if available
3. License
4. What the signal does in plain English
5. Inputs / indicators used
6. Why it might or might not fit a 10-trading-day horizon
7. How much adaptation would be required for our fixed 50-stock universe and Yahoo Finance data
8. Any obvious implementation or methodological concerns

Return the FIVE best candidates.

Then recommend the ONE simplest baseline signal to start from.

Do not select based on historical profitability.
Select based on:

- simplicity
- interpretability
- availability of code
- suitability for adaptation
- educational value

Also tell me whether any of the candidates already combine a moving-average crossover with ATR or volatility filtering.

---

## PUBLIC REPOSITORY RECORD

Update:

RESEARCH\_LOG.md
PROMPTS.md

Record:

- the repositories considered
- the criteria used
- the recommended baseline
- licensing notes
- the fact that GitHub popularity is being treated as evidence of adoption, not investment edge

Do not copy large amounts of third-party code into our project yet.

---

## VIDEO SUMMARY

When finished, end with:

VIDEO SUMMARY

THE QUESTION:
What were we trying to accomplish?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
List the best candidate signal ideas and identify the recommended starting point.

WHAT COULD BE WRONG:
Key caveats about using GitHub strategies or choosing among them.

THE NEXT CLUE:
What decision should I make before we implement anything?

Keep the entire VIDEO SUMMARY short enough to display clearly on one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Five candidates; AI proposed momentum, not adopted.

## Prompt 3

**PROMPT NUMBER:** 3

**CHAPTER / STAGE:** Human override / V0

**PURPOSE:** Choose a baseline for the human idea

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 2706

**ORIGINAL SHA-256:** `f32375d3f6e8f38c319b582269c1e526297892c16b7c8f9c3eb913e771930f75`

### FULL ORIGINAL PROMPT — VERBATIM

````text
I am not approving 20-session momentum as our baseline.

Your GitHub research identified moving-average crossover as another established, simple, understandable open-source signal family.

For this experiment, I want to select MOVING-AVERAGE CROSSOVER as our baseline because I have a separate hypothesis I eventually want to investigate:

A bullish moving-average crossover may be more informative when it occurs after a meaningful contraction in ATR as a percentage of price.

Do NOT test that ATR hypothesis yet.

First, I want us to define a clean GitHub-derived moving-average crossover baseline.

Review the moving-average crossover repositories already identified in the GitHub research and determine the simplest defensible bullish crossover specification for our approximately 10-trading-day research horizon.

We are interested ONLY in bullish/buy signals.

Do not optimize parameters against our historical data.

Do not run a backtest.

Determine:

- which GitHub repository/concept we are using as the baseline
- the exact fast SMA
- the exact slow SMA
- the precise definition of a bullish crossover
- why those parameters are reasonable for our short horizon
- what price information is available when the signal is calculated
- how next-open execution avoids lookahead
- whether the repository's code should be adapted or whether it is cleaner to implement the documented concept ourselves
- relevant licensing/attribution requirements

Call this:

V0 — GITHUB BASELINE

Then separately document, but DO NOT IMPLEMENT, my future hypothesis:

V1 — ATR-CONTRACTION + SMA CROSSOVER

Conceptually:

1. ATR as a percentage of price contracts materially.
2. A bullish SMA crossover subsequently occurs.
3. We ask whether that setup produces better subsequent 10-trading-day excess returns than the GitHub SMA crossover alone.

Do NOT choose the ATR lookback, contraction threshold, or exact definition yet. Those decisions must happen before testing and must not be optimized based on results.

Update:
RESEARCH\_LOG.md
PROMPTS.md

Clearly record that the human researcher overrode the AI recommendation of momentum and selected moving-average crossover because it creates a simple baseline for testing a separate volatility-contraction hypothesis.

VIDEO SUMMARY

THE QUESTION:
What baseline are we choosing and why?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
State the exact proposed V0 crossover specification and its GitHub origin.

WHAT COULD BE WRONG:
Important limitations of the crossover baseline and parameter choice.

THE NEXT CLUE:
What must we decide before we can add the ATR-contraction hypothesis?

Keep the VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Momentum rejected; strict SMA10/20 selected; ATR concept separated.

## Prompt 4

**PROMPT NUMBER:** 4

**CHAPTER / STAGE:** Preregistration

**PURPOSE:** Freeze human V1 before results

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 3465

**ORIGINAL SHA-256:** `b189f422b6aaa774cc5ee1302495c0b9a1ce2da2eb4bdd5b77b190c87b55776a`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now frozen V0 as our GitHub-derived baseline:

V0 — GITHUB BASELINE

- Bullish 10-day SMA crossing above 20-day SMA
- Fast SMA was strictly below slow SMA on the prior session
- Fast SMA is above slow SMA on the current session
- Signal calculated at the close
- Hypothetical entry at the next trading day’s open
- Outcome measured over the following 10 trading sessions relative to SPY

Now I want to preregister my human research idea before we look at any backtest results.

---

## V1 — ATR CONTRACTION + SMA CROSSOVER

The hypothesis is:

A bullish moving-average crossover may be more informative when it occurs after volatility has materially contracted.

Use:

ATR period:
14 trading days

ATR percentage:
ATR% = ATR(14) / closing price

ATR contraction lookback:
20 trading sessions

Define MATERIAL ATR CONTRACTION as:

Current ATR% is at least 20% below the maximum ATR% observed during the prior 20 trading sessions.

In other words:

current ATR% <= 0.80 × prior-20-session maximum ATR%

Use only information available by the current close.

V1 generates a bullish signal only when BOTH are true on the same signal date:

1. The V0 10/20 bullish SMA crossover occurs.
2. The ATR-contraction condition above is satisfied.

Do not change:

- SMA periods
- ATR period
- ATR lookback
- 20% contraction threshold

unless I explicitly authorize a later research change.

Do NOT backtest yet.

---

## HOW WE WILL JUDGE V1 VS V0

Preregister the following evaluation framework.

PRIMARY METRIC:
Average subsequent 10-trading-day excess return versus SPY.

SECONDARY METRICS:

- Median subsequent 10-day excess return versus SPY
- Hit rate: percentage of signals that outperform SPY over the same 10-day period
- Number of signals / sample size

We will compare:

V0 — all qualifying bullish 10/20 SMA crossovers

versus

V1 — only those V0 crossovers that also satisfy the ATR-contraction condition

Do not call V1 “better” merely because one metric improves.

When we eventually test it, evaluate:

- whether average excess return improves
- whether median excess return improves
- whether hit rate improves
- how much the ATR filter reduces sample size
- whether any apparent improvement is concentrated in a small number of stocks, sectors, or dates

Do not optimize the threshold after seeing results.

Do not claim statistical proof or a validated trading edge based on one year of data.

---

## DOCUMENTATION

Update:

RESEARCH\_LOG.md
PROMPTS.md

Clearly record that:

- V0 came from the GitHub moving-average crossover concept.
- V1 is the human researcher’s added hypothesis.
- All V1 parameters were selected BEFORE looking at V0 or V1 performance.
- The purpose is to test whether the added ATR clue improves the GitHub baseline, not to manufacture a profitable result.

Do not implement the data pipeline yet unless needed only to verify that these definitions are mathematically unambiguous.

Do not calculate historical results.

---

## VIDEO SUMMARY

End with:

VIDEO SUMMARY

THE QUESTION:
What exactly are we adding to the GitHub baseline?

WHAT WE DID:
3-5 short bullets.

WHAT WE NOW KNOW:
State the complete frozen V0 and V1 definitions.

WHAT COULD BE WRONG:
What conceptual weaknesses could this ATR filter have before we even test it?

THE NEXT CLUE:
What infrastructure and data do we now need to actually run the experiment?

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* ATR14, prior 20 maximum and 20% contraction frozen.

## Prompt 5

**PROMPT NUMBER:** 5

**CHAPTER / STAGE:** Infrastructure

**PURPOSE:** Build without performance review

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 5904

**ORIGINAL SHA-256:** `4b28344594d99edc959f111cb6f5c470a316e103efe0850e690a57f6d1bc7393`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now preregistered and frozen:

V0 — GITHUB BASELINE
Bullish SMA10 / SMA20 crossover.

V1 — HUMAN HYPOTHESIS
V0 plus ATR contraction:
ATR%(today) <= 0.80 × maximum ATR% over the prior 20 sessions,
excluding today,
where ATR% = ATR14 / Close.

No historical V0 or V1 performance has been examined.

Now build the infrastructure required to test these frozen hypotheses.

--------------------------------------------------
FIXED STOCK UNIVERSE
--------------------------------------------------

Use this exact fixed universe of 50 liquid U.S. stocks:

AAPL
MSFT
NVDA
AMZN
GOOGL
META
AVGO
AMD
ORCL
CRM
JPM
BAC
GS
MS
V
MA
XOM
CVX
COP
SLB
CAT
GE
RTX
ETN
HON
DE
WMT
COST
HD
MCD
NKE
SBUX
LLY
UNH
JNJ
ABBV
MRK
NFLX
DIS
T
VZ
TSLA
QCOM
TXN
IBM
AMAT
MU
LOW
PEP
KO

Benchmark:
SPY

This is deliberately a fixed experimental universe.

Do not claim it is a point-in-time historical S&P 500 universe.

Document the resulting universe-selection / survivorship limitation.

--------------------------------------------------
DATA
--------------------------------------------------

Use Yahoo Finance / yfinance.

Download sufficient daily OHLCV history to support:

- SMA20 warm-up
- ATR14
- prior-20-session ATR contraction calculation
- the full 12-month evaluation period
- forward 10-trading-day outcomes

Use approximately 18 months of historical data.

Prefer adjusted price data where appropriate, but ensure OHLC values used for ATR are internally consistent.

Explicitly document how yfinance adjustment settings affect:
- Open
- High
- Low
- Close

Do not mix adjusted Close with unadjusted High/Low when calculating ATR.

Validate:

- all 50 stocks and SPY downloaded
- no duplicate dates
- no obviously invalid prices
- missing observations identified
- trading dates aligned
- sufficient warm-up history exists

If a ticker fails, report it.
Do not silently substitute another stock.

If yfinance cache permissions or network access cause the same type of issue encountered in prior testing, fix the technical issue pragmatically and document it. Do not change the research methodology.

--------------------------------------------------
SIGNAL CALCULATIONS
--------------------------------------------------

Implement exactly the frozen definitions.

SMA10:
10-session simple moving average of Close.

SMA20:
20-session simple moving average of Close.

V0 bullish crossover:

Yesterday:
SMA10 < SMA20

Today:
SMA10 > SMA20

The signal is known only after today’s close.

ATR14:
Use standard Wilder-style Average True Range if practical.

True Range should use:
- High - Low
- abs(High - prior Close)
- abs(Low - prior Close)

ATR%:
ATR14 / Close

ATR contraction:

current ATR%
<=
0.80 × maximum ATR% over the PRIOR 20 trading sessions

The prior 20-session maximum must EXCLUDE the current date.

V1 signal:

V0 is true
AND
ATR contraction is true on the same signal date.

--------------------------------------------------
OUTCOME CALCULATION
--------------------------------------------------

For each historical V0 and V1 signal:

Signal:
current close

Entry:
next trading day Open

Exit/outcome:
after 10 trading intervals from entry

Calculate:

stock forward return

SPY forward return over the identical entry and exit dates

forward_10d_excess_return =
stock return - SPY return

Be extremely careful about indexing and off-by-one errors.

The outcome fields are evaluation-only and must never be used in signal construction.

--------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------

Create a clean, simple structure such as:

src/
data/
output/
tests/

Use only the minimal dependencies needed:

Python
yfinance
pandas
numpy

Use matplotlib only if necessary later.

Do not introduce VectorBT, TA-Lib, pandas-ta, machine learning, optimization tools, or databases.

--------------------------------------------------
VALIDATION
--------------------------------------------------

Add simple automated checks proving:

- the crossover uses only current/prior data
- ATR contraction excludes today from the prior-20 maximum
- forward returns begin at the next Open
- exactly 10 trading intervals are measured
- SPY uses the same entry and exit dates
- V1 is always a subset of V0
- outcome columns cannot affect signal generation

Do NOT evaluate V0 vs V1 performance yet.

You may calculate signals and outcomes to verify the pipeline, but do not summarize, compare, inspect, or interpret their returns.

The first legitimate performance comparison must happen in a later stage after the pipeline is frozen.

--------------------------------------------------
DOCUMENTATION
--------------------------------------------------

Update:

RESEARCH_LOG.md
PROMPTS.md

Record:
- fixed universe
- data source
- adjustment convention
- signal timing
- outcome timing
- implementation decisions
- validation results
- any technical issues

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
What infrastructure did we need to fairly test our frozen hypotheses?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
Report data quality, number of usable tickers, signal counts only if needed for validation, and whether the pipeline passed its checks.
Do NOT report performance.

WHAT COULD BE WRONG:
Important remaining data or implementation limitations.

THE NEXT CLUE:
Are we ready to freeze the pipeline and run the first legitimate V0 vs V1 backtest?

Keep the entire VIDEO SUMMARY short enough to display on one screen.

Then STOP.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Pipeline/tests created; KO bar quarantined.

## Prompt 6

**PROMPT NUMBER:** 6

**CHAPTER / STAGE:** Freeze

**PURPOSE:** Resolve KO and add sectors

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 3186

**ORIGINAL SHA-256:** `d28a46e194948db36622b95c95c713d080d074b8e080b36b2911e9726d37ec1c`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We are not ready to run the first legitimate V0 vs V1 performance comparison yet.

Before any performance is examined, resolve the remaining pipeline issues and freeze the research infrastructure.

---

1. REVIEW THE KO QUARANTINE

---

Investigate the single quarantined KO bar.

Determine:

- date of the bar
- why it was flagged
- whether it appears to be a Yahoo Finance data issue, corporate-action adjustment issue, missing/zero/invalid value, or something else
- whether it can be corrected objectively from the same data source without introducing discretion

Use this rule:

- If the bar can be corrected mechanically and unambiguously using Yahoo Finance data, fix it and document the fix.
- If it cannot be corrected objectively, exclude only the affected KO observation(s) from calculations that depend on that bar.
- Do NOT remove KO from the universe unless absolutely necessary.
- Do NOT substitute another stock.

Document the decision clearly.

---

2. ADD SECTOR MAPPING

---

Add a fixed sector label for each of the 50 stocks so we can later test whether any apparent result is concentrated in one sector.

Use broad GICS-style sector categories such as:

Information Technology
Communication Services
Consumer Discretionary
Consumer Staples
Financials
Health Care
Industrials
Energy

and any other standard sectors required by the universe.

Create a simple, auditable ticker-to-sector mapping file.

Do not use sector information in the signal.
It is for diagnostics only.

---

3. FREEZE THE PIPELINE

---

Once KO is resolved and sector mapping is added:

Freeze the following:

- stock universe
- benchmark
- data source
- adjustment convention
- SMA definitions
- ATR definition
- ATR-contraction definition
- V0 definition
- V1 definition
- signal timing
- next-open entry rule
- 10-trading-interval outcome rule
- SPY comparison
- evaluation window
- performance metrics
- sector mapping

Create a clear frozen specification file:

FROZEN\_SPECIFICATION.md

Include the exact formulas and timing rules in plain English.

Do NOT alter any research parameter after this point unless I explicitly authorize a new version later.

---

4. FINAL VALIDATION

---

Rerun the pipeline and all tests.

Confirm:

- all usable tickers process correctly
- V1 is a strict subset of V0
- no future information is used
- no performance statistic has been inspected or summarized
- the frozen specification matches the actual implementation

Do NOT run or reveal V0 vs V1 returns yet.

---

## DOCUMENTATION

Update:

RESEARCH\_LOG.md
PROMPTS.md

Record:

- KO investigation and resolution
- sector mapping
- pipeline freeze
- final validation status

---

## VIDEO SUMMARY

End with:

VIDEO SUMMARY

THE QUESTION:
What had to be resolved before we could trust the first backtest?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
State the KO resolution, sector mapping status, and final validation status.

WHAT COULD BE WRONG:
Remaining structural limitations that cannot be eliminated.

THE NEXT CLUE:
Are V0 and V1 now frozen and ready for the first legitimate performance comparison?

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Objective KO correction, fixed sectors and specification lock.

## Prompt 7

**PROMPT NUMBER:** 7

**CHAPTER / STAGE:** First performance comparison

**PURPOSE:** Compare frozen V0 and V1

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 5871

**ORIGINAL SHA-256:** `e25ece6c30c871be42af756f23403fa0ca71bb3ab7df436af7ddc2a76aa26a66`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now frozen:

V0 — GITHUB BASELINE
Bullish SMA10 / SMA20 crossover.

V1 — HUMAN HYPOTHESIS
V0 plus ATR contraction:
ATR%(today) <= 0.80 × maximum ATR% over the prior 20 sessions,
excluding today,
where ATR% = ATR14 / Close.

The stock universe, timing rules, data conventions, sector mapping, outcome calculation, and performance metrics are all frozen in FROZEN_SPECIFICATION.md.

All validation tests have passed.

You are now authorized to run the FIRST legitimate V0 vs V1 performance comparison.

Do NOT change any parameter.
Do NOT optimize anything.
Do NOT create V2.
Do NOT search for better thresholds.
Do NOT alter the stock universe.

--------------------------------------------------
PRIMARY QUESTION
--------------------------------------------------

Does requiring ATR contraction improve the subsequent 10-trading-day outcomes of the GitHub-derived bullish SMA crossover?

Compare:

V0
All qualifying bullish SMA10 / SMA20 crossovers.

versus

V1
Only V0 signals that also satisfy the frozen ATR-contraction rule.

--------------------------------------------------
EVALUATION WINDOW
--------------------------------------------------

Use the frozen most recent 12-month evaluation period.

Only include signals for which the complete next-open through 10-trading-interval outcome is available.

Do not treat signals near the end of the data set with incomplete forward outcomes as failures or zero returns.

--------------------------------------------------
PRIMARY METRIC
--------------------------------------------------

Average forward 10-trading-day excess return versus SPY.

--------------------------------------------------
SECONDARY METRICS
--------------------------------------------------

For V0 and V1 report:

- signal count
- average forward 10-day stock return
- average forward 10-day SPY return
- average forward 10-day excess return
- median forward 10-day excess return
- hit rate versus SPY
- percentage of positive absolute stock returns
- best individual outcome
- worst individual outcome

--------------------------------------------------
MOST IMPORTANT COMPARISON
--------------------------------------------------

Explicitly calculate:

V1 minus V0 difference in:

- average excess return
- median excess return
- hit rate

Also show how much the ATR filter reduces the number of signals.

Do NOT call V1 better merely because one metric improves.

--------------------------------------------------
DISTRIBUTION
--------------------------------------------------

Show enough distribution information to understand whether averages are misleading.

At minimum report:

- 25th percentile excess return
- median
- 75th percentile
- standard deviation

If practical, create a simple chart comparing the V0 and V1 excess-return distributions.

--------------------------------------------------
TIME CONSISTENCY
--------------------------------------------------

Break results into monthly signal cohorts.

For each month report:

- V0 count and average excess return
- V1 count and average excess return

Tell me whether any apparent result is heavily dependent on one or two months.

--------------------------------------------------
SECTOR CONSISTENCY
--------------------------------------------------

Using the frozen sector mapping, report V0 and V1 results by sector where sample sizes permit.

Flag any sector that appears to dominate the aggregate result.

Do NOT interpret sparse sector samples as reliable evidence.

--------------------------------------------------
STOCK CONCENTRATION
--------------------------------------------------

Report:

- the stocks contributing the most V0 signals
- the stocks contributing the most V1 signals
- the stocks contributing the largest positive total excess-return contribution
- the stocks contributing the largest negative total excess-return contribution

This is diagnostic only.

--------------------------------------------------
OUTPUT FILES
--------------------------------------------------

Create clear output files such as:

output/v0_v1_summary.csv
output/v0_v1_monthly.csv
output/v0_v1_sector.csv
output/v0_v1_signals.csv

Create one or two simple charts if they materially help interpretation.

--------------------------------------------------
INTERPRETATION RULE
--------------------------------------------------

At the end, classify the first-pass result as one of:

V1 LOOKS BETTER
V0 LOOKS BETTER
MIXED
NO MEANINGFUL DIFFERENCE
INSUFFICIENT SAMPLE

This is a descriptive classification only.

Do NOT call the strategy validated.
Do NOT call it statistically proven.
Do NOT recommend trading it.

--------------------------------------------------
DOCUMENTATION
--------------------------------------------------

Update:

RESEARCH_LOG.md
PROMPTS.md

Record the complete first-pass results exactly as observed.

Do not hide disappointing results.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
Did the ATR-contraction clue improve the GitHub crossover baseline?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
Show V0 vs V1 side by side with:
- signal count
- average excess return
- median excess return
- hit rate

Then state the first-pass classification:
V1 LOOKS BETTER / V0 LOOKS BETTER / MIXED / NO MEANINGFUL DIFFERENCE / INSUFFICIENT SAMPLE.

WHAT COULD BE WRONG:
The most important reasons we should NOT trust the result yet.

THE NEXT CLUE:
What should we try to break before believing any apparent improvement?

Keep the VIDEO SUMMARY short enough to display clearly on one screen.

Then STOP.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* MIXED; mean improved, median and hit rate worsened.

## Prompt 8

**PROMPT NUMBER:** 8

**CHAPTER / STAGE:** Robustness

**PURPOSE:** Try to explain apparent improvement away

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 6614

**ORIGINAL SHA-256:** `7d9d237e85ea0e362ef6f50ef1805be182d2bcfac4341cc9bc01443b0297c1d2`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have completed the first frozen V0 vs V1 comparison.

The descriptive result was MIXED:

V0:
- 332 signals
- average 10-day excess return: -0.389 percentage points
- median excess return: -0.260 percentage points
- hit rate versus SPY: 48.49%

V1:
- 57 signals
- average 10-day excess return: +0.355 percentage points
- median excess return: -0.456 percentage points
- hit rate versus SPY: 47.37%

The ATR filter improved the MEAN but worsened the MEDIAN and HIT RATE.

I do NOT want to modify the strategy.

Change roles.

Assume the apparent improvement in V1's average excess return is misleading.

Your job is to try to explain why.

DO NOT:
- optimize parameters
- change SMA periods
- change ATR settings
- change the universe
- create V2
- search for a better strategy

--------------------------------------------------
1. OUTLIER AUDIT
--------------------------------------------------

Identify the largest positive and negative V1 outcomes.

Report:

- ticker
- signal date
- entry date
- exit date
- stock return
- SPY return
- excess return

Determine how much V1's average changes if:

A. the single best V1 outcome is removed
B. the best 3 outcomes are removed
C. the best 5% of V1 outcomes are winsorized or excluded for diagnostic purposes only

Do the equivalent downside diagnostic for the worst observations.

Do NOT redefine the official result.
These are robustness diagnostics only.

--------------------------------------------------
2. CONTRIBUTION CONCENTRATION
--------------------------------------------------

Determine what percentage of V1's total cumulative excess-return contribution comes from:

- best single observation
- best 3 observations
- best 5 observations

Identify the stocks responsible for the largest positive contribution.

Tell me whether the positive average is dependent on a very small number of events.

--------------------------------------------------
3. DATE / MONTH CONCENTRATION
--------------------------------------------------

Analyze V1 by:

- signal month
- calendar date clusters

Determine:

- whether one month dominates the result
- whether multiple stocks generated signals around the same market event
- whether apparently separate observations are economically related

Flag periods where many signals occurred together.

--------------------------------------------------
4. SECTOR CONCENTRATION
--------------------------------------------------

Using the frozen sector labels:

Report V1:
- signal count by sector
- average excess return by sector
- total excess-return contribution by sector

Determine whether one sector is responsible for most of the positive aggregate result.

Do not interpret tiny sector samples as evidence.

--------------------------------------------------
5. STOCK CONCENTRATION
--------------------------------------------------

Report:

- number of V1 signals per stock
- average outcome per stock where sample size permits
- total excess-return contribution per stock

Determine whether repeated signals in one or two stocks disproportionately drive the result.

--------------------------------------------------
6. DEPENDENCE / OVERLAPPING OUTCOMES
--------------------------------------------------

Our 10-day outcomes overlap.

Quantify how frequently V1 signal holding periods overlap:

- within the same stock
- across different stocks
- during broad market clusters

Explain in plain English why 57 observations should NOT automatically be treated as 57 independent experiments.

Do not attempt to manufacture a corrected p-value unless a simple defensible method exists.

--------------------------------------------------
7. EXECUTION SENSITIVITY
--------------------------------------------------

Without changing the official next-open specification, run diagnostic comparisons for:

- entry at next Open (official)
- entry at next Close

This is not optimization.

The purpose is to determine whether the result is unusually dependent on idealized next-open execution.

Clearly label the alternative as a diagnostic only.

--------------------------------------------------
8. ATR-MECHANISM CHECK
--------------------------------------------------

Investigate Codex's earlier concern:

"An old volatility spike or rising price can make ATR% appear contracted."

For V1 signals, examine whether the contraction condition is commonly satisfied because:

A. a single unusually high ATR% observation remains inside the prior-20 maximum window
B. Close has risen enough to reduce ATR% even when raw ATR has not meaningfully fallen
C. volatility genuinely declined across the window

Do not change the ATR definition.

Classify this only as a diagnostic of what our frozen rule is actually selecting.

--------------------------------------------------
PASS / CAUTION / FAIL
--------------------------------------------------

Give each category a rating:

- Data integrity
- Outlier dependence
- Stock concentration
- Sector concentration
- Date/regime concentration
- Observation dependence
- Execution sensitivity
- ATR mechanism

Use:

PASS
CAUTION
FAIL

Then give V1 an overall robustness classification:

SURVIVES INITIAL ATTACK
FRAGILE
FAILS INITIAL ATTACK
INCONCLUSIVE

Do NOT create or recommend V2 yet.

--------------------------------------------------
OUTPUTS
--------------------------------------------------

Create useful diagnostic outputs in output/ and charts only where they materially clarify the result.

Update:

RESEARCH_LOG.md
PROMPTS.md

Preserve the original V0/V1 results unchanged.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
Is V1's positive average real evidence, or is something else producing it?

WHAT WE DID:
3-5 short bullets describing the attacks.

WHAT WE FOUND:
Identify the most important explanation for the difference between V1's positive mean and negative median/hit rate.
Include the effect of removing the largest winners if important.

ROBUSTNESS SCORECARD:
Brief PASS / CAUTION / FAIL results for the major diagnostics.

WHAT COULD BE WRONG:
What remains unresolved even after these diagnostics?

THE NEXT CLUE:
What did this failure/stress test teach us that should inform our next hypothesis?

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.

Do not create V2.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* FRAGILE; outlier/stock/sector dependence.

## Prompt 9

**PROMPT NUMBER:** 9

**CHAPTER / STAGE:** Long-term trend diagnostic

**PURPOSE:** Examine human trend-alignment idea

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 4062

**ORIGINAL SHA-256:** `1a1f07ac65418341c014edfe73425cd0239b280b88f90cfa5fb637506a406d22`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now stress-tested frozen V1.

The important conclusion is:

V1'S POSITIVE MEAN WAS FRAGILE.

The average 10-day excess return was +0.355 percentage points, but:

- removing the single best event reduced it to -0.154 pp
- removing the best three reduced it to -0.771 pp
- median excess return was already negative
- hit rate was below 50%
- stock and sector concentration failed robustness checks

Do NOT modify V0 or V1.

Do NOT optimize ATR parameters.

Do NOT search broadly for combinations that make the backtest profitable.

This stage is about LEARNING FROM FAILURE.

---

## PRIMARY QUESTION

What did the failed/fragile V1 experiment teach us about what might be missing from the hypothesis?

I have one human research idea I want to examine:

Perhaps a short-term bullish SMA crossover after ATR contraction is more meaningful when it occurs inside an already-positive LONG-TERM TREND.

Specifically, I am interested in the concept:

- price above the 200-day SMA
- 200-day SMA itself rising

Do NOT create V2 yet.

First investigate whether this is a conceptually sensible next hypothesis.

---

## LONG-TERM TREND DIAGNOSTIC

Extend historical data only as necessary to calculate SMA200 with adequate warm-up.

Do not change the frozen 12-month evaluation window.

For each historical V1 signal, calculate using information available on the signal date:

1. Was Close above SMA200?

2. Was SMA200 rising?

For this exploratory diagnostic, define “rising SMA200” simply and transparently as:

SMA200 today > SMA200 20 trading sessions ago.

Also calculate:

- distance of Close above/below SMA200
- 20-session change in SMA200

Do not use these features to alter V1.

---

## COMPARE THE SIGNAL ENVIRONMENTS

Describe V1 outcomes for:

A. Close above SMA200 AND SMA200 rising

B. Close above SMA200 but SMA200 not rising

C. Close below SMA200

Report only descriptive results:

- signal count
- average excess return
- median excess return
- hit rate

The purpose is NOT to claim that the best subgroup is a new proven strategy.

The purpose is to understand whether long-term trend alignment appears economically relevant enough to justify a NEW hypothesis.

---

## LEARN FROM THE FAILURES

Also compare the characteristics of:

- largest V1 winners
- largest V1 losers

Ask whether the losers appear disproportionately associated with:

- weak long-term trends
- certain sectors
- repeated stock names
- clustered dates/regimes

Do not search dozens of new indicators.

Keep this investigation narrow.

---

## INTERPRETATION

At the end, answer:

Does the evidence provide a reasonable conceptual basis for testing this NEW hypothesis?

V2 CANDIDATE:

V1
PLUS
Close > SMA200
PLUS
SMA200 today > SMA200 20 sessions ago

Classify the evidence as:

STRONG REASON TO TEST
REASONABLE HYPOTHESIS TO TEST
WEAK RATIONALE
NO RATIONALE

Important:

Even if the exploratory numbers look attractive, explicitly state that we have already seen this historical period.

Therefore any V2 created from this diagnostic will be exploratory and will require future/out-of-sample validation.

Do NOT call it validated.

---

## DOCUMENTATION

Update:

RESEARCH\_LOG.md
PROMPTS.md

Preserve all V0/V1 results unchanged.

Document that the long-term-trend idea originated with the human researcher before this diagnostic was run.

---

## VIDEO SUMMARY

End with:

VIDEO SUMMARY

THE QUESTION:
What did V1's failure teach us, and is long-term trend a sensible next clue?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
Summarize whether V1 behaved differently above a rising SMA200 versus other environments.

WHAT FAILURE TAUGHT US:
State the most important lesson from V1.

THE NEXT HYPOTHESIS:
State whether V2 = V1 + price above rising SMA200 is justified for exploratory testing.

WHAT COULD BE WRONG:
Explicitly note that this hypothesis was informed by data we have already examined.

THE NEXT CLUE:
Should we preregister V2 and test it without changing anything else?

Keep the VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* WEAK RATIONALE; no V2.

## Prompt 10

**PROMPT NUMBER:** 10

**CHAPTER / STAGE:** Decision gate

**PURPOSE:** Synthesize and stop modifying

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 3056

**ORIGINAL SHA-256:** `c738c5249272ce3608794d275eb63d45f6fc33430829c41d4fb5e7e69c299a3a`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now completed:

V0 — GitHub SMA10/SMA20 bullish crossover baseline

V1 — V0 plus the preregistered ATR-contraction condition

V1 initially improved the mean return, but robustness testing showed that the apparent improvement was fragile and heavily dependent on a few large winners.

We then investigated the independent human hypothesis that long-term positive trend might improve V1.

The result provided WEAK RATIONALE:

- 33 signals above a rising SMA200
- mean excess return: -0.463 percentage points
- hit rate: 45.45%
- four of the five worst V1 losses occurred in that environment

We will NOT create or promote V2 from this evidence.

---

## PRIMARY QUESTION

What should a disciplined researcher conclude from everything we have learned so far?

This stage is about knowing when NOT to keep modifying a model.

Do NOT:

- optimize any parameter
- create V2
- test additional indicators
- alter ATR thresholds
- alter SMA periods
- search for profitable subgroups
- change the universe

---

## SYNTHESIZE THE EVIDENCE

Summarize what we learned about:

1. V0 — GitHub SMA crossover baseline
2. V1 — ATR-contraction hypothesis
3. robustness of V1
4. long-term-trend diagnostic
5. sample size and observation dependence
6. what evidence would actually be needed before calling any version a trading edge

Separate conclusions into:

SUPPORTED BY THE EVIDENCE
NOT SUPPORTED BY THE EVIDENCE
STILL UNKNOWN

---

## DECISION GATE

Choose one of:

A. PROMOTE V0
B. PROMOTE V1
C. CREATE V2
D. DO NOT PROMOTE A STRATEGY — KEEP V0/V1 AS RESEARCH SIGNALS

Use only the evidence already generated.

My expectation is that D may be appropriate, but make the classification based on the documented research record.

If D is chosen, explain why stopping here is a successful research outcome rather than a failed project.

---

## PROSPECTIVE LEARNING

If no strategy deserves promotion, define what a clean prospective experiment should look like going forward.

At minimum consider:

- keep V0 and V1 definitions frozen
- generate signals on new market data
- record them before outcomes are known
- measure the same 10-trading-day excess returns
- accumulate genuinely out-of-sample evidence
- do not modify the signal based on each new outcome

Do NOT begin that prospective tracking yet.

---

## DOCUMENTATION

Update:

RESEARCH\_LOG.md
PROMPTS.md

Record explicitly that we chose not to manufacture a better backtest by continuing to search the same historical sample.

---

## VIDEO SUMMARY

End with:

VIDEO SUMMARY

THE QUESTION:
What should we conclude after the signal failed its robustness tests?

WHAT WE DID:
3-5 short bullets.

WHAT WE LEARNED:
The most important research lessons.

THE DECISION:
A / B / C / D, with one sentence explaining why.

WHY STOPPING CAN BE SUCCESS:
Explain why refusing to overfit is itself a positive outcome.

THE NEXT CLUE:
What can we build from this research without pretending we discovered a validated edge?

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* D: retain research signals; do not promote.

## Prompt 11

**PROMPT NUMBER:** 11

**CHAPTER / STAGE:** Chapter 7 / system build

**PURPOSE:** Build prospective journal engine

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 5473

**ORIGINAL SHA-256:** `665a5675ab119d28b8f4772a02297ab44a04b2914d35758464c56d28e99c7a32`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have decided:

D — DO NOT PROMOTE A STRATEGY.

V0 and V1 remain frozen research signals only.

We will not create V2, optimize parameters, or continue searching the same historical sample for a profitable variation.

Our next task is to turn the frozen research into a repeatable prospective signal engine.

--------------------------------------------------
PRIMARY GOAL
--------------------------------------------------

Build a simple command-line research engine that can be run on any new trading day and answer:

1. Which of the fixed 50 stocks currently generate a V0 bullish SMA crossover?
2. Which of those also satisfy the frozen V1 ATR-contraction condition?
3. What are the underlying feature values for each signal?
4. Can we record each new signal before its 10-trading-day outcome is known?
5. Can we later append the realized outcome without changing the original signal record?

This is a research journal, NOT an automated trading system.

--------------------------------------------------
FROZEN SIGNAL DEFINITIONS
--------------------------------------------------

Do not change any frozen research rule.

V0:
- SMA10 < SMA20 yesterday
- SMA10 > SMA20 today
- signal known after close
- hypothetical entry next trading day Open

V1:
V0
AND
ATR%(today) <= 0.80 × maximum ATR% over the prior 20 sessions, excluding today
where ATR% = ATR14 / Close

Benchmark:
SPY

Outcome:
10 trading intervals from next-open entry, measured relative to SPY.

--------------------------------------------------
CURRENT-SIGNAL OUTPUT
--------------------------------------------------

Create a daily output that includes for all 50 stocks:

- ticker
- latest data date
- Close
- SMA10
- SMA20
- prior-day SMA10
- prior-day SMA20
- ATR14
- ATR%
- prior-20-session max ATR%
- ATR contraction threshold
- V0 TRUE/FALSE
- V1 TRUE/FALSE
- sector

Create:

output/current_signal_scan.csv

Also create a concise:

output/current_signals_only.csv

containing only current V0/V1 signals.

--------------------------------------------------
PROSPECTIVE JOURNAL
--------------------------------------------------

Create a persistent file:

output/prospective_signal_journal.csv

Each new signal should be written once with:

- run date/time
- market data date
- ticker
- sector
- signal type: V0 or V1
- feature values at signal time
- next-open entry date once available
- next-open entry price once available
- outcome status: PENDING / COMPLETE
- exit date once available
- stock return
- SPY return
- excess return

Important:

- Never overwrite the original signal-date features.
- Never backfill a signal that was not recorded prospectively unless clearly labeled HISTORICAL/RETROSPECTIVE.
- Avoid duplicate signal records.
- Outcomes may be appended only after the full 10-trading-interval window exists.
- Preserve the exact frozen methodology.

--------------------------------------------------
RUN COMMAND
--------------------------------------------------

Create one simple reproducible command for the user, for example:

python -m src.run_signal_engine

or an equally simple equivalent.

The command should:

1. fetch/update Yahoo Finance data
2. validate data
3. calculate frozen V0/V1 features
4. generate current scan
5. append genuinely new signals to the prospective journal
6. update previously pending outcomes when enough time has passed
7. print a concise terminal summary

Do not require manual editing of code between runs.

--------------------------------------------------
SAFETY / INTERPRETATION
--------------------------------------------------

The terminal output and documentation must clearly state:

- these are research signals, not investment recommendations
- no strategy was validated
- V0/V1 failed to demonstrate a robust edge in the historical experiment
- the purpose of the journal is to collect new out-of-sample evidence

--------------------------------------------------
TESTS
--------------------------------------------------

Add tests for:

- no duplicate journal entries
- pending outcomes remain unchanged until complete
- original signal features are immutable
- V1 remains a subset of V0
- new runs do not rewrite historical signals
- run command is reproducible

Keep the implementation simple.

--------------------------------------------------
DOCUMENTATION
--------------------------------------------------

Update:

RESEARCH_LOG.md
PROMPTS.md

Record that Chapter 7 is now about BUILDING THE SYSTEM, not claiming success.

Do not yet create the public GitHub README/START_HERE package. That comes later.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
Can we turn failed-but-useful research into a repeatable system that gathers new evidence?

WHAT WE DID:
3-5 short bullets.

WHAT WE BUILT:
Name the run command, current-signal outputs, and prospective journal.

WHAT THIS SYSTEM DOES NOT CLAIM:
One short statement about why this is not a validated strategy.

WHAT COULD BE WRONG:
Remaining operational/data limitations.

THE NEXT CLUE:
Run the frozen engine on the latest available market data and show what it says today.

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Engine and tests; initial live run deferred.

## Prompt 12

**PROMPT NUMBER:** 12

**CHAPTER / STAGE:** First live run

**PURPOSE:** Run exact engine and monitor

**SOURCE:** Original conversation message; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 3541

**ORIGINAL SHA-256:** `d21ec130d2e7825cfed591d91e56a19e4c114aa602859c1dcc5c09725d4349eb`

### FULL ORIGINAL PROMPT — VERBATIM

````text
Run the frozen research signal engine on the latest available market data.

Do NOT change any methodology.
Do NOT optimize anything.
Do NOT create V2.
Do NOT reinterpret historical results.

Use the exact frozen V0/V1 definitions and the command-line engine we just built.

---

## PRIMARY TASK

Run:

python -m src.run\_signal\_engine

using the latest Yahoo Finance data available.

Then inspect:

output/current\_signal\_scan.csv
output/current\_signals\_only.csv
output/prospective\_signal\_journal.csv

---

## REPORT TODAY'S STATE

Tell me:

1. Latest market-data date used

2. Whether all 50 stocks plus SPY updated successfully

3. Number of current:

   - V0 signals
   - V1 signals

4. List every current V0 signal

5. List every current V1 signal

6. For each current signal show:

   - ticker
   - sector
   - Close
   - SMA10
   - SMA20
   - ATR%
   - prior-20 maximum ATR%
   - whether ATR contraction is satisfied
   - signal type

7. Show a concise Top 10 WATCHLIST even if fewer than 10 stocks have active signals.

The watchlist should NOT invent a new score.

Use only frozen information to order it.

Order priority:

A. current V1 signals first
B. current V0-only signals next
C. if fewer than 10 active signals exist, fill remaining spots using stocks closest to a bullish SMA10/SMA20 crossover, measured by the percentage gap between SMA10 and SMA20

Clearly label non-signals as:

NEAR SIGNAL — NOT ACTIVE

This watchlist is for educational monitoring only.

---

## PROSPECTIVE JOURNAL

Confirm whether any genuinely new current signals were appended to:

output/prospective\_signal\_journal.csv

Report:

- new records added
- duplicates prevented
- pending outcomes
- completed outcomes if any

Do not backfill anything that was not previously recorded prospectively.

---

## DATA / OPERATIONAL CHECK

Report any:

- failed downloads
- stale tickers
- missing observations
- calendar issues
- data corrections
- journal issues

If Yahoo Finance has not yet published today's final daily bar, use the most recent completed daily bar and state that clearly.

---

## INTERPRETATION

Do NOT call any current stock a recommendation.

Do NOT imply that the current signal has a validated edge.

The key message is:

We started with an idea, tested it, discovered that it was not robust, refused to overfit it, and still built a system capable of collecting new evidence prospectively.

---

## OUTPUTS

Ensure these are current and saved:

output/current\_signal\_scan.csv
output/current\_signals\_only.csv
output/prospective\_signal\_journal.csv

Create:

output/current\_watchlist\_top10.csv

---

## DOCUMENTATION

Update:

RESEARCH\_LOG.md
PROMPTS.md

Record the first live/prospective engine run exactly as it occurred.

---

## VIDEO SUMMARY

End with:

VIDEO SUMMARY

THE QUESTION:
What does our frozen research system say today?

WHAT WE DID:
3-5 short bullets.

WHAT WE FOUND:
State:

- latest data date
- number of V0 signals
- number of V1 signals
- active signal tickers
- Top 10 watchlist

WHAT WAS ADDED TO THE JOURNAL:
State whether any genuinely prospective signals were recorded.

WHAT THIS MEANS:
One short paragraph explaining that this is a live research output, not a validated trading recommendation.

WHAT COULD BE WRONG:
Any operational or data warnings.

THE NEXT CLUE:
How do we package the entire experiment so viewers can clone it, inspect it, and use it as the starting point for their own treasure hunt?

Keep the VIDEO SUMMARY short enough for one screen.

Then STOP.

````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* 3 V0 / 2 V1; five retrospective records, no new prospective evidence.

## Prompt 13

**PROMPT NUMBER:** 13

**CHAPTER / STAGE:** Public educational release

**PURPOSE:** Make the project understandable and runnable

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 8243

**ORIGINAL SHA-256:** `5743b37400f70ad535d7064ea4889a534dfd0175f05ae2f8becf01a13e660ab4`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have completed the research experiment and the first live run of the frozen research engine.

The project now contains:

- a defined research question
- a Research Constitution
- a complete Research Log
- a chronological prompt history
- GitHub-derived V0 baseline
- human-added V1 ATR hypothesis
- frozen specifications
- historical backtest
- robustness testing
- failure analysis
- prospective research engine
- current signal scan
- current watchlist
- prospective journal framework

The research conclusion is:

NO VERSION HAS DEMONSTRATED A ROBUST TRADING EDGE.

V0 and V1 remain educational/research signals only.

Now prepare this project to be published as a clean public GitHub repository for viewers of the video.

--------------------------------------------------
PRIMARY GOAL
--------------------------------------------------

A viewer should be able to:

1. Find this repository on GitHub.
2. Understand what the experiment was trying to do.
3. Understand what we found.
4. Understand what failed.
5. See every major prompt.
6. Inspect the research log.
7. Reproduce the research environment.
8. Run the frozen research engine.
9. Understand the limitations.
10. Use the project as a starting architecture for a different experiment.

The public repository should encourage adaptation and learning rather than blind copying of the trading signal.

--------------------------------------------------
CREATE README.md
--------------------------------------------------

Create a polished public README.md.

It should include:

TITLE:
AI Treasure Hunt — Building a Stock Research Signal With Codex

SUBTITLE / PURPOSE:
A transparent educational experiment showing how to go from an idea to a tested, challenged, repeatable research system using AI and open-source tools.

Include sections:

1. WHY THIS PROJECT EXISTS

Explain:
- curiosity
- experimentation
- not reinventing the wheel
- learning from failure
- empowerment and agency
- the goal is to learn how to investigate ideas, not to copy a trading signal

2. THE RESEARCH QUESTION

Explain simply:
Can a bullish moving-average crossover produce better subsequent 10-trading-day relative outcomes when preceded by meaningful ATR contraction?

3. WHAT CAME FROM GITHUB

Explain:
- V0 originated from an open-source moving-average crossover concept
- GitHub popularity was treated as software adoption, not evidence of alpha
- list and attribute the specific repository/concept we used
- include licensing/attribution notes

4. WHAT WE ADDED

Explain:
- V1 was the human research hypothesis
- ATR contraction rule
- why it was conceptually interesting

5. WHAT HAPPENED

Summarize accurately:
- V0 results
- V1 first-pass results
- robustness failure
- long-term-trend diagnostic
- decision not to promote a strategy

Do not cherry-pick.

6. WHAT WE BUILT

Explain:
- frozen signal engine
- current scan
- current signals
- watchlist
- prospective journal

7. HOW TO RUN IT

Give simple reproducible setup instructions.

Prefer:

python -m venv ...
pip install -r requirements-engine.txt
python -m src.run_signal_engine

Adapt commands appropriately for Windows/macOS if necessary.

8. IMPORTANT LIMITATIONS

Clearly include:
- fixed hand-selected stock universe
- one recent year
- overlapping outcomes
- retrospective vendor revisions
- idealized execution
- no validated edge
- educational use only

9. PROJECT STRUCTURE

Explain the important files/folders.

10. START YOUR OWN TREASURE HUNT

Point viewers to:
START_HERE.md
PROMPTS.md
SOCRATES_MODE.md

Use the line:

“Don’t copy my treasure hunt. Start your own.”

--------------------------------------------------
CREATE START_HERE.md
--------------------------------------------------

Create a very simple beginner-friendly guide.

Assume the viewer may:

- have never used GitHub
- have never used Codex
- not know Python
- not know what a repository is

Explain in plain English:

WHAT THIS IS

WHAT YOU CAN DO WITH IT

HOW TO CLONE / DOWNLOAD IT

HOW TO OPEN THE FOLDER IN AN AI CODING ENVIRONMENT

HOW TO ASK THE AI TO EXPLAIN THE PROJECT

HOW TO RUN THE EXISTING SYSTEM

HOW TO CHANGE THE QUESTION RATHER THAN COPY THE SIGNAL

Include example adaptation ideas such as:

- ETFs
- mutual funds
- different stock universes
- different horizons
- earnings revisions
- crypto
- risk analysis

Do NOT encourage unvalidated live trading.

--------------------------------------------------
PROMPTS.md
--------------------------------------------------

Review PROMPTS.md.

Ensure it contains the major prompts in chronological order and is readable by a viewer.

For each major prompt, include:

- Prompt number
- Stage/chapter
- Purpose
- Full prompt or sufficiently complete original instruction
- brief result/decision

Do not rewrite history.

Preserve failed paths and human overrides.

--------------------------------------------------
RESEARCH_LOG.md
--------------------------------------------------

Review for public readability.

Do not delete technical details, failures, or unattractive results.

Add a brief navigation/table of contents if useful.

--------------------------------------------------
FROZEN_SPECIFICATION.md
--------------------------------------------------

Ensure the specification is clear enough for an independent reader to reproduce V0 and V1 exactly.

--------------------------------------------------
PUBLIC SAFETY / CLEANUP
--------------------------------------------------

Audit the entire repository for:

- usernames
- local filesystem paths
- credentials
- API keys
- tokens
- private files
- machine-specific cache paths
- temporary outputs that should not be public
- oversized data files
- unnecessary generated artifacts

Add or update .gitignore appropriately.

Do NOT delete research records needed for transparency.

Do not include large cached Yahoo data files in the public repository unless there is a strong reproducibility reason and licensing permits it.

Prefer code that fetches data itself.

--------------------------------------------------
LICENSE / ATTRIBUTION
--------------------------------------------------

Review the licenses of any third-party code or concepts we adapted.

Do not publish copied third-party code in violation of its license.

Create:

THIRD_PARTY_NOTICES.md

Include:
- repository/project
- URL
- license
- what was used/adapted
- required attribution

If our own repository needs a license, recommend an appropriate simple open-source license, but do not choose one silently if legal ambiguity exists.

--------------------------------------------------
REPRODUCIBILITY CHECK
--------------------------------------------------

From a clean-environment perspective, verify that a new user could understand how to install and run the project.

Do not need to create a new machine, but inspect for hidden dependencies or assumptions.

--------------------------------------------------
DOCUMENTATION
--------------------------------------------------

Update:

RESEARCH_LOG.md
PROMPTS.md

Record that the repository was prepared for public educational release.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
Can someone else understand, reproduce, and extend the entire experiment?

WHAT WE DID:
3-5 short bullets.

WHAT VIEWERS NOW GET:
List:
- code
- prompts
- research log
- frozen methodology
- current research engine
- public documentation

WHAT WE ARE NOT GIVING THEM:
One sentence explaining that this is not a validated trading strategy or recommendation.

WHAT STILL NEEDS TO HAPPEN:
State what remains before the repository can actually be uploaded/published on GitHub.

THE NEXT CLUE:
Build Socrates Mode so the repository helps viewers discover THEIR question instead of simply copying ours.

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Public docs, notices and clean-checkout compatibility; publication/license pending.

## Prompt 14

**PROMPT NUMBER:** 14

**CHAPTER / STAGE:** Socrates Mode

**PURPOSE:** Help viewers discover their own question before code

**SOURCE:** Original submitted text attachment; authoritative source recovered and compared in full.

**VERIFICATION STATUS:** VERBATIM VERIFIED

**PRIVACY REDACTIONS:** NONE

**ORIGINAL UTF-8 BYTES:** 7148

**ORIGINAL SHA-256:** `ebf99753e6cc1e257dd9d1e103c2310ec6507a85e21f58f75dab2ac9c6b1bdfe`

### FULL ORIGINAL PROMPT — VERBATIM

````text
We have now completed the research experiment and prepared the project for public GitHub release.

The final task is to build:

SOCRATES_MODE.md

This is one of the most important parts of the public project.

The goal is NOT to help viewers reproduce my exact signal.

The goal is to help them use this repository as a starting laboratory for THEIR own curiosity.

Core philosophy:

“Don’t copy my treasure hunt. Start your own.”

and:

“Your job is not to give me treasure.
Your job is to help me become a better treasure hunter.”

--------------------------------------------------
PRIMARY GOAL
--------------------------------------------------

Create a Socratic-mode instruction that a viewer can paste into Codex or another AI coding environment after cloning this repository.

The AI should NOT immediately build anything.

It should first interview the viewer and help them turn vague curiosity into a testable research question.

The process should encourage:

- curiosity
- systems thinking
- experimentation
- simplicity
- falsifiability
- awareness of bias
- willingness to fail
- learning from failure
- reuse of existing open-source tools
- agency

--------------------------------------------------
SOCRATES MODE BEHAVIOR
--------------------------------------------------

The AI should begin by saying, in plain English, that it will help the user discover what they want to investigate before writing code.

Then ask ONE question at a time.

Do not dump 20 questions at once.

Use follow-up questions based on the user’s answers.

The interview should eventually clarify:

1. What are you curious about?

2. What market, asset class, business problem, or real-world system interests you?

3. Are you trying to:
   - predict something
   - compare things
   - identify change
   - understand risk
   - rank opportunities
   - automate a process
   - or answer another kind of question?

4. What time horizon matters?

5. What data could realistically be accessed?

6. What would count as a useful outcome?

7. What assumptions are you making?

8. What could fool us?

9. What existing GitHub/open-source tools might already solve part of the problem?

10. What is the simplest version of the experiment we could run first?

11. How could we fail cheaply and learn quickly?

12. What evidence would cause us to reject the hypothesis?

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------

Socrates Mode must:

- NOT propose a strategy before interviewing the user
- NOT optimize for profitability
- NOT assume the user’s first question is the best question
- challenge vague language
- identify hidden assumptions
- explicitly ask what could prove the user wrong
- prefer a small first experiment over an elaborate system
- recommend existing open-source tools before reinventing basic infrastructure
- distinguish software popularity from evidence that an idea works
- stop before implementation and ask the user to approve the research question

The AI should behave like:

- a curious research partner
- a skeptical scientist
- a systems thinker
- an entrepreneurial collaborator

NOT like:
- a salesperson
- a guru
- a signal vendor
- an answer machine

--------------------------------------------------
THE SOCRATIC OUTPUT
--------------------------------------------------

Once the interview is complete, produce:

TREASURE HUNT BRIEF

THE QUESTION:
A precise, testable research question.

WHY IT MATTERS:
Why the user is curious about it.

THE SIMPLEST EXPERIMENT:
The smallest useful first test.

WHAT WE NEED:
Data, tools, and assumptions.

WHAT COULD FOOL US:
Major biases or failure modes.

WHAT WOULD PROVE US WRONG:
Clear falsification criteria.

OPEN-SOURCE BUILDING BLOCKS:
What we should look for on GitHub before building from scratch.

FAIL CHEAPLY PLAN:
How to test the idea with minimal cost and complexity.

NEXT DECISION:
The one thing the user should approve before any code is written.

Then STOP.

Do NOT implement anything until the user approves the brief.

--------------------------------------------------
EXAMPLES
--------------------------------------------------

Inside SOCRATES_MODE.md, include a few concise examples showing how the same lab could be adapted to:

- ETFs
- mutual funds
- earnings revisions
- crypto
- portfolio risk
- a business/customer problem
- something completely outside finance

The examples should show different questions, not complete solutions.

--------------------------------------------------
BEGINNER-FRIENDLY USE
--------------------------------------------------

Add a section:

HOW TO USE SOCRATES MODE

Explain:

1. Clone/download the repo.
2. Open it in Codex or another AI coding environment.
3. Open SOCRATES_MODE.md.
4. Tell the AI:

   “Use SOCRATES_MODE.md and interview me before building anything.”

5. Answer the questions honestly.
6. Approve the TREASURE HUNT BRIEF before implementation.

Keep this simple enough for someone who has never used GitHub before.

--------------------------------------------------
AGENCY / EMPOWERMENT
--------------------------------------------------

Include a short final section explaining the philosophy:

Empowerment:
“I can figure this out.”

Agency:
“I can actually do something about it.”

AI lowers the cost of trying.

Failure becomes useful when it teaches you something.

The point of the repository is to help the viewer move from consuming answers to investigating questions.

Use this closing line:

“Same tools. New questions. Your treasure hunt.”

--------------------------------------------------
FINAL REPOSITORY REVIEW
--------------------------------------------------

After creating SOCRATES_MODE.md:

- update README.md to link to it prominently
- update START_HERE.md to explain how to use it
- update PROMPTS.md
- update RESEARCH_LOG.md

Do a final repository audit for:

- missing links
- unclear instructions
- private information
- machine-specific paths
- unnecessary files
- reproducibility problems

Do NOT publish anything yet.

--------------------------------------------------
VIDEO SUMMARY
--------------------------------------------------

End with:

VIDEO SUMMARY

THE QUESTION:
Can this repository help someone discover and investigate their own question?

WHAT WE DID:
3-5 short bullets.

WHAT SOCRATES MODE DOES:
Explain the interview → research brief → user approval flow.

WHY THIS MATTERS:
One short paragraph connecting curiosity, failure, empowerment and agency.

WHAT VIEWERS CAN DO NEXT:
Explain how they can clone the repo and start their own experiment.

WHAT STILL NEEDS TO HAPPEN:
State the final steps required before public GitHub publication.

FINAL MESSAGE:
“Don’t copy my treasure hunt. Start your own.”

Keep the entire VIDEO SUMMARY short enough for one screen.

Then STOP.
````

### RESULT / DECISION

*Editorial summary, separate from the original prompt:* Pasteable interview → research brief → explicit approval; no publication.

## Verification table

| Prompt | Status | Authoritative source | Privacy redactions |
| --- | --- | --- | --- |
| Prompt 1 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 2 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 3 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 4 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 5 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 6 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 7 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 8 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 9 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 10 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 11 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 12 | VERBATIM VERIFIED | Original conversation message | NONE |
| Prompt 13 | VERBATIM VERIFIED | Original submitted text attachment | NONE |
| Prompt 14 | VERBATIM VERIFIED | Original submitted text attachment | NONE |

**ALL 14 ORIGINAL PROMPTS VERIFIED FOR PUBLICATION: YES**

Verified: **14 / 14**. Original sources required: **NONE**. Privacy redactions: **NONE**. This verification clears the full-prompt publication requirement; separate license and GitHub-publication approvals remain outstanding.
