"""Tablas del EDA listas para las páginas. Todas se apoyan en metricas.py: nadie recalcula a mano."""
import numpy as np
import pandas as pd

from . import metricas


def descriptiva_numerica(df, columnas):
    """Una columna por variable y una fila por medida (localización, variabilidad y forma)."""
    return pd.DataFrame({c: metricas.resumen_numerico(df[c]) for c in columnas})


def descriptiva_por_grupo(df, valor, grupo):
    """Comparación entre grupos: n, media, mediana, desviación e IQR de una variable numérica."""
    g = df.groupby(grupo)[valor]
    return pd.DataFrame({"n": g.count(), "media": g.mean(), "mediana": g.median(), "desviacion": g.std(),
                         "iqr": g.quantile(0.75) - g.quantile(0.25)}).sort_values("mediana", ascending=False)


def gini_por_grupo(df, valor, grupo):
    return df.groupby(grupo)[valor].apply(metricas.gini).rename("gini")


def entropia_por_grupo(df, columna, grupo):
    return df.groupby(grupo)[columna].apply(metricas.entropia_normalizada).rename("entropia_normalizada")


def participacion_top(valores, fraccion=0.10):
    """Qué parte del total acumula el top `fraccion` de las unidades (p. ej. el 10 % de las escuelas)."""
    x = np.sort(pd.Series(valores).dropna().to_numpy(dtype=float))[::-1]
    k = max(1, int(np.ceil(len(x) * fraccion)))
    return float(x[:k].sum() / x.sum())


def antes_despues(antes, despues, columnas):
    """Estadísticos de cada variable antes y después de preparar (el PDF pide al menos 3 variables)."""
    filas = []
    for c in columnas:
        a, d = metricas.resumen_numerico(antes[c]), metricas.resumen_numerico(despues[c])
        filas.append({"variable": c, "n_antes": a["n"], "n_despues": d["n"],
                      "media_antes": a["media"], "media_despues": d["media"],
                      "mediana_antes": a["mediana"], "mediana_despues": d["mediana"],
                      "desv_antes": a["desviacion"], "desv_despues": d["desviacion"],
                      "gini_antes": metricas.gini(antes[c]), "gini_despues": metricas.gini(despues[c])})
    return pd.DataFrame(filas).set_index("variable")


CAMPOS_HALLAZGO = ["Hallazgo", "Evidencia", "Tipo", "Pregunta de E0", "Consecuencia"]


def tabla_hallazgos(hallazgos):
    """hallazgos: lista de diccionarios con las claves de CAMPOS_HALLAZGO. Numera H1, H2, ..."""
    t = pd.DataFrame(hallazgos, columns=CAMPOS_HALLAZGO)
    t.index = [f"H{i + 1}" for i in range(len(t))]
    return t
