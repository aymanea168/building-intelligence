import os

import pandas as pd

from scripts.scrape import parse_mbdd_with_sampling
# from parsers.sdnet import parse_sdnet
# from parsers.fbd import parse_fbd


MBDD_PATH = "data/raw/mbdd2025"
PROCESS_PATH = "data/processed"

data=[]

data += parse_mbdd_with_sampling(
    image_dir=os.path.join(MBDD_PATH, "images"),
    label_dir=os.path.join(MBDD_PATH, "labels"),
    samples_per_class=100
)


# data += parse_sdnet(
#     "data/raw/sdnet2018"
# )


# data += parse_fbd(
#     "data/raw/fbd"
# )



df = pd.DataFrame(data)


df.to_csv(
    os.path.join(PROCESS_PATH, "metadata.csv"),
    index=False
)


print(df.head())

