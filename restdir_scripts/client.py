#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''


from restdir.client import DirectoryService
from restdir.auth import AuthService

URI = "http://127.0.0.1:3002"

def main():
    '''Entry point'''

    dir=DirectoryService(URI, "uri_auth").get_root("admin")
    response=dir.new_directory("dirA")
    print(response)
    print(dir.self_info())
    dir.remove_directory("dirA")
    res3=dir.new_file("test.txt","/test.txt")
    res4=dir.list_files()
    
    dir.remove_file("test.txt")
    res5=dir.list_files()
    print(res3)
    print(res4)
    print(res5)

if __name__ == '__main__':
    main()