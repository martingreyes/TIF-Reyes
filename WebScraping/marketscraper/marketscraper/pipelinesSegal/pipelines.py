import re
from itemadapter import ItemAdapter

class SegalPrecioPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price_keys = ['precio']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = round(float(value.replace(".", "").replace(",", ".")), 2)
            value = int(value)
            adapter[price_key] = float(value)
        return item


class SegalPipeline:

    marcas_shampoo = ["PANTENE", "HEAD SHOULDERS", "SUAVE", "SEDAL", "PLUSBELLE", 
                    "INECTO", "DOVE", "ALGABO", "VO5", "ELVIVE","TRESEMMÉ"
                    ]

    marcas_gaseosas = ["COCA COLA", "POWERADE", "PEPSI", "SCHWEPPES", "SPRITE", 
                    "MIRINDA", "SEVEN UP", "LEVITE", "FANTA", "PASO DE LOS TOROS", 
                    "SECCO", "MANAOS", "RUMIPAL", "TALCA","7UP","BAGGIO"
                    ]
    
    marcas_leches = ["ARMONÍA", "LA SERENÍSIMA", "TREGAR", "CINDOR", "YOGURLAC", 
                    "ILOLAY"
                    ]

    marcas_panes = ["ARGENTINA", "VENEZIANA", "LACTAL", "BIMBO"]

    marcas_arroces = ["DON MARCOS", "GALLO","LUCCHETTI", "MAXIMO","PERSEGUIDO"]

    marcas_jabones = ["REXONA","LUX"]

    marcas_yerbas = ["CRUZ DE MALTA","MAÑANITA","NOBLEZA GAUCHA","TARAGUI","UNIÓN","VERDEFLOR", "CHAMIGO","SALUS", "BUENAS Y SANTAS"]

    marcas_fideos = ["LA PROVIDENCIA","KNORR","FAVORITA","LUCCHETTI","MATARAZZO","TERRABUSI","DON VICENTE", "DON FELIPE","ARCOR","PROVIDENCIA"]

    def capturar_marca(self, nombre):
        if any(marca in nombre for marca in self.marcas_shampoo):
            marcas_validas = self.marcas_shampoo
        elif any(marca in nombre for marca in self.marcas_gaseosas):
            marcas_validas = self.marcas_gaseosas
        elif any(marca in nombre for marca in self.marcas_leches):
            marcas_validas = self.marcas_leches
        elif any(marca in nombre for marca in self.marcas_panes):
            marcas_validas = self.marcas_panes
            encontradas = []
            for marca in marcas_validas:
                if marca in nombre:
                    encontradas.append(marca)
            if len(encontradas) > 1:
                encontradas.remove("LACTAL")
                return encontradas[0]
        elif any(marca in nombre for marca in self.marcas_arroces):
            marcas_validas = self.marcas_arroces   
        elif any(marca in nombre for marca in self.marcas_jabones):
            marcas_validas = self.marcas_jabones
        elif any(marca in nombre for marca in self.marcas_yerbas):
            marcas_validas = self.marcas_yerbas
        elif any(marca in nombre for marca in self.marcas_fideos):
            marcas_validas = self.marcas_fideos
        else:
            return "?"  
        marca_pattern = r"\b(?:{})\b".format("|".join(map(re.escape, marcas_validas)))
        match_marca = re.search(marca_pattern, nombre, re.IGNORECASE) 
        marca = match_marca.group() if match_marca else "?"
        return marca

    def capturar_descripcion(self, nombre):
        marca = self.capturar_marca(nombre)
        nombre = nombre.replace("SHAMPOO", "").strip()
        volumen_pattern = r'\bx?\s*\d+(?:[,.]\d+)?\s*(?:Lt|cc|ml|L|Lts|LT|gr|g|Kg|kg)\b'

        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and "LECHE PET" in nombre:
            volumen = "LECHE PET"
        elif not match_volumen and nombre == "LECHE CHOCOLATADA LA SERENÍSIMA":
            volumen = ""
        else:
            return "?"
        nombre = nombre.replace("LECHE PET", "").strip()
        nombre = nombre.replace("LECHE", "").strip()
        nombre = nombre.replace("ARROZ", "").strip()
        nombre = nombre.replace("JABÓN", "").strip()
        nombre = nombre.replace("YERBA", "").strip()
        nombre = nombre.replace("FIDEOS", "").strip()
        descripcion = re.sub(volumen_pattern, "", nombre).strip()
        descripcion = descripcion.replace(marca, "").strip()
        descripcion = descripcion.replace("PAN", "").strip()
        descripcion = re.sub(r'\s+', ' ', descripcion)
        return descripcion

    def capturar_volumen(self, nombre):
        marca = self.capturar_marca(nombre)
        descripcion = self.capturar_descripcion(nombre)
        volumen_pattern = r'\bx?\s*\d+(?:[,.]\d+)?\s*(?:Lt|cc|ml|L|Lts|LT|gr|g|Kg|kg)\b'
        match_volumen = re.search(volumen_pattern, nombre)
        if match_volumen:
            volumen = match_volumen.group(0)
        elif not match_volumen and "LECHE PET" in nombre:
            return "1000"
        elif not match_volumen and nombre == "LECHE CHOCOLATADA LA SERENÍSIMA":
            return "1000"
        volumen = volumen.replace("ml","")
        volumen = volumen.replace("cc","")
        volumen = volumen.replace("Lts","")
        volumen = volumen.replace("LT","")
        volumen = volumen.replace("Lt","")
        volumen = volumen.replace("L","")
        volumen = volumen.replace("Kg","")
        volumen = volumen.replace("kg","")
        volumen = volumen.replace("gr","")
        volumen = volumen.replace("g","")
        volumen = volumen.replace("x","").strip()
        if float(volumen.replace(',', '.')) < 7: 
            return str(int(float(volumen.replace(',', '.')) * 1000))

        if marca in self.marcas_jabones or 'Jabon' in nombre:
            numeros = re.findall(r'\d+', descripcion)
            if numeros:  
                nuevo_volumen = int(volumen) * int(numeros[0])
                if nuevo_volumen > 600:
                    return volumen.strip()
                else:
                    volumen = str(nuevo_volumen)

        return volumen.strip()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        nombre = item['nombre_crudo']
        item["tienda"] = "Segal"
        item["marca"] = self.capturar_marca(nombre)
        item["descripcion"] = self.capturar_descripcion(nombre)
        item["volumen"] = self.capturar_volumen(nombre)

        return item
