import os
from pathlib import Path

import platformdirs
import requests
from tqdm import tqdm


def download_dataset(
    dataset: str,
    organization: str,
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
    datasets: list[str],
    organizations: list[str] | None = None,
    folder: Path | None = None,
    refresh: bool = False,
) -> list[Path]:
    if organizations is None:
        RESEARCH_PORTAL_API = os.getenv("RESEARCH_PORTAL_API", "https://research.minder.care/api")
        MINDER_TOKEN = (
            os.environ["MINDER_TOKEN"]
            if "MINDER_TOKEN" in os.environ
            else Path(os.environ["RESEARCH_PORTAL_TOKEN_PATH"]).read_text("utf-8").rstrip()
        )
        response = requests.get(
            f"{RESEARCH_PORTAL_API}/info/organizations",
            headers={"Authorization": f"Bearer {MINDER_TOKEN}"},
            timeout=None,
        )
        response.raise_for_status()
        organizations = [organization["id"] for organization in response.json()["organizations"]]
    return [
        download_dataset(dataset, organization, folder, refresh)
        for dataset in datasets
        for organization in organizations
    ]
