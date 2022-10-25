#!/usr/bin/env python3

'''
    Implementacion del servicio de directorios DIRESTORY
'''

import sqlite3
import uuid
import json
from collections import deque
import os

BD_PATH = "./db/data.db"
ADMIN="admin"



PERMISSION_ERR = 0
DIR_NOTFOUND_ERR = 1 
ALREADYEXISTS_ERR = 2
DOESNOTEXIST_ERR = 3
class DirectoyException(Exception):
    '''Errores causados por fallos de la persistencia'''
    def __init__(self, message='unknown', code='uknown'):
        self.msg = message
        self.code = code

    def __str__(self):
        return f'DirestoryError: {self.msg}'
    

class Directory:
    '''Implementa todas las operaciones sobre un objeto tipo Dir()'''

    def __init__(self):
        try:
            self.bd_con = sqlite3.connect(BD_PATH)
            cur = self.bd_con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS directories(uuid text PRIMARY KEY, uuid_parent text, name text, childs text [], tuples text [], readable_by text [], writeable_by text [])")  
            cur.execute("SELECT * FROM directories")   
            if not cur.fetchall():
                self.bd_con.commit()
                self.bd_con.close()
                self.init_root()

        except Exception as Error:
            print(Error)
        
        
    def init_root(self): 
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
   
        id=1
        uuid_parent=0
        name="/"
        readable_by = list()
        writeable_by =list()
        files=list()
        childs=list()
        readable_by.append(ADMIN)
        writeable_by.append(ADMIN)
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)
        childs_str=json.dumps(childs)
        files_str=json.dumps(files)
        
        sql_data=(str(id), uuid_parent, name, childs_str, files_str, readable_by_str, writeable_by_str)
        sql_sentence=("INSERT INTO directories(uuid, uuid_parent, name, childs, tuples, readable_by, writeable_by) VALUES(?,?,?,?,?,?,?)")
        cur.execute(sql_sentence, sql_data)
       
        self.bd_con.commit()
        self.bd_con.close()
        
       
    def _checkUser_Writeable(self, id_dir, user):

        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id_dir,)
        sql_sentence = ("SELECT writeable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        writeable_by_tup = cur.fetchone()[0]
        
        writeable_by = json.loads(writeable_by_tup)
        
        self.bd_con.close()
        
        if user not in writeable_by:
            return False

        return True


    def _checkUser_Readable(self, id_dir, user):  
        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id_dir,)
        sql_sentence = ("SELECT readable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        readable_by_tup = cur.fetchone()[0]
        
        readable_by = json.loads(readable_by_tup)
        
        self.bd_con.close()
        
        if user not in readable_by:
            return False

        return True


    def _checkDirectory(self, uuid):
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data = (uuid,)
        sql_sentence="SELECT * FROM directories WHERE uuid=?"
        cur.execute(sql_sentence,sql_data)
        if not cur.fetchall():
            self.bd_con.close()
            return False
        self.bd_con.close()
        return True
    

    def _get_Name_dir(self, id):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (id,)
        sql_sentence = ("SELECT name FROM directories WHERE uuid=?")
        cur.execute(sql_sentence, sql_data)
        name = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(name)


    def _get_UUID_dir(self, uuid_parent, name):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (uuid_parent, name)
        sql_sentence = ("SELECT uuid FROM directories WHERE uuid_parent=? AND name=?")
        cur.execute(sql_sentence, sql_data)

        uid = cur.fetchone()
        self.bd_con.close()
        
        if uid == None:
            return False
        
        uuid_dir = uid[0]
                
        return str(uuid_dir)


    def _get_dirChilds(self, uuid):
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data = (str(uuid),)
        sql_sentence = ("SELECT childs FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        childs_tuple = cur.fetchone()[0]
        
        self.bd_con.close()
        
        return childs_tuple


    def _get_dirFiles(self, uuid):
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (str(uuid),)
        sql_sentence = ("SELECT tuples FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        files_tuple = cur.fetchone()[0]
        
        self.bd_con.close()
        
        return files_tuple


    def _get_writeableBy(self, id):
        '''Comprueba si el user esta en writeable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id,)
        sql_sentence = ("SELECT writeable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        writeable_by_tup = cur.fetchone()[0]
        
        writeable_by = json.loads(writeable_by_tup)
        
        self.bd_con.close()
        
        return writeable_by


    def _get_UUID_parent(self, id):
        '''obtener UUID de un dir'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        sql_data = (id,)
        sql_sentence = ("SELECT uuid_parent FROM directories WHERE uuid=?")
        cur.execute(sql_sentence, sql_data)
        uuid_parent = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(uuid_parent)
        

    def _get_readableBy(self, id):
        '''Comprueba si el user esta en readable_by'''
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
    
        sql_data = (id,)
        sql_sentence = ("SELECT readable_by FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)
        readable_by_tup = cur.fetchone()[0] 
        readable_by = json.loads(readable_by_tup)
        
        self.bd_con.close()
        
        return readable_by
    
    
    def _get_dirURL(self, id):
        '''Obtener la el path de un dir desde root'''
        dir_name=self._get_Name_dir(id)
        path = "" 
        listPath = deque()
        listPath.append(dir_name) 
        while(dir_name != "/"):
            parent = self._get_UUID_parent(id)
            dir_name = self._get_Name_dir(parent)
            listPath.append(dir_name)
        
        while(len(listPath)!= 0):
            if dir_name =="/":
                path+= listPath.pop()
            else:
                path += listPath.pop() + "/"
        
        return path
        
        
    def new_dir(self, uuid_parent, name, user):
        '''Crea un nuevo directorio incluyendolo en la BD'''
        if not self._checkDirectory(uuid_parent):
            raise DirectoyException(f"Directory {uuid_parent} doesn't exist", DIR_NOTFOUND_ERR)

        has_permission = self._checkUser_Writeable(uuid_parent, user)

        if not has_permission:
            raise DirectoyException(f"User {user} doesn't have writing permissions", PERMISSION_ERR)

        '''Añade nuevo child al parent'''

        id=uuid.uuid1()

        childs = self._get_dirChilds(uuid_parent)
        new_child = str(id)
        childs_list = json.loads(childs) 
        for child in childs_list:
            if name == self._get_Name_dir(child):
                raise DirectoyException(f'Another child with the name {name} in current directory', ALREADYEXISTS_ERR)
                    
        childs_list.append(new_child)
        childs_str = json.dumps(childs_list)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()

        sql_data3 =(childs_str, uuid_parent)
        sql_sentence3  = ("UPDATE directories SET childs=? WHERE uuid=?")
        
        '''Añade el directorio a la BD'''
        cur.execute(sql_sentence3, sql_data3)
        self.bd_con.commit()
        
        readable_by = list()
        writeable_by = list()
        files=list()
        childs=list()
        readable_by.append(user)
        writeable_by.append(user)
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)
        files_str=json.dumps(files)
        childs_str=json.dumps(childs)

        sql_data=(str(id), uuid_parent, name, childs_str, files_str, readable_by_str, writeable_by_str)
        sql_sentence = ("INSERT INTO directories(uuid, uuid_parent, name, childs, tuples, readable_by, writeable_by) VALUES(?,?,?,?,?,?,?)")
        
        cur.execute(sql_sentence, sql_data)

        self.bd_con.commit()
        self.bd_con.close()


    def remove_dir(self, uuid_parent, name, user):
        '''Elimina un directorio de la BD'''
        if not self._checkDirectory(uuid_parent):
            raise DirectoyException(f"Directory {uuid_parent} doesn't exist", DIR_NOTFOUND_ERR)
        
        id_dir = self._get_UUID_dir(uuid_parent, name)
        
        childs = self._get_dirChilds(uuid_parent)   
        childs_list = json.loads(childs)
        if id_dir not in childs_list:
            raise DirectoyException(f"It doesn't exist a directory with the name {name}", DOESNOTEXIST_ERR)

        for child in childs_list:
            if id_dir == child:
                childs_list.remove(id_dir)
                childs_str = json.dumps(childs_list)

        has_permission = self._checkUser_Writeable(id_dir, user)
        if not has_permission:
                raise DirectoyException(f"User {user} doesn't have writing permissions", PERMISSION_ERR)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        '''Eliminar este directorio del array de hijos del padre'''
        sql_data3 = (childs_str, uuid_parent,)
        sql_sentence3 = ("UPDATE directories SET childs=? WHERE uuid=?")    

        cur.execute(sql_sentence3, sql_data3)
        self.bd_con.commit()

        sql_data = (id_dir,)
        sql_sentence = ("DELETE FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
        
    def add_user_readable(self, id, user, owner):  
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
                raise DirectoyException(f"User {user} doesn't have writing permissions")

        if not self._checkDirectory(id):
            raise DirectoyException(f"Directory {id} doesn't exist")

        readers=self._get_readableBy(id)  
        readers.append(user)
        readers_str=json.dumps(readers)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data=(readers_str, id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
                

    def remove_user_readable(self, id, user, owner):  
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
                raise DirectoyException(f"User {user} doesn't have writing permissions")
        
        if not self._checkDirectory(id):
            raise DirectoyException(f'Error while adding user readable, directory {id} does not exist')
  
        readers=self._get_readableBy(id)  
        if user not in readers:
            raise DirectoyException(f'Error while removing user writable, user {user} not in writable_by list')
        elif user==ADMIN:
            raise DirectoyException(f'Error while removing user writable, ADMIN user is UNALTERABLE')

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        readers.remove(user)
        readers_str=json.dumps(readers)
        
        sql_data=(readers_str, id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()


    def add_user_writeable(self,id, user, owner):
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            raise DirectoyException(f'{owner} has not permissions to add user writeable')

        if not self._checkDirectory(id):
            raise DirectoyException(f'Error while adding user writeable, directory {id} does not exist')
        
        writers=self._get_writeableBy(id)  
        writers.append(user)
        writers_str=json.dumps(writers)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
                

    def remove_user_writeable(self, id, user, owner):
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            raise DirectoyException(f'{owner} has not permissions to remove user writeable')

        if not self._checkDirectory(id):
            raise DirectoyException(f'Error while removing user writeable, directory {id} does not exist')

        writers=self._get_writeableBy(id)
        if user not in writers:
            raise DirectoyException(f'Error while removing user writeable, user {user} not in writeable_by list')

        elif user==ADMIN:
            raise DirectoyException(f'Error while removing user writeable, ADMIN user is UNALTERABLE')
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        writers.remove(user)
        writers_str=json.dumps(writers)
        
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
    
    def add_file(self, id, user, name, url=None):
    
        '''Vacia la lista'''
        if not self._checkDirectory(id):
            raise DirectoyException(f"Directory {id} doesn't exist", DIR_NOTFOUND_ERR)
            
        if not url:
            url=self._get_dirURL(id) +"/"+name

        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            raise DirectoyException(f"{user} doens't have permissions writing permissions", PERMISSION_ERR)    

        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)
        print(tuples_list)
        for file_tuple in tuples_list:
            if name == file_tuple[0]:
                raise DirectoyException(f"A file with the name {name} already exists", ALREADYEXISTS_ERR)

        tuples_list.append(tuple((name, url)))
        print(tuples_list)
        
        childs=self._get_dirChilds(id)
        childs_list = json.loads(childs) 
        for child in childs_list:
            if name == self._get_Name_dir(child):
                raise DirectoyException(f"A directory with the name {name} already exists", ALREADYEXISTS_ERR)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_str = json.dumps(tuples_list)
        sql_data = (tuples_str, id,)
        
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()

        return url
    
    
    def remove_file(self, id, user, name):
        '''Vacia la lista'''
        if not self._checkDirectory(id):
            raise DirectoyException(f"Directory {id} doesn't exist", DIR_NOTFOUND_ERR)
                   
        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            raise DirectoyException(f"{user} doens't have permissions writing permissions", PERMISSION_ERR)  

        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)  

        found=False
       
        for file_tuple in tuples_list:
            if name == file_tuple[0]:
                tuples_list.remove(file_tuple) 
                found = True
        
        if not found:
            raise DirectoyException(f"A file with the name {tuples_list} doesn't exists, {tuples_list}", DOESNOTEXIST_ERR) 
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_str = json.dumps(tuples_list)
        sql_data = (tuples_str, id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()


if __name__=="__main__":
    dirDB=Directory()
    dirDB.add_file(1,"admin","jose","/dick/cock")
   # dirDB.new_dir(1, "prueba", "admin")
    #dirDB.remove_dir(1, "prueba", "admin")
