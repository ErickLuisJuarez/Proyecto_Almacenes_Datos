-- ============================================================================
-- Validaciones del DW poblado (E2): conteos, llaves huérfanas y unicidad del grano.
-- Cada consulta debe mostrar el resultado esperado; capturar pantalla para pipeline.qmd.
-- NO EJECUTADAS todavía en BigQuery. Los nombres de dataset vienen de pipeline/config.yaml.
-- ============================================================================

-- 1) Conteo de filas por tabla (ninguna debe quedar en 0)
SELECT 'dim_cct' AS tabla, COUNT(*) AS filas FROM eq_dw.dim_cct
UNION ALL SELECT 'dim_geografica', COUNT(*) FROM eq_dw.dim_geografica
UNION ALL SELECT 'dim_fecha', COUNT(*) FROM eq_dw.dim_fecha
UNION ALL SELECT 'dim_marginacion', COUNT(*) FROM eq_dw.dim_marginacion
UNION ALL SELECT 'dim_perfil_hardware', COUNT(*) FROM eq_dw.dim_perfil_hardware
UNION ALL SELECT 'fact_infraestructura_escolar', COUNT(*) FROM eq_dw.fact_infraestructura_escolar;

-- 2) Llaves huérfanas en el hecho (esperado: 0 en cada columna)
SELECT
    COUNTIF(c.sk_cct IS NULL) AS huerfanas_cct,
    COUNTIF(g.sk_geografica IS NULL) AS huerfanas_geografica,
    COUNTIF(f.sk_fecha IS NULL) AS huerfanas_fecha,
    COUNTIF(m.sk_marginacion IS NULL) AS huerfanas_marginacion
FROM eq_dw.fact_infraestructura_escolar AS h
LEFT JOIN eq_dw.dim_cct AS c ON h.sk_cct = c.sk_cct
LEFT JOIN eq_dw.dim_geografica AS g ON h.sk_geografica = g.sk_geografica
LEFT JOIN eq_dw.dim_fecha AS f ON h.sk_fecha = f.sk_fecha
LEFT JOIN eq_dw.dim_marginacion AS m ON h.sk_marginacion = m.sk_marginacion;

-- 3) Grano único: una fila por CCT por ciclo escolar (esperado: cero filas)
SELECT sk_cct, sk_fecha, COUNT(*) AS repeticiones
FROM eq_dw.fact_infraestructura_escolar
GROUP BY sk_cct, sk_fecha
HAVING COUNT(*) > 1;

-- 4) Llaves nulas en el hecho (esperado: 0)
SELECT COUNTIF(sk_cct IS NULL OR sk_geografica IS NULL OR sk_fecha IS NULL OR sk_marginacion IS NULL) AS llaves_nulas
FROM eq_dw.fact_infraestructura_escolar;
