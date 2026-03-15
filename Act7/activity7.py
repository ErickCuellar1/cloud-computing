import os
import json
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# Clave generada en el portal de Azure

print("Clave de suscripción guardada")
# URL de la aplicación que queremos correr


print("URL del servicio guardada")
# URL de una imágen a utilizar
image_url = 'https://github.com/gilecheverria/MNA_data/blob/main/Images/amusement_park.png?raw=true'
print("URL de la imagen guardada")



image_url = 'https://datagef.blob.core.windows.net/contenedorgilbertoecheverria/amusement_park.png?raw=true'
print("URL de la imagen actualizada")
# Configuración de la clave a utilizar
headers = {'Ocp-Apim-Subscription-Key': subscription_key}

print("Encabezados de la solicitud configurados")
# Parámtros para la solicitud al servicio
params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'true',
    # 'returnFaceAttributes': 'age, gender headPose, smile, facialHair, glasses, emotion',
}

print("Parámetros de la solicitud configurados")
# Llamada al servicio
response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
# Almacenar el resultado en formato JSON
faces = response.json()
print("Respuesta del servicio recibida y convertida a JSON")
# Mostrar el resultado como texto
print(json.dumps(faces))


# Descargar los datos de la imagen
img_data = requests.get(image_url)
# Crear un objeto para poder dibujar la foto
img = Image.open(BytesIO(img_data.content))

# Nuevo objeto para poder dibujar figuras sobre la foto
draw = ImageDraw.Draw(img)

# Mostrar un rectángulo alrededor de las caras detectadas
for face in faces:
  rect = face['faceRectangle']
  left = rect['left']
  top = rect['top']
  right = left + rect['width']
  bottom = top + rect['height']

  draw.rectangle([left, top, right, bottom], outline='red', width=3)

# Formateo de la imagen resultante
plt.figure(figsize=(14, 10))
plt.imshow(img)
plt.axis('off')
plt.title(f"{len(faces)} face(s) detected")
plt.show()

