"""Prueba de humo de las páginas .qmd de E2: extrae las celdas de Python y las ejecuta en orden, con datos de prueba
si todavía no hay muestra real. Sirve para detectar errores ANTES de hacer quarto render.
Correr desde pipeline/:  python tests/test_paginas.py"""
import os
import re
import sys
from pathlib import Path

PIPELINE = Path(__file__).resolve().parents[1]
PAGINAS = PIPELINE.parent / "entregas" / "E2_eda_preparacion"
CELDA = re.compile(r"^```\{python\}\n(.*?)^```", re.S | re.M)

fallas = 0
for pagina in sorted(PAGINAS.glob("*.qmd")):
    celdas = CELDA.findall(pagina.read_text(encoding="utf-8"))
    if not celdas:
        continue
    os.chdir(PAGINAS)                                   # Quarto ejecuta cada página desde su carpeta
    sys.path.insert(0, str(PIPELINE))
    espacio = {"__name__": "__main__"}
    for i, codigo in enumerate(celdas, 1):
        codigo = "\n".join(l for l in codigo.splitlines() if not l.startswith("#|"))
        try:
            exec(compile(codigo, f"{pagina.name}[celda {i}]", "exec"), espacio)
        except Exception as e:                           # noqa: BLE001
            fallas += 1
            print(f"FALLA en {pagina.name}, celda {i}: {type(e).__name__}: {e}")
            break
    else:
        print(f"OK  {pagina.name}: {len(celdas)} celdas")
if fallas:
    sys.exit(1)
print("Todas las páginas ejecutan")
