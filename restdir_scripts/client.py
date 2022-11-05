#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio REST
'''


from restdir.client import DirectoryService

URI = "http://127.0.0.1:3002"

def main():
    '''Entry point'''
    dir=DirectoryService(URI).get_root("admin")
    dir.remove_directory("dirA")
    response=dir.new_directory("dirA")
    print(response)
    dir.remove_file("test.txt")
    res3=dir.new_file("test.txt","/test.txt")
    res4=dir.list_files()

    print(res3)
    print(res4)


if __name__ == '__main__':
    main()