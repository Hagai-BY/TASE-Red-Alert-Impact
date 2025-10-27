# Market Impact of Rocket Alerts on TASE (High-Frequency Study)

Minute-by-minute event study on the Tel Aviv Stock Exchange (TASE).  
Raw order-book messages are reconstructed into executed trades and aggregated to 1-minute OHLCV/turnover; events are aligned to rocket alerts and estimated via a two-way fixed-effects panel.

## Problem
Rocket alerts can affect prices and liquidity within minutes, yet public data rarely arrives as clean, aligned, high-frequency series. The goals are:
1) convert noisy order-book messages into uniform 1-minute security-level series;  
2) estimate short-run abnormal returns and turnover around alerts while controlling for stock and time effects.

## Methodology
1. **Order book → trades**  
   Parse add/cancel/execute messages, reconstruct prints, reconcile volumes, enforce tick size, de-duplicate, validate timestamps/sequence.

2. **Continuous 1-minute bars**  
   Aggregate to 1m OHLCV and turnover (₪), handle missing minutes, and mark open/close and halts.

3. **Focus on market movers**  
   Use the most influential TASE-35 constituents (by index weight/turnover) to maximize signal-to-noise.

4. **Event alignment**  
   Merge Home Front Command alerts and build a symmetric ±15-minute window per alert; exclude open/close and overlapping windows.

5. **Controls for time patterns**  
   Include minute-of-day seasonality and event-time indicators (τ = −15..+15).

6. **Panel models**  
   Returns:
   \[
     r_{i,t} = \alpha_i + \gamma_{m(t)} + \sum_{\tau=-15}^{+15} \delta_\tau \mathbf{1}\{\text{event time}=\tau\} + \varepsilon_{i,t}
   \]
   Turnover (log/level as specified) with Newey–West HAC errors; grouped Wald tests for pre/around/post.

7. **Quality control**  
   Sequence/time checks, volume reconciliation, tick-size enforcement, de-duplication, sparse-interval handling, outlier flags, validation of minute aggregates.

## Results (high level)
- **Returns:** small but statistically significant negative move around the alert; trough ≈ −0.035% several minutes post-alert.  
- **Turnover:** sharper immediate drop, ~6% per minute on average in the first five minutes; ≈ ₪1.45M cumulative over 15 minutes for the analyzed names.  
- No immediate full rebound within the ±15-minute window.

Figures, robustness checks, and grouped-Wald tests appear in the notebooks and poster.

## Repository layout

notebooks/
Return_Panel_Model.ipynb # returns panel with two-way FE
Turnover_OLS-HAC_model.ipynb # turnover model with HAC errors
poster/
Research_Poster_Hagai_BY.pdf
src/
config.py # path helpers (DATA_ROOT, sample/raw)
data/
README.md # data notes; raw files are not tracked


## Quick start
```bash
git clone https://github.com/Hagai-BY/TASE-Red-Alert-Impact.git
cd TASE-Red-Alert-Impact

python -m venv .venv
# Windows:
. .venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
jupyter lab  # or: jupyter notebook

Open notebooks/Return_Panel_Model.ipynb or notebooks/Turnover_OLS-HAC_model.ipynb and run all cells.
If required CSVs are not found locally, the notebooks download them from the shared Google Drive folder into data/raw/.


Inline in notebooks:
No action required. The notebooks download from the shared Drive folder when files are missing and then load from data/raw/.


