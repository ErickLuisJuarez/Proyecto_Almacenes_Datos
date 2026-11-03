"""Pruebas de los helpers de calidad, reducción y EDA.  Correr desde pipeline/:  python tests/test_helpers.py"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import calidad, eda, reduccion  # noqa: E402

# atípicos por IQR
s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 100.0])
mascara, (inf, sup) = calidad.atipicos_iqr(s)
assert mascara.sum() == 1 and bool(mascara.iloc[-1]) and inf < 1 and sup < 100

# chi-cuadrada: asociación perfecta (V = 1) e independencia (V ~ 0)
x = pd.Series(list("ab") * 50)
r = reduccion.chi2_con_efecto(x, x)
assert abs(r["v_cramer"] - 1) < 1e-9 and r["p_valor"] < 1e-6
y = pd.Series(list("aabb") * 25)
assert reduccion.chi2_con_efecto(x, y)["v_cramer"] < 0.05
assert np.allclose(reduccion.ajustar_bonferroni([0.01, 0.2, 0.5]), [0.03, 0.6, 1.0])

# correlación y PCA con columnas redundantes
rng = np.random.default_rng(0)
a = rng.normal(size=300)
df = pd.DataFrame({"a": a, "b": 2 * a + rng.normal(scale=0.01, size=300), "c": rng.normal(size=300)})
m, pares = reduccion.correlaciones_redundantes(df, ["a", "b", "c"], 0.9)
assert len(pares) == 1 and {pares.loc[0, "variable_a"], pares.loc[0, "variable_b"]} == {"a", "b"}
var, cargas, n = reduccion.pca_varianza(df, ["a", "b", "c"], 0.60)
assert abs(var["acumulada"].iloc[-1] - 1) < 1e-9 and var["varianza"].iloc[0] > 0.6 and n == 1

# plantilla de decisión: no se escapa ninguna variable
assert len(reduccion.plantilla_decision(df)) == 3

# EDA: participación del top y Gini por grupo
assert abs(eda.participacion_top([10] + [1] * 9, 0.10) - 10 / 19) < 1e-12
d = pd.DataFrame({"g": list("aabb"), "v": [1, 1, 0, 8]})
gg = eda.gini_por_grupo(d, "v", "g")
assert gg["a"] == 0 and abs(gg["b"] - 0.5) < 1e-12
print("Todas las pruebas de helpers pasaron")
