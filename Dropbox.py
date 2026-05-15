import os
import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper
from dotenv import load_dotenv

load_dotenv()

app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
server_addr = "localhost"
server_port = 8070
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (peticion)

        primera_linea =peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response)
        client_connection.close()
        server_socket.close()

        return auth_code


    def do_oauth(self):
        auth_url = "https://www.dropbox.com/oauth2/authorize"
        params_get = {
            "client_id": app_key,
            "response_type": "code",
            "redirect_uri": redirect_uri
        }
        
        url_completa = auth_url + "?" + urllib.parse.urlencode(params_get)
        print("Abriendo navegador para autorización OAuth...")
        webbrowser.open(url_completa)

        auth_code = self.local_server()

        token_url = "https://api.dropboxapi.com/oauth2/token"
        datos_post = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": app_key,
            "client_secret": app_secret,
            "redirect_uri": redirect_uri
        }
        
        print("Intercambiando authorization code por access token...")
        respuesta = requests.post(token_url, data=datos_post)
        
        if respuesta.status_code == 200:
            token_data = respuesta.json()
            # Actualizamos el atributo como exige el enunciado
            self._access_token = token_data.get("access_token")
            print("Access token obtenido con éxito.")
        else:
            print(f"Error al obtener el token: {respuesta.status_code} - {respuesta.text}")

        self._root.destroy()


    def list_folder(self, msg_listbox):
        print("/list_folder")
        uri = 'https://api.dropboxapi.com/2/files/list_folder'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        ruta = "" if self._path == "/" else self._path

        data = {
            'path': ruta
        }

        respuesta = requests.post(uri, headers=headers, data=json.dumps(data))

        if respuesta.status_code == 200:
            contenido_json = respuesta.json()
        else:
            contenido_json = {}
            print(respuesta.text)

        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)


    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Dropbox-API-Arg': json.dumps({'path': file_path, 'mode': 'add', 'autorename': True}),
            'Content-Type': 'application/octet-stream'
        }

        respuesta = requests.post(uri, headers=headers, data=file_data)

        if respuesta.status_code == 200:
            print(respuesta.json())
        else:
            print(respuesta.text)


    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        data = {
            'path': file_path
        }

        respuesta = requests.post(uri, headers=headers, data=json.dumps(data))

        if respuesta.status_code == 200:
            print(respuesta.json())
        else:
            print(respuesta.text)


    def create_folder(self, path):
        print("/create_folder")
        uri = 'https://api.dropboxapi.com/2/files/create_folder_v2'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        data = {
            'autorename': False,
            'path': path
        }

        respuesta = requests.post(uri, headers=headers, data=json.dumps(data))

        if respuesta.status_code == 200:
            print(respuesta.json())
        else:
            print(respuesta.text)


    def get_current_account(self):
        print("/get_current_account")
        uri = 'https://api.dropboxapi.com/2/users/get_current_account'

        headers = {
            'Authorization': 'Bearer ' + self._access_token
        }

        respuesta = requests.post(uri, headers=headers)

        if respuesta.status_code == 200:
            info = respuesta.json()
            nombre = info.get('name', {}).get('display_name')
            email = info.get('email')
            # En lugar de hacer un print, ahora devolvemos los datos
            return nombre, email
        else:
            print(respuesta.text)
            return None, None

    def share_file(self, file_path):
        print("/share_file")
        uri = 'https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        # Le decimos a Dropbox qué archivo queremos compartir
        data = {
            'path': file_path,
            'settings': {
                'requested_visibility': 'public'
            }
        }

        respuesta = requests.post(uri, headers=headers, data=json.dumps(data))

        if respuesta.status_code == 200:
            # Si todo va bien, sacamos la URL del JSON de respuesta
            enlace = respuesta.json().get('url')
            return enlace
        else:
            # Si da error (por ejemplo, si el archivo ya estaba compartido de antes)
            print("Error o el archivo ya tiene un enlace compartido:")
            print(respuesta.text)
            return None

    def move_file(self, from_path, to_path):
        print("/move_file")
        uri = 'https://api.dropboxapi.com/2/files/move_v2'

        headers = {
            'Authorization': 'Bearer ' + self._access_token,
            'Content-Type': 'application/json'
        }

        # autorename=False porque queremos el nombre exacto que escriba el usuario
        data = {
            'from_path': from_path,
            'to_path': to_path,
            'autorename': False
        }

        respuesta = requests.post(uri, headers=headers, data=json.dumps(data))

        if respuesta.status_code == 200:
            print("Archivo renombrado/movido con éxito")
            return True
        else:
            print("Error al renombrar el archivo:")
            print(respuesta.text)
            return False