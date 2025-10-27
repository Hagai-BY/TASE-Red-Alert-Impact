# Market Impact of Rocket Alerts on TASE (High-Frequency Event Study)

This repository contains my guided research measuring the minute-by-minute market impact of rocket alerts on the Tel Aviv Stock Exchange (TASE). The pipeline converts **raw order-book messages** to **executed trades** and aggregates them to **1-minute OHLCV / turnover** series for panel estimation.

## Highlights
- **Order book → trades**: Parse order/add/cancel/execute messages, reconstruct prints, reconcile volumes, enforce tick size, deduplicate, and validate timestamps/sequence.
- **Minute bars**: Aggregate to 1-minute OHLCV and turnover (NIS), handle missing minutes, suspend/open/close periods, and mark halts.
- **Event alignment**: Merge the Home Front Command alert API and align events to a **±15 minute** window per alert; exclude open/close and overlapping windows.
- **Two-way fixed effects**: Estimate abnormal returns with **stock fixed effects** and **time effects** (minute-of-day seasonality and event-time dummies). Turnover modeled with OLS and **Newey–West HAC** errors; grouped Wald tests for pre/around/post windows.
- **Reproducibility**: Poster (PDF) and notebooks for returns and turnover models are included.

## Panel specs (compact)
Returns:
\[ r_{i,t} = \alpha_i + \gamma_{m(t)} + \sum_{\tau=-15}^{+15} \delta_\tau \cdot 1[\text{event time}=\tau] + \varepsilon_{i,t} \]
Turnover (log):
\[ y_{i,t} = \alpha_i + \gamma_{m(t)} + \sum_{\tau=-15}^{+15} \beta_\tau \cdot 1[\text{event time}=\tau] + u_{i,t} \]
With HAC(Newey–West) for robust inference.

## Repository layout
```
notebooks/
  Return_Panel_Model.ipynb
  Turnover_OLS-HAC_model.ipynb
poster/
  Research_Poster_Hagai_Ben_Yehiel.pdf
src/
  (optional) scripts for parsing, aggregation, alignment, and modeling
data/
  README.md (data access notes; raw data not tracked)
```

## Data access
- **Order book / trades**: use your exchange data feeds (not distributed here).  
- **Rocket alerts**: Home Front Command alert API (documented in the notebook).  
> Large files are **not committed**. See `.gitignore`. Consider Git LFS for PDFs/PNGs if needed.

## Quick start
```bash
# 1) create and activate env
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# 2) install deps
pip install -r requirements.txt

# 3) open notebooks
jupyter lab  # or: jupyter notebook
```

## Requirements (main)
See `requirements.txt` for versions: pandas, numpy, scipy, statsmodels, linearmodels, scikit-learn, matplotlib, jupyter.

## License
MIT


## Download data from Google Drive

Use the provided script to pull large CSVs from Google Drive (after setting file sharing to "Anyone with the link → Viewer"):

```bash
pip install -r requirements.txt
python download_data.py --orderbook <drive_link_or_id_for_order_book_ta125>                             --alerts    <drive_link_or_id_for_ta35_with_alerts>
```

The script accepts either a raw ID or a full share URL and downloads into `data/raw/`.  
Configure paths with `DATA_ROOT` env var or `data_config.yaml`.


## Run "as is" — options

**A. Auto-download from Google Drive**
1) Put your public share links or file IDs into `data_links.json` (copy from `data_links.example.json`).
2) Run:
```bash
python download_data.py --auto
```
This will fetch the files into `data/raw/`.

**B. Quick demo with tiny samples**
If you already have the big CSVs locally, create small samples and commit them so anyone can run:
```bash
python make_sample.py --orderbook data/raw/order_book_ta125.csv                           --alerts    data/raw/ta35_with_alerts.csv
git add data/sample/*
git commit -m "Add tiny sample data for demo runs"
git push
```
Notebooks will detect `data/sample/` first if present.

**C. Use a custom data directory**
```bash
# Windows
set DATA_ROOT=D:\TASE_DATA
# macOS/Linux
export DATA_ROOT=/path/to/TASE_DATA
```


**Folder link option**
Instead of two file links you can provide a single Google Drive **folder** link/ID containing the CSVs:
```bash
python download_data.py --folder "<drive_folder_link_or_id>"
# or auto via data_links.json:
# { "folder": "<drive_folder_link_or_id>" }
python download_data.py --auto
```
The script will download the folder and try to locate files named
`order_book_ta125.csv` and `ta35_with_alerts.csv` automatically.
