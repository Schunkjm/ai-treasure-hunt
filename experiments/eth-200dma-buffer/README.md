# ETH 200-DMA buffer experiment

James's first AI Treasure Hunt experiment (separate from the lab's frozen stock study).

**Question:** While daily ETH is above its 200-day moving average, how large is a typical drop from a recent high — and what buffer covers about 80% of those dips?

**Headline (2026-09-17 run):** train 80th-percentile buffer **14.19%**; holdout coverage **~81%**. See `REPORT.md`.

## Files
- `REPORT.md` — full write-up
- `analyze_eth_buffer.py` — reproducible script
- `episode_drawdowns*.csv`, `regime_max_drawdowns.csv` — outputs

## Re-run
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install yfinance pandas numpy
python analyze_eth_buffer.py
```
