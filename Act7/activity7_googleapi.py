import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Permisos requeridos para leer mensajes y adjuntos
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
# Obtener el servicio de la API de Gmail con autenticación a partir de las credenciales almacenadas o mediante el proceso de autenticación OAuth2
# Referencias: https://developers.google.com/workspace/gmail/api/quickstart/python?hl=es-419
    creds = None
    # El archivo token.json almacena los tokens de acceso del usuario
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    #Al ejecturarse el script por primera vez, se solicitará al usuario que inicie sesión y autorice el acceso a su cuenta de Gmail. Luego, las credenciales se guardarán en token.json para futuros usos.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def download_attachments(extension, after_date, before_date):
    service = get_service()

    # Consulta de búsqueda: extensión y rango de fechas
    query = f"has:attachment filename:{extension} after:{after_date} before:{before_date}"
    
    #Extraer los mensajes que cumplen con los criterios de búsqueda
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No se encontraron mensajes con esos criterios.")
        return

    for msg in messages:
        # Iterar sobre los mensajes encontrados y descargar los adjuntos que coincidan con la extensión especificada

        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = message.get('payload')
        
        for part in payload.get('parts', []):
            if part.get('filename') and part['filename'].lower().endswith(extension.lower()):
                attachment_id = part['body'].get('attachmentId')
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=msg['id'], id=attachment_id
                ).execute()
                
                data = attachment.get('data')
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                
                path = part['filename']
                with open(path, 'wb') as f:
                    f.write(file_data)
                print(f"Descargado: {path}")


download_attachments('.xml', '2025/01/01', '2025/12/31')