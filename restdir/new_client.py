'''
    Interfaces para el acceso al servicio de directorio
'''
import requests
import json

HEADERS = {"content-type": "application/json"}
token='1234'
ADMIN_HEADER = {"admin-token": "admin"}
USER_HEADER = {"user-token": ""}
URI = "http://127.0.0.1:5000"

class DirectoryException(Exception):
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'DirectoryException: {self.msg}'

class DirectoryService:
    '''Cliente de acceso al servicio de directorio'''

    def get_root(self, user):
        '''Obtiene el directorio raiz'''
        
        USER_HEADER['user-token'] = user
        return Directory(URI,user)



class Directory:
    '''Cliente de acceso a un directorio'''
    def __init__(self, uri, user, timeout=120):
        '''uri should be the root of the API,
            example: http://127.0.0.1:5000/
        '''
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.timeout = timeout

        root_info=self.getRoot()        
        
        self.id = root_info['dir_id']
        self.childs = root_info['childs']
        self.actual_user = user
        
    def getRoot(self):
        result = requests.get(
            f'{self.root}v1/directory/root',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)

        if result.status_code == 401:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
         
        rootInfo = json.loads(result.content.decode('utf-8'))
        return rootInfo
        

    def list_directories(self):
        '''Obtiene una lista de todos los subdirectorios del directorio''' 
        dir_id = self.id_parent
        nombre_hijo=self.name_dir

        result = requests.get(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')


    def new_directory(self, directory_name):
        '''Crea un nuevo subdirectorio en el directorio'''
        dir_id = self.id
        nombre_hijo = directory_name
        result = requests.put(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404 or result.status_code == 409:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def remove_directory(self, directory_name):
        '''Elimina un subdirectorio del directorio'''
        result = requests.delete(
            f'{self.root}v1/directory/{self.id}/{directory_name}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 204:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')
        

    def list_files(self):
        '''Obtiene una lista de ficheros del directorio'''
        dir_id = self.id
        result = requests.get(
            f'{self.root}v1/files/{dir_id}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')


    def new_file(self, filename, blob_id):
        '''Crea un nuevo fichero a partir de un blob'''
        result = requests.put(
            f'{self.root}v1/files/{self.id}/{filename}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404 or result.status_code == 400:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')  


    def remove_file(self, filename):
        '''Elimina un fichero del directorio'''
        dir_id = self.id
        result = requests.delete(
            f'{self.root}v1/files/{dir_id}/{filename}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 204:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')


    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        raise NotImplementedError()

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        raise NotImplementedError()

    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        raise NotImplementedError()

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        raise NotImplementedError()
