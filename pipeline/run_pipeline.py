#!/usr/bin/env python3
"""Punto de entrada único del pipeline de E2: staging -> limpieza -> reducción -> muestreo -> carga al DW.

  python run_pipeline.py --demo     # prueba el flujo con datos SINTÉTICOS, sin credenciales
  python run_pipeline.py            # corrida real contra BigQuery (requiere autenticación, ver README)
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import calidad, carga, exportar, ingesta, limpieza, muestreo, reduccion, utils  # noqa: E402

EXPORTAR_DESPUES = {"ingesta": "crudo", "muestreo": "limpio"}   # lo que leen las páginas .qmd
PASOS = [("ingesta", ingesta), ("calidad", calidad), ("limpieza", limpieza),
         ("reduccion", reduccion), ("muestreo", muestreo), ("carga", carga)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true", help="datos sintéticos, sin BigQuery")
    ap.add_argument("--config", default=None, help="ruta a un config.yaml alternativo")
    args = ap.parse_args()

    ctx = {"cfg": utils.cargar_config(args.config), "demo": args.demo, "df": None,
           "registro": utils.Registro()}
    for nombre, modulo in PASOS:
        n_in = None if ctx["df"] is None else len(ctx["df"])
        t0 = time.time()
        print(f"[{nombre}]")
        ctx = modulo.ejecutar(ctx)
        n_out = None if ctx["df"] is None else len(ctx["df"])
        print(f"    filas entrada={n_in} salida={n_out} ({time.time() - t0:.1f}s)")
        if nombre in EXPORTAR_DESPUES:
            print(f"    exportado: {exportar.guardar_dataset(ctx, EXPORTAR_DESPUES[nombre])}")

    ruta = exportar.guardar_registro(ctx)
    print(f"\nRegistro de limpieza guardado en {ruta}")


if __name__ == "__main__":
    main()
