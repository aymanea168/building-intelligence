"""
Dataset building pipeline for construction defects.

Parses raw defect images and labels to create a structured dataset with metadata.
Supports multiple dataset sources (MBDD, SDNet, FBD) with sampling.
"""

import os
from typing import List, Dict, Any

import pandas as pd

from scripts.scrape import parse_mbdd_with_sampling

# Uncomment to include additional datasets:
# from scripts.sdnet import parse_sdnet
# from scripts.fbd import parse_fbd


# ============================================================================
# Configuration
# ============================================================================

MBDD_PATH = "data/raw/mbdd2025"
PROCESS_PATH = "data/processed"


# ============================================================================
# Dataset Building
# ============================================================================


def build_dataset() -> pd.DataFrame:
    """
    Parse and combine defect datasets from multiple sources.

    Returns:
        DataFrame with columns: image_path, dataset, defect, and other metadata
    """
    records: List[Dict[str, Any]] = []

    # Parse MBDD dataset with sampling
    records += parse_mbdd_with_sampling(
        image_dir=os.path.join(MBDD_PATH, "images"),
        label_dir=os.path.join(MBDD_PATH, "labels"),
        samples_per_class=100,
    )

    # Uncomment to include additional datasets:
    # records += parse_sdnet("data/raw/sdnet2018")
    # records += parse_fbd("data/raw/fbd")

    return pd.DataFrame(records)


def save_dataset(df: pd.DataFrame, output_path = None) -> None:
    """
    Save dataset to CSV file.

    Args:
        df: DataFrame to save
        output_path: Output file path (default: data/processed/metadata.csv)
    """
    if output_path is None:
        output_path = os.path.join(PROCESS_PATH, "metadata.csv")

    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(df.head())


if __name__ == "__main__":
    dataset = build_dataset()
    save_dataset(dataset)


