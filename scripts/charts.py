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
INPUT_DIR = os.path.join(Path(SCRIPT_DIR).parent, "data", "clean")
OUTPUT_DIR = os.path.join(Path(SCRIPT_DIR).parent, "fig")


def lfsave(filename: str, x: tuple[str, str], y: tuple[str, str], title: str = ""):
    df = pd.read_csv(os.path.join(INPUT_DIR, filename), delimiter=",")
    df = df[pd.to_numeric(df[x[0]], errors="coerce").notna()].astype(float)

    logger.debug(f"Processing {filename}...")
    logger.debug(df.head(5))
    df.plot(
        kind="line",
        x=x[0],
        xlabel=x[1],
        y=y[0],
        ylabel=y[1],
        label=y[1],
    )
    plt.title(title)
    plt.savefig(os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.png"))


filename = "meta_infl_annum_99_23.csv"
lfsave(
    filename,
    ("ano", "Ano"),
    ("meta", "Meta de inflação"),
    "Metas de inflação (1999-2023)",
)
