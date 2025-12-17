# storage.py
import os
import json
from datetime import datetime

REPORTS_DIR = 'reports'
STATS_FILE = 'stats.json'

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def save_report(rows, filename_prefix='report'):
    ensure_reports_dir()
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    outname = f"{filename_prefix}_{ts}.json"
    path = os.path.join(REPORTS_DIR, outname)
    data = {'timestamp': ts, 'candidates': rows}
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
    update_stats(len(rows))
    return path

def read_stats():
    if not os.path.exists(STATS_FILE):
        return {'total_processed': 0}
    with open(STATS_FILE, 'r') as f:
        return json.load(f)

def update_stats(n=0):
    stats = read_stats()
    stats['total_processed'] = stats.get('total_processed', 0) + n
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)
