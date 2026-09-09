"""First authorized descriptive evaluation. Does not modify frozen files.

Run from repository root: python -m analysis.first_comparison
No threshold search, parameter options, universe changes, or new signals.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from src.config import UNIVERSE, EVALUATION_START, AS_OF
from src.frozen import verify_freeze, load_sectors
from src.data import expected_sessions

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output/frozen_2026-09-08"
OUTPUT = ROOT / "output"
EXCESS = "forward_10d_excess_return"
STOCK = "stock_forward_return"
SPY = "spy_forward_return"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(frame):
    """All return columns in reporting tables use percent / percentage points."""
    n = len(frame)
    e = frame[EXCESS]
    return {
        "signal_count": n,
        "average_stock_return_pct": frame[STOCK].mean() * 100,
        "average_spy_return_pct": frame[SPY].mean() * 100,
        "average_excess_return_pp": e.mean() * 100,
        "median_excess_return_pp": e.median() * 100,
        "hit_rate_pct": (e.gt(0).sum() / n * 100) if n else np.nan,
        "positive_stock_return_pct": (frame[STOCK].gt(0).sum() / n * 100) if n else np.nan,
        "q25_excess_return_pp": e.quantile(.25, interpolation="linear") * 100,
        "q75_excess_return_pp": e.quantile(.75, interpolation="linear") * 100,
        "std_excess_return_pp": e.std(ddof=1) * 100,
        "best_excess_return_pp": e.max() * 100,
        "worst_excess_return_pp": e.min() * 100,
        "best_stock_return_pct": frame[STOCK].max() * 100,
        "worst_stock_return_pct": frame[STOCK].min() * 100,
        "sum_excess_return_pp_not_portfolio": e.sum() * 100 if n else 0.,
    }


def load_events():
    verify_freeze()
    manifest = json.loads((SOURCE / "manifest.json").read_text())
    for relative, expected in manifest["output_sha256"].items():
        if sha(SOURCE / relative) != expected:
            raise ValueError(f"Frozen output altered: {relative}")
    sectors = load_sectors()
    pieces = []
    sessions = expected_sessions()
    benchmark = pd.read_csv(SOURCE / "adjusted/SPY.csv", index_col="Date", parse_dates=True)
    for ticker in UNIVERSE:
        f = pd.read_csv(SOURCE / "events" / f"{ticker}.csv",
                        parse_dates=["Date", "entry_date", "exit_date"],
                        dtype={"v0": "boolean", "v1": "boolean", "atr_contracted": "boolean"})
        f["ticker"] = ticker
        if f.Date.duplicated().any() or not f.v0.all() or not f.sector.eq(sectors[ticker]).all():
            raise ValueError(f"Event identity mismatch: {ticker}")
        if not f.Date.between(pd.Timestamp(EVALUATION_START), pd.Timestamp(AS_OF)).all():
            raise ValueError("Signal outside frozen evaluation period")
        available = f.outcome_status.eq("available")
        finite = np.isfinite(f[[STOCK, SPY, EXCESS]]).all(axis=1)
        if not available.equals(finite):
            raise ValueError("Outcome status and finite labels disagree")
        f["included_in_evaluation"] = available & f.entry_date.ge(pd.Timestamp(EVALUATION_START)) & f.exit_date.le(pd.Timestamp(AS_OF))
        if not f.loc[available, "included_in_evaluation"].all():
            raise ValueError("Available outcome outside evaluation window")
        # Independent check of saved labels against frozen price endpoints.
        a = f.loc[available]
        stock = pd.read_csv(SOURCE / "adjusted" / f"{ticker}.csv", index_col="Date", parse_dates=True)
        entry = pd.DatetimeIndex(a.entry_date)
        exit_ = pd.DatetimeIndex(a.exit_date)
        t = sessions.get_indexer(pd.DatetimeIndex(a.Date))
        np.testing.assert_array_equal(sessions.get_indexer(entry), t + 1)
        np.testing.assert_array_equal(sessions.get_indexer(exit_), t + 11)
        expected_stock = stock.Open.reindex(exit_).to_numpy() / stock.Open.reindex(entry).to_numpy() - 1
        expected_spy = benchmark.Open.reindex(exit_).to_numpy() / benchmark.Open.reindex(entry).to_numpy() - 1
        np.testing.assert_allclose(a[STOCK], expected_stock, rtol=1e-12, atol=1e-14)
        np.testing.assert_allclose(a[SPY], expected_spy, rtol=1e-12, atol=1e-14)
        np.testing.assert_allclose(a[EXCESS], expected_stock - expected_spy, rtol=1e-12, atol=1e-14)
        pieces.append(f)
    events = pd.concat(pieces, ignore_index=True).sort_values(["Date", "ticker"]).reset_index(drop=True)
    if events.duplicated(["ticker", "Date"]).any():
        raise ValueError("Duplicate stock-signal observations")
    events["signal_month"] = events.Date.dt.to_period("M").astype(str)
    return events


def grouped_results(samples, field, labels):
    rows = []
    for label in labels:
        row = {field: label}
        for name, sample in samples.items():
            group = sample.loc[sample[field].eq(label)]
            result = metrics(group)
            row.update({name + "_" + key: value for key, value in result.items()})
            row[name + "_share_of_signals_pct"] = len(group) / len(sample) * 100 if len(sample) else np.nan
            row[name + "_contribution_to_overall_mean_pp"] = group[EXCESS].sum() / len(sample) * 100 if len(sample) else np.nan
        row["V1_minus_V0_average_excess_pp"] = row["V1_average_excess_return_pp"] - row["V0_average_excess_return_pp"]
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    destination = OUTPUT / "v0_v1_summary.csv"
    if destination.exists():
        raise RuntimeError("First-pass report already exists; do not overwrite research history")
    events = load_events()
    evaluated = events.loc[events.included_in_evaluation].copy()
    samples = {"V0": evaluated, "V1": evaluated.loc[evaluated.v1.fillna(False)].copy()}
    summary_rows = []
    for name, sample in samples.items():
        detected = events if name == "V0" else events.loc[events.v1.fillna(False)]
        summary_rows.append({"version": name, **metrics(sample),
                             "detected_signals": len(detected),
                             "pending_signals": int(detected.outcome_status.eq("pending_horizon").sum()),
                             "missing_outcome_signals": int(detected.outcome_status.eq("missing_endpoint_price").sum()),
                             "atr_classification_unavailable": int(sample.atr_contracted.isna().sum())})
    summary = pd.DataFrame(summary_rows).set_index("version")
    difference = {key: summary.loc["V1", key] - summary.loc["V0", key] for key in (
        "average_excess_return_pp", "median_excess_return_pp", "hit_rate_pct")}
    difference["signals_removed"] = len(samples["V0"]) - len(samples["V1"])
    difference["signal_reduction_pct"] = 100 * (1 - len(samples["V1"]) / len(samples["V0"]))
    difference["signal_retention_pct"] = 100 - difference["signal_reduction_pct"]
    months = pd.period_range(EVALUATION_START, AS_OF, freq="M").astype(str)
    monthly = grouped_results(samples, "signal_month", months)
    sector = grouped_results(samples, "sector", sorted(load_sectors().unique()))
    stocks = grouped_results(samples, "ticker", UNIVERSE)
    dates = grouped_results(samples, "Date", sorted(evaluated.Date.unique()))
    # Observation maxima/minima, not fitted rules. Report identities and both returns.
    extremes = []
    for name, sample in samples.items():
        for column, label in ((EXCESS, "excess"), (STOCK, "stock")):
            for which in ("best", "worst"):
                if len(sample):
                    value = sample[column].max() if which == "best" else sample[column].min()
                    for _, row in sample.loc[sample[column].eq(value)].iterrows():
                        extremes.append({"version": name, "outcome": which + "_" + label,
                                         "ticker": row.ticker, "signal_date": row.Date,
                                         "entry_date": row.entry_date, "exit_date": row.exit_date,
                                         "stock_return_pct": row[STOCK] * 100,
                                         "spy_return_pct": row[SPY] * 100,
                                         "excess_return_pp": row[EXCESS] * 100})
    # Influence diagnostics requested by month/sector/stock. Headline results
    # always retain every qualifying event. No new strategy or optimization.
    influence = []
    for field, labels in (("signal_month", months), ("sector", sorted(load_sectors().unique())), ("ticker", UNIVERSE)):
        for label in labels:
            row = {"group_type": field, "omitted_group": label}
            for name, sample in samples.items():
                rest = sample.loc[~sample[field].eq(label)]
                row[name + "_remaining_count"] = len(rest)
                row[name + "_remaining_mean_excess_pp"] = rest[EXCESS].mean() * 100
            row["remaining_mean_difference_pp"] = row["V1_remaining_mean_excess_pp"] - row["V0_remaining_mean_excess_pp"]
            influence.append(row)
    top_two = monthly.loc[monthly.V1_signal_count.gt(0)].nlargest(2, "V1_sum_excess_return_pp_not_portfolio").signal_month.tolist()
    top_two_context = {"omitted_months": top_two}
    for name, sample in samples.items():
        rest = sample.loc[~sample.signal_month.isin(top_two)]
        top_two_context[name] = metrics(rest)
    # Reconciliation independent of grouped means and count weighting.
    for name, sample in samples.items():
        for table in (monthly, sector, stocks):
            assert table[name + "_signal_count"].sum() == len(sample)
            np.testing.assert_allclose(table[name + "_contribution_to_overall_mean_pp"].sum(), sample[EXCESS].mean() * 100, atol=1e-12)
        np.testing.assert_allclose(summary.loc[name, "average_excess_return_pp"],
                                   summary.loc[name, "average_stock_return_pct"] - summary.loc[name, "average_spy_return_pct"], atol=1e-12)
    OUTPUT.mkdir(exist_ok=True)
    summary.to_csv(destination, float_format="%.15g")
    pd.DataFrame([difference]).to_csv(OUTPUT / "v0_v1_difference.csv", index=False, float_format="%.15g")
    for name, frame in (("monthly", monthly), ("sector", sector), ("stocks", stocks), ("dates", dates),
                        ("signals", events), ("extremes", pd.DataFrame(extremes)), ("influence", pd.DataFrame(influence))):
        frame.to_csv(OUTPUT / f"v0_v1_{name}.csv", index=False, float_format="%.15g")
    context = {"first_evaluation_utc": datetime.now(timezone.utc).isoformat(),
               "frozen_input_manifest_sha256": sha(SOURCE / "manifest.json"),
               "frozen_lock_sha256": sha(ROOT / "FROZEN_LOCK.json"),
               "evaluator_sha256": sha(Path(__file__)), "difference": difference,
               "top_two_V1_contribution_months_diagnostic": top_two_context,
               "percentile_method": "linear", "standard_deviation_ddof": 1,
               "integrity_endpoint_and_reconciliation_checks": "passed"}
    (OUTPUT / "v0_v1_evaluation_manifest.json").write_text(json.dumps(context, indent=2) + "\n")
    # Two presentation charts only; no change to data or research parameters.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = {"V0": "#2364aa", "V1": "#c45b19"}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(9, 5), layout="constrained")
    for name, sample in samples.items():
        x = np.sort(sample[EXCESS].to_numpy() * 100)
        ax.step(x, np.arange(1, len(x) + 1) / len(x) * 100, where="post", label=f"{name} (n={len(x)})", color=colors[name], linewidth=2)
    ax.axvline(0, color="#777777", linewidth=.8, linestyle="--")
    ax.set(title="10-trading-interval excess-return distributions", xlabel="Stock return minus SPY return (percentage points)", ylabel="Cumulative share of signals (%)", ylim=(0, 102))
    ax.legend(loc="lower right")
    ax.grid(alpha=.18)
    fig.savefig(OUTPUT / "v0_v1_distribution.png", dpi=180)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(11, 5), layout="constrained")
    x = np.arange(len(monthly))
    for offset, name in ((-.2, "V0"), (.2, "V1")):
        vals = monthly[name + "_average_excess_return_pp"].to_numpy()
        bars = ax.bar(x + offset, vals, width=.38, color=colors[name], label=name)
        for bar, n, val in zip(bars, monthly[name + "_signal_count"], vals):
            if n:
                ax.annotate(f"n={n}", (bar.get_x() + bar.get_width()/2, val), xytext=(0, 4 if val >= 0 else -4), textcoords="offset points", ha="center", va="bottom" if val >= 0 else "top", fontsize=7)
    ax.axhline(0, color="#777777", linewidth=.8)
    ax.set_xticks(x, monthly.signal_month, rotation=45, ha="right")
    ax.set(title="Monthly signal cohorts: average excess return", ylabel="Percentage points")
    ax.margins(y=.2)
    ax.legend()
    ax.grid(axis="y", alpha=.18)
    fig.savefig(OUTPUT / "v0_v1_monthly.png", dpi=180)
    plt.close(fig)
    verify_freeze()
    print(summary.to_string())
    print("\nV1 minus V0:", json.dumps(difference, indent=2))
    print("\nMonthly:", monthly[["signal_month", "V0_signal_count", "V0_average_excess_return_pp", "V1_signal_count", "V1_average_excess_return_pp"]].to_string(index=False))
    print("\nSector:", sector[["sector", "V0_signal_count", "V0_average_excess_return_pp", "V1_signal_count", "V1_average_excess_return_pp"]].to_string(index=False))


if __name__ == "__main__":
    main()
