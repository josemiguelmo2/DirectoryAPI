#!/usr/bin/env python3

"""
    Implementacion ejemplo de servidor y servicio REST
"""
from flask import Flask, make_response, request
import json
from restdir.directory import Directory, DirectoyException

PERMISSION_ERR = 0
DIR_NOTFOUND_ERR = 1
ALREADYEXISTS_ERR = 2
DOESNOTEXIST_ERR = 3


def server(app, dir):
    @app.route("/v1/directory/<dir_id>", methods=["GET"])
    def dir_info(dir_id):
        """Añadir elemento a lista"""

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = dir._checkUser_Readable(dir_id, token)
            if not has_permission:
                return make_response(f"User {token} has no readable permission", 401)

        # falta capturar excepcion si id no existe
        childs = dir._get_dirChilds(dir_id)
        parent = dir._get_UUID_parent(dir_id)
        childs_list = json.loads(childs)

        names_childs = list()

        for child in childs_list:
            names_childs.append(dir._get_Name_dir(child))

        response = {"dir_id": dir_id, "childs": names_childs, "parent": parent}

        return make_response(json.dumps(response), 200)

    @app.route("/v1/directory/<dir_id>/<nombre_hijo>", methods=["GET"])
    def dir_childs(dir_id, nombre_hijo):
        """Añadir elemento a lista"""

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if not dir._checkDirectory(dir_id):
            return make_response(f"Directory {dir_id} does not exist", 404)

        id = dir._get_UUID_dir(dir_id, nombre_hijo)

        if not id:
            return make_response(
                f"Directory {dir_id} does not have {nombre_hijo} as child", 404
            )

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = dir._checkUser_Readable(id, token)
            if not has_permission:
                return make_response(f"User {token} has no readable permission", 401)

        childs = dir._get_dirChilds(id)
        childs_list = json.loads(childs)

        response = {"childs_ids": childs_list}

        return make_response(json.dumps(response), 200)

    @app.route("/v1/directory/<dir_id>/<nombre_hijo>", methods=["PUT"])
    def new_dir(dir_id, nombre_hijo):
        """Borrar un elemento o la lista entera"""

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            dir.new_dir(dir_id, nombre_hijo, token)
            id = dir._get_UUID_dir(dir_id, nombre_hijo)
            response = {"dir_id": id}
        except DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == ALREADYEXISTS_ERR:
                return make_response(err.msg, 409)

        return make_response(json.dumps(response), 200)

    @app.route("/v1/directory/<dir_id>/<nombre_hijo>", methods=["DELETE"])
    def remove_dir(dir_id, nombre_hijo):
        '''Obtener el elemento numero "index"'''

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            dir.remove_dir(dir_id, nombre_hijo, token)
            response = ""

        except DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == DOESNOTEXIST_ERR:
                return make_response(err.msg, 404)

        return make_response(response, 204)

    @app.route("/v1/files/<dir_id>", methods=["GET"])
    def get_dir_files(dir_id):
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if not dir._checkDirectory(dir_id):
            return make_response(f"Directory {dir_id} does not exist", 404)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = dir._checkUser_Readable(dir_id, token)
            if not has_permission:
                return make_response(f"User {token} has no readable permission", 401)

        files = dir._get_dirFiles(dir_id)
        files_list = json.loads(files)
        names = list()
        for x in files_list:
            names.append(x[0])

        response = {"files": names}

        return make_response(json.dumps(response), 200)

    @app.route("/v1/files/<dir_id>/<filename>", methods=["GET"])
    def get_file_url(dir_id, filename):
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if not dir._checkDirectory(dir_id):
            return make_response(f"Directory {dir_id} does not exist", 404)

        if "admin-token" not in headers:
            token = headers["user-token"]
            has_permission = dir._checkUser_Readable(dir_id, token)
            if not has_permission:
                return make_response(f"User {token} has no readable permission", 401)

        url = ""
        files = json.loads(dir._get_dirFiles(dir_id))

        for x in files:
            if x[0] == filename:
                url = x[1]

        return make_response(str(url), 200)

    @app.route("/v1/files/<dir_id>/<filename>", methods=["PUT"])
    def add_file(dir_id, filename):
        url = request.data.decode("utf-8")
        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            url = dir.add_file(dir_id, token, filename, url)
            response = {"URL": url}
            return make_response(json.dumps(response), 200)
        except DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == ALREADYEXISTS_ERR:
                return make_response(err.msg, 400)

    @app.route("/v1/files/<dir_id>/<filename>", methods=["DELETE"])
    def delete_file(dir_id, filename):

        headers = request.headers
        if "admin-token" not in headers and "user-token" not in headers:
            return make_response(f"Bad headers", 401)

        if "admin-token" not in headers:
            token = headers["user-token"]
        else:
            token = headers["admin-token"]

        try:
            dir.remove_file(dir_id, token, filename)
            return make_response("", 204)
        except DirectoyException as err:
            if err.code == PERMISSION_ERR:
                return make_response(err.msg, 401)
            if err.code == DIR_NOTFOUND_ERR:
                return make_response(err.msg, 404)
            if err.code == DOESNOTEXIST_ERR:
                return make_response(err.msg, 404)
