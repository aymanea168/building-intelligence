"""
Dataset parsing utilities for construction defect datasets.

Includes parsers for MBDD2025 and other defect dataset formats.
"""

import os
import random
from typing import Any, Dict, List


# ============================================================================
# Dataset Configuration
# ============================================================================

# MBDD2025 class mapping
MBDD_CLASS_MAP = {
    0: "crack",
    1: "leakage",
    2: "corrosion",
    3: "abscission",
    4: "bulge",
}


# ============================================================================
# MBDD2025 Parser
# ============================================================================


def parse_mbdd_with_sampling(
    image_dir: str,
    label_dir: str,
    samples_per_class: int = 100,
) -> List[Dict[str, Any]]:
    """
    Parse MBDD2025 dataset with stratified sampling.

    For each defect class, samples up to `samples_per_class` images.
    If fewer samples exist, includes all available images.

    Args:
        image_dir: Directory containing image files
        label_dir: Directory containing label files (YOLO format)
        samples_per_class: Number of samples per defect class

    Returns:
        List of dictionaries with keys: image_path, defect, dataset
    """
    # Organize candidates by class
    class_images: Dict[str, List[Dict[str, Any]]] = {
        defect: [] for defect in MBDD_CLASS_MAP.values()
    }

    # Parse all label files
    for label_file in os.listdir(label_dir):
        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(label_dir, label_file)
        image_name = label_file.replace(".txt", ".jpg")
        image_path = os.path.join(image_dir, image_name)

        # Skip if image doesn't exist
        if not os.path.exists(image_path):
            continue

        # Read label file (YOLO format: class_id)
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])

            if class_id not in MBDD_CLASS_MAP:
                continue

            defect = MBDD_CLASS_MAP[class_id]
            class_images[defect].append(
                {
                    "image_path": image_path,
                    "defect": defect,
                    "dataset": "MBDD2025",
                }
            )

    # Stratified sampling per class
    random.seed(42)  # For reproducibility
    sampled: List[Dict[str, Any]] = []

    for defect, items in class_images.items():
        if not items:
            continue

        # Sample up to samples_per_class items
        num_samples = min(len(items), samples_per_class)
        sampled_items = random.sample(items, num_samples)
        sampled.extend(sampled_items)

    return sampled
