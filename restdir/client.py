#!/usr/bin/env python3

'''
    REST access library + client example
'''

import json

import requests


HEADERS = {"content-type": "application/json"}
token='1234'
ADMIN_HEADER = {"admin-token": "admin"}
USER_HEADER = {"user-token": "1234"}
URI = "http://127.0.0.1:5000"

class DirectoryException(Exception):
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'DirectoryException: {self.msg}'


class RestListClient:
    '''Library to access to the REST API of restlist'''
    def __init__(self, uri, timeout=120):
        '''uri should be the root of the API,
            example: http://127.0.0.1:5000/
        '''
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.timeout = timeout

    def root_info(self):

        result = requests.get(
            f'{self.root}v1/directory/root',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401:
            raise DirectoryException(result.content.decode('utf-8'))
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def get_dir_childs(self, dir_id, nombre_hijo): #esta esta mal
        result = requests.get(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')
    

    def new_dir(self, dir_id, nombre_hijo):
        '''Access to a item by its index'''
        result = requests.put(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404 or result.status_code == 409:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def remove_dir(self, dir_id, nombre_hijo):
        '''Access to a item by its index'''
        result = requests.delete(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 204:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def get_dir_files(self, dir_id):
        '''Send request to check if an element exists in the list'''
        result = requests.get(
            f'{self.root}v1/files/{dir_id}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def get_file_url(self, dir_id, filename):
        '''Send request to check if an element exists in the list'''
        result = requests.get(
            f'{self.root}v1/files/{dir_id}/{filename}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')   
    
    
    def add_file(self, dir_id,filename):
        '''Send request to remove an element from the list'''
        result = requests.put(
            f'{self.root}v1/files/{dir_id}/{filename}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404 or result.status_code == 400:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')  


    def remove_file(self,dir_id,filename):
        '''Query for number of occurrences of a given item'''
        result = requests.delete(
            f'{self.root}v1/files/{dir_id}/{filename}',
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise DirectoryException(result.content.decode('utf-8'))           
        if result.status_code != 204:
            raise DirectoryException(f'Unexpected status code: {result.status_code}')

    

if __name__=="__main__":
    r=RestListClient(URI)
    #print(r.get_dir_files(1))
    #print(r.new_dir("1","pollaza"))
    #print(r.get_file_url(1, "jose"))
    print(r.remove_file(str("fccc46b6-5482-11ed-81ed-018e3b9df965"),"gabenismo7"))
