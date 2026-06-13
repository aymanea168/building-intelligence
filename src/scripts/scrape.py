import os
import random


# scrape mbdd2025 dataset


MBDD_CLASS_MAP = {
    0: "crack",
    1: "leakage",
    2: "corrosion",
    3: "abscission",
    4: "bulge"
}


def parse_mbdd_with_sampling(
    image_dir,
    label_dir,
    samples_per_class=100
):

    # store candidates per class
    class_images = {c: [] for c in MBDD_CLASS_MAP.values()}

    for label_file in os.listdir(label_dir):

        if not label_file.endswith(".txt"):
            continue

        label_path = os.path.join(label_dir, label_file)

        image_name = label_file.replace(".txt", ".jpg")
        image_path = os.path.join(image_dir, image_name)

        if not os.path.exists(image_path):
            continue

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:

            parts = line.strip().split()

            class_id = int(parts[0])

            if class_id not in MBDD_CLASS_MAP:
                continue

            defect = MBDD_CLASS_MAP[class_id]

            class_images[defect].append({
                "image_path": image_path,
                "defect": defect,
                "dataset": "MBDD2025"
            })

    # 🎯 sampling step
    sampled = []

    random.seed(42)  # for reproducibility
    for defect, items in class_images.items():

        if len(items) == 0:
            continue

        if len(items) < samples_per_class:
            sampled_items = items  # fallback (no sampling)
        else:
            sampled_items = random.sample(items, samples_per_class)

        sampled.extend(sampled_items)

    return sampled