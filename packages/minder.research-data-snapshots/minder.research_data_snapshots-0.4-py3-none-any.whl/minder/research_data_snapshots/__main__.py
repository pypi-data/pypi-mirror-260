import argparse
import os
from pathlib import Path

import platformdirs
import requests
from tqdm import tqdm


def download_dataset(
    organization: str,
    dataset: str,
    folder: Path | None = None,
    refresh: bool = False,
) -> Path:
    if not folder:
        folder = platformdirs.user_cache_path("research-data-snapshots")
    file = (folder / organization / dataset).with_suffix(".parquet")
    if file.exists() and not refresh:
        return file
    file.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PORTAL_API = os.getenv("RESEARCH_PORTAL_API", "https://research.minder.care/api")
    MINDER_TOKEN = (
        os.environ["MINDER_TOKEN"]
        if "MINDER_TOKEN" in os.environ
        else Path(os.environ["RESEARCH_PORTAL_TOKEN_PATH"]).read_text("utf-8").rstrip()
    )
    with file.open(mode="wb") as f:
        response = requests.get(
            f"{RESEARCH_PORTAL_API}/data/organization/{organization}/{dataset}.parquet",
            headers={"Authorization": f"Bearer {MINDER_TOKEN}"},
            stream=True,
            timeout=None,
        )
        response.raise_for_status()
        progress = tqdm(
            desc=str(file),
            total=int(response.headers.get("content-length", -1)),
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        )
        for chunk in response.iter_content(1024):
            f.write(chunk)
            progress.update(len(chunk))
    return file


def download_datasets(
    organizations: list[str],
    datasets: list[str],
    folder: Path | None = None,
    refresh: bool = False,
) -> list[Path]:
    return [
        download_dataset(organization, dataset, folder, refresh)
        for dataset in datasets
        for organization in organizations
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--organization", nargs="+", required=True, help="organisation identifier(s)")
    parser.add_argument("--dataset", nargs="+", required=True, help="dataset name(s)")
    parser.add_argument("--folder", type=Path, help="output folder")
    parser.add_argument("--refresh", action="store_true", help="refresh selected datasets")
    args = parser.parse_args()
    download_datasets(args.organization, args.dataset, args.folder, args.refresh)
