from sqlalchemy import create_engine, text # type: ignore
import pandas as pd # type: ignore
import os

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
        with self.engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE productos"))
        df.to_sql('productos', con=self.engine, if_exists="append", index=False)

    def get_active_tables(self) -> list:
        query = text("SELECT spider_name FROM supermercados WHERE is_active = true")
        with self.engine.connect() as conn:
            result = conn.execute(query)
            return [row[0] for row in result]

