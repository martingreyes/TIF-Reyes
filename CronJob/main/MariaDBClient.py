from sqlalchemy import create_engine, text # type: ignore
import pandas as pd # type: ignore
import os
import logging

class MariaDBClient:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.engine = create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    def insert_into_db(self, table: str, df: pd.DataFrame):
        df.to_sql(table, con=self.engine, if_exists="append", index=False)


    def insert_into_productos(self, df: pd.DataFrame):
        # with self.engine.begin() as conn:
        #     conn.execute(text("TRUNCATE TABLE productos"))
        df.to_sql('productos', con=self.engine, if_exists="append", index=False)

    def get_active_tables(self) -> list:
        query = text("SELECT spider_name FROM supermercados WHERE is_active = true")
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return [row[0] for row in result]
        
    def get_products(self) -> pd.DataFrame:
        query = text("SELECT * FROM productos")
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        
    def delete_products(self, df_to_delete: pd.DataFrame):
        if df_to_delete.empty:
            return
        ids = df_to_delete['id_producto'].tolist()
        placeholders = ", ".join([f":id_{i}" for i in range(len(ids))])
        query = text(f"DELETE FROM productos WHERE id_producto IN ({placeholders})")
        params = {f"id_{i}": id_ for i, id_ in enumerate(ids)}
        with self.engine.begin() as conn:
            conn.execute(query, params)
        logging.info(f"Se eliminaron {len(df_to_delete)} productos.")


    def update_products(self, df_to_update: pd.DataFrame):
        if df_to_update.empty:
            return
        
        with self.engine.begin() as conn:
            for _, row in df_to_update.iterrows():
                query = text("""
                    UPDATE productos
                    SET precio = :precio, url = :url
                    WHERE id_producto = :id_producto
                """)
                conn.execute(query, {
                    "__ingestion_timestamp": row["__ingestion_timestamp"],
                    "precio": row["precio"],
                    "url": row["url"],
                    "id_producto": row["id_producto"]
                })
        logging.info(f"Se actualizaron {len(df_to_update)} productos.")

    def get_products_by_groups(self, new_only_df: pd.DataFrame) -> pd.DataFrame:
        if new_only_df.empty:
            return pd.DataFrame()
        
        id_grupos = new_only_df['id_grupo'].unique()
        id_grupo_str = ', '.join(map(str, id_grupos))
        query = text(f"""
        SELECT p.id_producto, p.categoria, p.marca, p.descripcion, p.volumen, s.nombre as supermercado
        FROM productos p
        INNER JOIN supermercados s ON p.id_supermercado = s.id_supermercado
        WHERE p.id_grupo IN ({id_grupo_str})
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query)
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        
    def update_product_subgroups(self, updates: list[dict]):

        if not updates:
            return
        
        # Convertir la lista de updates a DataFrame
        updates_df = pd.DataFrame(updates)
        
        # Actualización masiva usando pandas
        with self.engine.begin() as conn:
            for _, group in updates_df.groupby('id_subgrupo'):
                ids = group['id_producto'].tolist()
                id_subgrupo = group['id_subgrupo'].iloc[0]
                
                # Crear la consulta parametrizada
                placeholders = ", ".join([f":id_{i}" for i in range(len(ids))])
                query = text(f"""
                    UPDATE productos 
                    SET id_subgrupo = :id_subgrupo 
                    WHERE id_producto IN ({placeholders})
                """)
                
                # Preparar parámetros
                params = {"id_subgrupo": id_subgrupo}
                params.update({f"id_{i}": id_ for i, id_ in enumerate(ids)})
                
                # Ejecutar la actualización
                conn.execute(query, params)





        


