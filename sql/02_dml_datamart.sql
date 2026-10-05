-- Consultas para el Data Mart --
-- P4: Ahorro de presupuesto por municipio --
SELECT
    geo.entidad,
    geo.municipio,
    SUM(hechos.monto_ahorro_licenciamiento_mxn) AS ahorro_total
FROM
    dw.fact_infraestructura_escolar AS hechos
INNER JOIN dw.dim_geografica AS geo
    ON hechos.sk_geografica = geo.sk_geografica
GROUP BY ROLLUP(geo.entidad, geo.municipio)
ORDER BY geo.entidad, geo.municipio;
