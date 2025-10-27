#!/usr/bin/env python
"""
Create tiny sample files from the large CSVs, so notebooks can run without full data.
Usage:
  python make_sample.py --orderbook data/raw/order_book_ta125.csv --alerts data/raw/ta35_with_alerts.csv --outdir data/sample
The script keeps only two tickers and one trading day.
"""
import argparse, os, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--orderbook", required=True)
    ap.add_argument("--alerts", required=True)
    ap.add_argument("--outdir", default="data/sample")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    # Alerts sample: keep a handful of rows
    alerts = pd.read_csv(args.alerts)
    if "date" in alerts.columns:
        # keep a single day
        d0 = alerts["date"].astype(str).iloc[0]
        alerts_s = alerts[alerts["date"].astype(str).eq(d0)].head(100)
    else:
        alerts_s = alerts.head(100)
    alerts_s.to_csv(os.path.join(args.outdir, "ta35_with_alerts_sample.csv"), index=False)

    # Order book sample: keep two tickers and one day if columns exist
    ob = pd.read_csv(args.orderbook)
    keep_cols = ob.columns.tolist()
    # try to infer columns
    ticker_col = next((c for c in keep_cols if c.lower() in ("ticker","symbol","secid","instrument")), None)
    date_col   = next((c for c in keep_cols if "date" in c.lower()), None)
    sample = ob
    if ticker_col:
        top_syms = sample[ticker_col].dropna().astype(str).value_counts().index[:2].tolist()
        sample = sample[sample[ticker_col].astype(str).isin(top_syms)]
    if date_col:
        d0 = sample[date_col].astype(str).iloc[0]
        sample = sample[sample[date_col].astype(str).eq(d0)]
    sample = sample.head(10000)  # cap size
    sample.to_csv(os.path.join(args.outdir, "order_book_ta125_sample.csv"), index=False)
    print("Wrote samples to", args.outdir)

if __name__ == "__main__":
    main()
