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

class RestListError(Exception):
    '''Error caused by wrong responses from server'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'RestListError: {self.msg}'


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
            raise RestListError(result.content.decode('utf-8'))
        if result.status_code != 200:
            raise RestListError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def get_dir_childs(self, dir_id, nombre_hijo):
        result = requests.get(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise RestListError(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise RestListError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')
    

    def new_dir(self, dir_id, nombre_hijo):
        '''Access to a item by its index'''
        result = requests.put(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise RestListError(result.content.decode('utf-8'))           
        if result.status_code != 200:
            raise RestListError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def remove_dir(self, dir_id, nombre_hijo):
        '''Access to a item by its index'''
        result = requests.delete(
            f'{self.root}v1/directory/{dir_id}/{nombre_hijo}',  
            headers=ADMIN_HEADER,
            timeout=self.timeout)
        
        if result.status_code == 401 or result.status_code == 404:
            raise RestListError(result.content.decode('utf-8'))           
        if result.status_code != 204:
            raise RestListError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    def exists(self, element):
        '''Send request to check if an element exists in the list'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element}
        result = requests.post(
            f'{self.root}v1/elements/exists',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        return result.status_code == 204


    def remove(self, element, all_occurrences=False):
        '''Send request to remove an element from the list'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element, "remove_all": all_occurrences}
        result = requests.delete(
            f'{self.root}v1/elements',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code == 404:
            raise ValueError(f'Element "{element}" not in the list')
        return result.status_code == 204

    def count(self, element):
        '''Query for number of occurrences of a given item'''
        if not isinstance(element, str):
            raise ValueError("element is not a string value")
        req_body = {"element": element}
        result = requests.post(
            f'{self.root}v1/elements/count',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        response = result.content.decode('utf-8')
        try:
            return int(response)
        except ValueError as error:
            raise RestListError(f'Unknown response from server: {response}') from error

    def len(self):
        '''Send a request to get the number of elements in the list'''
        result = requests.get(
            f'{self.root}v1/elements/count',
            headers=HEADERS,
            timeout=self.timeout
        )
        response = result.content.decode('utf-8')
        try:
            return int(response)
        except ValueError as error:
            raise RestListError(f'Unknown response from server: {response}') from error

    def __len__(self):
        return self.len()

if __name__=="__main__":
    r=RestListClient(URI)
    print(r.remove_dir("1", "pollaza"))
   # print(r.new_dir("1","pollaza"))
