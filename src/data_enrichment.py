
# import os
# import json
# import pandas as pd
# from PIL import Image
# from tqdm import tqdm

# import torch
# from transformers import AutoProcessor, DeepseekVLForConditionalGeneration


# # =========================
# # 1. LOAD MODEL
# # =========================

# model_name = "deepseek-community/deepseek-vl-1.3b-chat"

# model = DeepseekVLForConditionalGeneration.from_pretrained(
#     model_name,
#     device_map="auto",
#     attn_implementation="sdpa",
#     torch_dtype=torch.float16
# )

# processor = AutoProcessor.from_pretrained(model_name)


# # =========================
# # 2. INSPECTION PROMPT
# # =========================

# PROMPT = """
# You are a construction defect inspection AI.

# Analyze the image carefully.

# Return ONLY the JSON response in the following format, each field with max 3 distinct elements, no repetition:

# {
#  "visual_description": "...",
#  "severity": "low|medium|high",
#  "possible_causes": "...",
#  "inspection_actions": "...",
#  "recommendations": "..."
# }

# Rules:
# - List two or three possible causes
# - List two or three possible recommendations
# - List two or three possible inspection actions
# - Do not hallucinate building structure details
# - Be concise and technical
# - List 3 distinct elements max for each field
# - Do not repeat or paraphrase the same sentence

# """


# # =========================
# # 3. VLM INFERENCE FUNCTION
# # =========================

# def analyze_image(image_path, defect_label):

#     image = Image.open(image_path).convert("RGB")

#     messages = [
#         {
#             "role": "user",
#             "content": [
#                 {"type": "image", "image": image},
#                 {
#                     "type": "text",
#                     "text": f"""
#                             Defect label (dataset): {defect_label}

#                             {PROMPT}
#                             """
#                 }
#             ]
#         }
#     ]

#     inputs = processor.apply_chat_template(
#         messages,
#         add_generation_prompt=True,
#         tokenize=True,
#         return_dict=True,
#         return_tensors="pt"
#     ).to(model.device, dtype=model.dtype)

#     with torch.no_grad():
#         generated_ids = model.generate(
#             **inputs,
#             max_new_tokens=101,
#             # temperature=0.2
#         )

#     generated_ids_trimmed = [
#         out_ids[len(in_ids):]
#         for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
#     ]

#     output = processor.batch_decode(
#         generated_ids_trimmed,
#         skip_special_tokens=True,
#         clean_up_tokenization_spaces=False
#     )[0]

#     return output


# # =========================
# # 4. LOAD YOUR DATASET
# # =========================

# df = pd.read_csv("data/processed/metadata.csv")

# results = []

# # optional cache (VERY IMPORTANT for long runs)
# CACHE_DIR = "data/cache"
# os.makedirs(CACHE_DIR, exist_ok=True)


# # =========================
# # 5. PROCESS LOOP
# # =========================

# for _, row in tqdm(df.iterrows(), total=len(df)):

#     image_path = row["image_path"]
#     defect = row["defect"]
#     # surface = row.get("surface_type", "unknown")

#     cache_file = os.path.join(
#         CACHE_DIR,
#         os.path.basename(image_path) + ".json"
#     )
        
#     vlm_output = analyze_image(
#         image_path,
#         defect,
        
#     )

#     # save cache
#     with open(cache_file, "w") as f:
#         json.dump(
#             {"output": vlm_output},
#             f,
#             indent=2
#         )


#     results.append({
#         "image_path": image_path,
#         "defect_type": defect,
#         # "surface_type": surface,
#         "vlm_analysis": vlm_output
#     })


# # =========================
# # 6. SAVE ENRICHED DATASET
# # =========================

# with open("data/enriched_dataset.json", "w") as f:
#     json.dump(results, f, indent=2)

# print("Done → enriched_dataset.json created")






# import os
# import json

# import pandas as pd

# from PIL import Image

# from tqdm import tqdm

# import google.generativeai as genai

# from dotenv import load_dotenv

# load_dotenv('.env')


# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # =========================
# # API SETUP
# # =========================

# genai.configure(
#     api_key=GEMINI_API_KEY
# )

# model = genai.GenerativeModel(
#     "gemini-2.5-flash"
# )



# # ==========================
# # JSON SCHEMA
# # ==========================


# response_schema = {

#     "type": "object",

#     "properties": {
#         "description":
#         {
#             "type":"string"
#         },

#         "severity":
#         {
#             "type":"string"
#         },

#         "causes":
#         {
#             "type":"array",
#             "items":
#             {
#                 "type":"string"
#             }
#         },

#         "inspection_actions":
#         {
#             "type":"array",
#             "items":
#             {
#                 "type":"string"
#             }
#         },

#         "recommendations":
#         {
#             "type":"array",
#             "items":
#             {
#                 "type":"string"
#             }
#         }
#     }
# }

# # =========================
# # PROMPT
# # =========================


# PROMPT = """
# You are a construction defect inspection AI.

# Analyze the image carefully.

# Return ONLY the JSON response in the following format, each field with max 3 distinct elements, no repetition:

# {
#  "visual_description": "...",
#  "severity": "low|medium|high",
#  "possible_causes": "...",
#  "inspection_actions": "...",
#  "recommendations": "..."
# }

# Rules:
# - List two or three possible causes
# - List two or three possible recommendations
# - List two or three possible inspection actions
# - Do not hallucinate building structure details
# - Be concise and technical
# - List 3 distinct elements max for each field
# - Do not repeat or paraphrase the same sentence

# """

# # =========================
# # IMAGE ANALYSIS
# # =========================

# def analyze_image(
#     image_path,
#     defect,
# ):
#     img = Image.open(image_path)
#     response = model.generate_content(
#         [
#             PROMPT,
#             f"""
#             Dataset defect:
#             {defect}
#             """,
#             img
#         ],
#         generation_config={
#             "response_mime_type": "application/json",
#             "response_schema": response_schema
#         }
#     )

#     return json.loads(
#         response.text
#     )

# # =========================
# # DATASET LOOP
# # =========================


# df = pd.read_csv(
#     "data/processed/metadata.csv"
# )

# results=[]

# for _, row in tqdm(df.iterrows(), total=len(df)):
#     try:
#         ai_data = analyze_image(row.image_path, row.defect)
        
#         results.append({
#             "image_path": row["image_path"],

#             "dataset": row["dataset"],

#             "defect": row["defect"],

#             # ---- VLM fields ----

#             "description": ai_data["description"],

#             "severity": ai_data["severity"],

#             "causes": ai_data["causes"],

#             "inspection_actions": ai_data["inspection_actions"],

#             "recommendations": ai_data["recommendations"]
#         })

#         print( f"image is {row.image_path} is validated and enriched")

#     except Exception as e:
#         print( "failed:", row.image_path, e)

# with open("data/enriched_dataset.json", "w") as f:
#     json.dump(results, f, indent=2)

# print("finished")





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