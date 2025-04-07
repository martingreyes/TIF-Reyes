from itemadapter import ItemAdapter
import re
class AtomoPrecioPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        # Convierte el precio de '$\xa01.113,00' a un formato numérico, pero deberia convertir # 836,00\xa0$
        price_keys = ['precio']

        for price_key in price_keys:
            value = adapter.get(price_key)

            # Eliminar caracteres como '$', '\xa0' y espacios
            value = value.replace('\xa0', '').replace(' ', '').replace('$', '')

            # Reemplazar el separador decimal de ',' a '.'
            value = value.replace('.', '').replace(',', '.')

            try:
                adapter[price_key] = round(float(value), 2)
            except ValueError:
                spider.logger.error(f"No se pudo convertir el precio: {value}")
                adapter[price_key] = None  # o podés levantar una excepción si preferís

        return item

class AtomoPipeline:

    marcas_shampoo = [  "PANTENE", "HEAD & SHOULDER", "SUAVE", "SEDAL", "PLUSBELLE", 
                        "INECTO", "DOVE", "ALGABO", "VO5", "TRESEMME","ELVIVE", "FRUCTIS", "317", "JOHNSON"
                    ]

    marcas_gaseosas = [ "COCA COLA", "PEPSI", "SCHWEPPES", "SPRITE", "SEVEN UP", 
                        "LEVITE", "FANTA", "P.DE LOS TOROS", "SECCO", "MANAOS",
                        "MIRINDA","RUMIPAL", "PASO DE LOS TOROS"
                    ]
    
    marcas_leches = ["LA SERENISIMA","VERONICA"]

    marcas_panes = ["LACTAL", "BELIER", "BIMBO", "MILLAN"] 

    marcas_arroces = ["GALLO","TIO CARLOS","AMANDA","NOBLE","SAN JAVIER", "ALA", "DON MARCOS", "MENCHO", "MOCOVI", "VINCHA DE ORO", "APOSTOLES"]

    marcas_jabones = ["DUC","DOVE","PLUSBELLE","REXONA","LUX","PROTEX","VERITAS","ST TROPEZ",
                    "NIVEA", "PALMOLIVE","KENIA", "CAMPOS VERDES", "LIMOL","ESTRELLA"]


    marcas_yerbas = ["CACHAMATE","LIEBIG","AMANDA","VERDEFLOR","ROSAMONTE","PLAYADITO","TARAGUI",
                    "CHAMIGO","CBSE","UNION","LA TRANQUERA","ATOMO","PIPORE","PRO BELL","YERBACID"
                    ,"BUENAS Y SANTAS","MAS SABOR","DON ARREGUI","SALUS","LA HOJA", "MAÑANITA",
                    "DON LUCAS","CACHAMAI","CRUZ DE MALTA","LA MERCED"]
    
    marcas_fideos = ["BAUZA","LA PROVIDENCIA","LUCCHETTI","LUCHETTI", "MATARAZZO", "FAVORITA", "ROBLES","LUCIA", "SAN AGUSTIN", "YUKA","MAROLIO"]



    def capturar_marca(self,nombre):
        nombre = nombre.replace("LA PROV.", "LA PROVIDENCIA")
        if any(marca in nombre for marca in self.marcas_yerbas):
            marcas_validas = self.marcas_yerbas
        elif any(marca in nombre for marca in self.marcas_shampoo):
            marcas_validas = self.marcas_shampoo
        elif any(marca in nombre for marca in self.marcas_gaseosas):
            marcas_validas = self.marcas_gaseosas
        elif any(marca in nombre for marca in self.marcas_leches):
            marcas_validas = self.marcas_leches
        elif any(marca in nombre for marca in self.marcas_panes):
            marcas_validas = self.marcas_panes
        elif any(marca in nombre for marca in self.marcas_arroces):
            marcas_validas = self.marcas_arroces
        elif any(marca in nombre for marca in self.marcas_jabones):
            marcas_validas = self.marcas_jabones
        elif any(marca in nombre for marca in self.marcas_fideos):
            marcas_validas = self.marcas_fideos
        else:
            return "?"  
        marca_pattern = r"\b(?:{})\b".format("|".join(map(re.escape, marcas_validas)))
        match_marca = re.search(marca_pattern, nombre, re.IGNORECASE) 
        marca = match_marca.group() if match_marca else "?"
        return marca

    def capturar_descripcion(self,nombre):
        nombre = nombre.replace("LA PROV.", "LA PROVIDENCIA")
        marca = self.capturar_marca(nombre)
        nombre = nombre.replace("SHAMPOO", "").strip()
        nombre = nombre.replace("PANADERIA", "").strip()
        nombre = nombre.replace("GASEOSAS", "").strip()
        nombre = nombre.replace("GASEOSA", "").strip()
        nombre = nombre.replace("FLIAR", "").strip()
        nombre = nombre.replace("LECHE U.A.T.", "").strip()
        nombre = nombre.replace("ARROZ", "").strip()
        nombre = nombre.replace("JABON", "").strip()
        nombre = nombre.replace("TOCADOR", "").strip()
        nombre = nombre.replace("YERBA", "").strip()
        nombre = nombre.replace("FIDEOS", "").strip()
        volumen_pattern = r"(\d+)\s*(?:ML|CC|LTS|KG|GRS)\.?\.?"
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        else:
            return "?"
        descripcion = re.sub(volumen_pattern, "", nombre).strip()
        descripcion = descripcion.replace(marca, "").strip()
        descripcion = descripcion.replace("PAN", "").strip()
        descripcion = re.sub(r'\s+', ' ', descripcion)
        return descripcion

    def capturar_volumen(self,nombre):
        volumen_pattern = r"(\d+)\s*(?:ML|CC|LTS|KG|GRS)\.?\.?"
        match_volumen = re.search(volumen_pattern, nombre)
        volumen = match_volumen.group(0)
        volumen = volumen.replace("KG","")
        volumen = volumen.replace(" ML.","")
        volumen = volumen.replace("ML.","")
        volumen = volumen.replace("ML","")
        volumen = volumen.replace(" CC.","")
        volumen = volumen.replace("CC.","")
        volumen = volumen.replace("CC","")
        volumen = volumen.replace("LTS.","")
        
        volumen = volumen.replace("LTS","")
        volumen = volumen.replace("GRS","")
        if float(volumen.replace(',', '.')) < 7: 
            return str(int(float(volumen.replace(',', '.')) * 1000)).strip() 
        return volumen.strip()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        nombre = item['nombre_crudo']
        item["tienda"] = "Atomo"
        item["marca"] = self.capturar_marca(nombre)
        item["descripcion"] = self.capturar_descripcion(nombre)
        item["volumen"] = self.capturar_volumen(nombre)

        return item
