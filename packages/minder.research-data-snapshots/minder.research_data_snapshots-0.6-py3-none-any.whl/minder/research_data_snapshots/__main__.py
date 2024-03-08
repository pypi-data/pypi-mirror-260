import argparse
from pathlib import Path

from minder.research_data_snapshots import download_datasets

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", nargs="+", required=True, help="dataset name(s)")
parser.add_argument("--organization", nargs="+", help="organisation identifier(s)")
parser.add_argument("--folder", type=Path, help="output folder")
parser.add_argument("--refresh", action="store_true", help="refresh selected datasets")
args = parser.parse_args()
download_datasets(args.dataset, args.organization, args.folder, args.refresh)
