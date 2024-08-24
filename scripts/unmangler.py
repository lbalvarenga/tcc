import logging
import logging.config
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(Path(SCRIPT_DIR).parent, "data")
OUTPUT_DIR = os.path.join(Path(SCRIPT_DIR).parent, "data", "clean")


def unmangle(filename: str, cols: dict[str, type], source: str):
    logger.debug(f"Processing '{filename}'")
    df = pd.read_csv(os.path.join(INPUT_DIR, filename), header=None)

    df = df.T.iloc[:, 0:2]  # Transpose cols

    df.columns = cols.keys()
    df = df.astype(cols)
    df.loc[len(df.index)] = ["Fonte", source]

    logger.debug(f"\n{df.head(5)}")
    df.to_csv(
        os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}_t.csv"), index=False
    )


filename = "ibge_deflator_96_21.csv"
unmangle(filename, {"ano": int, "deflator": float}, "IBGE - Contas Nacionais Anuais")
# defl.columns = ["ano", "deflator"]

filename = "ibge_pib_rsmi_96_21.csv"
unmangle(filename, {"ano": int, "pib": int}, "IBGE - Contas Nacionais Anuais")

filename = "ibge_ipca_hist_94_23.xls"
logger.debug(f"Processing '{filename}'")
acum = pd.read_excel(os.path.join(INPUT_DIR, filename), sheet_name="acum")
acum.loc[len(acum.index)] = [
    "Fonte",
    "IBGE, Diretoria de Pesquisas, Coordenação de Índices de Preços, Sistema Nacional de Índices de Preços ao Consumidor.",
]
logger.debug(f"\n{acum.head(5)}")
acum.to_csv(
    os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}_t.csv"), index=False
)
