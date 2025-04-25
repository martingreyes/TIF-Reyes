import re
import unittest

from pipelines import NormalizarPipeline

class TestExpresionesRegulares(unittest.TestCase):
    def test_marca(self):
        normalizar = NormalizarPipeline()
        self.assertEqual(normalizar.normalizar_marca("Tio Carlos"), "TIO CARLOS")
        self.assertEqual(normalizar.normalizar_marca("LUCHETTI"), "LUCCHETTI")
        self.assertEqual(normalizar.normalizar_marca("7UP"), "SEVEN UP")
        self.assertEqual(normalizar.normalizar_marca("P.DE LOS TOROS"), "PASO DE LOS TOROS")
        self.assertEqual(normalizar.normalizar_marca("ARMONÍA"), "ARMONIA")
        self.assertEqual(normalizar.normalizar_marca("LA SEREN."), "LA SERENISIMA")
        self.assertEqual(normalizar.normalizar_marca("LS"), "LA SERENISIMA")
        self.assertEqual(normalizar.normalizar_marca("Serenisima"), "LA SERENISIMA")
        self.assertEqual(normalizar.normalizar_marca("LA ESPA?OLA"), "LA ESPANOLA")
        self.assertEqual(normalizar.normalizar_marca("HEAD & SHOULDERS"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("HEAD & SHOULDER"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("HEAD SHOULDERS"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("Head Shoulders"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("Johnson"), "JOHNSONS")
        self.assertEqual(normalizar.normalizar_marca("TRESEMMÉ"), "TRESEMME")
        self.assertEqual(normalizar.normalizar_marca("Cruz Malta"), "CRUZ DE MALTA")
        self.assertEqual(normalizar.normalizar_marca("UNIÓN"), "UNION")
        self.assertEqual(normalizar.normalizar_marca("HEAD & SHOULDER"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("Head & Sh"), "HEAD & SHOULDERS")
        self.assertEqual(normalizar.normalizar_marca("LA PROVIDENCIA"), "LA PROVIDENCIA")
        self.assertEqual(normalizar.normalizar_marca("PROVIDENCIA"), "LA PROVIDENCIA")

    def test_descripcion(self):
        normalizar = NormalizarPipeline()
        #Arroces
        self.assertEqual(normalizar.normalizar_descripcion("DOBLE CAROLINA CAJA","Arroces"), "DOBLE CAROLINA")
        self.assertEqual(normalizar.normalizar_descripcion("L.FINO 0 0 0 0 0","Arroces"), "LARGO FINO 00000")
        self.assertEqual(normalizar.normalizar_descripcion("L.FINO 5/0","Arroces"), "LARGO FINO 00000")
        self.assertEqual(normalizar.normalizar_descripcion("P/PREPARA RIS.A LA ESPAÑO","Arroces"), "RISOTTO A LA ESPANOLA")
        self.assertEqual(normalizar.normalizar_descripcion("PARB. BOLSA","Arroces"), "PARBOIL")
        self.assertEqual(normalizar.normalizar_descripcion("PARBOIT","Arroces"), "PARBOIL")
        self.assertEqual(normalizar.normalizar_descripcion("RISOTTO ESPA?OLA","Arroces"), "RISOTTO ESPANOLA")
        self.assertEqual(normalizar.normalizar_descripcion("P/PREPARA SAB.WOK ORIENT","Arroces"), "SABORES DEL MUNDO WOK ORIENTAL") 
        self.assertEqual(normalizar.normalizar_descripcion("P/PREPARA SAB.MEDITERRANE","Arroces"), "SABORES DEL MUNDO MEDITERRANEO") 
        self.assertEqual(normalizar.normalizar_descripcion("Sabores Del Mundo Mediterraneo","Arroces"), "SABORES DEL MUNDO MEDITERRANEO")
        self.assertEqual(normalizar.normalizar_descripcion("Sabores Del Mundo Wok Oriental","Arroces"), "SABORES DEL MUNDO WOK ORIENTAL")
        self.assertEqual(normalizar.normalizar_descripcion("Sabores Del Mundo Curry Asiatico","Arroces"), "SABORES DEL MUNDO CURRI ASIATICO")
        self.assertEqual(normalizar.normalizar_descripcion("SABORES DEL MUNDO CURRI ASIATICO","Arroces"), "SABORES DEL MUNDO CURRI ASIATICO")
        self.assertEqual(normalizar.normalizar_descripcion("RISOTTO TRAT.CHAMPI","Arroces"), "RISOTTO TRATTORIA CHAMPI")
        #Fideos  
        self.assertEqual(normalizar.normalizar_descripcion("3VEG.TIRA.","Fideos"), "3 VEGETALES TIRABUZON")
        # #Gaseosas
        self.assertEqual(normalizar.normalizar_descripcion("POMELO","Gaseosas"), "POMELO")
        self.assertEqual(normalizar.normalizar_descripcion("POM","Gaseosas"), "POMELO")
        self.assertEqual(normalizar.normalizar_descripcion("DESCARTABLE","Gaseosas"), "")
        self.assertEqual(normalizar.normalizar_descripcion("RETORNABLE","Gaseosas"), "")
        self.assertEqual(normalizar.normalizar_descripcion("SABOR","Gaseosas"), "")
        self.assertEqual(normalizar.normalizar_descripcion("ZERO","Gaseosas"), "SIN AZUCAR")
        self.assertEqual(normalizar.normalizar_descripcion("DIETETICA","Gaseosas"), "")
        #Jabones
        self.assertEqual(normalizar.normalizar_descripcion("GLICERINA OFERTA 3+1","Jabones"), "GLICERINA OFERTA 4")
        self.assertEqual(normalizar.normalizar_descripcion("GLICERINA U.ACEITE.ESE.","Jabones"), "GLICERINA U. ACEITES ESENCIALES")
        self.assertEqual(normalizar.normalizar_descripcion("JAZMIN CREMOSO","Jabones"), "JAZMIN CREMOSO")
        self.assertEqual(normalizar.normalizar_descripcion("JAZMIN BOTANIC CR","Jabones"), "JAZMIN BOTANIC CREMOSO")
        #Leches
        self.assertEqual(normalizar.normalizar_descripcion("PARC. DESCREMADA 1%","Leches"), "PARCIALMENTE DESCREMADA 1%")
        self.assertEqual(normalizar.normalizar_descripcion("PARCIA.DESCR. LIV.2%","Leches"), "PARCIALMENTE DESCREMADA LIVIANA 2%")
        self.assertEqual(normalizar.normalizar_descripcion("LV ENTERA","Leches"), "ENTERA")
        self.assertEqual(normalizar.normalizar_descripcion("Larga Vida Entera","Leches"), "ENTERA")
        self.assertEqual(normalizar.normalizar_descripcion("L.VIDA ENTERA","Leches"), "ENTERA")
        self.assertEqual(normalizar.normalizar_descripcion("LA SERENISIMA 0% LACTOSA BOTELLA 1000","Leches"), "LA SERENISIMA 0% LACTOSA 1000")
        # #Panes
        # self.assertEqual(normalizar.normalizar_descripcion("","Panes"), "")
        #Shampoos
        self.assertEqual(normalizar.normalizar_descripcion("Restauracion Instantanea","Shampoos"), "RESTAURACION INSTANTANEA")
        self.assertEqual(normalizar.normalizar_descripcion("Restauracion","Shampoos"), "RESTAURACION")
        self.assertEqual(normalizar.normalizar_descripcion("RESTAURACIÓN INSTANTÁNEA DOY PACK","Shampoos"), "RESTAURACION INSTANTANEA DOY PACK")
        self.assertEqual(normalizar.normalizar_descripcion("RITUAL REPARACIÓN","Shampoos"), "RITUAL REPARACION")
        self.assertEqual(normalizar.normalizar_descripcion("RITUAL DE REPAR FORT PALTA","Shampoos"), "RITUAL DE REPARACION FORT PALTA")
        self.assertEqual(normalizar.normalizar_descripcion("RITUAL REPARACIÓN","Shampoos"), "RITUAL REPARACION")
        self.assertEqual(normalizar.normalizar_descripcion("RIZOS DEFINIDOS","Shampoos"), "RIZOS DEFINIDOS")
        self.assertEqual(normalizar.normalizar_descripcion("REGEN.EXTREMA","Shampoos"), "REGEN.EXTREMA")
        self.assertEqual(normalizar.normalizar_descripcion("Liso Perfecto","Shampoos"), "LISO PERFECTO")
        self.assertEqual(normalizar.normalizar_descripcion("Esencial Restauracion","Shampoos"), "ESENCIA RESTAURACION")
        self.assertEqual(normalizar.normalizar_descripcion("Esencia Fuerza Reparadora","Shampoos"), "ESENCIA FUERZA REPARADORA")
        self.assertEqual(normalizar.normalizar_descripcion("BALANCE REPARADOR","Shampoos"), "BALANCE REPARADOR")
        self.assertEqual(normalizar.normalizar_descripcion("ESENC RESTAURACION","Shampoos"), "ESENCIA RESTAURACION")
        

        
        #Yerbas
        self.assertEqual(normalizar.normalizar_descripcion("COMP. +BOLDO","Yerbas"), "BOLDO")
        
if __name__ == '__main__':
    unittest.main()