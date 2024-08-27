import pandas as pd
import os
from pathlib import Path
from functools import reduce

# WARN: RUN INFLA FIRST

SCRIPT_DIR = os.path.dirname(__file__)
IO_DIR = os.path.join(Path(SCRIPT_DIR).parent, "data", "stata")

files = [
    "cambio_96_24_mensal.csv",
    "ipa_ep_di_96_24_mensal.csv",
    "ipca_96_24_mensal.csv",
    "pib_defl_96_24_mensal.csv",
    "selic_96_24_mensal.csv",
    "meta_infl_avg_mensal.csv",
]

csvs = [pd.read_csv(os.path.join(IO_DIR, f), index_col="date") for f in files]


joined = reduce(lambda l, r: pd.merge(l, r, on=["date"], how="outer"), csvs).reset_index() # Join all
joined = joined[~(joined["date"] < "1999-01-01")].reset_index().drop("index", axis=1)  #  Data is complete after 1999
joined = joined[~(joined["date"] > "2023-12-31")].reset_index().drop("index", axis=1).set_index("date")
joined = joined.rename({"tgt": "metabcb"}, axis=1)[:-1]

print(joined)

joined.to_csv(os.path.join(IO_DIR, "joined.csv"))
