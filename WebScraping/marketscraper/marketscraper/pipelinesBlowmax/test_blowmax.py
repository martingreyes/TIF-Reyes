import re
import unittest

from pipelines import BlowmaxPipeline

class TestExpresionesRegulares(unittest.TestCase):
    def test_marca(self):
        blowmax = BlowmaxPipeline()
        self.assertEqual(blowmax.capturar_marca("AC DOVE OLEO NUTRICION SUPERIOR X400ML"), "DOVE")
        self.assertEqual(blowmax.capturar_marca("SH HEAD SHOULDERS CHARCOAL X180ML"), "HEAD SHOULDERS")
        self.assertEqual(blowmax.capturar_marca("SH PLUSBELLE ESENCIA RESTAURACION 970ML"), "PLUSBELLE")
        self.assertEqual(blowmax.capturar_marca("SH Pepe"), "?")
        self.assertEqual(blowmax.capturar_marca("SH ELVIVE DREAM LONG 200ML"), "ELVIVE")
        self.assertEqual(blowmax.capturar_marca("SH SEDAL CARBON ACTIVADO PEONIAS X190ML"), "SEDAL")
        self.assertEqual(blowmax.capturar_marca("SH SEDAL BOMBA NUTRICION X 340ML"), "SEDAL")
        self.assertEqual(blowmax.capturar_marca("GASEOSA COCA COLA LATA X 310CC"), "COCA COLA")
        self.assertEqual(blowmax.capturar_marca("GASEOSA MANAOS GRANADINA X 3LT"), "MANAOS")
        self.assertEqual(blowmax.capturar_marca("GASEOSA SCHWEPPES TONICA X 1,5LT"), "SCHWEPPES")
        self.assertEqual(blowmax.capturar_marca("GASEOSA SPRITE X 500CC"), "SPRITE")
        self.assertEqual(blowmax.capturar_marca("GASEOSA TALCA POMELO 3LT"), "TALCA")
        self.assertEqual(blowmax.capturar_marca("GASEOSA PRITTY  LIMON X 2,25LT  "), "PRITTY LIMON")
        self.assertEqual(blowmax.capturar_marca("GASEOSA PRITTY  LIMON X 3LT  "), "PRITTY LIMON")
        self.assertEqual(blowmax.capturar_marca("GASEOSA PRITTY  LIMON X 500CC  "), "PRITTY LIMON")
        self.assertEqual(blowmax.capturar_marca("LECHE ILOLAY LV DESCREMADA X1LT"), "ILOLAY")
        self.assertEqual(blowmax.capturar_marca("LECHE LS PARC. DESCREMADA ZERO LACTOSA 1L"), "LS")
        self.assertEqual(blowmax.capturar_marca("LECHE TREGAR DESCREMADA X 1LT"), "TREGAR")
        self.assertEqual(blowmax.capturar_marca("LECHE LS SACHET ULTRA ENTERA 1 LT 3%"), "LS")
        self.assertEqual(blowmax.capturar_marca("LECHE LS UAT BOTELLA ENTERA CLASICA 3%"), "LS")
        self.assertEqual(blowmax.capturar_marca("LECHE ANGELITA LIVIANA"), "ANGELITA")
        self.assertEqual(blowmax.capturar_marca("PAN BIMBO ARTESANO X 500GR"), "BIMBO")
        self.assertEqual(blowmax.capturar_marca("PAN BIMBO LIVIANO ACTI LECHE 550GR"), "BIMBO")
        self.assertEqual(blowmax.capturar_marca("PAN LA ESPA?OLA LACTAL MULTISEMILLAS 450GR"), "LA ESPA?OLA")
        self.assertEqual(blowmax.capturar_marca("PAN LA ESPANOLA LACTAL DOLBLE SALVADO380GR"), "LA ESPANOLA")
        self.assertEqual(blowmax.capturar_marca("PAN LACTAL RF DE MESA X315GR"), "LACTAL")
        self.assertEqual(blowmax.capturar_marca("ARROZ DON MARCOS LARGO FINO X 500G"), "DON MARCOS")
        self.assertEqual(blowmax.capturar_marca("ARROZ GALLO DOBLE CAROLINA CAJA X 1KG"), "GALLO")
        self.assertEqual(blowmax.capturar_marca("ARROZ GALLO RISOTTO PRIM 240GR"), "GALLO")
        self.assertEqual(blowmax.capturar_marca("ARROZ GALLO RISOTTO ESPA?OLA 240GR"), "GALLO")
        self.assertEqual(blowmax.capturar_marca("ARROZ TIO CARLOS LARGO FINO X 500GR"), "TIO CARLOS")
        self.assertEqual(blowmax.capturar_marca("ARROZ GALLO ORO PARBOIL X 500GR"), "GALLO")
        self.assertEqual(blowmax.capturar_marca("ARROZ TIO CARLOS DOBLE CAROLINA X 500GR"), "TIO CARLOS")
        self.assertEqual(blowmax.capturar_marca("JABON KENIA COLOR MIX 3X90GR"), "KENIA")
        self.assertEqual(blowmax.capturar_marca("JABON DOVE BLANCO X 90GRS"), "DOVE")
        self.assertEqual(blowmax.capturar_marca("JABON KENIA CREMOSO 4X90G"), "KENIA")
        self.assertEqual(blowmax.capturar_marca("JABON KENIA GLICERINA OFERTA 3+1 360GR"), "KENIA")
        self.assertEqual(blowmax.capturar_marca("JABON LUX JAZMIN BOTANIC CR 125G"), "LUX")
        self.assertEqual(blowmax.capturar_marca("JABON LUX JAZMIN BOTANIC CR 3 X 125G"), "LUX")
        self.assertEqual(blowmax.capturar_marca("JABON LUX ROSAS FRANCESAS BOTANIC 125GR"), "LUX")
        self.assertEqual(blowmax.capturar_marca("JABON PATRICIA ALLEN TROPICALX130GR"), "PATRICIA ALLEN")
        self.assertEqual(blowmax.capturar_marca("JABON PLUSBELLE BALANCE NUTRIOIL 125GRS"), "PLUSBELLE")
        self.assertEqual(blowmax.capturar_marca("JABON REXONA ANTIBACTERIAL ORIG.90GR"), "REXONA")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE CHAMIGO X 1KG"), "CHAMIGO")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE PLAYADITO C/PALO SUAVE X1KG"), "PLAYADITO")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE PLAYADITO C/PALO SUAVE X500GR"), "PLAYADITO")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE TARAGUI C/ PALO FLEX 1KG"), "TARAGUI")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE TARAGUI FLEX S/PALO 1KG"), "TARAGUI")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE VERDEFLOR BOLDO X500GR"), "VERDEFLOR")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE YERBACID CEDRON X500GR"), "YERBACID")
        self.assertEqual(blowmax.capturar_marca("YERBA MATE YERBACID TRADICIONAL X500GR"), "YERBACID")
        self.assertEqual(blowmax.capturar_marca("FIDEOS BAUZA SECOS CABELLO DE ANGEL 500G"), "BAUZA")
        self.assertEqual(blowmax.capturar_marca("FIDEOS LA PROVIDENCIA CODO X500GR"), "LA PROVIDENCIA")
        self.assertEqual(blowmax.capturar_marca("FIDEOS LUCCHETTI MOSTACHOL N?51 X 500GR"), "LUCCHETTI")
        self.assertEqual(blowmax.capturar_marca("FIDEOS MATARAZZO MONO X 500GR"), "MATARAZZO")
        self.assertEqual(blowmax.capturar_marca("FIDEOS SAN AGUSTIN TALLARIN X 500GR"), "SAN AGUSTIN")
        self.assertEqual(blowmax.capturar_marca("FIDEOS TERRABUSI MOSTACHOL 500GR"), "TERRABUSI")
        self.assertEqual(blowmax.capturar_marca("GASEOSA SCHWEPPES POMELO S/AZUCAR LATA X310C"), "SCHWEPPES")
        self.assertEqual(blowmax.capturar_marca("FIDEOS CELESTIAL RADIATORE 500GR"), "CELESTIAL")

    def test_descripcion(self):
        blowmax = BlowmaxPipeline()
        self.assertEqual(blowmax.capturar_descripcion("AC DOVE OLEO NUTRICION SUPERIOR X400ML"), "OLEO NUTRICION SUPERIOR")
        self.assertEqual(blowmax.capturar_descripcion("SH HEAD SHOULDERS CHARCOAL X180ML"), "CHARCOAL")
        self.assertEqual(blowmax.capturar_descripcion("SH PLUSBELLE ESENCIA RESTAURACION 970ML"), "ESENCIA RESTAURACION")
        self.assertEqual(blowmax.capturar_descripcion("SH ELVIVE DREAM LONG 200ML"), "DREAM LONG")
        self.assertEqual(blowmax.capturar_descripcion("SH SEDAL CARBON ACTIVADO PEONIAS X190ML"), "CARBON ACTIVADO PEONIAS")
        self.assertEqual(blowmax.capturar_descripcion("SH SEDAL BOMBA NUTRICION X 340ML"), "BOMBA NUTRICION")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA COCA COLA LATA X 310CC"), "LATA")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA MANAOS GRANADINA X 3LT"), "GRANADINA")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA SCHWEPPES TONICA X 1,5LT"), "TONICA")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA SPRITE X 500CC"), "")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA TALCA POMELO 3LT"), "POMELO")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA SPRITE X 2.25LT"), "")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA PRITTY LIMON SIN AZUCAR X 1,5LT  "), "SIN AZUCAR")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA DIETETICA PASO DE LOS TOROS POMELO 1500 CC."), "DIETETICA POMELO")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA PRITTY  LIMON X 2,25LT  "), "")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA PRITTY  LIMON X 3LT  "), "")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA PRITTY  LIMON X 500CC  "), "")
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA 7UP RETORNABLE X 2,25LT  "), "RETORNABLE")
        self.assertEqual(blowmax.capturar_descripcion("LECHE ILOLAY LV DESCREMADA X1LT"), "LV DESCREMADA")
        self.assertEqual(blowmax.capturar_descripcion("LECHE LS PARC. DESCREMADA ZERO LACTOSA 1L"), "PARC. DESCREMADA ZERO LACTOSA")
        self.assertEqual(blowmax.capturar_descripcion("LECHE TREGAR DESCREMADA X 1LT"), "DESCREMADA")
        self.assertEqual(blowmax.capturar_descripcion("LECHE LS SACHET ULTRA ENTERA 1 LT 3%"), "SACHET ULTRA ENTERA 3%")
        self.assertEqual(blowmax.capturar_descripcion("LECHE LS UAT BOTELLA ENTERA CLASICA 3%"), "ENTERA CLASICA 3%")
        self.assertEqual(blowmax.capturar_descripcion("LECHE LS REDUCIDA LACTOSA F/VIT SACHET 1LT"), "REDUCIDA LACTOSA F/VIT SACHET")
        self.assertEqual(blowmax.capturar_descripcion("LECHE LS UAT BOTELLA PARC. DESCREMADA 1%"), "PARC. DESCREMADA 1%")
        self.assertEqual(blowmax.capturar_descripcion("LECHE ILOLAY LV DESCREMADA"), "?")
        self.assertEqual(blowmax.capturar_descripcion("LECHE ANGELITA LIVIANA 1LT"), "LIVIANA")
        self.assertEqual(blowmax.capturar_descripcion("PAN BIMBO ARTESANO X 500GR"), "ARTESANO")
        self.assertEqual(blowmax.capturar_descripcion("PAN BIMBO LIVIANO ACTI LECHE 550GR"), "LIVIANO ACTI LECHE")
        self.assertEqual(blowmax.capturar_descripcion("PAN LA ESPA?OLA LACTAL MULTISEMILLAS 450GR"), "LACTAL MULTISEMILLAS")
        self.assertEqual(blowmax.capturar_descripcion("PAN LA ESPANOLA LACTAL DOLBLE SALVADO380GR"), "LACTAL DOLBLE SALVADO")
        self.assertEqual(blowmax.capturar_descripcion("PAN LACTAL RF DE MESA X315GR"), "RF DE MESA")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ DON MARCOS LARGO FINO X 500G"), "LARGO FINO")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ GALLO DOBLE CAROLINA CAJA X 1KG"), "DOBLE CAROLINA CAJA")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ GALLO RISOTTO PRIM 240GR"), "RISOTTO PRIM")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ GALLO RISOTTO ESPA?OLA 240GR"), "RISOTTO ESPA?OLA")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ TIO CARLOS LARGO FINO X 500GR"), "LARGO FINO")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ GALLO ORO PARBOIL X 500GR"), "ORO PARBOIL")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ EL GRANDE X 500 GR  "), "")
        self.assertEqual(blowmax.capturar_descripcion("ARROZ TIO CARLOS DOBLE CAROLINA X 500GR"), "DOBLE CAROLINA")
        self.assertEqual(blowmax.capturar_descripcion("JABON KENIA COLOR MIX 3X90GR"), "COLOR MIX 3")
        self.assertEqual(blowmax.capturar_descripcion("JABON DOVE BLANCO X 90GRS"), "BLANCO")
        self.assertEqual(blowmax.capturar_descripcion("JABON KENIA CREMOSO 4X90G"), "CREMOSO 4")
        self.assertEqual(blowmax.capturar_descripcion("JABON KENIA GLICERINA OFERTA 3+1 360GR"), "GLICERINA OFERTA 3+1")
        self.assertEqual(blowmax.capturar_descripcion("JABON LUX JAZMIN BOTANIC CR 125G"), "JAZMIN BOTANIC CR")
        self.assertEqual(blowmax.capturar_descripcion("JABON LUX JAZMIN BOTANIC CR 3 X 125G"), "JAZMIN BOTANIC CR 3")
        self.assertEqual(blowmax.capturar_descripcion("JABON LUX ROSAS FRANCESAS BOTANIC 125GR"), "ROSAS FRANCESAS BOTANIC")
        self.assertEqual(blowmax.capturar_descripcion("JABON PATRICIA ALLEN TROPICALX130GR"), "TROPICAL")
        self.assertEqual(blowmax.capturar_descripcion("JABON PLUSBELLE BALANCE NUTRIOIL 125GRS"), "BALANCE NUTRIOIL")
        self.assertEqual(blowmax.capturar_descripcion("JABON REXONA ANTIBACTERIAL ORIG.90GR"), "ANTIBACTERIAL ORIG.")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE CHAMIGO X 1KG"), "")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE PLAYADITO C/PALO SUAVE X1KG"), "C/PALO SUAVE")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE PLAYADITO C/PALO SUAVE X500GR"), "C/PALO SUAVE")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE TARAGUI C/ PALO FLEX 1KG"), "C/ PALO FLEX")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE TARAGUI FLEX S/PALO 1KG"), "FLEX S/PALO")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE VERDEFLOR BOLDO X500GR"), "BOLDO")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE YERBACID CEDRON X500GR"), "CEDRON")
        self.assertEqual(blowmax.capturar_descripcion("YERBA MATE YERBACID TRADICIONAL X500GR"), "TRADICIONAL")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS BAUZA SECOS CABELLO DE ANGEL 500G"), "SECOS CABELLO DE ANGEL")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS LA PROVIDENCIA CODO X500GR"), "CODO")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS LUCCHETTI MOSTACHOL N?51 X 500GR"), "MOSTACHOL N?51")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS MATARAZZO MONO X 500GR"), "MONO")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS SAN AGUSTIN TALLARIN X 500GR"), "TALLARIN")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS TERRABUSI MOSTACHOL 500GR"), "MOSTACHOL") 
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS NANI DE MAIZ  X 350 GR "), "DE MAIZ") 
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS BLUE PATNA FETUCCINI 500GR  "), "FETUCCINI")  
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS ARGENTINA FRESCOS AL HUEVO X 500GR  "), "FRESCOS AL HUEVO")  
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA CODITO C/HIERRO 500GR  "), "CODITO C/HIERRO")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA DEDALITOS C/HIERRO 500GR  "), "DEDALITOS C/HIERRO")     
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA MOSTACHOL C/HIERRO 500GR  "), "MOSTACHOL C/HIERRO")     
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA SPAGHETTI C/HIERRO 500GR  "), "SPAGHETTI C/HIERRO")     
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA TALLARIN C/HIERRO 500GR  "), "TALLARIN C/HIERRO")     
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS FAVORITA TIRABUZON C/HIERRO 500GR  "), "TIRABUZON C/HIERRO")  
        self.assertEqual(blowmax.capturar_descripcion("GASEOSA SCHWEPPES POMELO S/AZUCAR LATA X310C"), "POMELO S/AZUCAR LATA")   
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS CELESTIAL RADIATORE 500GR"), "RADIATORE")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS CELESTIAL TIRABUZON 500GR  "), "TIRABUZON")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS CELESTIAL MOSTACHOL 500GR  "), "MOSTACHOL")
        self.assertEqual(blowmax.capturar_descripcion("FIDEOS CELESTIAL SPAGHETTI 500GR  "), "SPAGHETTI")
           

    def test_volumen(self):
        blowmax = BlowmaxPipeline()
        self.assertEqual(blowmax.capturar_volumen("AC DOVE OLEO NUTRICION SUPERIOR X400ML"), "400")
        self.assertEqual(blowmax.capturar_volumen("SH HEAD SHOULDERS CHARCOAL X180ML"), "180")
        self.assertEqual(blowmax.capturar_volumen("SH PLUSBELLE ESENCIA RESTAURACION 970ML"), "970")
        self.assertEqual(blowmax.capturar_volumen("SH ELVIVE DREAM LONG 200ML"), "200")
        self.assertEqual(blowmax.capturar_volumen("SH SEDAL CARBON ACTIVADO PEONIAS X190ML"), "190")
        self.assertEqual(blowmax.capturar_volumen("SH SEDAL BOMBA NUTRICION X 340ML"), "340")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA COCA COLA LATA X 310CC"), "310")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA MANAOS GRANADINA X 3LT"), "3000")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA SCHWEPPES TONICA X 1,5LT"), "1500")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA SPRITE X 500CC"), "500")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA TALCA POMELO 3LT"), "3000")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA SPRITE X 2.25LT "), "2250")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA DIETETICA PASO DE LOS TOROS POMELO 1500 CC."), "1500")
        self.assertEqual(blowmax.capturar_volumen("LECHE ILOLAY LV DESCREMADA X1LT"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE LS PARC. DESCREMADA ZERO LACTOSA 1L"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE TREGAR DESCREMADA X 1LT"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE LS SACHET ULTRA ENTERA 1 LT 3%"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE LS UAT BOTELLA ENTERA CLASICA 3%"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE LS REDUCIDA LACTOSA F/VIT SACHET 1LT"), "1000")
        self.assertEqual(blowmax.capturar_volumen("LECHE LS UAT BOTELLA PARC. DESCREMADA 1%"), "1000")
        self.assertEqual(blowmax.capturar_volumen("PAN BIMBO ARTESANO X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("PAN BIMBO LIVIANO ACTI LECHE 550GR"), "550")
        self.assertEqual(blowmax.capturar_volumen("PAN LA ESPA?OLA LACTAL MULTISEMILLAS 450GR"), "450")
        self.assertEqual(blowmax.capturar_volumen("PAN LA ESPANOLA LACTAL DOLBLE SALVADO380GR"), "380")
        self.assertEqual(blowmax.capturar_volumen("PAN LACTAL RF DE MESA X315GR"), "315")
        self.assertEqual(blowmax.capturar_volumen("ARROZ DON MARCOS LARGO FINO X 500G"), "500")
        self.assertEqual(blowmax.capturar_volumen("ARROZ GALLO DOBLE CAROLINA CAJA X 1KG"), "1000")
        self.assertEqual(blowmax.capturar_volumen("ARROZ GALLO RISOTTO PRIM 240GR"), "240")
        self.assertEqual(blowmax.capturar_volumen("ARROZ GALLO RISOTTO ESPA?OLA 240GR"), "240")
        self.assertEqual(blowmax.capturar_volumen("ARROZ TIO CARLOS LARGO FINO X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("ARROZ GALLO ORO PARBOIL X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("ARROZ TIO CARLOS DOBLE CAROLINA X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("JABON DOVE BLANCO X 90GRS"), "90")
        self.assertEqual(blowmax.capturar_volumen("JABON KENIA CREMOSO 4X90G"), "360")
        self.assertEqual(blowmax.capturar_volumen("JABON KENIA GLICERINA OFERTA 3+1 360GR"), "360") 
        self.assertEqual(blowmax.capturar_volumen("JABON LUX JAZMIN BOTANIC CR 125G"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX JAZMIN BOTANIC CR 3 X 125G"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX ROSAS FRANCESAS BOTANIC 125GR"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON PATRICIA ALLEN TROPICALX130GR"), "130")
        self.assertEqual(blowmax.capturar_volumen("JABON PLUSBELLE BALANCE NUTRIOIL 125GRS"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA ANTIBACTERIAL ORIG.90GR"), "90")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE CHAMIGO X 1KG"), "1000")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE PLAYADITO C/PALO SUAVE X1KG"), "1000")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE PLAYADITO C/PALO SUAVE X500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE TARAGUI C/ PALO FLEX 1KG"), "1000")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE TARAGUI FLEX S/PALO 1KG"), "1000")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE VERDEFLOR BOLDO X500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE YERBACID CEDRON X500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("YERBA MATE YERBACID TRADICIONAL X500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS BAUZA SECOS CABELLO DE ANGEL 500G"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS LA PROVIDENCIA CODO X500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS LUCCHETTI MOSTACHOL N?51 X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS MATARAZZO MONO X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS SAN AGUSTIN TALLARIN X 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS TERRABUSI MOSTACHOL 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("GASEOSA SCHWEPPES POMELO S/AZUCAR LATA X310C"), "310")

        self.assertEqual(blowmax.capturar_volumen("JABON KENIA COLOR MIX 3X90GR"), "270")
        self.assertEqual(blowmax.capturar_volumen("JABON KENIA CREMOSO 4X90G"), "360")
        self.assertEqual(blowmax.capturar_volumen("JABON KENIA GLICERINA OFERTA 3+1 360GR"), "360")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX FLOR DE VAINILLA BOTA.3 X 125G"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX LIRIO AZUL BOTANIC 3 X 125G"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX ORQUIDEA NEGRA 125G"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON LUX ORQUIDEA NEGRA BOTANIC 3 X 125G"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON PLUSBELLE ENERGIA NUTRIOIL 3X125GR"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON PLUSBELLE FRESCURA NUTRIOIL 3X125GR"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON PLUSBELLE FRESCURA NUTRIOL X125GR"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON PLUSBELLE RELAJACION NUTRIOIL 3X125GR"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA ANTIB FRESH X90G"), "90")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA ANTIBACTERIAL ALOE 3X90G"), "270")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA ANTIBACTERIAL ORIG.90GR"), "90")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA BAMBOO X125G"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA GLICERINA NEUTRO HIPORLARG 3X90G"), "270")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA GLICERINA NEUTRO X90G"), "90")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA NUTRITIVA ORCHID 125GR"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA NUTRITIVA ORCHID 3X125GR"), "375")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA SENSIBLE FR DERM X125G"), "125")
        self.assertEqual(blowmax.capturar_volumen("JABON REXONA SENSIBLE FRESH 3X125G"), "375")

        self.assertEqual(blowmax.capturar_volumen("FIDEOS CELESTIAL RADIATORE 500GR"), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS CELESTIAL TIRABUZON 500GR  "), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS CELESTIAL MOSTACHOL 500GR  "), "500")
        self.assertEqual(blowmax.capturar_volumen("FIDEOS CELESTIAL SPAGHETTI 500GR  "), "500")






if __name__ == '__main__':
    unittest.main()
