#!/usr/bin/env python
"""
Download large data files from Google Drive into ./data/raw using gdown.
Usage examples:
  python download_data.py --orderbook <drive_link_or_id> --alerts <drive_link_or_id>
  python download_data.py --orderbook 1abcDEF... --alerts https://drive.google.com/file/d/2GhIJKl.../view?usp=sharing
"""
import argparse, os, re, sys
try:
    import gdown
except ImportError:
    print("Please install gdown: pip install gdown", file=sys.stderr)
    sys.exit(1)

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)


def extract_folder_id(s: str) -> str:
    # Match folder URLs like /folders/<id>
    m = re.search(r"/folders/([a-zA-Z0-9_-]{20,})", s)
    if m: return m.group(1)
    # Fallback to plain id
    if re.fullmatch(r"[a-zA-Z0-9_-]{20,}", s):
        return s
    return None

def extract_id(s: str) -> str:

    # Accept full Drive URLs or raw IDs
    m = re.search(r"/d/([a-zA-Z0-9_-]{20,})", s)
    if m:
        return m.group(1)
    m = re.search(r"[?&]id=([a-zA-Z0-9_-]{20,})", s)
    if m:
        return m.group(1)
    # If looks like an ID, return as-is
    if re.fullmatch(r"[a-zA-Z0-9_-]{20,}", s):
        return s
    raise ValueError("Could not parse Google Drive file id from input. Provide a share link or id.")


def download_one(file_id: str, out_path: str):
    print(f"Downloading id={file_id} -> {out_path}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, out_path, quiet=False)

def download_folder(folder_id: str, outdir: str):
    print(f"Downloading folder id={folder_id} -> {outdir}")
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    gdown.download_folder(url=url, output=outdir, quiet=False, use_cookies=False)

    print(f"Downloading id={file_id} -> {out_path}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, out_path, quiet=False)



def read_links_from_json(p: str):
    import json
    with open(p, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("orderbook"), cfg.get("alerts"), cfg.get("folder")

    import json
    with open(p, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg.get("orderbook"), cfg.get("alerts")

def main():

    ap = argparse.ArgumentParser()
    ap.add_argument("--auto", action="store_true", help="Read Drive IDs/links from data_links.json in repo root")
    ap.add_argument("--folder", type=str, help="Drive folder link or id; will download folder and try to locate required CSVs")
    ap.add_argument("--auto", action="store_true", help="Read Drive IDs/links from data_links.json in repo root")
    ap.add_argument("--orderbook", type=str, help="Drive link or id for order_book_ta125.csv")
    ap.add_argument("--alerts", type=str, help="Drive link or id for ta35_with_alerts.csv")
    ap.add_argument("--outdir", type=str, default=RAW_DIR, help="Output directory (default: data/raw)")
    
args = ap.parse_args()

if args.auto:
    ob, al, fo = read_links_from_json("data_links.json") if os.path.exists("data_links.json") else read_links_from_json("data_links.example.json")
    if ob and not args.orderbook:
        args.orderbook = ob
    if al and not args.alerts:
        args.alerts = al
    if fo and not args.folder:
        args.folder = fo


    os.makedirs(args.outdir, exist_ok=True)


# Option A: explicit files
if args.orderbook:
    oid = extract_id(args.orderbook)
    download_one(oid, os.path.join(args.outdir, "order_book_ta125.csv"))
if args.alerts:
    aid = extract_id(args.alerts)
    download_one(aid, os.path.join(args.outdir, "ta35_with_alerts.csv"))

# Option B: folder link/id
if args.folder and not (args.orderbook and args.alerts):
    fid = extract_folder_id(args.folder)
    if not fid:
        raise ValueError("Could not parse folder id. Provide a valid Drive folder link or id.")
    tmp = os.path.join(args.outdir, "_tmp_folder")
    os.makedirs(tmp, exist_ok=True)
    download_folder(fid, tmp)

    # Try to locate required files by name
    ob_name_candidates = ["order_book_ta125.csv", "order_book.csv", "orderbook.csv"]
    al_name_candidates = ["ta35_with_alerts.csv", "alerts.csv"]
    found_ob = None; found_al = None
    for root, _, files in os.walk(tmp):
        for f in files:
            fn = f.lower()
            if not found_ob and fn in [c.lower() for c in ob_name_candidates]:
                found_ob = os.path.join(root, f)
            if not found_al and fn in [c.lower() for c in al_name_candidates]:
                found_al = os.path.join(root, f)

    if found_ob:
        shutil.copy(found_ob, os.path.join(args.outdir, "order_book_ta125.csv"))
    if found_al:
        shutil.copy(found_al, os.path.join(args.outdir, "ta35_with_alerts.csv"))
    if not (found_ob or found_al):
        print("Downloaded folder but could not find expected CSV names. Please provide explicit file links with --orderbook/--alerts.", file=sys.stderr)

    # cleanup temp
    try:
        import shutil as _sh
        _sh.rmtree(tmp, ignore_errors=True)
    except Exception:
        pass

print("Done.")


if __name__ == "__main__":
    main()
