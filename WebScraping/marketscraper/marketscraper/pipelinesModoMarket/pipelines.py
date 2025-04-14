import re
from itemadapter import ItemAdapter

class ModoMarketPrecioPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price_keys = ['precio']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = round(float(value), 2)
            value = int(value)
            adapter[price_key] = float(value)
        return item


class ModoMarketPipeline:

    marcas_shampoo = ['Pantene', 'Head & Shoulders', 
                    'Suave', 'Sedal', 'Plusbelle', 'Inecto', 'Dove', 
                    'Algabo', 'Vo5', 'Elvive', 'Tresemme', 'Clear Men', 'Garnier', 
                    'Johnsons', 'Tio Nacho', "Garnier", "Head Shoulders", "Johnson", "Fructis", "Clear", "Head & Sh","Head Sh"]

    marcas_gaseosas = ['Coca Cola', 'Powerade', 'Pepsi', 'Schweppes', 'Sprite', 
                        'Mirinda', '7Up', 'Levite', 'Fanta', 'Paso De Los Toros', 
                        'Secco', 'Manaos', 'Rumipal', 'Yaci', 'Talca',"Sierra De Los Padres"]

    marcas_leche = ["Tregar", "Ilolay", "La Serenisima", "Veronica", 
                    "Milkaut", "Serenisima", "Angelita", "Las Tres Niñas"
                    ]

    marcas_pan = ["Bimbo","Fargo","Lactal","La Española","Dialecto"]

    marcas_arroces = ["Gallo", "Tio Carlos", "Mocovi", "Dos Hermanos", "Lucchetti", "Topador", "Primor"]

    marcas_jabones = ["Lux","Gigante","Rexona","Campos Verdes","Dove","Plusbelle","Nivea",
                        "Zorro","Veritas","Palmolive", "campos Verdes"]

    marcas_yerbas = ["Playadito","Verdeflor","Cbse","Chamigo","Union","Mañanita","Rosamonte",
                    "Nobleza Gaucha","Cruz Malta","Cruz De Malta","Taragui","Amanda","La Merced",
                    "La Tranquera","Yervita","Don Lucas","Don Arregui","La Hoja", "Nobleza  Gaucha", "Pipore","Canarias","Cachamate"]

    marcas_fideos = ["Terrabusi","Matarazzo","Don Vicente","Lucchetti","Robles","San Agustin",
                    "Favorita","Knorr","Soyarroz","Grandiet", "Arcor", "Caseritos"]

    def capturar_marca(self,nombre):
        if any(marca in nombre for marca in self.marcas_yerbas):
            marcas_validas = self.marcas_yerbas
        elif any(marca in nombre for marca in self.marcas_shampoo):
            marcas_validas = self.marcas_shampoo
        elif any(marca in nombre for marca in self.marcas_gaseosas):
            marcas_validas = self.marcas_gaseosas
        elif any(marca in nombre for marca in self.marcas_leche):
            marcas_validas = self.marcas_leche
        elif any(marca in nombre for marca in self.marcas_pan):
            marcas_validas = self.marcas_pan
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
        nombre = nombre.replace("Shampoo", "").strip()
        nombre = nombre.replace("Gaseosa", "").strip()
        nombre = nombre.replace("Leche", "").strip()
        nombre = nombre.replace("Arroz", "").strip()
        nombre = nombre.replace("Jabon", "").strip()
        nombre = nombre.replace("Jab.", "").strip()
        nombre = nombre.replace("Yerba", "").strip()
        nombre = nombre.replace("Fideos", "").strip()
        nombre = nombre.replace("Familiar", "").strip()
        if any(marca in nombre for marca in self.marcas_yerbas):
            if "Hierbas" not in nombre:
                nombre = nombre.replace("Hierba","").strip()
        volumen_pattern = r"\b(?:X\s*)?(?:\d+(?:.\d+)?\s*)?(\d+(?:.\d+)?)\s*(?:(?:Lt|lt|Cc|cc|Ml|ml|L|l|Grs|Gr|G|Kg|K|gr|g|M)\b)"
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and marca in self.marcas_jabones:
            volumen_pattern = r'(?<=X\s)\d+'
            match = re.search(volumen_pattern, nombre)
            volumen = "X " + match.group()

        else:
            return "?"
        #Esto es para el caso de "Shampoo Elvive Reparacion Total 5 200 Ml" que esta el 5 200
        match = re.search(r'\b(\d+)\s+(\d+\s*\S+)', volumen)
        if match:
            resto = match.group(1)
            volumen = match.group(2)
        descripcion = nombre.replace(volumen,"").strip()
        descripcion = descripcion.replace(marca,"").strip()
        descripcion = descripcion.replace("Pan","").strip()
        descripcion = re.sub(r'\s+', ' ', descripcion)
        return descripcion

    def capturar_volumen(self,nombre):
        marca = self.capturar_marca(nombre)
        volumen_pattern = r"\b(?:X\s*)?(?:\d+(?:.\d+)?\s*)?(\d+(?:.\d+)?)\s*(?:(?:Lt|lt|Cc|cc|Ml|ml|L|l|Grs|Gr|G|Kg|K|gr|g|M)\b)"
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
            #Esto es para el caso de "Shampoo Elvive Reparacion Total 5 200 Ml" que esta el 5 200
            match = re.search(r'\b(\d+)\s+(\d+\s*\S+)', volumen)
            if match:
                resto = match.group(1)
                volumen = match.group(2)
        elif not match_volumen and marca in self.marcas_jabones:
            volumen_pattern = r'(?<=X\s)\d+'
            match = re.search(volumen_pattern, nombre)
            return match.group()

        volumen = volumen.replace("X","")
        volumen = volumen.replace("Lt","")
        volumen = volumen.replace("lt","")
        volumen = volumen.replace("Ml","")
        volumen = volumen.replace("Cc","")
        volumen = volumen.replace("cc","")
        volumen = volumen.replace("Grs","")
        volumen = volumen.replace("Gr","")
        volumen = volumen.replace("gr","")
        volumen = volumen.replace("Kg","")
        volumen = volumen.replace("K","")
        volumen = volumen.replace("G","")
        volumen = volumen.replace("g","")
        volumen = volumen.replace("ml","")
        volumen = volumen.replace("L","")
        volumen = volumen.replace("l","")
        volumen = volumen.replace("M","")

        if float(volumen.replace(',', '.')) < 7: 
            return str(int(float(volumen.replace(',', '.')) * 1000)).strip() 
        return volumen.strip()


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        nombre = item['nombre_crudo']
        item["tienda"] = "ModoMarket"
        item["marca"] = self.capturar_marca(nombre)
        item["descripcion"] = self.capturar_descripcion(nombre)
        item["volumen"] = self.capturar_volumen(nombre)

        return item