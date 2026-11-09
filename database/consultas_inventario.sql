-- ============================================================================
-- SCRIPT DE ANÁLISIS AVANZADO: SEGMENTACIÓN ABC (PARETO 80/20) Y AGREGACIÓN
-- PROYECTO: SMARTSTOCK FORECASTING
-- OBJETIVO: Optimizar índices y segmentar SKUs según su aporte a la facturación.
-- ============================================================================

-- 1. OPTIMIZACIÓN DE INFRAESTRUCTURA Y RENDIMIENTO (ESTRATEGIA DE INDEXACIÓN)
-- Creamos índices compuestos e índices B-Tree para optimizar los JOINs y agrupaciones temporales.
CREATE INDEX IF NOT EXISTS idx_transactions_stock_date 
ON ecommerce_transactions (stock_code, invoice_date);

CREATE INDEX IF NOT EXISTS idx_transactions_customer_country 
ON ecommerce_transactions (customer_id, country);


-- 2. VISTA ANALÍTICA AVANZADA: CLASIFICACIÓN ABC DE INVENTARIOS (PARETO 80/20)
-- Utiliza múltiples CTEs y Funciones de Ventana para calcular la participación acumulada.
CREATE OR REPLACE VIEW vista_segmentacion_abc_pareto AS
WITH Revenue_Por_Producto AS (
    SELECT 
        stock_code,
        description,
        SUM(quantity * unit_price) AS total_revenue,
        COUNT(invoice_no) AS total_transacciones
    FROM ecommerce_transactions
    WHERE quantity > 0 AND unit_price > 0 -- Filtro de consistencia en el origen
    GROUP BY stock_code, description
),
Acumulado_Revenue AS (
    SELECT 
        stock_code,
        description,
        total_revenue,
        total_transacciones,
        SUM(total_revenue) OVER (ORDER BY total_revenue DESC) AS revenue_acumulado,
        SUM(total_revenue) OVER () AS revenue_total_global
    FROM Revenue_Por_Producto
),
Porcentaje_Pareto AS (
    SELECT 
        stock_code,
        description,
        total_revenue,
        total_transacciones,
        ROUND((revenue_acumulado / revenue_total_global) * 100, 2) AS porcentaje_acumulado
    FROM Acumulado_Revenue
)
SELECT 
    stock_code,
    description,
    total_revenue,
    total_transacciones,
    porcentaje_acumulado,
    CASE 
        WHEN porcentaje_acumulado <= 80.00 THEN 'A (Crítico - 80% Facturación)'
        WHEN porcentaje_acumulado <= 95.00 THEN 'B (Medio - 15% Facturación)'
        ELSE 'C (Bajo - 5% Facturación)'
    END AS clasificacion_abc
FROM Porcentaje_Pareto;


-- 3. CONSULTA DE AGREGACIÓN TEMPORAL PARA SERIES DE TIEMPO (INSUMO PYTHON)
-- Estructuración de datos históricos agregados mensualmente listos para modelos predictivos.
SELECT 
    stock_code,
    DATE_TRUNC('month', invoice_date)::DATE AS mes_no,
    SUM(quantity) AS total_unidades_demandadas,
    SUM(quantity * unit_price) AS facturacion_mensual,
    COUNT(DISTINCT invoice_no) AS volumen_pedidos
FROM ecommerce_transactions
WHERE quantity > 0 
  AND stock_code IN (SELECT stock_code FROM vista_segmentacion_abc_pareto WHERE porcentaje_acumulado <= 80.00)
GROUP BY stock_code, DATE_TRUNC('month', invoice_date)::DATE
ORDER BY stock_code, mes_no ASC;
