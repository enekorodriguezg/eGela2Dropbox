# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
import time
import helper
import re


class eGela:
    _login = 0
    _cookie = ""
    _curso = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. PETICION #####")
        metodo = 'GET'
        uri = "https://egela.ehu.eus/login/index.php"

        if hasattr(username, 'get'):
            username = username.get()
        if hasattr(password, 'get'):
            password = password.get()

        print(f"{metodo} {uri}")

        respuesta1 = requests.get(uri, allow_redirects=False)

        print(f"{respuesta1.status_code} {respuesta1.reason}")
        if 'Set-Cookie' in respuesta1.headers:
            print(f"Set-Cookie: {respuesta1.headers['Set-Cookie']}")
            match = re.search(r'(MoodleSessionegela=[^;]+)', respuesta1.headers['Set-Cookie'])
            if match:
                self._cookie = match.group(1)
        if 'Location' in respuesta1.headers:
            print(f"Location: {respuesta1.headers['Location']}")

        html1 = BeautifulSoup(respuesta1.content, 'html.parser')
        logintoken = html1.find('input', {'name': 'logintoken'})['value']

        progress = 25
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 2. PETICION #####")
        metodo = 'POST'
        datos = {'username': username, 'password': password, 'logintoken': logintoken}
        datos_form = urllib.parse.urlencode(datos)
        cabeceras = {'Cookie': self._cookie, 'Content-Type': 'application/x-www-form-urlencoded'}

        print(f"{metodo} {uri}")
        print(datos_form)

        respuesta2 = requests.post(uri, data=datos_form, headers=cabeceras, allow_redirects=False)

        print(f"{respuesta2.status_code} {respuesta2.reason}")
        if 'Set-Cookie' in respuesta2.headers:
            print(f"Set-Cookie: {respuesta2.headers['Set-Cookie']}")
            match = re.search(r'(MoodleSessionegela=[^;]+)', respuesta2.headers['Set-Cookie'])
            if match:
                self._cookie = match.group(1)
        if 'Location' in respuesta2.headers:
            print(f"Location: {respuesta2.headers['Location']}")

        uri3 = respuesta2.headers.get('Location', uri)

        progress = 50
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 3. PETICION #####")
        metodo = 'GET'
        cabeceras = {'Cookie': self._cookie}

        print(f"{metodo} {uri3}")

        respuesta3 = requests.get(uri3, headers=cabeceras, allow_redirects=False)

        print(f"{respuesta3.status_code} {respuesta3.reason}")
        if 'Set-Cookie' in respuesta3.headers:
            print(f"Set-Cookie: {respuesta3.headers['Set-Cookie']}")
            match = re.search(r'(MoodleSessionegela=[^;]+)', respuesta3.headers['Set-Cookie'])
            if match:
                self._cookie = match.group(1)
        if 'Location' in respuesta3.headers:
            print(f"Location: {respuesta3.headers['Location']}")

        uri4 = respuesta3.headers.get('Location', uri3)

        progress = 75
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 4. PETICION #####")
        metodo = 'GET'

        print(f"{metodo} {uri4}")

        respuesta4 = requests.get(uri4, headers=cabeceras, allow_redirects=False)

        print(f"{respuesta4.status_code} {respuesta4.reason}")
        if 'Set-Cookie' in respuesta4.headers:
            print(f"Set-Cookie: {respuesta4.headers['Set-Cookie']}")
            match = re.search(r'(MoodleSessionegela=[^;]+)', respuesta4.headers['Set-Cookie'])
            if match:
                self._cookie = match.group(1)
        if 'Location' in respuesta4.headers:
            print(f"Location: {respuesta4.headers['Location']}")

        html4 = BeautifulSoup(respuesta4.content, 'html.parser')

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)
        popup.destroy()

        COMPROBACION_DE_LOG_IN = html4.find('a', href=lambda href: href and 'logout.php' in href) is not None

        if COMPROBACION_DE_LOG_IN:
            self._login = 1
            self._curso = "https://egela.ehu.eus/course/view.php?id=109324"
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")


    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de la asignatura en eGela) #####")
        cabeceras = {'Cookie': self._cookie}
        respuesta5 = requests.get(self._curso, headers=cabeceras, allow_redirects=False)
        html5 = BeautifulSoup(respuesta5.content, 'html.parser')

        print("\n##### Analisis del HTML... #####")
        enlaces = html5.find_all('a', {'class': 'aalink'})
        NUMERO_DE_PDF_EN_EGELA = []

        for enlace in enlaces:
            img = enlace.find('img')
            if img and 'pdf' in img.get('src', ''):
                span_name = enlace.find('span', {'class': 'instancename'})
                if span_name:
                    nombre = span_name.text.replace(' Archivo', '').strip() + '.pdf'
                    link = enlace.get('href')
                    NUMERO_DE_PDF_EN_EGELA.append({'pdf_name': nombre, 'pdf_link': link})

        if len(NUMERO_DE_PDF_EN_EGELA) > 0:
            progress_step = float(100.0 / len(NUMERO_DE_PDF_EN_EGELA))

            for pdf in NUMERO_DE_PDF_EN_EGELA:
                self._refs.append(pdf)
                progress += progress_step
                progress_var.set(progress)
                progress_bar.update()
                time.sleep(0.1)

        popup.destroy()
        return self._refs


    def get_pdf(self, selection):
        print("\t##### descargando  PDF... #####")

        pdf_name = self._refs[selection]['pdf_name']
        pdf_link = self._refs[selection]['pdf_link']

        cabeceras = {'Cookie': self._cookie}
        respuesta = requests.get(pdf_link, headers=cabeceras, allow_redirects=True)
        pdf_content = respuesta.content

        return pdf_name, pdf_content