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

   **Returns (two-way FE):**

   $$
   r_{i,t}
   \=\
   \sum_{k=-15}^{+15} \gamma_k\, D_{k,t}
   \+\ \alpha_i \+\ \delta_d \+\ \theta_h \+\ \varepsilon_{i,t}
   $$

   **Turnover (log, HAC):**

   $$
   \log\!\bigl(1+\mathrm{Turnover}^{\mathrm{TA35}}_{t}\bigr)
   \=\
   \sum_{k=-15}^{+15} \beta_k\, D_{k,t}
   \+\ \delta_d \+\ \theta_h \+\ \varepsilon_{t}
   $$


7. **Quality control**  
   Sequence/time checks, volume reconciliation, tick-size enforcement, de-duplication, sparse-interval handling, outlier flags, validation of minute aggregates.

## Results (high level)
- **Returns:** small but statistically significant negative move around the alert; trough ≈ −0.035% several minutes post-alert.  
- **Turnover:** sharper immediate drop, ~6% per minute on average in the first five minutes; ≈ ₪1.45M cumulative over 15 minutes for the analyzed names.  
- No immediate full rebound within the ±15-minute window.

Figures, robustness checks, and grouped-Wald tests appear in the notebooks and poster.

## Repository layout

repo-root/
├─ notebooks/
│ ├─ Return_Panel_Model.ipynb
│ └─ Turnover_OLS-HAC_model.ipynb
├─ poster/
│ └─ Research_Poster_Hagai_BY.pdf
├─ src/
│ └─ config.py
├─ data/
│ ├─ README.md
│ └─ (raw/ and sample/ are created locally; git-ignored)
├─ download_data.py
├─ make_sample.py
├─ requirements.txt
└─ README.md


### Quick start
```markdown
## Quick start

git clone https://github.com/Hagai-BY/TASE-Red-Alert-Impact.git
cd TASE-Red-Alert-Impact

python -m venv .venv
# Windows:
. .venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
jupyter lab  # or: jupyter notebook

# Open notebooks/Return_Panel_Model.ipynb or notebooks/Turnover_OLS-HAC_model.ipynb and run all cells.
# If required CSVs are not found locally, the notebooks download them from the shared Google Drive folder into data/raw/.



