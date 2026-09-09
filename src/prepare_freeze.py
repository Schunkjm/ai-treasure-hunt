"""One-time Yahoo-only data/sector investigation; no outcome files read."""
from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import yfinance as yf
from .config import UNIVERSE

ROOT = Path(__file__).resolve().parents[1]


def main():
    if (ROOT / "FROZEN_LOCK.json").exists():
        raise RuntimeError("Preparation is disabled after freeze; a new version requires user authorization")
    evidence = ROOT / "data" / "freeze_investigation"
    evidence.mkdir(parents=True, exist_ok=True)
    (ROOT / "reference").mkdir(exist_ok=True)
    yf.set_tz_cache_location(str(ROOT / ".cache" / "yfinance"))
    summary = {"retrieved_utc": datetime.now(timezone.utc).isoformat()}
    for interval in ("1d", "1m"):
        try:
            frame = yf.Ticker("KO").history(
                start="2026-09-08", end="2026-09-09", interval=interval,
                auto_adjust=False, back_adjust=False, actions=True,
                repair=False, keepna=True, prepost=False, rounding=False,
                raise_errors=True, timeout=20,
            )
            frame.to_csv(evidence / f"KO_{interval}.csv")
            item = {"rows": len(frame)}
            if not frame.empty:
                item.update({"first_timestamp": str(frame.index[0]), "last_timestamp": str(frame.index[-1]),
                             "Open": float(frame.Open.iloc[0]), "High": float(frame.High.max()),
                             "Low": float(frame.Low.min()), "Close": float(frame.Close.iloc[-1]),
                             "Volume": float(frame.Volume.sum())})
                for name in ("Adj Close", "Dividends", "Stock Splits"):
                    if name in frame:
                        item[name] = float(frame[name].iloc[-1])
            summary[interval] = item
        except Exception as exc:
            summary[interval] = {"error_type": type(exc).__name__}
    (evidence / "KO_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)
    translations = {"Technology": "Information Technology", "Consumer Cyclical": "Consumer Discretionary",
                    "Consumer Defensive": "Consumer Staples", "Healthcare": "Health Care",
                    "Financial Services": "Financials", "Communication Services": "Communication Services",
                    "Industrials": "Industrials", "Energy": "Energy", "Basic Materials": "Materials",
                    "Real Estate": "Real Estate", "Utilities": "Utilities"}
    rows = []
    for ticker in UNIVERSE:
        # Access only classification metadata. Do not retain or display quotes,
        # returns, analyst targets, valuation fields, or financial statistics.
        sector = yf.Ticker(ticker).get_info().get("sector")
        if sector not in translations:
            raise ValueError(f"Unmapped or unavailable sector for {ticker}: {sector}")
        rows.append({"ticker": ticker, "sector": translations[sector], "source_sector": sector,
                     "source_url": f"https://finance.yahoo.com/quote/{ticker}/profile/",
                     "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                     "classification_basis": "Yahoo sector normalized to broad GICS-style labels; diagnostics only"})
        print(f"Sector recorded: {ticker} -> {translations[sector]}", flush=True)
    with (ROOT / "reference" / "sectors.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
