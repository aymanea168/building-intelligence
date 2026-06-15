import json
from pydoc import text
from PIL import Image
import torch

from models import text_model, clip_model, preprocess, text_collection, image_collection, device


def create_document(item):

    document = f"""
        Defect type: {item['defect']}
        Description: {item['description']}
        Severity: {item['severity']}
        Causes: {', '.join(item['causes'])}
        Inspection actions: {', '.join(item['inspection_actions'])}
        Recommendations: {', '.join(item['recommendations'])}
        """

    return document



clip_model.eval()


clip_model.to(device)


import json

with open("data/enriched_openrouter.json") as f:
    data = json.load(f)

for idx, item in enumerate(data):

    doc_id = str(idx)

    # -------------------------
    # TEXT EMBEDDING (384D)
    # -------------------------

    document = create_document(item)

    text_vector = text_model.encode(document).tolist()

    text_collection.add(
        ids=[f"text_{doc_id}"],
        documents=[document],
        embeddings=[text_vector],
        metadatas=[{
            "image_path": item["image_path"],
            "defect": item["defect"]
        }]
    )

    # -------------------------
    # IMAGE EMBEDDING (512D)
    # -------------------------

    image = Image.open(item["image_path"]).convert("RGB")

    image_tensor = preprocess(image).unsqueeze(0).to(device) # type: ignore

    with torch.no_grad():
        image_vector = clip_model.encode_image(image_tensor).cpu().numpy()[0].tolist() # type: ignore

    image_collection.add(
        ids=[f"img_{doc_id}"],
        documents=[document],   # optional but useful for debugging
        embeddings=[image_vector],
        metadatas=[{
            "image_path": item["image_path"],
            "defect": item["defect"]
        }]
    )


print("database created")