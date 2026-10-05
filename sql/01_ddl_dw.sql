-- DIMENSIONES --
CREATE TABLE dw.dim_cct (
    sk_cct INT64 NOT NULL,
    id_cct STRING,
    nombre_escuela STRING,
    nivel_educativo STRING
);

CREATE TABLE dw.dim_geografica (
    sk_geografica INT64 NOT NULL,
    id_ine STRING,
    entidad STRING,
    municipio STRING,
    localidad STRING
);

CREATE TABLE dw.dim_fecha (
    sk_fecha INT64 NOT NULL,
    ciclo_escolar STRING,
    anio STRING,
    mes STRING
);

CREATE TABLE dw.dim_perfil_hardware (
    sk_perfil_hardware INT64 NOT NULL,
    id_perfil_hardware STRING,
    nombre_perfil STRING,
    cluster_id STRING
);

CREATE TABLE dw.dim_marginacion (
    sk_marginacion INT64 NOT NULL,
    id_marginacion STRING,
    indice_marginacion FLOAT64,
    grado_marginacion STRING
);

-- TABLA DE HECHOS --
CREATE TABLE dw.fact_infraestructura_escolar (
    sk_hecho INT64 NOT NULL,
    sk_cct INT64,
    sk_geografica INT64,
    sk_fecha INT64,
    sk_perfil_hardware INT64,
    sk_marginacion INT64,
    computadora INT64,
    laptop INT64,
    con_luz STRING,
    internet STRING,
    pob_total INT64,
    monto_pef_2026 FLOAT64,
    monto_ahorro_licenciamiento_mxn FLOAT64
);
