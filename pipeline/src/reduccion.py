"""PASO 4 — REDUCCIÓN DE DIMENSIONALIDAD.  Responsable: Cesar.

Las FUNCIONES de abajo están listas y probadas (tests/test_helpers.py): úsenlas desde reduccion.qmd.
Lo que NO está hecho y es de Cesar: elegir la variable objetivo (proxy acordada), correr las técnicas sobre las
variables correctas, decidir qué se conserva y justificarlo, y llenar ctx["tabla_decision"] en ejecutar().
Contrato de ctx["tabla_decision"]: UNA FILA POR CADA VARIABLE del dataset con Variable | Tipo | Tecnicas |
Decision (conservar/descartar/transformar/combinar) | Justificacion. Umbrales: ctx["cfg"]["umbrales"].
Fuga de información: imputación, estandarización, PCA y selección por chi² aprenden de los datos; aquí se calculan
sobre todo el dataset solo para decidir, pero en el modelado se ajustarán únicamente con entrenamiento (documentarlo).
Cuidado con la circularidad: si la variable objetivo se arma con con_luz y equipos, no se prueba con_luz contra ella.
"""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def plantilla_decision(df):
    """Una fila por variable, con el tipo detectado y el resto por llenar: así ninguna variable se queda sin decisión."""
    return pd.DataFrame({"Variable": df.columns,
                         "Tipo": ["Numérica" if pd.api.types.is_numeric_dtype(df[c]) else "Categórica" for c in df.columns],
                         "Técnica(s)": "[PENDIENTE]", "Decisión": "[PENDIENTE]", "Justificación": "[PENDIENTE]"})


def discretizar(serie, cuantiles=4):
    """Convierte una numérica en categorías por cuantiles para poder usar chi-cuadrada."""
    return pd.qcut(serie, q=cuantiles, duplicates="drop")


def chi2_con_efecto(x, y):
    """Chi-cuadrada entre dos categóricas, con tamaño del efecto (V de Cramér) y la proporción de celdas con
    frecuencia esperada < 5 (si es alta, la prueba no es confiable). Con n grande casi todo sale significativo: leer V."""
    t = pd.crosstab(x, y)
    if min(t.shape) < 2:   # una variable con una sola categoría: no hay nada que probar
        return {"chi2": np.nan, "gl": 0, "p_valor": np.nan, "n": int(t.to_numpy().sum()),
                "v_cramer": np.nan, "celdas_esperadas_menores_a_5": np.nan}
    chi2, p, gl, esperadas = stats.chi2_contingency(t, correction=False)   # sin corrección de Yates: V de Cramér estándar
    n, k = int(t.to_numpy().sum()), min(t.shape) - 1
    return {"chi2": float(chi2), "gl": int(gl), "p_valor": float(p), "n": n,
            "v_cramer": float(np.sqrt(chi2 / (n * k))) if k > 0 else np.nan,
            "celdas_esperadas_menores_a_5": float((esperadas < 5).mean())}


def ajustar_bonferroni(p_valores):
    """p ajustado por comparaciones múltiples (Bonferroni): p * número de pruebas, con tope de 1."""
    p = np.asarray(p_valores, dtype=float)
    return np.minimum(1.0, p * len(p))


def correlaciones_redundantes(df, columnas, umbral=0.90):
    """Matriz de Spearman y pares con |rho| >= umbral (candidatos a redundantes: se conserva uno y se justifica cuál)."""
    m = df[columnas].corr(method="spearman")
    pares = [(a, b, float(m.loc[a, b])) for i, a in enumerate(columnas) for b in columnas[i + 1:]
             if abs(m.loc[a, b]) >= umbral]
    return m, pd.DataFrame(pares, columns=["variable_a", "variable_b", "rho"])


def pca_varianza(df, columnas, objetivo=0.85):
    """PCA sobre variables numéricas estandarizadas (se descartan filas con faltantes). Devuelve la tabla de varianza
    explicada (para el scree), las cargas y cuántos componentes hacen falta para llegar a `objetivo`.
    No aplicar sin discusión a variables binarias o one-hot."""
    X = StandardScaler().fit_transform(df[columnas].dropna())
    pca = PCA().fit(X)
    varianza = pd.DataFrame({"componente": [f"PC{i + 1}" for i in range(len(pca.explained_variance_ratio_))],
                             "varianza": pca.explained_variance_ratio_,
                             "acumulada": np.cumsum(pca.explained_variance_ratio_)})
    cargas = pd.DataFrame(pca.components_.T, index=columnas, columns=varianza["componente"])
    return varianza, cargas, int((varianza["acumulada"] < objetivo).sum() + 1)


def ejecutar(ctx):
    print("    reducción: PENDIENTE (Cesar): ver docstring; funciones auxiliares ya disponibles")
    return ctx
