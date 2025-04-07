from itemadapter import ItemAdapter
import re

class SuperaPrecioPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price_keys = ['precio']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = round(float(value.replace(",", "")), 2)
            value = int(value)
            adapter[price_key] = float(value)
        return item


class SuperaPipeline:

    marcas_shampoo = ["PANTENE", "HEAD & SHOULDERS", "SUAVE", "SEDAL", "PLUSBELLE", 
                    "INECTO", "DOVE", "ALGABO", "VO5", "ELVIVE","TRESEMME"
                    ]

    marcas_gaseosas = ["COCA COLA", "POWERADE","PEPSI", "SCHWEPPES", "SPRITE", 
                    "MIRINDA","7UP", "LEVITE", "FANTA","PASO DE LOS TOROS", 
                    "SECCO", "MANAOS","RUMIPAL","YACI","TALCA"
                    ]
    
    marcas_leches = ["ILOLAY", "LA SEREN.","LA SERENISIMA","LATTE","LS","TREGAR",
                    "VERONICA"
                    ]

    marcas_panes = ["VENEZIANA", "LA ESPANOLA"]

    marcas_arroces = ["EL GRANDE","GALLO","LUCCHETTI","TIO CARLOS"]

    marcas_jabones = ["DOVE","REXONA","LUX","PLUSBELLE"]

    marcas_yerbas = ["PLAYADITO","ROSAMONTE","TARAGUI","VERDEFLOR","YERBACID"]

    marcas_fideos = ["DON VICENTE","LA PROVIDENCIA","LUCCHETTI","SAN AGUSTIN","TERRABUSI", "MATARAZZO"
                    ]


    def capturar_marca(self,nombre):
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
        marca = self.capturar_marca(nombre)
        nombre = nombre.replace("LECHE", "").strip()
        if marca in self.marcas_shampoo:
            nombre = nombre.replace("SH", "").strip()
        nombre = nombre.replace("GASEOSA", "").strip()
        nombre = nombre.replace("FLIAR", "").strip()
        nombre = nombre.replace("ARROZ", "").strip()
        nombre = nombre.replace("JABON", "").strip()
        nombre = nombre.replace("YERBA MATE", "").strip()
        nombre = nombre.replace("FIDEOS", "").strip()
        volumen_pattern = r"\b(?:X\s*)?(\d+(?:[,.]\d+)?)\s*(?:(?:LT|CC|ML|L|GRS|GR|G|KG)\b)"
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and "UAT BOTELLA" in nombre:
            volumen = "UAT BOTELLA"
        elif not match_volumen and marca in self.marcas_jabones:
            numero_pattern = r'(?<=X)\d+[A-Za-z]+'
            match = re.search(numero_pattern,nombre)
            volumen = "X" + match.group(0)
        elif not match_volumen and marca in self.marcas_panes:
            numero_pattern = r'\d+'
            match = re.search(numero_pattern, nombre)
            volumen = match.group() + "GR"


        else:
            return "?"
        descripcion = nombre.replace(volumen, "").strip()
        descripcion = descripcion.replace(marca, "").strip()
        descripcion = descripcion.replace("PAN","").strip()
        descripcion = re.sub(r'\s+', ' ', descripcion)
        return descripcion

    def capturar_volumen(self,nombre):
        marca = self.capturar_marca(nombre)
        volumen_pattern = r"\b(?:X\s*)?(\d+(?:[,.]\d+)?)\s*(?:(?:LT|CC|ML|L|GRS|GR|G|KG)\b)"
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and "UAT BOTELLA" in nombre:
            return "1000"
        elif not match_volumen and marca in self.marcas_jabones:
            numero_pattern = r'(?<=X)\d+[A-Za-z]+'
            match = re.search(numero_pattern,nombre)
            volumen = "X" + match.group(0)
        elif not match_volumen and marca in self.marcas_panes:
            numero_pattern = r'\d+'
            match = re.search(numero_pattern, nombre)
            return match.group()
        volumen = volumen.replace("X","")
        volumen = volumen.replace("ML","")
        volumen = volumen.replace("CC","")
        volumen = volumen.replace("GRS","")
        volumen = volumen.replace("GR","")
        volumen = volumen.replace("KG","")
        volumen = volumen.replace("G","")
        volumen = volumen.replace("LT","")
        volumen = volumen.replace("L","")
        volumen = volumen.replace(".",",")
        if float(volumen.replace(',', '.')) < 7: 
            return str(int(float(volumen.replace(',', '.')) * 1000)).strip() 
        return volumen.strip()



    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        nombre = item['nombre_crudo']
        item["tienda"] = "Supera"
        item["marca"] = self.capturar_marca(nombre)
        item["descripcion"] = self.capturar_descripcion(nombre)
        item["volumen"] = self.capturar_volumen(nombre)


        return item
