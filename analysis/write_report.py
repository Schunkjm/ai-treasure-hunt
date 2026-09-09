"""Publish the first observed results and append them to the audit log."""
from pathlib import Path
import hashlib
import json
import pandas as pd
from src.frozen import verify_freeze

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"


def table(frame, digits=6):
    def cell(value):
        if pd.isna(value):
            return "n/a"
        if isinstance(value, float):
            return f"{value:.{digits}f}"
        return str(value)
    lines = ["| " + " | ".join(frame.columns) + " |", "| " + " | ".join(["---"] * len(frame.columns)) + " |"]
    lines += ["| " + " | ".join(cell(x) for x in row) + " |" for row in frame.itertuples(index=False, name=None)]
    return "\n".join(lines)


def main():
    verify_freeze()
    summary = pd.read_csv(OUT / "v0_v1_summary.csv").set_index("version")
    monthly = pd.read_csv(OUT / "v0_v1_monthly.csv")
    sector = pd.read_csv(OUT / "v0_v1_sector.csv")
    stocks = pd.read_csv(OUT / "v0_v1_stocks.csv")
    extremes = pd.read_csv(OUT / "v0_v1_extremes.csv")
    difference = pd.read_csv(OUT / "v0_v1_difference.csv")
    manifest = json.loads((OUT / "v0_v1_evaluation_manifest.json").read_text())
    headline = summary.T.reset_index(names="Metric")
    def group_table(frame, field):
        return frame[[field, "V0_signal_count", "V0_average_excess_return_pp", "V1_signal_count", "V1_average_excess_return_pp"]]
    report = """# First legitimate V0 versus V1 comparison

Observed on 2026-09-08. **Descriptive classification: MIXED.**

The ATR filter improves the average excess return, but worsens the median and hit rate, removes 82.83% of completed signals, and leaves a result sensitive to a few outcomes and sector composition. It does not establish a validated trading strategy, statistical proof, or a recommendation to trade.

## Population and integrity

Used the unchanged frozen 2025-09-08 through 2026-09-08 evaluation window and the corrected, locked Yahoo snapshot. Only complete next-open through t+11-open outcomes are included. Latest possible mature signal date is 2026-08-21. V0 has 343 detected events: 332 completed and 11 pending. V1 has 62 detected events: 57 completed and 5 pending. No missing-endpoint events and no unknown ATR classifications occur among evaluated events. Pending observations are retained in the signals file and excluded from statistics, never treated as zero or failures.

Before evaluation, verified all frozen-file hashes and saved-output hashes. Independently recomputed saved labels from the frozen adjusted stock/SPY endpoint opens and checked dates, differences, duplicates, sectors, and evaluation inclusion. Group counts/contributions reconcile to the totals, and mean excess equals mean stock minus mean benchmark. Three new synthetic reporting tests passed. Frozen parameters, sector mapping, source data, source code, tests and specification remained unchanged. This new evaluator lives separately in analysis/ and is not V2.

Additional reporting conventions were stated before the first calculation: equal weight per completed stock-signal; linear-interpolated percentiles; sample standard deviation (ddof=1); strictly positive returns for hit/positive-absolute rates; best/worst reported for both excess and stock returns. These descriptive additions were explicitly requested in this stage and do not change the frozen primary metric. matplotlib 3.10.7, already installed, was used only for the requested static charts. CSVs use the existing pandas implementation; no workbook or strategy framework was introduced.

## Complete headline results

Return columns ending in pct are percentages. Excess-return columns ending in pp are percentage points. Hit/positive-return rates are percentages. Counts are integers. Statistics below are displayed to six decimals; CSV outputs retain 15 significant digits. Blank CSV statistics mean unavailable, not zero.

""" + table(headline) + "\n\n## V1 minus V0\n\n" + table(difference) + """

The mean improves by +0.744309 pp; the median worsens by −0.196789 pp and hit rate by −1.125555 percentage points. The filter retains 17.168675% of completed V0 signals. On detected signals including pending events, it retains 62 of 343 and removes 281 (81.924198%); the primary count comparison is based on completed outcomes only.

V1's average stock return increases only about 0.273057 pp, while its matched SPY average is about 0.471251 pp lower. SPY's two averages differ because the filter selects different stock-signal dates. These are signal-weighted benchmark returns, not SPY's return over the whole year; the difference helps explain the larger excess-return change.

## Distribution and individual outcomes

V0's middle 50% spans −4.791084 to +3.626756 pp; V1's spans −4.609197 to +3.979292 pp. Both medians are negative. V1's dispersion is larger (7.860473 versus 7.070080 pp sample standard deviation). The mean therefore does not describe a typical successful signal or a uniform distributional improvement.

""" + table(extremes) + """

The best V1 event is QCOM's 2026-04-16 signal, +28.908575 pp excess return. Removing that single event from V1 as an influence diagnostic changes its mean to −0.154410 pp (56 events). The reported headline remains +0.355467 pp with all 57 events. This diagnostic does not authorize discarding the event or selecting rules around it. Large positive and negative events warrant independent data review before interpreting them as economic effects.

Excess-return empirical distributions (generated chart not distributed; local path: `output/v0_v1_distribution.png`)

The curves show cumulative shares on their full observed ranges, without a fitted distribution or tail trimming. V0 includes V1; the curves are not independent samples.

## Monthly signal cohorts

""" + table(group_table(monthly, "signal_month")) + """

September 2025 is a partial beginning month. August 2026 ends at the last mature signal date. September 2026 has no completed outcomes. A zero count is not a zero-return month. V1 has a higher monthly mean in only 4 of the 10 months with completed observations in both groups. Several V1 month counts are just 1–3; do not treat these as reliable monthly effects.

The largest positive V1 contribution months are September 2025 (one signal, about +17.998463 pp summed excess) and December 2025 (16 signals, about +16.867907 pp summed excess). Together their summed contribution exceeds V1's net total because other months offset it. Excluding those same two months from both groups, solely as a concentration diagnostic, leaves V1 at −0.365119 pp (40 signals) and V0 at −0.891304 pp (276 signals). Thus the positive sign of V1's mean is sensitive to these months, but its relative mean advantage persists in that diagnostic.

Removing any single month leaves V1's mean above V0's. Its positive mean becomes very small when September 2025, December 2025, or July 2026 is individually omitted. This supports caution about the level and tails, not a claim that one month alone explains the entire relative mean difference.

Monthly cohorts (generated chart not distributed; local path: `output/v0_v1_monthly.png`)

## Sector consistency

""" + table(group_table(sector, "sector")) + """

Information Technology contributes 27 of 57 V1 signals (47.368421%), compared with 84 of 332 V0 signals (25.301205%). Excluding that same sector from both groups changes the remaining means to V1 −0.527616 pp (30 signals) versus V0 −0.392540 pp (248 signals), reversing the mean ordering by −0.135076 pp. The apparent aggregate advantage is therefore sensitive to IT composition.

Energy has the strongest V1 sector mean, +5.394960 pp, from only six events. Without Energy, V1's mean becomes −0.237414 pp versus V0 −0.557858 pp: its positive sign disappears, although the relative advantage remains. Information Technology and Energy provide positive contributions that offset substantial negative contributions elsewhere, notably Industrials. V1 sector samples range from 2 to 27; even the largest is limited and dependent. All sector rows are shown, with sparse samples explicitly treated as descriptive only.

## Stock concentration

Most V0 signals: NVDA, AVGO, ETN, MRK and IBM tie at nine each. Most V1 signals: AMD, QCOM and MU tie at four each; IBM and AMAT follow at three each. Counts below include only complete outcomes.

Largest positive summed excess contributions: V0 — AMD +60.150191 pp, AMAT +30.953553 pp, QCOM +23.270164 pp, XOM +20.731276 pp, MU +17.561763 pp. V1 — QCOM +31.241333 pp, AMD +19.166693 pp, XOM +18.708027 pp, TSLA +11.803365 pp, CVX +8.316858 pp.

Largest negative summed excess contributions: V0 — IBM −46.305842 pp, ORCL −40.597093 pp, META −39.048234 pp, WMT −27.768010 pp, AVGO −26.183430 pp. V1 — RTX −15.776880 pp, NKE −10.309093 pp, META −9.151811 pp, MSFT −9.058891 pp, CAT −8.150876 pp.

These sums are additive diagnostics over overlapping events, NOT portfolio returns or compounded wealth. A stock's contribution to the overall mean is its summed excess divided by the whole strategy sample count. Removing QCOM as a diagnostic makes V1's mean −0.207164 pp; removing AMD or XOM leaves means of about +0.020659 or +0.028247 pp. These results identify influence, not stocks to drop.

The largest V1 count on any one signal date is three, occurring on 2026-01-05, 2026-08-17 and 2026-08-21. Low same-date counts do not make overlapping ten-interval outcomes independent.

The following complete stock table retains every stock, including those with no V1 signals. Zero summed contribution for an empty group is an additive identity; its mean remains unavailable.

""" + table(stocks[["ticker", "V0_signal_count", "V1_signal_count", "V0_average_excess_return_pp", "V1_average_excess_return_pp", "V0_sum_excess_return_pp_not_portfolio", "V1_sum_excess_return_pp_not_portfolio"]]) + """

## Classification and limits

**MIXED.** The primary mean improves, but the median, hit rate, absolute-positive rate and sample size move unfavorably, while dispersion increases. The favorable mean depends on influential events and sector composition. No numerical economic-materiality threshold or statistical test was preregistered, so neither significance nor a validated edge is claimed.

The experiment uses one recent year, a selected fixed universe, retrospective Yahoo prices, one documented source repair, static sector labels, idealized opening prints, and gross outcomes without execution costs. V1 is a nested subset of V0 and events overlap. The 57 V1 signals are not 57 independent trials. The same period is now observed and must not later be described as untouched out-of-sample evidence.

Next proposed stage, not run here: independently audit influential price events, then challenge whether the relative result survives comparisons that account for sector/date composition and dependence. Keep the frozen signal unchanged. No V2, threshold search, parameter changes, or recommendation to trade.

## Reproducibility and output files

Evaluator: analysis/first_comparison.py. Synthetic reporting tests: analysis/test_first_comparison.py. Existing first-pass outputs cannot be overwritten by its command. Primary CSVs: output/v0_v1_summary.csv, output/v0_v1_monthly.csv, output/v0_v1_sector.csv, output/v0_v1_signals.csv. Additional diagnostics: output/v0_v1_difference.csv, output/v0_v1_stocks.csv, output/v0_v1_dates.csv, output/v0_v1_extremes.csv, output/v0_v1_influence.csv. The signals file retains pending events, membership flags, inclusion flags, and original fractional return columns. Aggregated CSV return units are explicitly pct/pp.

The evaluation manifest records the timestamp, frozen manifest/lock hashes, evaluator hash, percentile/dispersion conventions, and verification status. FIRST_PASS_RESULTS.md and the appended research-log entry provide a public-safe narrative and complete stock/month/sector results; vendor and generated data files remain gitignored under the existing publication policy.
"""
    report_path = ROOT / "FIRST_PASS_RESULTS.md"
    if report_path.exists():
        raise RuntimeError("First observed report already exists")
    report_path.write_text(report, encoding="utf-8")
    log = ROOT / "RESEARCH_LOG.md"
    with log.open("a", encoding="utf-8") as handle:
        handle.write("\n\n## 2026-09-08 — FIRST legitimate performance comparison: MIXED\n\n")
        handle.write("User authorization: Prompt 007. Complete first-pass report follows; frozen definitions and inputs were not changed. Earlier statements that no performance had been viewed describe earlier stages and are superseded by this explicitly authorized evaluation.\n\n")
        # Keep the chronological log readable without duplicated top-level headings.
        handle.write(report.replace("# First legitimate V0 versus V1 comparison", "### First observed results", 1).replace("\n## ", "\n#### "))
    manifest["classification"] = "MIXED"
    manifest["classification_basis"] = "Mean improves; median and hit rate worsen, sample shrinks, influential events/sector sensitivity"
    manifest["report_writer_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest["report_sha256"] = hashlib.sha256(report_path.read_bytes()).hexdigest()
    manifest["reported_output_sha256"] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob("v0_v1_*")) if p.suffix in (".csv", ".png")}
    (OUT / "v0_v1_evaluation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    verify_freeze()
    print("Report and complete research-log entry written. Frozen infrastructure unchanged.")


if __name__ == "__main__":
    main()
