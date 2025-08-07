import os
import pickle
from typing import Optional
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

credential_path = os.path.join(os.getcwd(), 'assest', "credentials.json")
token_path = os.path.join(os.getcwd(), 'assest', "token.pickle")

# Escopos definem o que sua aplicação pode fazer (ler fotos/vídeos)
_SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary.readonly',
]

def get_photos_service():
    """Autentica e cria o serviço da API do Google Photos."""
    creds = None
    # O arquivo token.pickle armazena os tokens de acesso e atualização do usuário.
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Se não houver credenciais válidas, permite que o usuário faça login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_path, _SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a próxima execução
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    return service


def credentials(scopes: list):
    """
    Obtains and returns Google Sheets API credentials. If valid credentials
    """
    creds: Optional[Credentials] = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if creds and creds.valid and not creds.expired:
        return creds
    elif creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if os.path.exists(credential_path):
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_path, scopes
            )
            credsAuth = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, "w", encoding="utf-8") as token:
                token.write(credsAuth.to_json())
            return credsAuth
        else:
            raise FileNotFoundError("credentials.json not found.")


def authenticate(scopes: list):
    """Autentica o usuário e retorna o serviço da API."""    
    service = get_photos_service()
    return service


def list_videos(service):
    """Lista os vídeos na biblioteca."""
    try:
        # Você pode adicionar filtros para buscar por data, etc.
        results = service.mediaItems().list(pageSize=10).execute()
        return results.get('mediaItems', [])
    except HttpError as e:
        print(f"Erro ao listar vídeos: {e}")
        raise e
    except Exception as e:
        print(f"Erro generico de \n{e}")
        raise e


def main_budo_backup():
    """Função principal para autenticar e listar vídeos."""
    service = authenticate(_SCOPES)
    videos = list_videos(service)
    for video in videos:
        print(f"Vídeo encontrado: {video['filename']}, ID: {video['id']}")
        # Para baixar, você usaria o video['baseUrl']
