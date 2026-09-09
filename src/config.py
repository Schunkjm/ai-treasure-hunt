"""Preregistered settings. Changes require a research-log amendment."""

UNIVERSE = tuple("""AAPL MSFT NVDA AMZN GOOGL META AVGO AMD ORCL CRM
JPM BAC GS MS V MA XOM CVX COP SLB CAT GE RTX ETN HON DE WMT COST HD MCD
NKE SBUX LLY UNH JNJ ABBV MRK NFLX DIS T VZ TSLA QCOM TXN IBM AMAT MU
LOW PEP KO""".split())
BENCHMARK = "SPY"
FAST = 10
SLOW = 20
ATR_PERIOD = 14
CONTRACTION_LOOKBACK = 20
CONTRACTION_MULTIPLIER = 0.80
HORIZON = 10
# Frozen before downloading or inspecting outcomes, after the Sep 8 close.
HISTORY_START = "2025-03-08"
AS_OF = "2026-09-08"
DOWNLOAD_END_EXCLUSIVE = "2026-09-09"
EVALUATION_START = "2025-09-08"
DATA_SETTINGS = dict(interval="1d", auto_adjust=False, back_adjust=False,
                     actions=True, repair=False, keepna=True, prepost=False,
                     rounding=False)
METRICS = {
    "primary": "arithmetic_mean_signal_excess_return",
    "secondary": ["median_signal_excess_return", "hit_rate_excess_strictly_positive", "signal_sample_size"],
    "weighting": "equal_weight_per_measurable_stock_signal",
    "return_units": "fractions; multiply by 100 for percentage-point display",
    "comparison": "all_V0_vs_V1_subset_same_endpoints",
}
# Regular full-day exchange closures within this bounded snapshot span.
# Half days remain sessions. Source and limitation: PIPELINE.md.
HOLIDAYS = (
    "2025-04-18", "2025-05-26", "2025-06-19", "2025-07-04",
    "2025-09-01", "2025-11-27", "2025-12-25", "2026-01-01",
    "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
    "2026-06-19", "2026-07-03", "2026-09-07",
)
