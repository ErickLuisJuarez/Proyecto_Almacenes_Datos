"""Carga del dataset analítico para las páginas .qmd y los análisis.
Si todavía no existe la muestra real que genera el pipeline, devuelve datos SINTÉTICOS y lo avisa (es_demo = True)
para que todos puedan trabajar y previsualizar desde el día 1. NUNCA entregar con es_demo = True.
"""
import pandas as pd

from . import ingesta, limpieza, utils

MUESTRA = utils.RAIZ / "data" / "sample"

FUENTES = {  # fuente de cada variable del dataset analítico (E1)
    "id_cct": "SEP, Infraestructura física educativa", "nivel_educativo": "SEP, Infraestructura física educativa",
    "entidad": "SEP, Infraestructura física educativa", "ciclo_escolar": "SEP, Infraestructura física educativa",
    "computadora": "SEP, Infraestructura física educativa", "laptop": "SEP, Infraestructura física educativa",
    "con_luz": "SEP, Infraestructura física educativa", "internet": "SEP, Infraestructura física educativa",
    "indice_marginacion": "CONAPO, Índice de marginación 2020", "grado_marginacion": "CONAPO, Índice de marginación 2020",
    "pob_total": "CONAPO, Índice de marginación 2020", "monto_pef_2026_entidad": "SHCP, PEF 2026 (Ramo 11)",
}


def _demo(version):
    cfg = utils.cargar_config()
    ctx = {"cfg": cfg, "demo": True, "df": ingesta._datos_demo(cfg["semilla"]), "registro": utils.Registro()}
    return limpieza.ejecutar(ctx) if version == "limpio" else ctx


def cargar(version="crudo"):
    """version: 'crudo' (antes de preparar: para el EDA) o 'limpio' (después). Devuelve (df, es_demo)."""
    ruta = MUESTRA / f"analitico_{version}.csv"
    if ruta.exists():
        return pd.read_csv(ruta), False
    return _demo(version)["df"], True


def registro_limpieza():
    """Registro de limpieza como DataFrame, y si es de prueba. Lo genera el pipeline."""
    ruta = MUESTRA / "registro_limpieza.csv"
    if ruta.exists():
        return pd.read_csv(ruta), False
    return _demo("limpio")["registro"].a_dataframe(), True


def aviso(es_demo):
    """Texto Markdown para el inicio de una página: avisa si lo que se ve son datos de prueba."""
    if es_demo:
        return ("> **ATENCIÓN: datos sintéticos de prueba.** Todavía no existe la muestra real que genera el pipeline "
                "(`pipeline/data/sample/`). Las cifras y figuras de esta página NO son resultados. No entregar así.")
    return ""


def datos_de_partida(df):
    """Filas, variables, fuente, tipo y faltantes de cada variable, más periodo y territorio cubiertos."""
    tabla = pd.DataFrame({"variable": df.columns, "tipo": [str(t) for t in df.dtypes],
                          "fuente": [FUENTES.get(c, "derivada") for c in df.columns],
                          "faltantes": df.isna().sum().values})
    resumen = {"filas": len(df), "variables": df.shape[1],
               "ciclos": sorted(df["ciclo_escolar"].dropna().unique().tolist()),
               "entidades": int(df["entidad"].nunique()), "escuelas": int(df["id_cct"].nunique())}
    return tabla, resumen
