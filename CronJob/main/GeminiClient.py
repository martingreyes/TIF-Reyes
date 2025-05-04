from google.genai import types # type: ignore
from google import genai
import pandas as pd
import ast
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key_env = os.getenv("API_KEYS", "")
        self.api_keys = [key.strip() for key in api_key_env.split(",") if key.strip()]
        self.index = 0
        self.model = 'gemini-2.0-flash'
        self.client = None
        self._set_client()
        self.instruction = """
A continuación, te proporcionaré una lista de productos comercializados por distintos supermercados. Cada producto es una cadena de texto con el siguiente formato:

"id_producto - Categoría - Marca - Descripción - Volumen - Supermercado"

Tu tarea es **agrupar los productos equivalentes**, entendiendo por equivalentes aquellos que coinciden en categoría, marca, descripción (con cierta tolerancia) y volumen, pero provienen de supermercados diferentes.

Reglas para agrupar:
- **Cada grupo debe contener productos equivalentes, sin repetir supermercados dentro del mismo grupo**. La parte "Supermercado" (última parte de la cadena) es lo que se debe considerar como el identificador del supermercado, por ejemplo "Blowmax", "Atomo", "Modo Market". Es decir, un grupo no puede tener dos productos del mismo supermercado.
- **Puede haber entre 1 y 4 productos por grupo** (ya que hay 4 supermercados distintos). Cada grupo puede estar formado por un mínimo de 1 producto y un máximo de 4 productos, cada uno de un supermercado distinto.
- Un mismo producto no puede pertenecer a más de un grupo.
- El ID del producto (al inicio) no debe influir en la comparación, pero debe mantenerse en el resultado para identificar el producto.
- Dos productos se consideran equivalentes aunque su descripción difiera en solo una palabra no determinante. 
    Por ejemplo, considera equivalentes las descripciones "BRILLO LUMINOSIDAD" y "BRILLO", "LARGOS SPAGUETTI" y "SPAGUETTI", "TIRABUZON HUEVO" y "AL HUEVO TIRABUZON", "MEN 2EN1 FZA EXTREM" y "2 EN 1 FUERZA EXTREMA", ya que la diferencia no altera significativamente el significado del producto.

### Salida esperada:
Una lista de listas, donde cada sublista representa un grupo de productos equivalentes. Cada cadena debe mantenerse completa (incluyendo el ID).

Ejemplo 1 de input:
['434004420 - Yerbas - VERDEFLOR - - 500 - Blowmax', '873462784 - Yerbas - VERDEFLOR - BOLDO - 500 - Atomo', '983274982 - Yerbas - VERDEFLOR - BOLDO - 500 - Blowmax', '456789012 - Yerbas - VERDEFLOR - BOLDO - 500 - Modo Market', '234567891 - Yerbas - VERDEFLOR - CEDRON - 500 - Atomo', '567890123 - Yerbas - VERDEFLOR - CEDRON - 500 - Blowmax', '678901234 - Yerbas - VERDEFLOR - CEDRON - 500 - Modo Market', '789012345 - Yerbas - VERDEFLOR - HIERBAS - 500 - Atomo', '890123456 - Yerbas - VERDEFLOR - MENTA - 500 - Atomo', '901234567 - Yerbas - VERDEFLOR - MENTA - 500 - Blowmax', '123450987 - Yerbas - VERDEFLOR - MENTA - 500 - Modo Market', '234561098 - Yerbas - VERDEFLOR - NARANJA - 500 - Blowmax', '345672109 - Yerbas - VERDEFLOR - NARANJA - 500 - Modo Market', '456783210 - Yerbas - VERDEFLOR - PEPERINA - 500 - Blowmax', '567894321 - Yerbas - VERDEFLOR - SERRANA - 500 - Casa Segal', '678905432 - Yerbas - VERDEFLOR - TRADICIONAL ROJA CON PALO - 500 - Modo Market']

Ejemplo 1 de output esperado: 
[['434004420 - Yerbas - VERDEFLOR - - 500 - Blowmax'], ['873462784 - Yerbas - VERDEFLOR - BOLDO - 500 - Atomo', '983274982 - Yerbas - VERDEFLOR - BOLDO - 500 - Blowmax', '456789012 - Yerbas - VERDEFLOR - BOLDO - 500 - Modo Market'], ['234567891 - Yerbas - VERDEFLOR - CEDRON - 500 - Atomo', '567890123 - Yerbas - VERDEFLOR - CEDRON - 500 - Blowmax', '678901234 - Yerbas - VERDEFLOR - CEDRON - 500 - Modo Market'], ['789012345 - Yerbas - VERDEFLOR - HIERBAS - 500 - Atomo'], ['890123456 - Yerbas - VERDEFLOR - MENTA - 500 - Atomo', '901234567 - Yerbas - VERDEFLOR - MENTA - 500 - Blowmax', '123450987 - Yerbas - VERDEFLOR - MENTA - 500 - Modo Market'], ['234561098 - Yerbas - VERDEFLOR - NARANJA - 500 - Blowmax', '345672109 - Yerbas - VERDEFLOR - NARANJA - 500 - Modo Market'], ['456783210 - Yerbas - VERDEFLOR - PEPERINA - 500 - Blowmax'], ['567894321 - Yerbas - VERDEFLOR - SERRANA - 500 - Casa Segal'], ['678905432 - Yerbas - VERDEFLOR - TRADICIONAL ROJA CON PALO - 500 - Modo Market']]

Ejemplo 2 de input: 
['112233445 - Shampoos - PLUSBELLE - ANTIOXIDANTE - 1000 - Casa Segal', '223344556 - Shampoos - PLUSBELLE - BALANCE - 1000 - Casa Segal', '334455667 - Shampoos - PLUSBELLE - BALANCE REPARADOR - 1000 - Blowmax', '445566778 - Shampoos - PLUSBELLE - BRILLO - 1000 - Blowmax', '556677889 - Shampoos - PLUSBELLE - BRILLO - 1000 - Casa Segal', '667788990 - Shampoos - PLUSBELLE - BRILLO LUMINOSIDAD - 1000 - Modo Market', '778899001 - Shampoos - PLUSBELLE - CUIDADO SUAVIDAD - 1000 - Modo Market', '889900112 - Shampoos - PLUSBELLE - ESENCIA CONTROL FRIZZ - 1000 - Modo Market', '990011223 - Shampoos - PLUSBELLE - FRESCURA - 1000 - Modo Market', '001122334 - Shampoos - PLUSBELLE - FRESCURA - 1000 - Casa Segal', '112233556 - Shampoos - PLUSBELLE - FRESCURA VITALIDAD - 1000 - Blowmax', '223344667 - Shampoos - PLUSBELLE - FUERZA ANTIOXID - 1000 - Atomo', '334455778 - Shampoos - PLUSBELLE - FUERZA ANTIOXIDANTE - 1000 - Modo Market', '445566889 - Shampoos - PLUSBELLE - HIDRATACION - 1000 - Blowmax', '556677900 - Shampoos - PLUSBELLE - NUTRICION - 1000 - Casa Segal', '667788011 - Shampoos - PLUSBELLE - NUTRICION CR OLEO MACADA - 1000 - Blowmax', '778899122 - Shampoos - PLUSBELLE - NUTRICION CREME - 1000 - Modo Market', '889900233 - Shampoos - PLUSBELLE - PROTECCION - 1000 - Modo Market', '990011344 - Shampoos - PLUSBELLE - REACTIVACION HIDRATANTE - 1000 - Blowmax', '001122455 - Shampoos - PLUSBELLE - SUAVIDAD - 1000 - Casa Segal', '112233566 - Shampoos - PLUSBELLE - SUAVIDAD MANZANA - 1000 - Blowmax', '223344677 - Shampoos - PLUSBELLE - VITALIDAD RENOVADORA - 1000 - Blowmax']

Ejemplo 2 de output esperado: 
[['112233445 - Shampoos - PLUSBELLE - ANTIOXIDANTE - 1000 - Casa Segal'], ['223344556 - Shampoos - PLUSBELLE - BALANCE - 1000 - Casa Segal', '334455667 - Shampoos - PLUSBELLE - BALANCE REPARADOR - 1000 - Blowmax'], ['445566778 - Shampoos - PLUSBELLE - BRILLO - 1000 - Blowmax', '556677889 - Shampoos - PLUSBELLE - BRILLO - 1000 - Casa Segal', '667788990 - Shampoos - PLUSBELLE - BRILLO LUMINOSIDAD - 1000 - Modo Market'], ['778899001 - Shampoos - PLUSBELLE - CUIDADO SUAVIDAD - 1000 - Modo Market'], ['889900112 - Shampoos - PLUSBELLE - ESENCIA CONTROL FRIZZ - 1000 - Modo Market'], ['990011223 - Shampoos - PLUSBELLE - FRESCURA - 1000 - Modo Market', '001122334 - Shampoos - PLUSBELLE - FRESCURA - 1000 - Casa Segal', '112233556 - Shampoos - PLUSBELLE - FRESCURA VITALIDAD - 1000 - Blowmax'], ['223344667 - Shampoos - PLUSBELLE - FUERZA ANTIOXID - 1000 - Atomo', '334455778 - Shampoos - PLUSBELLE - FUERZA ANTIOXIDANTE - 1000 - Modo Market'], ['445566889 - Shampoos - PLUSBELLE - HIDRATACION - 1000 - Blowmax'], ['667788011 - Shampoos - PLUSBELLE - NUTRICION CR OLEO MACADA - 1000 - Blowmax', '778899122 - Shampoos - PLUSBELLE - NUTRICION CREME - 1000 - Modo Market', '556677900 - Shampoos - PLUSBELLE - NUTRICION - 1000 - Casa Segal'], ['889900233 - Shampoos - PLUSBELLE - PROTECCION - 1000 - Modo Market'], ['990011344 - Shampoos - PLUSBELLE - REACTIVACION HIDRATANTE - 1000 - Blowmax'], ['001122455 - Shampoos - PLUSBELLE - SUAVIDAD - 1000 - Casa Segal', '112233566 - Shampoos - PLUSBELLE - SUAVIDAD MANZANA - 1000 - Blowmax'], ['223344677 - Shampoos - PLUSBELLE - VITALIDAD RENOVADORA - 1000 - Blowmax']]
    
- El output debe ser una lista de listas, donde cada sublista representa un grupo de productos equivalentes.
- La salida debe estar en una única línea, sin saltos de línea (\n), sin tabulaciones (\t), ni ningún tipo de formato multilineal.
- La salida debe poder escribirse directamente en un archivo `.txt`.
- **No agregues ningún tipo de texto adicional**. Solo devuélveme la lista de listas, sin explicaciones, sin código ni instrucciones.

Devuélveme únicamente la lista de listas, sin ningún texto adicional.
"""

    def _load_instruction(self, filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()

    def _set_client(self):
        key = self.api_keys[self.index]
        self.client = genai.Client(api_key=key)

    def _rotate_key(self):
        self.index = (self.index + 1) % len(self.api_keys)
        self._set_client()

    def ask(self, prompt: str):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.instruction
                ),
            )
            return ast.literal_eval(response.text)
        except Exception as e:
            print(f"Error con API key {self.api_keys[self.index]}: {e}")
            self._rotate_key()
            return self.ask(prompt)
        

