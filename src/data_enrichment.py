"""
Data enrichment pipeline for construction defects.

Analyzes images using a vision language model (VLM) to extract:
- Detailed defect descriptions
- Severity classifications
- Root cause analysis
- Inspection actions
- Recommendations

Stores enriched metadata in JSON format for downstream processing.
"""

import base64
import json
import re
from typing import Any, Dict, List

import pandas as pd
from tqdm import tqdm

from models import MODEL, llm_client


# ============================================================================
# Prompts
# ============================================================================

VLM_ANALYSIS_PROMPT = """
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


# ============================================================================
# Image Processing
# ============================================================================


def encode_image(image_path: str) -> str:
    """
    Encode image to base64 string for API transmission.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded image string
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ============================================================================
# VLM Analysis
# ============================================================================


def analyze_image(image_path: str, defect: str) -> str:
    """
    Analyze image using vision language model.

    Args:
        image_path: Path to the image file
        defect: Type of defect to analyze

    Returns:
        VLM response as JSON string
    """
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
{VLM_ANALYSIS_PROMPT}

Defect: {defect}
""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
    )

    return str(response.choices[0].message.content)


def parse_vlm_output(text: str) -> Dict[str, Any]:
    """
    Parse VLM output and extract JSON.

    Attempts to parse as JSON directly, then falls back to regex
    extraction if the response contains extraneous text.

    Args:
        text: VLM response text

    Returns:
        Parsed JSON data as dictionary
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract JSON block with regex
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

    return {}


# ============================================================================
# Enrichment Pipeline
# ============================================================================


def enrich_dataset(
    input_csv: str = "data/processed/metadata.csv",
    output_json: str = "data/enriched_openrouter1.json",
    skip_rows: int = 0,
) -> None:
    """
    Process dataset: analyze images and enrich with VLM insights.

    Args:
        input_csv: Path to metadata CSV file
        output_json: Path to output enriched JSON file
        skip_rows: Number of rows to skip (for resuming interrupted runs)
    """
    df = pd.read_csv(input_csv)
    results = []

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        if idx < skip_rows: # type: ignore
            continue

        try:
            vlm_output = analyze_image(row["image_path"], row["defect"])
            parsed_data = parse_vlm_output(vlm_output)

            enriched_record = {
                "image_path": row["image_path"],
                "dataset": row["dataset"],
                "defect": row["defect"],
                "description": parsed_data.get("description", ""),
                "severity": parsed_data.get("severity", ""),
                "causes": parsed_data.get("causes", []),
                "inspection_actions": parsed_data.get("inspection_actions", []),
                "recommendations": parsed_data.get("recommendations", []),
            }

            results.append(enriched_record)

        except Exception as e:
            print(f"Error processing {row['image_path']}: {e}")

    with open(output_json, "a") as f:
        json.dump(results, f, indent=2)

    print(f"Done → {output_json}")


if __name__ == "__main__":
    enrich_dataset()
