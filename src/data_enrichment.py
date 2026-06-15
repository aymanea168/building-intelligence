import base64
import json
import pandas as pd

from tqdm import tqdm

from models import MODEL, llm_client


# =========================
# PROMPT
# =========================

PROMPT = """
You are a construction inspection AI.

Analyze the image of a building defect.

Return ONLY valid JSON:

{
 "description": "",
 "severity": "low|medium|high",
 "causes": [],
 "inspection_actions": [],
 "recommendations": []
}

Rules:
- Only visible evidence
- Causes are hypotheses
- Be concise and technical
"""


# =========================
# IMAGE ENCODING
# =========================

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# =========================
# VLM CALL
# =========================

def analyze_image(image_path, defect):

    base64_img = encode_image(image_path)

    response = llm_client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        {PROMPT}

                        Defect: {defect}
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_img}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content


def parse_vlm_output(text):
    try:
        data = json.loads(text)
    except Exception:
        # fallback: try to extract JSON block
        import re

        match = re.search(r"\{.*\}", text, re.S)

        if match:
            try:
                data = json.loads(match.group())
            except:
                data = {}

        else:
            data = {}

    return data

# =========================
# LOAD DATASET
# =========================

df = pd.read_csv("data/processed/metadata.csv")

results = []


# =========================
# LOOP
# =========================

for i, row in tqdm(df.iterrows(), total=len(df)):
    if i < 50: # type: ignore
        continue
    try:
        output = analyze_image(
            row["image_path"],
            row["defect"],
        )
        parsed = parse_vlm_output(output)

        results.append({
            "image_path": row["image_path"],
            "dataset": row["dataset"],
            "defect": row["defect"],

            "description": parsed.get("description", ""),
            "severity": parsed.get("severity", ""),
            "causes": parsed.get("causes", []),
            "inspection_actions": parsed.get("inspection_actions", []),
            "recommendations": parsed.get("recommendations", [])
        })

    except Exception as e:
        print("error:", row["image_path"], e)


# =========================
# SAVE
# =========================

with open("data/enriched_openrouter1.json", "a") as f:
    json.dump(results, f, indent=2)

print("Done → enriched_openrouter1.json")