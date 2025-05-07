from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
import os
import logging

class MariaDBClient:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(url)
        self.Session = sessionmaker(bind=self.engine)


    def get_products_by_category(self, categoria: str):
        session = self.Session()
        all_articulos = []

        try:
            grupos_result = session.execute(
                text("SELECT DISTINCT id_grupo FROM productos WHERE categoria = :categoria"),
                {"categoria": categoria}
            )
            grupos = [row.id_grupo for row in grupos_result]

            for grupo in grupos:
                subgrupos_result = session.execute(
                    text("SELECT DISTINCT id_subgrupo FROM productos WHERE categoria = :categoria AND id_grupo = :grupo"),
                    {"categoria": categoria, "grupo": grupo}
                )
                subgrupos = [row.id_subgrupo for row in subgrupos_result]

                for subgrupo in subgrupos:
                    productos_result = session.execute(
                        text("SELECT p.categoria as categoria, p.nombre as nombre, p.precio as precio, s.nombre as supermercado, p.url as url, p.id_producto as p_id FROM productos p INNER JOIN supermercados s on p.id_supermercado = s.id_supermercado WHERE p.categoria = :categoria  AND p.id_grupo = :grupo AND p.id_subgrupo = :subgrupo"),
                        {"categoria": categoria,  "grupo": grupo, "subgrupo": subgrupo}
                    )

                    articulos = []

                    for row in productos_result:
                        
                        if row.categoria == 'Shampoos':
                            nombre_mod = 'Shampoo ' + row.nombre + ' ml'
                        elif row.categoria == 'Leches':
                            nombre_mod = 'Leche ' + row.nombre + ' ml'
                        elif row.categoria == 'Panes':
                            nombre_mod = 'Pan ' + row.nombre + ' g'
                        elif row.categoria == 'Arroces':
                            nombre_mod = 'Arroz ' + row.nombre + ' g'
                        elif row.categoria == 'Yerbas':
                            nombre_mod = 'Yerba ' + row.nombre + ' g'
                        elif row.categoria == 'Gaseosas':
                            nombre_mod = 'Gaseosa ' + row.nombre + ' ml'
                        elif row.categoria == 'Jabones':
                            nombre_mod = 'Jabón ' + row.nombre + ' g'
                        elif row.categoria == 'Fideos':
                            nombre_mod = 'Fideos ' + row.nombre + ' g'
                        else:
                            nombre_mod = row.nombre

                        articulo = {
                            "nombre": ' '.join(nombre_mod.title().split()),
                            "precio": row.precio,
                            "supermercado": row.supermercado.title(),
                            "url": row.url,
                            "p_id": row.p_id
                        }
                        articulos.append(articulo)

                    if articulos:
                        all_articulos.append(articulos)

            all_articulos.sort(key=len, reverse=True)

            return all_articulos

        finally:
            session.close()

    def get_products_by_description(self, nombre: str):
        session = self.Session()
        nombre = nombre.upper()
        all_articulos = []

        try:
            grupos_result = session.execute(
                text(f"SELECT DISTINCT id_grupo FROM productos WHERE UPPER(nombre) LIKE :nombre"),
                {"nombre": f"%{nombre}%"} 
            )
            grupos = [row.id_grupo for row in grupos_result]

            for grupo in grupos:
                subgrupos_result = session.execute(
                    text(f"SELECT DISTINCT id_subgrupo FROM productos WHERE UPPER(nombre) LIKE :nombre AND id_grupo = :grupo"),
                    {"nombre": f"%{nombre}%", "grupo": grupo} 
                )
                subgrupos = [row.id_subgrupo for row in subgrupos_result]

                for subgrupo in subgrupos:
                    productos_result = session.execute(
                        text(f"SELECT p.categoria as categoria, p.nombre as nombre, p.precio as precio, s.nombre as supermercado, p.url as url, p.id_producto as p_id FROM productos p INNER JOIN supermercados s ON p.id_supermercado = s.id_supermercado WHERE UPPER(p.nombre) LIKE :nombre AND p.id_grupo = :grupo AND p.id_subgrupo = :subgrupo"),
                        {"nombre": f"%{nombre}%", "grupo": grupo, "subgrupo": subgrupo}
                    )

                    articulos = []

                    for row in productos_result:
                        
                        if row.categoria == 'Shampoos':
                            nombre_mod = 'Shampoo ' + row.nombre + ' ml'
                        elif row.categoria == 'Leches':
                            nombre_mod = 'Leche ' + row.nombre + ' ml'
                        elif row.categoria == 'Panes':
                            nombre_mod = 'Pan ' + row.nombre + ' g'
                        elif row.categoria == 'Arroces':
                            nombre_mod = 'Arroz ' + row.nombre + ' g'
                        elif row.categoria == 'Yerbas':
                            nombre_mod = 'Yerba ' + row.nombre + ' g'
                        elif row.categoria == 'Gaseosas':
                            nombre_mod = 'Gaseosa ' + row.nombre + ' ml'
                        elif row.categoria == 'Jabones':
                            nombre_mod = 'Jabón ' + row.nombre + ' g'
                        elif row.categoria == 'Fideos':
                            nombre_mod = 'Fideos ' + row.nombre + ' g'
                        else:
                            nombre_mod = row.nombre
                            nombre_mod += ' g'

                        articulo = {
                            "nombre": ' '.join(nombre_mod.title().split()),
                            "precio": row.precio,
                            "supermercado": row.supermercado.title(),
                            "url": row.url,
                            "p_id": row.p_id
                        }
                        articulos.append(articulo)

                    if articulos:
                        all_articulos.append(articulos)

            all_articulos.sort(key=len, reverse=True)

            return all_articulos

        finally:
            session.close()

    def get_info(self):
        session = self.Session()
        try:
            supermercados_result = session.execute(
                text("SELECT nombre, url FROM supermercados WHERE is_active IS TRUE")
            )
            supermercados = [
                {"supermercado": row.nombre.title(), "url": row.url}
                for row in supermercados_result
            ]

            last_update_result = session.execute(
                text("SELECT MAX(__ingestion_timestamp) as last_update FROM webscraping_info")
            ).scalar()

            if last_update_result:
                # formatted_date = last_update_result.strftime("%d/%m/%Y %I:%M %p")
                formatted_date = last_update_result.strftime("%d/%m/%Y %H:%M")
            else:
                formatted_date = None

            return {
                "supermercados": supermercados,
                "lastUpdate": formatted_date
            }

        finally:
            session.close()

