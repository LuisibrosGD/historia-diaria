import os
import requests
import json
import re
from datetime import datetime

api_key = os.environ.get("OPENROUTER_API_KEY")

prompt = """
Escribe una historia corta de ciencia ficción o fantasía.
Debes devolver tu respuesta EXACTAMENTE en este formato:
<TITULO>Aquí va el título</TITULO>
<HISTORIA>Aquí va la historia en unos dos o tres párrafos.</HISTORIA>
<IMAGEN>una_sola_palabra_clave_en_ingles_para_describir_la_historia</IMAGEN>
"""

try:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps({"model": "stepfun/step-3.5-flash:free", "messages": [{"role": "user", "content": prompt}]})
    )
    respuesta_ia = response.json()['choices'][0]['message']['content']
except Exception as e:
    respuesta_ia = "<TITULO>Error</TITULO><HISTORIA>Fallo al conectar con la API.</HISTORIA><IMAGEN>error</IMAGEN>"

titulo_match = re.search(r'<TITULO>(.*?)</TITULO>', respuesta_ia, re.DOTALL)
historia_match = re.search(r'<HISTORIA>(.*?)</HISTORIA>', respuesta_ia, re.DOTALL)
imagen_match = re.search(r'<IMAGEN>(.*?)</IMAGEN>', respuesta_ia, re.DOTALL)

nuevo_titulo = titulo_match.group(1).strip() if titulo_match else "Historia sin título"
nueva_historia = historia_match.group(1).strip() if historia_match else "Error al generar la historia."
palabra_imagen = imagen_match.group(1).strip() if imagen_match else "robot"
palabra_imagen_segura = palabra_imagen.replace(' ', '%20')
url_imagen = f"https://image.pollinations.ai/prompt/{palabra_imagen_segura}?width=600&height=350&nologo=true"
# --- NUEVA LÓGICA DE HISTORIAL Y MEMORIA ---

# 1. Configurar fechas
fecha_hoy = datetime.now()
año = fecha_hoy.strftime("%Y")
mes_num = fecha_hoy.strftime("%m")
dia = fecha_hoy.strftime("%d")

meses_español = {"01":"Enero", "02":"Febrero", "03":"Marzo", "04":"Abril", "05":"Mayo", "06":"Junio", "07":"Julio", "08":"Agosto", "09":"Septiembre", "10":"Octubre", "11":"Noviembre", "12":"Diciembre"}
nombre_mes = meses_español[mes_num]

# El nombre del archivo único para la historia de hoy
nombre_archivo_hoy = f"historia-{año}-{mes_num}-{dia}.html"

# 2. Cargar la base de datos (historial.json)
if os.path.exists('historial.json'):
    with open('historial.json', 'r', encoding='utf-8') as f:
        historial = json.load(f)
else:
    historial = {}

# 3. Añadir la historia de hoy a la base de datos
llave_mes = f"{nombre_mes} {año}"
if llave_mes not in historial:
    historial[llave_mes] = []

# Evitar duplicados si ejecutas el script varias veces el mismo día
if not any(item['archivo'] == nombre_archivo_hoy for item in historial[llave_mes]):
    historial[llave_mes].insert(0, {"titulo": nuevo_titulo, "archivo": nombre_archivo_hoy})

# 4. Guardar la base de datos actualizada
with open('historial.json', 'w', encoding='utf-8') as f:
    json.dump(historial, f, ensure_ascii=False, indent=4)

# 5. Generar el código HTML para el Menú Lateral
menu_html = ""
for mes, historias in historial.items():
    menu_html += f'<h3 class="mes-titulo">{mes}</h3>'
    menu_html += '<ul class="lista-historias">'
    for item in historias:
        menu_html += f'<li><a href="{item["archivo"]}">{item["titulo"]}</a></li>'
    menu_html += '</ul>'

# --- FIN NUEVA LÓGICA ---

# Leer la plantilla
with open('plantilla.html', 'r', encoding='utf-8') as archivo:
    contenido_html = archivo.read()

# Reemplazar todas las variables, incluyendo el nuevo {{MENU}}
contenido_html = contenido_html.replace('{{TITULO}}', nuevo_titulo)
contenido_html = contenido_html.replace('{{HISTORIA}}', nueva_historia)
contenido_html = contenido_html.replace('{{IMAGEN_URL}}', url_imagen)
contenido_html = contenido_html.replace('{{MENU}}', menu_html)

# Guardar como index.html (La página de inicio que siempre muestra lo más reciente)
with open('index.html', 'w', encoding='utf-8') as archivo:
    archivo.write(contenido_html)

# Guardar TAMBIÉN como un archivo individual (El archivo permanente de esta historia)
with open(nombre_archivo_hoy, 'w', encoding='utf-8') as archivo:
    archivo.write(contenido_html)

print("¡Página generada y guardada en el historial con éxito!")
