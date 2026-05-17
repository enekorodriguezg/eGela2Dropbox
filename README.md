# 🚀 eGela2Dropbox

## 📖 Descripción del Proyecto
**eGela2Dropbox** es una aplicación de escritorio desarrollada en Python que permite a los estudiantes de la asignatura "Sistemas Web" automatizar la transferencia de material de estudio. La herramienta se conecta al aula virtual (eGela/Moodle), extrae selectivamente los documentos PDF disponibles y los sube de manera directa a una cuenta de Dropbox del usuario, gestionando la autenticación mediante un flujo completo de OAuth 2.0.

## 👥 Autores y Contexto
Este proyecto ha sido desarrollado como práctica académica para la asignatura **Sistemas Web** por:
- Eneko Rodríguez
- Urko Horas
- Aimar Larriba

## ⚙️ Arquitectura y Tecnologías
- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter (Compatible con Windows y Linux/X11 gracias a Pillow).
- **Extracción de Datos (Web Scraping):** BeautifulSoup4 y Requests.
- **Integración Cloud:** API de Dropbox (HTTP/REST), OAuth 2.0 con captura de token por socket local.
- **Gestión de Entorno:** python-dotenv para el manejo seguro de credenciales.

## 📋 Requisitos Previos
1. Python 3.x instalado en el sistema.
2. Cuenta de desarrollador en [Dropbox App Console](https://www.dropbox.com/developers/apps).
3. Una aplicación de Dropbox creada con permisos (Scopes) configurados para lectura/escritura de archivos (`files.content.read`, `files.content.write`) e información de cuenta (`account_info.read`).

## 🛠️ Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/enekorodriguezg/eGela2Dropbox.git](https://github.com/enekorodriguezg/eGela2Dropbox.git)
   cd eGela2Dropbox
   ```

2. **Instalar dependencias:**
   Se recomienda utilizar un entorno virtual (venv) para evitar conflictos a nivel de sistema operativo.
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   - Localiza el archivo `.env.example` en la raíz del proyecto.
   - Crea una copia exacta de este archivo y renómbrala a `.env`.
   - Rellena las credenciales proporcionadas por tu consola de Dropbox:
   ```env
   APP_KEY=tu_app_key_aqui
   APP_SECRET=tu_app_secret_aqui
   ```
   *Nota de seguridad: El archivo `.env` está incluido en el `.gitignore` por defecto. Nunca lo subas al repositorio.*

4. **Configuración de Redirección (OAuth):**
   Asegúrate de que en la configuración de tu aplicación en la consola de Dropbox, dentro del apartado *OAuth 2 Redirect URIs*, esté añadida exactamente esta URL local para que el socket intercepte la respuesta: `http://localhost:8070`

## 💻 Uso de la Aplicación

Para iniciar la interfaz gráfica y comenzar el flujo, ejecuta el archivo principal:
   ```bash
   python actividad_4.py
   ```

### 🔄 Flujo de Operación:
1. **Autenticación eGela:** Introduce tus credenciales universitarias. El sistema interceptará las cookies de sesión y extraerá dinámicamente los PDFs de la asignatura actual.
2. **Autenticación Dropbox:** Se abrirá una pestaña en tu navegador web. Concede los permisos a la aplicación. Un servidor local (puerto 8070) capturará el `access_token` de forma limpia y cerrará el ciclo.
3. **Transferencia:** Selecciona uno o varios archivos deseados en la lista de eGela (izquierda) y utiliza los controles centrales para subirlos a tu ruta actual en Dropbox (derecha).

## ✨ Funcionalidades Avanzadas de la API
Además del núcleo básico de transferencia, la aplicación integra las siguientes llamadas a la API de Dropbox para ofrecer una gestión completa desde la interfaz:
- **Consulta de Perfil:** Obtención dinámica del nombre y correo del usuario autenticado (`/users/get_current_account`).
- **Gestión de Directorios:** Creación de nuevas carpetas (`/files/create_folder_v2`) y navegación jerárquica.
- **Compartición de Archivos:** Generación de enlaces públicos de descarga listos para el portapapeles (`/sharing/create_shared_link_with_settings`).
- **Manipulación de Ficheros:** Renombrado y movimiento de archivos en la nube (`/files/move_v2`) y borrado permanente (`/files/delete_v2`).

## 📄 Licencia
Este proyecto se distribuye bajo la **Licencia MIT**.

El software se proporciona "tal cual", sin garantía de ningún tipo, expresa o implícita. En ningún caso los autores o titulares de los derechos de autor serán responsables de ninguna reclamación, daños u otras responsabilidades. Consulta el archivo `LICENSE` adjunto en este repositorio para conocer los términos completos.
