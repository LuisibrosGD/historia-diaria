import os
import requests
import json
import re

# 1. Sacamos la API Key de la caja fuerte (las variables de entorno)
api_key = os.environ.get("OPENROUTER_API_KEY")

# 2. Diseñamos el prompt forzando una estructura estricta
prompt = """
Escribe una historia corta de ciencia ficción o fantasía.
Debes devolver tu respuesta EXACTAMENTE en este formato, sin texto adicional:
<TITULO>Aquí va el título</TITULO>
<HISTORIA>Aquí va la historia en unos dos o tres párrafos.</HISTORIA>
<IMAGEN>una_sola_palabra_clave_en_ingles_para_describir_la_historia</IMAGEN>
"""

# 3. Hacemos la llamada a la API de OpenRouter
try:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "stepfun/step-3.5-flash:free",
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    
    # Extraemos el texto de la respuesta
    respuesta_ia = response.json()['choices'][0]['message']['content']
except Exception as e:
    print(f"Error al conectar con la API: {e}")
    respuesta_ia = "<TITULO>Error</TITULO><HISTORIA>Fallo en la Matrix.</HISTORIA><IMAGEN>error</IMAGEN>"

# 4. Usamos Expresiones Regulares para extraer los datos
# (.*?) captura todo lo que esté entre las etiquetas. re.DOTALL permite que incluya saltos de línea.
titulo_match = re.search(r'<TITULO>(.*?)</TITULO>', respuesta_ia, re.DOTALL)
historia_match = re.search(r'<HISTORIA>(.*?)</HISTORIA>', respuesta_ia, re.DOTALL)
imagen_match = re.search(r'<IMAGEN>(.*?)</IMAGEN>', respuesta_ia, re.DOTALL)

nuevo_titulo = titulo_match.group(1).strip() if titulo_match else "Historia sin título"
nueva_historia = historia_match.group(1).strip() if historia_match else "La historia no pudo ser generada."
palabra_imagen = imagen_match.group(1).strip() if imagen_match else "robot"

# 5. Generamos la URL de la imagen (Pollinations genera la imagen basándose en la palabra final)
url_imagen = f"https://image.pollinations.ai/prompt/{palabra_imagen}?width=600&height=350&nologo=true"

# 6. Leemos la plantilla intacta
with open('plantilla.html', 'r', encoding='utf-8') as archivo:
    contenido_html = archivo.read()

# 7. Hacemos los reemplazos
contenido_html = contenido_html.replace('{{TITULO}}', nuevo_titulo)
contenido_html = contenido_html.replace('{{HISTORIA}}', nueva_historia)
contenido_html = contenido_html.replace('{{IMAGEN_URL}}', url_imagen)

# 8. Guardamos el resultado final en el index.html (que es el que se publica)
with open('index.html', 'w', encoding='utf-8') as archivo:
    archivo.write(contenido_html)

print("Página generada con éxito usando IA y Regex.")
