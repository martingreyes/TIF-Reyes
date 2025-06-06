import re
import unittest

from pipelines import AtomoPipeline

class TestExpresionesRegulares(unittest.TestCase):
    def test_marca(self):
        atomo = AtomoPipeline()
        self.assertEqual(atomo.capturar_marca("SHAMPOO HEAD & SHOULDER ANTI COMEZON 375 ML"), "HEAD & SHOULDER")
        self.assertEqual(atomo.capturar_marca("SHAMPOO FLIAR SUAVE BOMBA CERAMIDAS 930 ML."), "SUAVE")
        self.assertEqual(atomo.capturar_marca("SHAMPOO PANTENE LISO INFINITO 400 ML"), "PANTENE")
        self.assertEqual(atomo.capturar_marca("SHAMPOO FLIAR PLUSBELLE FUERZA ANTIOXID 1000 ML."), "PLUSBELLE")
        self.assertEqual(atomo.capturar_marca("SHAMPOO FLIAR PEPE"), "?")
        self.assertEqual(atomo.capturar_marca("SHAMPOO TRESEMME CAUTERIZACION 250 ML."), "TRESEMME")
        self.assertEqual(atomo.capturar_marca("GASEOSA DIET COCA COLA SIN AZUCAR 2500 CC."), "COCA COLA")
        self.assertEqual(atomo.capturar_marca("GASEOSAS SCHWEPPES POMELO ZERO 1500 CC."), "SCHWEPPES")
        self.assertEqual(atomo.capturar_marca("GASEOSAS LEVITE FIZZ POMELO 2250 CC.."), "LEVITE")
        self.assertEqual(atomo.capturar_marca("GASEOSAS SECCO COLA 3000 CC."), "SECCO")
        self.assertEqual(atomo.capturar_marca("GASEOSAS P.DE LOS TOROS POMELO 1500 CC."), "P.DE LOS TOROS")
        self.assertEqual(atomo.capturar_marca("GASEOSAS MIRINDA NARANJA 1500 CC."), "MIRINDA")
        self.assertEqual(atomo.capturar_marca("LECHE U.A.T. LA SERENISIMA PROTEIN 0% 1 LTS."), "LA SERENISIMA")
        self.assertEqual(atomo.capturar_marca("LECHE U.A.T. VERONICA DESCREMADA 1000 CC."), "VERONICA")
        self.assertEqual(atomo.capturar_marca("LECHE U.A.T. LA SERENISIMA 0% LACTOSA 1 LTS."), "LA SERENISIMA")
        self.assertEqual(atomo.capturar_marca("PAN REBANADO LACTAL LACTEADO 460 GRS"), "LACTAL")
        self.assertEqual(atomo.capturar_marca("PAN DE SALVADO LACTAL NVO 330 GRS"), "LACTAL")
        self.assertEqual(atomo.capturar_marca("ARROZ GALLO CARNAROLI ESTUCHE 500 GRS"), "GALLO")
        self.assertEqual(atomo.capturar_marca("ARROZ L.FINO TIO CARLOS 00000 500 GRS"), "TIO CARLOS")
        self.assertEqual(atomo.capturar_marca("ARROZ L.FINO AMANDA 0 0 0 0 0 500 GRS"), "AMANDA")
        self.assertEqual(atomo.capturar_marca("ARROZ L.FINO NOBLE 5/0 500 GRS"), "NOBLE")
        self.assertEqual(atomo.capturar_marca("ARROZ L.FINO SAN JAVIER 00000 1000 GRS"), "SAN JAVIER")
        self.assertEqual(atomo.capturar_marca("ARROZ P/PREPARA GALLO RIS.PARME.AZAFR 240 GRS"), "GALLO")
        self.assertEqual(atomo.capturar_marca("ARROZ L.FINO ALA 1000 GRS"), "ALA")
        self.assertEqual(atomo.capturar_marca("ARROZ P/PREPARA GALLO RIS.PRO.4 QUESO 240 GRS"), "GALLO")
        self.assertEqual(atomo.capturar_marca("JABON TOCADOR DUC RELAX 110 GRS"), "DUC")
        self.assertEqual(atomo.capturar_marca("JABON TOCADOR DOVE ORIGINAL 720 GRS"), "DOVE")
        self.assertEqual(atomo.capturar_marca("JABON TOCADOR PLUSBELLE RELAJACION 120 GRS"), "PLUSBELLE")
        self.assertEqual(atomo.capturar_marca("JABON TOCADOR LUX ORQUIDEA NEGRA 375 GRS"), "LUX")
        self.assertEqual(atomo.capturar_marca("JABON ANTIB. PROTEX AVENA 125 GRS"), "PROTEX")
        self.assertEqual(atomo.capturar_marca("JABON GLICERINA VERITAS U.ACEITE.ESE. 120 GRS"), "VERITAS")
        self.assertEqual(atomo.capturar_marca("JABON GLICERINA ST TROPEZ TRICOLOR 3X90 270 GRS"), "ST TROPEZ")
        self.assertEqual(atomo.capturar_marca("JABON TOCADOR NIVEA AVENA 375 GRS"), "NIVEA")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. CACHAMATE COCO 500 GRS"), "CACHAMATE")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. VERDEFLOR +NARANJA 500 GRS"), "VERDEFLOR")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. VERDEFLOR CEDRON 500 GRS"), "VERDEFLOR")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. VERDEFLOR +BOLDO 1000 GRS"), "VERDEFLOR")
        self.assertEqual(atomo.capturar_marca("YERBA S/PALO TARAGUI 4FLEX 500 GRS"), "TARAGUI")
        self.assertEqual(atomo.capturar_marca("YERBA C/PALO CHAMIGO S/TACC 1000 GRS"), "CHAMIGO")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. CBSE SILUETA NARANJA 500 GRS"), "CBSE")
        self.assertEqual(atomo.capturar_marca("YERBA COMP. BUENAS Y SANTAS HIERBAS 500 GRS"), "BUENAS Y SANTAS")
        self.assertEqual(atomo.capturar_marca("FIDEOS GUISEROS LA PROV. RIGATTI 500 GRS"), "LA PROVIDENCIA")
        self.assertEqual(atomo.capturar_marca("FIDEOS GUISEROS BAUZA B.RIGATTI 500 GRS"), "BAUZA")
        self.assertEqual(atomo.capturar_marca("FIDEOS SOPEROS BAUZA B.DEDALITOS 500 GRS"), "BAUZA")
        self.assertEqual(atomo.capturar_marca("FIDEOS GUISEROS LA PROV. TIRABUZON 500 GRS"), "LA PROVIDENCIA")
        self.assertEqual(atomo.capturar_marca("FIDEOS LARGOS BAUZA LAMINADO MEDIAN 500 GRS"), "BAUZA")
        self.assertEqual(atomo.capturar_marca("FIDEOS LARGOS LUCHETTI TALLARIN 500 GRS"), "LUCHETTI")
        self.assertEqual(atomo.capturar_marca("FIDEOS GUISEROS LUCCHETTI PENNE RIGATE 500 GRS"), "LUCCHETTI")
        
            
    
    def test_descripcion(self):
        atomo = AtomoPipeline()
        self.assertEqual(atomo.capturar_descripcion("SHAMPOO FLIAR SUAVE BOMBA CERAMIDAS 930 ML."), "BOMBA CERAMIDAS")
        self.assertEqual(atomo.capturar_descripcion("SHAMPOO PANTENE LISO INFINITO 400 ML"), "LISO INFINITO")
        self.assertEqual(atomo.capturar_descripcion("SHAMPOO FLIAR PLUSBELLE FUERZA ANTIOXID 1000 ML."), "FUERZA ANTIOXID")
        self.assertEqual(atomo.capturar_descripcion("GASEOSA DIET COCA COLA SIN AZUCAR 2500 CC."), "DIET SIN AZUCAR")
        self.assertEqual(atomo.capturar_descripcion("GASEOSAS SCHWEPPES POMELO ZERO 1500 CC."), "POMELO ZERO")
        self.assertEqual(atomo.capturar_descripcion("GASEOSAS LEVITE FIZZ POMELO 2250 CC.."), "FIZZ POMELO")
        self.assertEqual(atomo.capturar_descripcion("GASEOSAS SECCO COLA 3000 CC."), "COLA")
        self.assertEqual(atomo.capturar_descripcion("GASEOSA DIETETICA PASO DE LOS TOROS POMELO 1500 CC."), "DIETETICA POMELO")
        self.assertEqual(atomo.capturar_descripcion("GASEOSAS P.DE LOS TOROS POMELO 1500 CC."), "POMELO")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. LA SERENISIMA PROTEIN 0% 1 LTS."), "PROTEIN 0%")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. VERONICA DESCREMADA 1000 CC."), "DESCREMADA")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. LA SERENISIMA 0% LACTOSA 1 LTS."), "0% LACTOSA")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. LA SERENISIMA 0% LACTOSA"), "?")
        self.assertEqual(atomo.capturar_descripcion("PAN REBANADO LACTAL LACTEADO 460 GRS"), "REBANADO LACTEADO")
        self.assertEqual(atomo.capturar_descripcion("PAN DE SALVADO LACTAL NVO 330 GRS"), "DE SALVADO NVO")
        self.assertEqual(atomo.capturar_descripcion("ARROZ GALLO CARNAROLI ESTUCHE 500 GRS"), "CARNAROLI ESTUCHE")
        self.assertEqual(atomo.capturar_descripcion("ARROZ L.FINO TIO CARLOS 00000 500 GRS"), "L.FINO 00000")
        self.assertEqual(atomo.capturar_descripcion("ARROZ L.FINO AMANDA 0 0 0 0 0 500 GRS"), "L.FINO 0 0 0 0 0")
        self.assertEqual(atomo.capturar_descripcion("ARROZ L.FINO NOBLE 5/0 500 GRS"), "L.FINO 5/0")
        self.assertEqual(atomo.capturar_descripcion("ARROZ L.FINO SAN JAVIER 00000 1000 GRS"), "L.FINO 00000")
        self.assertEqual(atomo.capturar_descripcion("ARROZ P/PREPARA GALLO RIS.PARME.AZAFR 240 GRS"), "P/PREPARA RIS.PARME.AZAFR")
        self.assertEqual(atomo.capturar_descripcion("ARROZ P/PREPARA GALLO RIS.PRO.4 QUESO 240 GRS"), "P/PREPARA RIS.PRO.4 QUESO")
        self.assertEqual(atomo.capturar_descripcion("ARROZ LARGO FINO MENCHO 0000 1 KG"), "LARGO FINO 0000")
        self.assertEqual(atomo.capturar_descripcion("ARROZ L.FINO ALA 1000 GRS"), "L.FINO")
        self.assertEqual(atomo.capturar_descripcion('ARROZ PARB. GALLO BOLSA 1 KG'), 'PARB. BOLSA')
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR DUC RELAX 110 GRS"), "RELAX")
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR DOVE ORIGINAL 720 GRS"), "ORIGINAL")
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR PLUSBELLE RELAJACION 120 GRS"), "RELAJACION")
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR LUX ORQUIDEA NEGRA 375 GRS"), "ORQUIDEA NEGRA")
        self.assertEqual(atomo.capturar_descripcion("JABON ANTIB. PROTEX AVENA 125 GRS"), "ANTIB. AVENA")
        self.assertEqual(atomo.capturar_descripcion("JABON GLICERINA VERITAS U.ACEITE.ESE. 120 GRS"), "GLICERINA U.ACEITE.ESE.")
        self.assertEqual(atomo.capturar_descripcion("JABON GLICERINA ST TROPEZ TRICOLOR 3X90 270 GRS"), "GLICERINA TRICOLOR 3X90")
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR NIVEA AVENA 375 GRS"), "AVENA")
        self.assertEqual(atomo.capturar_descripcion("JABON TOCADOR KENIA COLOR MIX 270 GRS"), "COLOR MIX")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. CACHAMATE COCO 500 GRS"), "COMP. COCO")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. VERDEFLOR +NARANJA 500 GRS"), "COMP. +NARANJA")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. VERDEFLOR CEDRON 500 GRS"), "COMP. CEDRON")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. VERDEFLOR +BOLDO 1000 GRS"), "COMP. +BOLDO")
        self.assertEqual(atomo.capturar_descripcion("YERBA S/PALO TARAGUI 4FLEX 500 GRS"), "S/PALO 4FLEX")
        self.assertEqual(atomo.capturar_descripcion("YERBA C/PALO CHAMIGO S/TACC 1000 GRS"), "C/PALO S/TACC")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. CBSE SILUETA NARANJA 500 GRS"), "COMP. SILUETA NARANJA")
        self.assertEqual(atomo.capturar_descripcion("YERBA COMP. BUENAS Y SANTAS HIERBAS 500 GRS"), "COMP. HIERBAS")
        self.assertEqual(atomo.capturar_descripcion("YERBA C/PALO MAÑANITA 4 FLEX 500 GRS"), "C/PALO 4 FLEX")
        self.assertEqual(atomo.capturar_descripcion("YERBA S/PALO DON LUCAS 500 GRS"), "S/PALO")
        self.assertEqual(atomo.capturar_descripcion("YERBA C/PALO LA HOJA 500 GRS"), "C/PALO")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS LA PROV. RIGATTI 500 GRS"), "GUISEROS RIGATTI")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS BAUZA B.RIGATTI 500 GRS"), "GUISEROS B.RIGATTI")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS SOPEROS BAUZA B.DEDALITOS 500 GRS"), "SOPEROS B.DEDALITOS")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS LA PROV. TIRABUZON 500 GRS"), "GUISEROS TIRABUZON")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS LARGOS BAUZA LAMINADO MEDIAN 500 GRS"), "LARGOS LAMINADO MEDIAN")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS LARGOS LUCHETTI TALLARIN 500 GRS"), "LARGOS TALLARIN")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS LUCCHETTI PENNE RIGATE 500 GRS"), "GUISEROS PENNE RIGATE")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS LARGOS LUCIA SPAGHETTI 500 GRS"), "LARGOS SPAGHETTI")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS ROBLES TIRABUZON MULTICOLOR 500 GRS"), "GUISEROS TIRABUZON MULTICOLOR")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. ILOLAY ENTERA 1000 CC."), "ENTERA")
        self.assertEqual(atomo.capturar_descripcion("LECHE U.A.T. ILOLAY DESCREMADA 1000 CC."), "DESCREMADA")
        self.assertEqual(atomo.capturar_descripcion("PAN REBANADO FARGO LACTEADO 585 GRS"), "REBANADO LACTEADO")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS GUISEROS PASTASOLE SPAGHETTI 500 GRS"), "GUISEROS SPAGHETTI")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS SOPEROS TERRABUSI AVE MARIA 1 500 GRS"), "SOPEROS AVE MARIA 1")
        self.assertEqual(atomo.capturar_descripcion("FIDEOS SOPEROS TERRABUSI DEDALITOS 500 GRS"), "SOPEROS DEDALITOS")
        

        
        


    def test_volumen(self):
        atomo = AtomoPipeline()
        self.assertEqual(atomo.capturar_volumen("SHAMPOO FLIAR SUAVE BOMBA CERAMIDAS 930 ML."), "930")
        self.assertEqual(atomo.capturar_volumen("SHAMPOO PANTENE LISO INFINITO 400 ML"), "400")
        self.assertEqual(atomo.capturar_volumen("SHAMPOO FLIAR PLUSBELLE FUERZA ANTIOXID 1000 ML."), "1000")
        self.assertEqual(atomo.capturar_volumen("GASEOSA DIET COCA COLA SIN AZUCAR 2500 CC."), "2500")
        self.assertEqual(atomo.capturar_volumen("GASEOSAS SCHWEPPES POMELO ZERO 1500 CC."), "1500")
        self.assertEqual(atomo.capturar_volumen("GASEOSAS LEVITE FIZZ POMELO 2250 CC."), "2250")
        self.assertEqual(atomo.capturar_volumen("GASEOSAS SECCO COLA 3000 CC."), "3000")
        self.assertEqual(atomo.capturar_volumen("GASEOSAS P.DE LOS TOROS POMELO 1500 CC."), "1500")
        self.assertEqual(atomo.capturar_volumen("LECHE U.A.T. LA SERENISIMA PROTEIN 0% 1 LTS."), "1000")
        self.assertEqual(atomo.capturar_volumen("LECHE U.A.T. VERONICA DESCREMADA 1000 CC."), "1000")
        self.assertEqual(atomo.capturar_volumen("LECHE U.A.T. LA SERENISIMA 0% LACTOSA 1 LTS."), "1000")
        self.assertEqual(atomo.capturar_volumen("PAN REBANADO LACTAL LACTEADO 460 GRS"), "460")
        self.assertEqual(atomo.capturar_volumen("PAN DE SALVADO LACTAL NVO 330 GRS"), "330")
        self.assertEqual(atomo.capturar_volumen("ARROZ GALLO CARNAROLI ESTUCHE 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("ARROZ L.FINO TIO CARLOS 00000 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("ARROZ L.FINO AMANDA 0 0 0 0 0 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("ARROZ L.FINO NOBLE 5/0 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("ARROZ LARGO FINO MENCHO 0000 1 KG"), "1000")
        self.assertEqual(atomo.capturar_volumen("ARROZ L.FINO SAN JAVIER 00000 1000 GRS"), "1000")
        self.assertEqual(atomo.capturar_volumen("ARROZ P/PREPARA GALLO RIS.PARME.AZAFR 240 GRS"), "240")
        self.assertEqual(atomo.capturar_volumen("ARROZ P/PREPARA GALLO RIS.PRO.4 QUESO 240 GRS"), "240")
        self.assertEqual(atomo.capturar_volumen("JABON TOCADOR DUC RELAX 110 GRS"), "110")
        self.assertEqual(atomo.capturar_volumen("JABON TOCADOR DOVE ORIGINAL 720 GRS"), "720")
        self.assertEqual(atomo.capturar_volumen("JABON TOCADOR PLUSBELLE RELAJACION 120 GRS"), "120")
        self.assertEqual(atomo.capturar_volumen("JABON TOCADOR LUX ORQUIDEA NEGRA 375 GRS"), "375")
        self.assertEqual(atomo.capturar_volumen("JABON ANTIB. PROTEX AVENA 125 GRS"), "125")
        self.assertEqual(atomo.capturar_volumen("JABON GLICERINA VERITAS U.ACEITE.ESE. 120 GRS"), "120")
        self.assertEqual(atomo.capturar_volumen("JABON GLICERINA ST TROPEZ TRICOLOR 3X90 270 GRS"), "270")
        self.assertEqual(atomo.capturar_volumen("JABON TOCADOR NIVEA AVENA 375 GRS"), "375")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. CACHAMATE COCO 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. VERDEFLOR +NARANJA 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. VERDEFLOR CEDRON 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. VERDEFLOR +BOLDO 1000 GRS"), "1000")
        self.assertEqual(atomo.capturar_volumen("YERBA S/PALO TARAGUI 4FLEX 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("YERBA C/PALO CHAMIGO S/TACC 1000 GRS"), "1000")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. CBSE SILUETA NARANJA 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("YERBA COMP. BUENAS Y SANTAS HIERBAS 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS GUISEROS LA PROV. RIGATTI 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS GUISEROS BAUZA B.RIGATTI 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS SOPEROS BAUZA B.DEDALITOS 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS GUISEROS LA PROV. TIRABUZON 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS LARGOS BAUZA LAMINADO MEDIAN 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS LARGOS LUCHETTI TALLARIN 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS GUISEROS LUCCHETTI PENNE RIGATE 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("LECHE U.A.T. ILOLAY ENTERA 1000 CC."), "1000")
        self.assertEqual(atomo.capturar_volumen("LECHE U.A.T. ILOLAY DESCREMADA 1000 CC."), "1000")
        self.assertEqual(atomo.capturar_volumen("PAN REBANADO FARGO LACTEADO 585 GRS"), "585")
        self.assertEqual(atomo.capturar_volumen("FIDEOS GUISEROS PASTASOLE SPAGHETTI 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS SOPEROS TERRABUSI AVE MARIA 1 500 GRS"), "500")
        self.assertEqual(atomo.capturar_volumen("FIDEOS SOPEROS TERRABUSI DEDALITOS 500 GRS"), "500")
        
        


if __name__ == '__main__':
    unittest.main()