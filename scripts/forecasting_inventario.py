"""
MÓDULO DE INGENIERÍA DE DATOS Y LIMPIEZA AUTOMATIZADA (ETL)
Proyecto: SmartStock Forecasting
Autor: Ricardo José Bolívar Orozco
"""

import pandas as pd
import numpy as np
import os
import logging

# Configuración del sistema de traza de logs para producción
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ECommerceETLPipeline:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """Carga el dataset transaccional manejando codificaciones comunes."""
        if not os.path.exists(self.file_path):
            logging.error(f"Archivo no encontrado en la ruta: {self.file_path}")
            raise FileNotFoundError
        
        logging.info("Iniciando la carga de datos transaccionales...")
        # Manejo de encoding clásico para datasets de UK / Europa
        self.df = pd.read_csv(self.file_path, encoding='ISO-8859-1')
        logging.info(f"Datos cargados exitosamente. Registros iniciales: {self.df.shape[0]}")
        return self.df

    def clean_data(self) -> pd.DataFrame:
        """Pipeline estricto de calidad de datos y eliminación de ruido operativo."""
        if self.df is None:
            self.load_data()

        logging.info("Ejecutando transformaciones y limpieza profunda...")

        # 1. Conversión de tipos estricta y formateo de tiempo uniforme
        self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'], errors='coerce')
        
        # 2. Gestión de nulos críticos sin pérdida de integridad masiva
        # Reemplazamos descripciones faltantes y removemos transacciones sin ID de cliente si es necesario
        self.df['Description'] = self.df['Description'].fillna('MUESTRA_SIN_DESCRIPCION').str.strip()
        
        # 3. Tratamiento analítico de devoluciones y cancelaciones
        # En e-commerce, cantidades negativas representan cancelaciones. Las aislamos del flujo normal de demanda.
        inicial_rows = self.df.shape[0]
        self.df = self.df[(self.df['Quantity'] > 0) & (self.df['UnitPrice'] > 0)]
        filas_eliminadas = inicial_rows - self.df.shape[0]
        logging.info(f"Filas inconsistentes removidas (valores <= 0 o cancelaciones): {filas_eliminadas}")

        # 4. Feature Engineering: Construcción del vector de ingresos agregados
        self.df['TotalRevenue'] = self.df['Quantity'] * self.df['UnitPrice']
        
        # Extraer dimensiones temporales para el EDA posterior
        self.df['Year'] = self.df['InvoiceDate'].dt.year
        self.df['Month'] = self.df['InvoiceDate'].dt.month
        self.df['DayOfWeek'] = self.df['InvoiceDate'].dt.dayofweek

        logging.info(f"Proceso ETL completado. Registros limpios para modelado: {self.df.shape[0]}")
        return self.df

    def export_to_csv(self, output_path: str):
        """Exporta el dataset procesado listo para el pipeline de Machine Learning."""
        if self.df is not None:
            self.df.to_csv(output_path, index=False)
            logging.info(f"Dataset limpio exportado correctamente en: {output_path}")

if __name__ == "__main__":
    # Bloque de ejecución de prueba local
    # Reemplaza con la ruta de tu archivo descargado de Kaggle 'data.csv'
    RUTA_DATASET = "data/data.csv" 
    RUTA_SALIDA = "data/ecommerce_limpio.csv"
    
    try:
        pipeline = ECommerceETLPipeline(RUTA_DATASET)
        pipeline.load_data()
        pipeline.clean_data()
        # pipeline.export_to_csv(RUTA_SALIDA) # Descomentar al tener las carpetas físicas creadas
    except Exception as e:
        logging.critical(f"Error fatal en la ejecución del pipeline: {e}")
