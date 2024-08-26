import logging
import logging.config
import os
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
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


def readcsv(filename: str, index: str = None):
    csv = pd.read_csv(
        os.path.join(INPUT_DIR, f"{os.path.splitext(filename)[0]}.csv"), delimiter=","
    )

    return csv.set_index(index) if index else csv


def lfplots(
    filename: str,
    x: tuple[str, str],
    y: List[tuple[str, str]],
    titles: tuple[str, str],
    df: pd.DataFrame,
    colors: List[str] = None,
):
    logger.debug(f"Processing {filename}...")
    logger.debug(f"\n{df.head(3)}")

    if not colors:
        colors = ["#2ea668"] * len(y)

    df.plot.line(
        x=x[0],
        xlabel=x[1],
        y=[k[0] for k in y],
        ylabel=titles[0],
        label=[k[1] for k in y],
        color=colors,
        figsize=(6, 3.5),
    )

    if not NO_TITLE:
        plt.title(titles[1])
    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, f"{os.path.splitext(filename)[0]}.png"))


def lfsave(
    filename: str,
    x: tuple[str, str],
    y: List[tuple[str, str]],
    title: str = "",
    colors: List[str] = None,
):
    df = readcsv(filename)
    df = df[pd.to_numeric(df[x[0]], errors="coerce").notna()].astype(float)

    lfplots(filename, x, y, title, df)


PLOT_ALL = False
NO_TITLE = True

# https://coolors.co/2ea668-03012c-a03e99-3587a4-fcff4b
COLORS = ["#2EA668", "#3587A4", "#A03E99", "#03012C", "#FCFF4B"]

if PLOT_ALL:
    lfsave(
        "meta_infl_annum_99_23",
        ("ano", "Ano"),
        [("meta", "Meta de inflação")],
        ("Inflação (%)", "Metas de inflação (1999-2023)"),
    )

    lfsave(
        "ibge_deflator_96_21_t",
        ("ano", "Ano"),
        [("deflator", "Deflator do PIB")],
        ("Deflator do PIB", "Deflator do PIB (1996-2021)"),
    )

    lfsave(
        "ibge_pib_rsmi_96_21_t",
        ("ano", "Ano"),
        [("pib", "PIB")],
        ("PIB (Milhões de Reais)", "PIB (1996-2021)"),
    )

    lfsave(
        "ibge_ipca_hist_96_23_t",
        ("ano", "Ano"),
        [("var%", "Variação da Inflação (%)")],
        ("Inflação (%)", "Variação da Inflação (%) (1996-2023)"),
    )

    ipca = readcsv("ibge_ipca_hist_96_23_t", "ano")
    meta = readcsv("meta_infl_annum_99_23", "ano")

    ipca_meta = (
        pd.concat([ipca, meta], axis=1, join="inner")
        .reset_index()[:-1]
        .astype({"ano": "int", "var%": "float", "meta": "float"})
    )
    lfplots(
        "ibge_ipca_bcb_meta_99_23_t",  # Filename
        ("ano", "Ano"),  # X column, display_name
        [
            ("var%", "Variação da Inflação (%) (IPCA)"),
            ("meta", "Meta de Inflação Anual (%) (BCB)"),
        ],  # Series Lines
        (
            "Taxa de Inflação (%)",
            "Inflação (%) x Meta BCB (1999-2023)",
        ),  # Y Title, Graph Title
        ipca_meta,  # Series
        COLORS[0:2],  # Series line colors
    )

    igpdi = readcsv("igpdi_96_24_t").astype(
        {"igpdi": "float", "var%": "float", "var%acum": "float"}
    )
    igpdi["date"] = pd.to_datetime(igpdi.date, format="%Y-%m-%d")
    igpdi = igpdi[~(igpdi["date"] < "2003-01-01")].reset_index()  # Filtra antes de 2003
    igpdi["var%acum"] = igpdi.apply(
        lambda d: d["var%acum"] - 79.92923136, axis=1
    )  # 2003 = 0
    igpdi["ano"] = pd.DatetimeIndex(igpdi["date"]).year
    # igpdi = igpdi.set_index("date")

    meta = readcsv("meta_infl_annum_99_23")[:-1].astype(
        {"ano": "int", "meta": "float", "metacum": "float"}
    )
    meta = meta.loc[meta.index.repeat(12)]
    meta = meta[~(meta["ano"] < 2003)].reset_index()  #  Filtra antes de 2003
    meta["metacum"] = meta.apply(lambda k: k["metacum"] - 25.5, axis=1)  # 2003 = 0

    igpdi_meta = pd.concat([igpdi, meta], axis=1, join="inner")
    igpdi_meta = igpdi_meta[["date", "var%acum", "meta", "metacum"]]

    lfplots(
        "igpdi_96_24_t",
        ("date", "Ano"),
        [("var%acum", "IGP-DI Acumulado (%)"), ("metacum", "Meta BCB Acumulada (%)")],
        ["Inflação (%)", "IGP-DI - Variação Acumulada"],
        igpdi_meta,
        COLORS[0:2],
    )

ipca = readcsv("ibge_ipca_hist_96_23_t")[:-1].astype({"ano": "int"})
meta = readcsv("meta_infl_annum_99_23")[:-1].astype(
    {"ano": "int", "meta": "float", "metacum": "float"}
)
meta = meta[~(meta["ano"] < 2003)].reset_index()  #  Filtra antes de 2003
meta["metacum"] = meta.apply(lambda k: k["metacum"] - 25.5, axis=1)  # 2003 = 0

ipca_meta = (
    pd.concat([ipca, meta], axis=1, join="inner")
    .reset_index()
    .astype(
        {
            "ano": "int",
            "var%": "float",
            "var%acum": "float",
            "meta": "float",
            "metacum": "float",
        }
    )
)

print(ipca)
print(meta)

ipca_meta = ipca_meta[["ano", "var%acum", "metacum"]]
cols = ["ano", "ano1", "var%acum", "metacum"]
ipca_meta.columns = cols
ipca_meta = ipca_meta[["ano", "var%acum", "metacum"]]
print(ipca_meta.dtypes)

lfplots(
    "ipca_meta_03_24_t",
    ("ano", "Ano"),
    [("var%acum", "IPCA Acumulado (%)"), ("metacum", "Meta BCB Acumulada (%)")],
    ["Inflação (%)", "IPCA - Variação Acumulada"],
    ipca_meta,
    COLORS[0:2],
)
