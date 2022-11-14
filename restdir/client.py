"""
    Interfaces para el acceso al servicio de directorio
"""
import requests
from restdir.auth import AuthService
HEADERS = {"content-type": "application/json"}
ADMIN_HEADER = {"admin-token": ""}
USER_HEADER = {"user-token": ""}
ROOT_ID = "root"


class DirectoryException(Exception):
    """Error caused by wrong responses from server"""

    def __init__(self, message="unknown"):
        self.msg = message

    def __str__(self):
        return f"DirectoryException: {self.msg}"


class DirectoryService:
    """Cliente de acceso al servicio de directorio"""

    def __init__(self, uri_dir, uri_auth):
        self.uri_dir = uri_dir
        self.uri_auth = uri_auth

    def get_root(self, user):
        """Obtiene el directorio raiz"""

        AuthServer=AuthService(self.uri_auth)
        try:
            if AuthServer.administrator_login(user):
                ADMIN_HEADER['admin-token'] = user
                return Directory(self.uri_dir, ADMIN_HEADER, ROOT_ID)
        except Exception:
            USER_HEADER["user-token"] = user
            return Directory(self.uri_dir, USER_HEADER, ROOT_ID)


class Directory:
    """Cliente de acceso a un directorio"""

    def __init__(self, uri, header, dir_id, timeout=120):
        """uri should be the root of the API,
        example: http://127.0.0.1:5000/
        """
        self.root = uri
        if not self.root.endswith("/"):
            self.root = f"{self.root}/"
        self.timeout = timeout

        self.id_dir = dir_id
        self.header = header
        self.childs = ""
        self.id_parent = ""

        print(self.self_info())

    def self_info(self):
        dir_id = self.id_dir
        result = requests.get(
            f"{self.root}v1/directory/{dir_id}",
            headers=self.header,
            timeout=self.timeout,
        )

        if result.status_code == 401:
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 200:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")

        info = result.content.decode("utf-8")

        return info

    def list_directories(self, nombre_hijo):
        """Obtiene una lista de todos los subdirectorios del directorio"""
        dir_id = self.id_parent

        result = requests.get(
            f"{self.root}v1/directory/{dir_id}/{nombre_hijo}",
            headers=self.header,
            timeout=self.timeout,
        )

        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 200:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
        return result.content.decode("utf-8")

    def new_directory(self, directory_name):
        """Crea un nuevo subdirectorio en el directorio"""
        dir_id = self.id_dir
        nombre_hijo = directory_name
        result = requests.put(
            f"{self.root}v1/directory/{dir_id}/{nombre_hijo}",
            headers=self.header,
            timeout=self.timeout,
        )

        if (
            result.status_code == 401
            or result.status_code == 404
            or result.status_code == 409
        ):
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 200:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
        return result.content.decode("utf-8")

    def remove_directory(self, directory_name):
        """Elimina un subdirectorio del directorio"""
        result = requests.delete(
            f"{self.root}v1/directory/{self.id_dir}/{directory_name}",
            headers=self.header,
            timeout=self.timeout,
        )

        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 204:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
        return result.content.decode("utf-8")

    def list_files(self):
        """Obtiene una lista de ficheros del directorio"""
        dir_id = self.id_dir
        result = requests.get(
            f"{self.root}v1/files/{dir_id}",
            headers=self.header,
            timeout=self.timeout
        )

        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 200:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
        return result.content.decode("utf-8")

    def new_file(self, filename, file_url):
        """Crea un nuevo fichero a partir de un blob"""
        result = requests.put(
            f"{self.root}v1/files/{self.id_dir}/{filename}",
            data=file_url,
            headers=self.header,
            timeout=self.timeout,
        )

        if (
            result.status_code == 401
            or result.status_code == 404
            or result.status_code == 400
        ):
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 200:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
        return result.content.decode("utf-8")

    def remove_file(self, filename):
        """Elimina un fichero del directorio"""
        dir_id = self.id_dir
        result = requests.delete(
            f"{self.root}v1/files/{dir_id}/{filename}",
            headers=self.header,
            timeout=self.timeout,
        )

        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode("utf-8"))
        if result.status_code != 204:
            raise DirectoryException(f"Unexpected status code: {result.status_code}")
