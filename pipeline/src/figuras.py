"""Figuras del EDA con las mismas reglas para todas: título que diga lo que muestra, ejes con nombre y unidades,
legibles en escala de grises. Título y etiquetas son argumentos OBLIGATORIOS (sin valor por defecto) a propósito.
Se guardan en entregas/E2_eda_preparacion/img/ como fig_<nombre>.png; el nombre lleva el número: '04_lorenz_computadoras'.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # sin ventana: sirve en servidores y dentro del pipeline
import matplotlib.pyplot as plt
import numpy as np

from . import metricas

IMG = Path(__file__).resolve().parents[2] / "entregas" / "E2_eda_preparacion" / "img"
AZUL, NARANJA = "#1F3A5F", "#D9822B"       # con luminosidad distinta: se distinguen también en grises
plt.rcParams.update({"figure.figsize": (7, 4.2), "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "font.size": 10})


def guardar(fig, nombre):
    IMG.mkdir(parents=True, exist_ok=True)
    ruta = IMG / f"fig_{nombre}.png"
    fig.savefig(ruta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return ruta


def histograma(serie, titulo, xlabel, ylabel, bins=30):
    fig, ax = plt.subplots()
    ax.hist(serie.dropna(), bins=bins, color=AZUL, edgecolor="white")
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    return fig


def barras_ordenadas(serie, titulo, xlabel, ylabel="Número de escuelas", max_categorias=15):
    f = serie.dropna().value_counts().head(max_categorias)
    fig, ax = plt.subplots()
    ax.bar(f.index.astype(str), f.values, color=AZUL)
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.tick_params(axis="x", rotation=45)
    return fig


def boxplot_por_grupo(df, valor, grupo, titulo, xlabel, ylabel):
    orden = df.groupby(grupo)[valor].median().sort_values().index
    fig, ax = plt.subplots()
    ax.boxplot([df.loc[df[grupo] == g, valor].dropna() for g in orden], tick_labels=[str(g) for g in orden],
               patch_artist=True, boxprops={"facecolor": "#C9D6E8"}, medianprops={"color": NARANJA, "linewidth": 2})
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.tick_params(axis="x", rotation=45)
    return fig


def curva_lorenz(valores, titulo, xlabel, ylabel):
    p, L = metricas.lorenz(valores)
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.plot(p, L, color=AZUL, linewidth=2, label=f"Curva de Lorenz (Gini = {metricas.gini(valores):.2f})")
    ax.plot([0, 1], [0, 1], color=NARANJA, linestyle="--", label="Igualdad perfecta")
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.legend()
    return fig


def mapa_calor(matriz, titulo):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matriz.values, cmap="Blues", vmin=-1, vmax=1)
    ax.set_xticks(range(len(matriz.columns)), matriz.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(matriz.index)), matriz.index)
    ax.grid(False)
    fig.colorbar(im, ax=ax, label="Correlación")
    ax.set_title(titulo)
    return fig


def comparar_antes_despues(antes, despues, titulo, xlabel, ylabel, bins=30):
    fig, ax = plt.subplots()
    ax.hist(antes.dropna(), bins=bins, alpha=0.6, color=AZUL, label="Antes de preparar")
    ax.hist(despues.dropna(), bins=bins, alpha=0.6, color=NARANJA, label="Después de preparar")
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.legend()
    return fig


def scree(varianza, titulo, objetivo):
    """Gráfico de sedimentación del PCA: varianza por componente y acumulada, con la línea del objetivo."""
    fig, ax = plt.subplots()
    ax.bar(varianza["componente"], varianza["varianza"] * 100, color=AZUL, label="Por componente")
    ax.plot(varianza["componente"], varianza["acumulada"] * 100, color=NARANJA, marker="o", label="Acumulada")
    ax.axhline(objetivo * 100, color="gray", linestyle="--", label=f"Objetivo ({objetivo:.0%})")
    ax.set(title=titulo, xlabel="Componente principal", ylabel="Varianza explicada (%)")
    ax.legend()
    return fig


IMG_DEMO = Path(__file__).resolve().parents[1] / "output" / "figuras_demo"   # ignorada por git


def mostrar(fig, nombre, pie, demo=False):
    """Guarda la figura y devuelve Markdown (imagen + 'Fig. N. pie') para una celda de Quarto.
    El número sale del prefijo del nombre ('04_lorenz' -> Fig. 4): texto y archivo siempre coinciden.
    Con demo=True (datos sintéticos) se guarda en pipeline/output/figuras_demo/ para que NUNCA lleguen a img/ ni a git."""
    from IPython.display import Markdown
    if demo:
        IMG_DEMO.mkdir(parents=True, exist_ok=True)
        fig.savefig(IMG_DEMO / f"fig_{nombre}.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        ruta = f"../../pipeline/output/figuras_demo/fig_{nombre}.png"
    else:
        guardar(fig, nombre)
        ruta = f"img/fig_{nombre}.png"
    return Markdown(f"![]({ruta})\n\n*Fig. {int(nombre.split('_')[0])}. {pie}*")
