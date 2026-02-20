import datetime

# 1. Datos de prueba (Más adelante, esto vendrá de una API como OpenAI)
fecha_de_hoy = datetime.date.today().strftime("%d de %B de %Y")
nuevo_titulo = f"La historia automatizada del {fecha_de_hoy}"
nueva_historia = "Había una vez un pequeño script de Python que vivía en la nube. Su único propósito en la vida era despertarse una vez al día, buscar etiquetas en un archivo HTML y transformarlas en hermosas historias para que el mundo las leyera. Y lo hacía a la perfección."

# 2. Leer tu plantilla HTML
with open('index.html', 'r', encoding='utf-8') as archivo:
    contenido_html = archivo.read()

# 3. Realizar el reemplazo de los patrones
contenido_html = contenido_html.replace('{{TITULO}}', nuevo_titulo)
contenido_html = contenido_html.replace('{{HISTORIA}}', nueva_historia)
# (La imagen la dejaremos estática por ahora hasta conectar una API de imágenes)

# 4. Sobrescribir el archivo HTML con los nuevos datos
with open('index.html', 'w', encoding='utf-8') as archivo:
    archivo.write(contenido_html)

print("¡El script se ejecutó y la página fue actualizada con éxito!")
