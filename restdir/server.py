#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''
import uuid
from flask import Flask, make_response, request
import json
import directory
import sys, argparse
import os
import auth_server

PERMISSION_ERR = 0
DIR_NOTFOUND_ERR = 1
ALREADYEXISTS_ERR = 2
DOESNOTEXIST_ERR = 3

app = Flask("restdir")

class Server():
    def __init__(self, admin, port, listening, db):
        self.admin = admin
        self.port = port
        self.listening = listening
        self.db = db
        self.dir= directory.Directory(self.db)  
        
    def run(self):
        global app
        app.run(host=self.listening, port=self.port, debug=True)


    @app.route('/v1/directory/root', methods=['GET'])
    def root_info(self):
        '''Añadir elemento a lista'''
        id = self.dir._get_UUID_dir(0, "/")

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = self.dir._checkUser_Readable(id, token)
            if not has_permission:
                return make_response(f'User {token} has no readable permission', 401)

        childs = self.dir._get_dirChilds(id)
        childs_list = json.loads(childs)

        names_childs = list()

        for child in childs_list:
            names_childs.append(self.dir._get_Name_dir(child))

        response = {"dir_id": id, "childs": names_childs}

        return make_response(json.dumps(response), 200)


    @app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['GET'])
    def dir_childs(self, dir_id, nombre_hijo):
        '''Añadir elemento a lista'''

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if not self.dir._checkDirectory(dir_id):
            return make_response(f'Directory {dir_id} does not exist', 404)

        id = self.dir._get_UUID_dir(dir_id, nombre_hijo)

        if not id:
            return make_response(f'Directory {dir_id} does not have {nombre_hijo} as child', 404)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = self.dir._checkUser_Readable(id, token)
            if not has_permission:
                return make_response(f'User {token} has no readable permission', 401)

        childs = self.dir._get_dirChilds(id)
        childs_list = json.loads(childs)

        response = {"childs_ids": childs_list}

        return make_response(json.dumps(response), 200)


    @app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['PUT'])
    def new_dir(self, dir_id, nombre_hijo):
        '''Borrar un elemento o la lista entera'''

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            self.dir.new_dir(dir_id, nombre_hijo, token)
            id = self.dir._get_UUID_dir(dir_id, nombre_hijo)
            response = {"dir_id": id}
        except directory.DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == ALREADYEXISTS_ERR:
                return make_response(err.msg, 409)

        return make_response(json.dumps(response), 200)


    @app.route('/v1/directory/<dir_id>/<nombre_hijo>', methods=['DELETE'])
    def remove_dir(self, dir_id, nombre_hijo):
        '''Obtener el elemento numero "index"'''

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            self.dir.remove_dir(dir_id, nombre_hijo, token)
            response = ""

        except directory.DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == DOESNOTEXIST_ERR:
                return make_response(err.msg, 404)

        return make_response(response, 204)


    @app.route('/v1/files/<dir_id>', methods=['GET'])
    def get_dir_files(self, dir_id):
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if not self.dir._checkDirectory(dir_id):
            return make_response(f'Directory {dir_id} does not exist', 404)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = self.dir._checkUser_Readable(dir_id, token)
            if not has_permission:
                return make_response(f'User {token} has no readable permission', 401)

        files = self.dir._get_dirFiles(dir_id)
        files_list = json.loads(files)

        response = {"files": files_list}

        return make_response(json.dumps(response), 200)


    @app.route('/v1/files/<dir_id>/<filename>', methods=['GET'])
    def get_file_url(self, dir_id, filename):
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if not self.dir._checkDirectory(dir_id):
            return make_response(f'Directory {dir_id} does not exist', 404)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = self.dir._checkUser_Readable(dir_id, token)
            if not has_permission:
                return make_response(f'User {token} has no readable permission', 401)

        url = ""
        files = json.loads(self.dir._get_dirFiles(dir_id))

        for x in files:
            if x[0] == filename:
                url = x[1]

        return make_response(str(url), 200)


    @app.route('/v1/files/<dir_id>/<filename>', methods=['PUT'])
    def add_file(self, dir_id, filename):
        
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
                url=self.dir.add_file(dir_id,token,filename)
                response = {"URL": url}
                return make_response(json.dumps(response), 200)
        except directory.DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == ALREADYEXISTS_ERR:
                return make_response(err.msg, 400)



    @app.route('/v1/files/<dir_id>/<filename>', methods=['DELETE'])
    def delete_file(self, dir_id, filename):
        
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f'Bad headers', 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
                self.dir.remove_file(dir_id,token,filename)        
                return make_response("", 204)
        except directory.DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == DOESNOTEXIST_ERR:
                return make_response(err.msg, 404)
        pass


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Introducir por lo menos 1 argumento: URL de Auth API")
        sys.exit()
        
    token = str(uuid.uuid4())
    puerto = 3002
    direccion = "0.0.0.0"
    ruta = os.getcwd()
    
    parser = argparse.ArgumentParser(description="Restdir arguments")
    parser.add_argument('pos_arg', type=str, help='A required integer positional argument') #<- URl api auth
    parser.add_argument("-a", "--admin", action='store', default=token, type=str)
    parser.add_argument("-p", "--port",  action='store', default=puerto, type=int)
    parser.add_argument("-l", "--listening", action='store', default=direccion, type=str)
    parser.add_argument("-d", "--db",  action='store', default=ruta, type=str)

    args = parser.parse_args()
    
    auth_serv=auth_server.AuthService(args.pos_arg)
    try:
        auth_serv.administrator_login(args.admin) #si no es admin salta error
    except Exception as e:
        print("El token de admin es erroneo")
        sys.exit()
    
    DirectoryAPI = Server(args.admin,args.port, args.listening, args.db)
    DirectoryAPI.run()
