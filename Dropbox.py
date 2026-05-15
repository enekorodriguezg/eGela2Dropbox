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
        # por el puerto 8090 esta escuchando el servidor que generamos
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # recibe la redireccio 302 del navegador
        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (peticion)

        # buscar en solicitud el "auth_code"
        primera_linea =peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        # devolver una respuesta al usuario
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
        # 1. Solicitar Autorización (Abrir el navegador)
        auth_url = "https://www.dropbox.com/oauth2/authorize"
        params_get = {
            "client_id": app_key,
            "response_type": "code",
            "redirect_uri": redirect_uri
        }
        
        # urllib.parse.urlencode convierte el diccionario en formato query string (?clave=valor)
        url_completa = auth_url + "?" + urllib.parse.urlencode(params_get)
        print("Abriendo navegador para autorización OAuth...")
        webbrowser.open(url_completa)

        # 2. Capturar el Código de Autorización (Tu servidor se queda escuchando aquí)
        auth_code = self.local_server()

        # 3. Intercambiar el Código por el Token Definitivo
        token_url = "https://api.dropboxapi.com/oauth2/token"
        datos_post = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": app_key,
            "client_secret": app_secret,
            "redirect_uri": redirect_uri
        }
        
        print("Intercambiando authorization code por access token...")
        # El POST requiere que enviemos los datos en el cuerpo de la petición (data)
        respuesta = requests.post(token_url, data=datos_post)
        
        if respuesta.status_code == 200:
            token_data = respuesta.json()
            # Actualizamos el atributo como exige el enunciado
            self._access_token = token_data.get("access_token")
            print("Access token obtenido con éxito.")
        else:
            print(f"Error al obtener el token: {respuesta.status_code} - {respuesta.text}")

        # Cerramos la ventana de login de Tkinter
        self._root.destroy()

        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)

    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

    def create_folder(self, path):
        print("/create_folder")
       # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
