"""Exporta lo que necesitan las páginas .qmd: el dataset en dos momentos (crudo y limpio) y el registro de limpieza.
Corrida real -> pipeline/data/sample/ (se sube a git: el repo lleva la muestra y el código para regenerarla).
Corrida --demo -> pipeline/output/ (NO se sube), para que datos sintéticos nunca se mezclen con los reales.
"""
from . import utils


def carpeta(ctx):
    c = utils.RAIZ / ("output" if ctx["demo"] else "data/sample")
    c.mkdir(parents=True, exist_ok=True)
    return c


def guardar_dataset(ctx, version):
    """version: 'crudo' (justo después de la ingesta, para el EDA) o 'limpio' (ya preparado)."""
    df, tope = ctx["df"], ctx["cfg"]["salida"]["muestra_filas"]
    if len(df) > tope:
        df = df.sample(n=tope, random_state=ctx["cfg"]["semilla"])
    ruta = carpeta(ctx) / f"analitico_{version}.csv"
    df.to_csv(ruta, index=False, encoding="utf-8")
    return ruta


def guardar_registro(ctx):
    return ctx["registro"].guardar(carpeta(ctx))
