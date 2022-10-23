#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''

from xml.dom import NotFoundErr
from flask import Flask, make_response, request
import json
import directory
PERMISSION_ERR = 0
DIR_NOTFOUND_ERR = 1 
ALREADYEXISTS_ERR = 2
DOESNOTEXIST_ERR = 3

app = Flask("restdir")
DIR = directory.Directory()


@app.route('/v1/directory/root', methods=['GET'])
def root_info():
    '''Añadir elemento a lista'''
    id = DIR._get_UUID_dir(0, "/")
    
    headers=request.headers
    if "admin-token" not in headers and "user-token" not in headers:
        return make_response(f'Bad headers', 401)
        
    if "admin-token" not in headers:
        token = headers["user-token"]
        has_permission = DIR._checkUser_Readable(id, token)
        if not has_permission:
            return make_response(f'User {token} has no readable permission', 401)  

    childs = DIR._get_dirChilds(id)
    childs_list = json.loads(childs)
    
    names_childs = list()
    
    for child in childs_list:  
        names_childs.append(DIR._get_Name_dir(child))
    
    response = {"dir_id": id, "childs":names_childs}

    return make_response(json.dumps(response), 200)


@app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['GET'])
def dir_childs(dir_id, nombre_hijo):
    '''Añadir elemento a lista'''
        
    headers=request.headers
    if "admin-token" not in headers and "user-token" not in headers:
        return make_response(f'Bad headers', 401)

    id = DIR._get_UUID_dir(dir_id, nombre_hijo)

    if not DIR._checkDirectory(dir_id):
        return make_response(f'Directory {dir_id} does not exist', 404)
    elif not id:
        return make_response(f'Directory {dir_id} does not have {nombre_hijo} as child', 404)

    if "admin-token" not in headers:
        token = headers["user-token"]
        has_permission = DIR._checkUser_Readable(id, token)
        if not has_permission:
            return make_response(f'User {token} has no readable permission', 401)  

    childs = DIR._get_dirChilds(id)
    childs_list = json.loads(childs)

    response = {"childs_ids":childs_list}

    return make_response(json.dumps(response), 200)


@app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['PUT'])
def new_dir(dir_id,nombre_hijo):
    '''Borrar un elemento o la lista entera'''
             
    headers=request.headers
    if "admin-token" not in headers and "user-token" not in headers:
        return make_response(f'Bad headers', 401)

    if "admin-token" not in headers:
        token = headers["user-token"]
    else:
        token = headers["admin-token"]
    
    try:
        DIR.new_dir(dir_id, nombre_hijo, token)
        id = DIR._get_UUID_dir(dir_id, nombre_hijo)
        response = {"dir_id": id}
    except directory.DirectoyException as err:
        if err.code == PERMISSION_ERR: 
            return make_response(f'User {token} has no writable permission', 401)
        if err.code == DIR_NOTFOUND_ERR:
            return make_response(f'Directory {dir_id} does not exist', 404)
        if err.code ==ALREADYEXISTS_ERR:
            return make_response(f'Directory {dir_id} already has {nombre_hijo} as child', 404)

    return make_response(json.dumps(response), 200)


@app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['DELETE'])
def remove_dir(dir_id, nombre_hijo):
    '''Obtener el elemento numero "index"'''
         
    headers=request.headers
    if "admin-token" not in headers and "user-token" not in headers:
        return make_response(f'Bad headers', 401)
        
    if "admin-token" not in headers:
        token = headers["user-token"]
    else:
        token = headers["admin-token"]
    
    try:
        DIR.remove_dir(dir_id, nombre_hijo, token)
        response = ""

    except directory.DirectoyException as err:
        if err.code == PERMISSION_ERR: 
            return make_response(f'User {token} has no writable permission', 401)
        if err.code == DIR_NOTFOUND_ERR:
            return make_response(f'Directory {dir_id} does not exist', 404)
        if err.code == DOESNOTEXIST_ERR:
            return make_response(f'Directory {dir_id} doesnt have {nombre_hijo} as child', 404)

    return make_response(response, 204)

# @app.route('/v1/elements/exists', methods=['POST'])
# def element_exist():
#     '''Devuelve si un elemento existe en la lista o no'''
#     if not request.is_json:
#         return make_response('Missing JSON', 400)
#     if 'element' not in request.get_json():
#         return make_response('Missing "element" key', 400)
#     if LIST.exists(request.get_json()['element']):
#         return make_response("", 204)
#     return make_response("Element not found", 404)

# @app.route('/v1/elements/count', methods=['GET', 'POST'])
# def element_count():
#     '''Devuelve la ocurrencias de un elemento en la lista o el tamaño de la lista'''
#     if request.method == 'GET':
#         return make_response(f"{LIST.len()}", 200)
#     if not request.is_json:
#         return make_response('Missing JSON', 400)
#     if 'element' not in request.get_json():
#         return make_response('Missing "element" key', 400)
#     element = request.get_json()['element']
#     return make_response(f"{LIST.count(element)}", 200)


def main():
    '''Entry point'''
    global app
    app.run(debug=True)

if __name__ == '__main__':
    main()
