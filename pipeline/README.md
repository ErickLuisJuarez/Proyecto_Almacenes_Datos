# Pipeline de E2: staging → limpieza → reducción → muestreo → carga al DW

Un solo punto de entrada: `run_pipeline.py`. Parámetros (proyecto, datasets, semilla, umbrales, costo supuesto de licencia) en `config.yaml`.

## Instalación
```bash
cd pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Autenticación (solo para la corrida real)
No se suben llaves ni archivos `.json`. Usen credenciales de aplicación:
```bash
gcloud auth application-default login
gcloud config set project proyectoalmacenesdatos   # o su propio proyecto (cambiar también config.yaml)
```
Cada integrante necesita permisos en el proyecto (BigQuery Job User y BigQuery Data Editor) o usar su propio proyecto.

## Ejecución
```bash
python run_pipeline.py --demo   # prueba el flujo con datos SINTÉTICOS, sin credenciales (unos segundos)
python run_pipeline.py          # corrida real contra BigQuery (tiempo: por medir)
```
El registro de limpieza queda en `pipeline/output/registro_limpieza.csv` (no se sube a git).

## Quién escribe qué (contratos en el docstring de cada archivo)
| Archivo | Responsable | Estado |
|---|---|---|
| `src/ingesta.py` | Mario | demo listo; **ingesta real pendiente** |
| `src/calidad.py` | Mario | diagnóstico básico listo; atípicos y llaves pendientes |
| `src/limpieza.py` | Mario | 2 ejemplos listos (texto, duplicados); faltantes y atípicos pendientes |
| `src/reduccion.py` | Cesar | pendiente |
| `src/muestreo.py` | Cesar | decisión "no aplica" lista; justificar o implementar |
| `src/carga.py` | Cesar | demo listo; **carga real pendiente** |

## Reglas
- Sin pasos manuales ni rutas absolutas; todo parámetro va en `config.yaml`.
- Idempotente: correrlo dos veces da el mismo resultado (`CREATE OR REPLACE`).
- Semilla fija (`config.yaml`) y versiones fijadas (`requirements.txt`).
- Cada tratamiento de datos se registra con `ctx["registro"].agregar(...)`; nada se elimina ni se imputa en silencio.
- Prueba externa: antes de entregar, alguien que NO escribió el pipeline lo corre desde un clon limpio y documenta el resultado en `pipeline.qmd`.

## Piezas compartidas (no reimplementar)
- `src/metricas.py`: Gini, curva de Lorenz, entropía normalizada y resúmenes estadísticos. Una sola implementación para cifras, figuras y texto.
- `src/figuras.py`: estilo y funciones de figuras (título y ejes obligatorios). Guardan en `entregas/E2_eda_preparacion/img/`.
- `src/utils.py`: `equipos(df)` y `apto_proxy(df)` son la definición única de esas dos variables derivadas.
- `tests/test_metricas.py`: `python tests/test_metricas.py` (debe imprimir "Todas las pruebas pasaron").

## Qué más hay en `src/` y `tests/`
- `src/datos.py`: carga el dataset para las páginas (crudo o limpio); si no hay muestra real, devuelve datos sintéticos y avisa.
- `src/eda.py`: tablas del EDA (descriptiva por variable y por grupo, Gini y entropía por grupo, antes vs. después, hallazgos).
- `src/calidad.py`: `tabla_calidad`, `atipicos_iqr`, `faltantes_por_grupo`.
- `src/reduccion.py`: `chi2_con_efecto` (con V de Cramér), `ajustar_bonferroni`, `correlaciones_redundantes`, `pca_varianza`, `plantilla_decision`.
- `src/exportar.py`: escribe la muestra y el registro de limpieza (real: `data/sample/`; demo: `output/`, ignorado por git).
- `tests/`: `test_metricas.py`, `test_helpers.py` y `test_paginas.py` (ejecuta las celdas de las páginas con datos de prueba).
