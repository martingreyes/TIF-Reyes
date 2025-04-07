from itemadapter import ItemAdapter
import re

class BlowmaxPrecioPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price_keys = ['precio']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = round(float(value.replace(".", "").replace(",", ".")), 2)
            value = int(value)
            adapter[price_key] = float(value)
        return item


class BlowmaxPipeline:

    marcas_shampoo = ["PANTENE", "HEAD SHOULDERS", "SUAVE", "SEDAL", "PLUSBELLE", 
                    "INECTO", "DOVE", "ALGABO", "VO5", "ELVIVE","JOHNSONS","TRESEMME"
                    ]

    marcas_gaseosas = ["COCA COLA", "PEPSI", "SCHWEPPES", "SPRITE", "SEVEN UP", 
                    "LEVITE", "FANTA", "PASO DE LOS TOROS", "SECCO", "MANAOS",
                    "RUMIPAL","TALCA","7UP","PRITTY LIMON","BAGGIO","MIRINDA"
                    ]

    marcas_leches = ["ILOLAY", "LS", "TREGAR", "VERONICA", "LATTE", "ANGELITA","ARMONIA"
                    ]

    marcas_panes = ["BIMBO","LA ESPA?OLA","LA ESPANOLA","LACTAL","VENEZIANA"]

    marcas_arroces = ["DON MARCOS", "GALLO", "TIO CARLOS", "EL GRANDE","BARBARA","CAÑUELAS","VINCHA DE ORO"]

    marcas_jabones = ["DOVE","KENIA","LUX","PATRICIA ALLEN","PLUSBELLE","REXONA"]

    marcas_yerbas = ["CHAMIGO","PLAYADITO","ROSAMONTE","TARAGUI","VERDEFLOR","YERBACID"]

    marcas_fideos = ["LA PROVIDENCIA", "BAUZA", "DON VICENTE","LUCCHETTI","MATARAZZO",
                    "SAN AGUSTIN","TERRABUSI","BAUZAS","NANI", "BLUE PATNA","ARGENTINA", "FAVORITA","SANTA ISABEL"]

    def capturar_marca(self,nombre):
        nombre = nombre.replace("  "," ").strip()
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
        nombre = nombre.replace("  "," ").strip()
        marca = self.capturar_marca(nombre)
        nombre = nombre.replace(marca, "")
        nombre = nombre.replace("AC ", "")
        if marca in self.marcas_shampoo:
            nombre = nombre.replace("SH ", "")
        nombre = nombre.replace("GASEOSA", "")
        nombre = nombre.replace("ARROZ", "")
        nombre = nombre.replace("JABON", "")
        nombre = nombre.replace("YERBA MATE", "")
        nombre = nombre.replace("FIDEOS", "")
        if marca in self.marcas_leches:
            nombre = nombre.replace("LECHE", "")
        volumen_pattern = r'\bX?\s*\d+(?:[,.]\d+)?\s*(?:LT|CC.|CC|C|ML|L|GRS|KG|GR|G)\b'
        match = re.search(volumen_pattern, nombre, re.IGNORECASE)
        if match:
            volumen = match.group(0)
        elif not match and "UAT BOTELLA" in nombre:
            volumen = "UAT BOTELLA"
        elif not match and marca in self.marcas_panes:
            numero_pattern = r'\d+'
            match = re.search(numero_pattern,nombre)
            volumen = match.group()+"GR"
        elif not match and marca in self.marcas_jabones:
            numero_pattern = r'(?<=X)\d+[A-Za-z]+'
            match = re.search(numero_pattern,nombre)
            volumen = "X" + match.group(0)
        else:
            return "?"
        if "CC." in nombre:
            nombre = nombre.replace(".","")
        descripcion = nombre.replace(volumen, "").strip()
        descripcion = descripcion.replace(marca, "").strip()
        descripcion = descripcion.replace("PAN","").strip()
        descripcion = descripcion.replace("  "," ").strip()
        return descripcion


    def capturar_volumen(self,nombre):
        descripcion = self.capturar_descripcion(nombre)
        nombre = nombre.replace(descripcion,"")
        volumen_pattern = r'\bX?\s*\d+(?:[,.]\d+)?\s*(?:LT|CC.|CC|C|ML|L|GRS|KG|GR|G)\b'
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and "UAT BOTELLA" in nombre:
            return "1000"
        elif not match and marca in self.marcas_panes:
            numero_pattern = r'\d+'
            match = re.search(numero_pattern,nombre)
            volumen = match.group()+"GR"
        elif not match and marca in self.marcas_jabones:
            numero_pattern = r'(?<=X)\d+[A-Za-z]+'
            match = re.search(numero_pattern,nombre)
            volumen = "X" + match.group(0)
        volumen = match_volumen.group(0)
        volumen = volumen.replace("X","")
        volumen = volumen.replace("LT","")
        volumen = volumen.replace("ML","")
        volumen = volumen.replace("CC.","")
        volumen = volumen.replace("CC","")
        volumen = volumen.replace("C","")
        volumen = volumen.replace("L","")
        volumen = volumen.replace("KG","")
        volumen = volumen.replace("GRS","")
        volumen = volumen.replace("GR","")
        volumen = volumen.replace("G","")
        volumen = volumen.replace(".",",")
        if float(volumen.replace(',', '.')) < 7: 
            return str(int(float(volumen.replace(',', '.')) * 1000)).strip() 
        return volumen.strip()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        nombre = item['nombre_crudo']
        item["tienda"] = "Blowmax"
        item["marca"] = self.capturar_marca(nombre)
        item["descripcion"] = self.capturar_descripcion(nombre)
        item["volumen"] = self.capturar_volumen(nombre)


        return item
