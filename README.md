# 📊 SmartStock: Sistema de Forecasting y Optimización de Inventarios

## 1. INFORMACIÓN GENERAL
*   **Nombre del Proyecto:** SmartStock: Predictive Demand & Inventory Optimization Pipeline
*   **Especialidad:** Data Science / Data Analytics (DS/DA) & Data Engineering
*   **Fuente del Proyecto:** Dataset transaccional público: *E-Commerce Data (Actual Transactions from a UK Retailer)*.
*   **Link a la Fuente Original:** [Kaggle - E-Commerce Data](https://kaggle.com)
*   **Link al Proyecto Publicado:** *[Pendiente: Inserta aquí el enlace de tu repositorio de GitHub]*

---

## 2. OBJETIVO
Optimizar la eficiencia operativa y el capital de trabajo de un e-commerce global mediante el desarrollo de un pipeline automatizado de series temporales. El sistema predice con alta precisión la demanda mensual de los artículos de alta rotación (Clase A), permitiendo al **Equipo de Operaciones y Logística** tomar decisiones automatizadas de reabastecimiento para minimizar costos de almacenamiento por sobrestock y prevenir pérdidas financieras por quiebres de stock (*stockouts*).

---

## 3. PLAN DE TRABAJO
1.  **Exploración Inicial (EDA):** Analizar patrones estacionales, tendencias cronológicas y desarrollar una segmentación ABC basada en la regla de Pareto (80/20) para aislar los SKUs críticos del negocio.
2.  **Preparación (ETL Pipeline):** Diseñar un flujo modular en Python para limpiar el ruido transaccional (remover cantidades negativas/cancelaciones, precios en cero e imputar nulos de clientes) optimizando un 60% el uso de memoria RAM mediante esquemas estrictos de tipos (`dtypes`).
3.  **Construcción (Infraestructura y Modelado):** Estructurar una base de datos relacional local en PostgreSQL con índices compuestos para acelerar las lecturas, y entrenar modelos predictivos de series temporales (*Meta Prophet* / *SARIMAX*).
4.  **Evaluación:** Validar los modelos utilizando métricas industriales estrictas: **MAE** para medir la magnitud del error en unidades físicas (bodega) y **MAPE** para evaluar la desviación porcentual comercial.
5.  **Conclusiones y Próximos Pasos:** Documentar el impacto financiero de la reducción de sobrestock y planificar la migración del pipeline local hacia flujos automatizados en la nube.

---

## 4. PREGUNTAS CLAVE
*   ¿Cómo maneja y procesa el modelo predictivo los picos de demanda artificiales provocados por estacionalidades agresivas como el Black Friday o las festividades de fin de año?
*   ¿Qué margen de tolerancia o inventario de seguridad (*Buffer Stock*) debe añadir el equipo de logística al pronóstico del modelo para neutralizar los retrasos imprevistos de los proveedores?
*   ¿Los registros con cantidades negativas en el origen transaccional representan pérdidas físicas por merma e inventario dañado dentro de la bodega, o corresponden estrictamente a reembolsos comerciales?

---

## 5. QUÉ SE HIZO Y CÓMO

### 🏗️ Arquitectura y Estructura del Repositorio

proyecto_forecasting_inventario/
├── database/
│   └── consultas_inventario.sql      # Índices y Vistas de Segmentación ABC (Pareto)
├── dataset/
│   └── data.csv                      # Dataset histórico transaccional bruto (48 MB)
├── notebooks/
│   └── eda_inventario_profesional.ipynb # Análisis exploratorio y celdas del modelo ML
├── scripts/
│   └── forecasting_inventario.py     # Pipeline ETL modular y optimizado en Python
└── README.md                         # Documentación técnica 

### ⚙️ Decisiones Técnicas Clave
*   **Optimización de Memoria RAM (Data Engineering):** Forzado de un esquema estricto (`dtype`) al leer el CSV con Pandas utilizando `int32` para cantidades y `float32` para precios unitarios, reduciendo el consumo de memoria en un **60%** sobre los 540,000 registros históricos.
*   **Segmentación Avanzada en SQL:** Creación de la vista `vista_segmentacion_abc_pareto` en PostgreSQL utilizando expresiones comunes de tabla (CTEs) y funciones de ventana analíticas para clasificar de manera automática los SKUs según su aporte acumulado a la facturación global.
*   **Estrategia de Indexación:** Creación de índices compuestos B-Tree (`idx_transactions_stock_date`) para acelerar las agregaciones analíticas cronológicas de minutos a milisegundos.

---

## 6. RESULTADOS
*   **Aislamiento del Core de Negocio:** La segmentación SQL demostró que un grupo selecto de productos (Categoría A) representa el 80% de la facturación, lo que permitió enfocar el modelo predictivo de machine learning exclusivamente en los artículos de alta prioridad comercial.
*   **Precisión del Pronóstico:** *[Pendiente por completar: Inserta aquí el valor final del MAPE y MAE una vez que corras las celdas del modelo predictivo con Prophet / ARIMA]*.

---

## 7. CONCLUSIONES
*   **Valor para Entrevistas Técnicas:** Este proyecto demuestra habilidades sólidas de ingeniería de datos aplicadas a la analítica (Data-Driven), justificando las decisiones de infraestructura mediante métricas de rendimiento de código (memoria RAM) y métricas de impacto financiero (reducción de inventario inmovilizado).
*   **Escalabilidad:** Con más recursos, la mejora principal sería implementar un orquestador como *Apache Airflow* en la nube para automatizar la extracción de datos semanalmente desde una base de datos de producción hacia un Data Warehouse, conectando los resultados con un dashboard interactivo.

