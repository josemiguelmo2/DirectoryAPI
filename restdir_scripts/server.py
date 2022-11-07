#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''
import sys
import argparse
import uuid
import os
from flask import Flask
from restdir.directory import Directory
from restdir.server import server
from restdir.auth import AuthService


def main():
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
    
    auth_serv=AuthService(args.pos_arg)
    try:
        auth_serv.administrator_login(args.admin) #si no es admin salta error
    except Exception:
        print("El token de admin es erroneo")
        sys.exit(1)
    
    app = Flask("restdir")
    DIR = Directory(args.db, args.admin) 
    server(app, DIR)
    app.run(host=args.listening, port=args.port, debug=True)


if __name__ == '__main__':
    main()