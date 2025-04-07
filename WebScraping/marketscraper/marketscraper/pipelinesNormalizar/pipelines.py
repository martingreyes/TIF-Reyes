import re
from itemadapter import ItemAdapter
from unidecode import unidecode

class NormalizarPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        marca = item["marca"]
        descripcion = item["descripcion"]
        tipo = item["categoria"]
        item["marca"] = self.normalizar_marca(marca)
        item["descripcion"] = self.normalizar_descripcion(descripcion,tipo)
        item["volumen"] = self.normalizar_volumen(item)


        return item

    def normalizar_marca(self,marca):
        marca = marca.upper()
        marca = unidecode(marca)
        if marca == "HEAD & SHOULDERS":
            return marca
        patrones = {
            "HEAD & SHOULDER": "HEAD & SHOULDERS",
            "HEAD SHOULDERS": "HEAD & SHOULDERS",
            "HEAD & SH":"HEAD & SHOULDERS",
            "HEAD SH": "HEAD & SHOULDERS",
            "P.DE LOS TOROS": "PASO DE LOS TOROS",
            "LUCHETTI": "LUCCHETTI",
            "7UP": "SEVEN UP",
            "LA ESPA?OLA": "LA ESPANOLA",
            "TRESEMMÉ":"TRESEMME",
            "ARMONÍA":"ARMONIA",
            "LA SERENÍSIMA":"LA SERENISIMA",
            "UNIÓN":"UNION",
            "LA SEREN.":"LA SERENISIMA",
            "CRUZ MALTA":"CRUZ DE MALTA",
            "LS":"LA SERENISIMA",   
            "JOHNSON": "JOHNSONS",  
            "BAUZAS":"BAUZA" 
        }   

        for patron, reemplazo in patrones.items():
            marca = re.sub(re.escape(patron), reemplazo, marca)
            if "LA SERENISIMA" not in marca:
                marca = marca.replace("SERENISIMA", "LA SERENISIMA")         

        marca = marca.strip()
        return marca

    def normalizar_descripcion(self,descripcion,tipo):
        descripcion = descripcion.upper()
        descripcion = descripcion.replace("°","?")
        descripcion = unidecode(descripcion)
        if tipo == "Arroces":

            patrones = {
            "0 0 0 0 0": "00000",
            "5/0": "00000",
            "L.FINO": "LARGO FINO",
            "FINOX": "FINO",
            "P/PREPARA": "",
            "PARBOIT": "PARBOIL",
            "PAQUETE": "",
            "RISOTTO": "RISOTTO",
            "ESPA?OLA": "ESPANOLA",
            "ESPAÑOLA": "ESPANOLA",
            "RIS.": "RISOTTO ",
            "PARB.": "PARBOIL",
            "BOLSA": "",
            "CAJA": "",
            "CURRY":"CURRI",
            "SAB.":"SABORES DEL MUNDO ",
            "TRAT.":"TRATTORIA "


            }

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)  
            
            if "ASIATICO" not in descripcion:
                descripcion = descripcion.replace("ASIAT","ASIATICO")  
    
            if "PRIMAVERA" not in descripcion:
                descripcion = descripcion.replace("PRIM", "PRIMAVERA")  
            if "MEDITERRANEO" not in descripcion:
                descripcion = descripcion.replace("MEDITERRANE","MEDITERRANEO")  
            if  "ORIENTAL" not in descripcion:
                descripcion = descripcion.replace("ORIENT","ORIENTAL" )  
            if "ESPANOLA" not in descripcion:
                descripcion = descripcion.replace("ESPANO", "ESPANOLA")  

            descripcion = descripcion.strip()


        if tipo == "Fideos":
            patrones = {
            "TALLARÍN": "TALLARIN",
            "MO?ITA": "MOÑITA",
            "CABELLO ANGEL": "CABELLO DE ANGEL",
            "GUISEROS": "",
            "MO?O": "MONO",
            "MONO": "MONO",
            "SECOS": "",
            "SOPEROS": "",
            "B.": "",
            "DEDALITOS": "DEDALITO",
            "MOÑOS": "MONO",
            "MUNICIONES": "MUNICION",
            "MOSTACHOLES": "MOSTACHOL",
            "VEG.":" VEGETALES ",
            "TIRA.":"TIRABUZON"
            }
            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)         

            descripcion = descripcion.strip()

        
        if tipo == "Gaseosas":
            patrones = {
            "LATA": "",
            "BOTELLA": "BOT",
            "BOT": "",
            "DIETETICA": "",
            "TÓNICA": "TONICA",
            "LIMA LIMON": "LIMA",
            "L-LIMON": "LIMA",
            "LIMA-LIMON": "LIMA",
            "S/AZUCAR": "SIN AZUCAR",
            "S- AZUCAR": "SIN AZUCAR",
            "SIN AZUCARES": "SIN AZUCAR",
            "ORIGINAL": "",    
            "DESCARTABLE":"",
            "RETORNABLE":"",
            "SABOR":"",
            "ZERO":"SIN AZUCAR"         
            }

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)          

            if "POMELO" not in descripcion:
                descripcion = descripcion.replace("POM","POMELO")

            if "DIETETICA" not in descripcion:
                descripcion = descripcion.replace("DIET","")

            descripcion = descripcion.strip()

        
        if tipo == "Jabones":
            patrones = {
            "PACK": "",
            "3+1": "4",
            "DE GLICERINA": "GLICERINA",
            "ACEITE.":" ACEITES ",
            "ESE.":"ESENCIALES",
            "JAB":""    
            }

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)

            if "CR" in descripcion.split():
                descripcion = descripcion.replace("CR","CREMOSO")

            descripcion = descripcion.strip()

            

        if tipo == "Leches":
            patrones = {
            "LV": "",
            "PARC.": "PARCIALMENTE ",
            "PARCIA.": "PARCIALMENTE ",
            "DESCR.": "DESCREMADA ",   
            "LIV.":"LIVIANA ",
            "LARGA VIDA":"",
            "BOTELLA":"",
            "CAJA":"",
            "SACHET":"",
            "L.VIDA":""
            }

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)         
            
            descripcion = descripcion.replace("  "," ")
            descripcion = descripcion.strip()


        if tipo == "Panes":
            patrones = {
            "TIPO": "",
            "C/SALVADO": "SALVADO",
            "CON SALVADO": "SALVADO",
            "DE MESA": "MESA",
            "RF": "",
            "REBANADO LACTEADO": "MESA"                
            }

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)          
            
            descripcion = descripcion.strip()

            
        if tipo == "Shampoos":
            patrones = {
                "DE NUTRICION": "NUTRICION",
                "NUTRICIÓN": "NUTRICION",
                "CARBÓN": "CARBON",
                "DOYPACK": "DOY PACK",
                "DP":"DOY PACK",
                "Y VIT C": "VIT C",
                "DOYP": "DOY PACK",
                "ESENCIAL": "ESENCIA",
                "INSTANTÁNEA":"INSTANTANEA",
                "NUTRICION SUP": "NUTRICION",
                "RECON.COMPLETA": "RECONSTRUCCION COMPLETA",
                "RECONSTRUCCIÓN":"RECONSTRUCCION",
                "RESTAURACIÓN":"RESTAURACION",
                "REGENERACIÓN":"REGENERACION",
                "REPARACIÓN":"REPARACION",
                "CARBON ACTIVADO PEONIAS": "CARBON ACTIVADO",
                "CARBON Y PEONIAS": "CARBON ACTIVADO",
                "COLÁGENO": "COLAGENO",
                "LARG SALUD": "LARGO SALUDABLE",
                "HIDRA-FORTALECE": "HIDRATA Y FORTALECE",
                "HIDRATACIÓN": "HIDRATACION",
            } 

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)   

            if "PERFECTO" not in descripcion:
                descripcion = descripcion.replace("PERF","PERFECTO")
            if "REPARADORA" not in descripcion and "REPARACION" not in descripcion and "REPARADOR" not in descripcion :
                descripcion = descripcion.replace("REPARADO","REPARADORA")
                descripcion = descripcion.replace("REPAR","REPARACION")
            if "RESTAURACION" not in descripcion:
                descripcion = descripcion.replace("REST","RESTAURACION")
            if "INSTANTANEA" not in descripcion:
                descripcion = descripcion.replace("INSTANTANE","INSTANTANEA")
            if "INSTANTANEA" not in descripcion:
                descripcion = descripcion.replace("INSTANT","INSTANTANEA")
            if "DEFINIDOS" not in descripcion:
                descripcion = descripcion.replace("DEF","DEFINIDOS")
            if "ESENCIA" not in descripcion:
                descripcion = descripcion.replace("ESENC","ESENCIA")
      

            descripcion = descripcion.strip()

        if tipo == "Yerbas":
            patrones = {
                "S.PALO": "SIN PALO",
                "C/ PALO":"CON PALO",
                "C/PALO":"CON PALO",
                "S/PALO": "SIN PALO",
                "SELECCIÓN":"SELECCION",
                "COMP.":"",
                "+":""

            } 

            for patron, reemplazo in patrones.items():
                descripcion = re.sub(re.escape(patron), reemplazo, descripcion)          

            descripcion = descripcion.strip()



        return descripcion
        

    def normalizar_volumen(self,item):
        tipo = item["categoria"]
        descripcion = item["descripcion"]
        volumen = item["volumen"]
        # if tipo == "Jabones":
        #     descripcion, volumen = self.corregir_volumen(descripcion, volumen)
        #     item["descripcion"] = descripcion
        if tipo == "Shampoos":
            marca = item["marca"]
            if marca == "SEDAL" and volumen == "300":
                if "DOY PACK" not in descripcion:
                    descripcion = descripcion + " DOY PACK"
                    item["descripcion"] = descripcion

        return volumen


    def encontrar_numero(self,cadena):
        patron = r'(\d+)\s*(?:U|u)|X\s*(\d+)\s*U|(\d+)'
        match = re.search(patron, cadena)
        if match:
            numero = match.group(1) or match.group(2) or match.group(3)
            cadena = re.sub(patron, '', cadena).strip()
        else:
            numero = None
        return cadena,numero

    def corregir_volumen(self,cadena,volumen):
        cadena, unidades = self.encontrar_numero(cadena)
        if unidades is not None:
            if volumen == "90":
                volumen = 90 * int(unidades)
            elif volumen == "120":
                volumen = 120 * int(unidades)
            elif volumen == "125":
                volumen = 125 * int(unidades)
        if int(volumen) == 360:
            cadena = cadena + " 4u"
        elif int(volumen) < 270:
            cadena = cadena + " 1u"
        elif int(volumen) >= 270 and int(volumen) < 720:
            cadena = cadena + " 3u"
        elif int(volumen) >= 720:
            cadena = cadena + " 8u"
        return cadena,str(volumen)