"""PASO 2 — CALIDAD (diagnóstico, no modifica nada).  Responsable: Mario.

Contrato: calcula cuántas filas/celdas están afectadas y en qué variables, y lo deja en ctx["diagnostico"].
NO limpia: eso se decide DESPUÉS de ver el diagnóstico (paso 3).
TODO (Mario): z robusto, llaves que no coinciden al unir fuentes, rangos y tipos imposibles.
"""
import pandas as pd

from . import utils


def tabla_calidad(df):
    """Diagnóstico por variable: tipo, faltantes (y %), valores distintos."""
    return pd.DataFrame({"tipo": df.dtypes.astype(str), "faltantes": df.isna().sum(),
                         "pct_faltantes": (df.isna().mean() * 100).round(2), "distintos": df.nunique()})


def atipicos_iqr(serie, k=1.5):
    """Marca como atípicos los valores fuera de [Q1 - k*IQR, Q3 + k*IQR]. Devuelve (máscara, (límite_inferior, límite_superior)).
    Un atípico NO se elimina por esto: primero decidir si es error o un valor extremo legítimo."""
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    inf, sup = q1 - k * (q3 - q1), q3 + k * (q3 - q1)
    return ((serie < inf) | (serie > sup)).fillna(False), (float(inf), float(sup))


def faltantes_por_grupo(df, columna, grupo):
    """Porcentaje de faltantes de `columna` dentro de cada grupo: sirve para ver si la ausencia tiene patrón."""
    return df.groupby(grupo)[columna].apply(lambda s: s.isna().mean() * 100).rename("pct_faltantes")



def ejecutar(ctx):
    df = ctx["df"]
    diag = {
        "filas": len(df),
        "variables": df.shape[1],
        "nulos_por_columna": df.isna().sum().to_dict(),
        "duplicados_exactos": int(df.duplicated().sum()),
        "duplicados_por_grano": int(df.duplicated(subset=utils.GRANO).sum()),
    }
    numericas = df.select_dtypes("number").columns
    diag["atipicos_iqr"] = {c: int(atipicos_iqr(df[c])[0].sum()) for c in numericas}
    ctx["diagnostico"] = diag
    print(f"    diagnóstico: {diag['filas']} filas, {diag['duplicados_por_grano']} duplicados por grano, "
          f"{sum(diag['nulos_por_columna'].values())} celdas faltantes")
    return ctx
