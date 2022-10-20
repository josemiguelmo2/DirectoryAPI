#!/usr/bin/env python3

'''
    Implementacion del servicio de directorios DIRESTORY
'''
from csv import writer
import os
import sqlite3
import uuid
import json
from collections import deque

BD_PATH = "./db/data.db"
ADMIN="admin"

class DirectoyException(Exception):
    '''Errores causados por fallos de la persistencia'''
    def __init__(self, message='unknown'):
        self.msg = message

    def __str__(self):
        return f'DirestoryError: {self.msg}'
    

class Directory:
    '''Implementa todas las operaciones sobre un objeto tipo Dir()'''

    def __init__(self):
        if os.path.exists(BD_PATH):
            try:
                self.bd_con = sqlite3.connect(BD_PATH)
                cur = self.bd_con.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS directories(uuid text PRIMARY KEY, uuid_parent text, name text, childs text [], tuples text [], readable_by text [], writeable_by text [])")  
                cur.execute("SELECT * FROM directories")   
                if not cur.fetchone():
                    self.bd_con.commit()
                    self.bd_con.close()
                    self.init_root()
            except Exception as Error:
                print(Error)
        else:
            print("No existe un fichero llamado "+BD_PATH)
        
        
    def init_root(self): 
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
   
        id=uuid.uuid1()
        uuid_parent=0
        name="/"
        readable_by = list()
        writeable_by =list()
        readable_by.append(ADMIN)
        writeable_by.append(ADMIN)
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)
        
        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence=("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?)")
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
        if not cur.fetchone()[0]:
            return False
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
        uuid_dir = cur.fetchone()[0]
                
        self.bd_con.close()
                
        return str(uuid_dir)


    def _get_dirChilds(self, uuid):
        cur = self.bd_con.cursor()
        sql_data = (str(uuid))
        sql_sentence = ("SELECT childs FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        childs_tuple = cur.fetchone()[0]
        return childs_tuple


    def _get_dirFiles(self, uuid):
        cur = self.bd_con.cursor()
        sql_data = (str(uuid))
        sql_sentence = ("SELECT tuples FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        files_tuple = cur.fetchone()[0]
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
        
        while(listPath.count()!= 0):
            path += listPath.pop() + "/"
        
        return path
        
        
    def new_dir(self, uuid_parent, name, user):
        '''Crea un nuevo directorio incluyendolo en la BD'''
        if not self._checkDirectory(uuid_parent):
            raise DirectoyException(f"Directory {uuid_parent} doesn't exist")

        has_permission = self._checkUser_Writeable(uuid_parent, user)
        print(has_permission)
        if not has_permission:
            #throw_exception
            pass

        '''Añade nuevo child al parent'''
        childs = self._get_dirChilds(uuid_parent)
        new_child = str(id)
        childs_list = json.loads(childs) 
        for child in childs_list:
            if name == self._get_Name_dir(child):
                raise DirectoyException(f'Another child with the name {name} in current directory')
                    
        childs_list.append(new_child)
        childs_str = json.dumps(childs_list)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()

        sql_data3 =(childs_str, uuid_parent)
        sql_sentence3  = ("UPDATE directories SET childs=? WHERE uuid=?")
        
        cur.execute(sql_sentence3, sql_data3)
        self.bd_con.commit()
        
        id=uuid.uuid1()
        readable_by = list()
        writeable_by = list()
        readable_by.append(user)
        writeable_by.append(user)
        
        readable_by_str=json.dumps(readable_by)
        writeable_by_str=json.dumps(writeable_by)

        sql_data=(str(id), uuid_parent, name, readable_by_str, writeable_by_str)
        sql_sentence = ("INSERT INTO directories(uuid, uuid_parent, name, readable_by, writeable_by) VALUES(?,?,?,?,?)")
        
        cur.execute(sql_sentence, sql_data)

        self.bd_con.commit()
        self.bd_con.close()


    def remove_dir(self, uuid_parent, name, user):
        '''Elimina un directorio de la BD'''
        if not self._checkDirectory(uuid_parent):
            raise DirectoyException(f"Directory {uuid_parent} doesn't exist")
        
        childs = self._get_dirChilds(uuid_parent)   
        childs_list = json.loads(childs)
        for child in childs_list:
            if id_dir == child:
                childs_list.remove(id_dir)
                childs_str = json.dumps(childs_list)
            else:
                raise DirectoyException(f"It does exist a directory with the name {name}")

        id_dir = self._get_UUID_dir(uuid_parent, name)
        has_permission = self._checkUser_Writeable(id_dir, user)
        if not has_permission:
                raise DirectoyException(f"User {user} doesn't have writing permissions")
        
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
            raise DirectoyException(f'Error while adding user writable, directory {id} does not exist')
        
        writers=self._get_writeableBy(id)  
        writers.append(user)
        writers_str=json.dumps(writers)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
                

    def remove_user_writeable(self, id, user, owner):
        '''Retorna si un elemento dado esta o no en la lista'''
        has_permission = self._checkUser_Writeable(id, owner)
        if not has_permission:
            raise DirectoyException(f'{owner} has not permissions to remove user writeable')

        if not self._checkDirectory(id):
            raise DirectoyException(f'Error while removing user writable, directory {id} does not exist')

        writers=self._get_writeableBy(id)
        if user not in writers:
            raise DirectoyException(f'Error while removing user writable, user {user} not in writable_by list')

        elif user==ADMIN:
            raise DirectoyException(f'Error while removing user writable, ADMIN user is UNALTERABLE')
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        writers.remove(user)
        writers_str=json.dumps(writers)
        
        sql_data=(writers_str, id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
    
    def add_file(self, id, user, name, url):
        '''Vacia la lista'''
        if not self._checkDirectory(id):
            raise DirectoyException(f"Directory {id} doesn't exist")

        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            raise DirectoyException(f"{user} doens't have permissions writing permissions")    

        file_tuple = (name, url)
        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)   
        for file_tuple in tuples_list:
            if name == file_tuple[0]:
                raise DirectoyException(f"A file with the name {name} already exists")

        updated_tuples = tuples_list.append(file_tuple)
        
        childs=self._get_dirChilds(id)
        childs_list = json.loads(childs) 
        for child in childs_list:
            if name == self._get_Name_dir(child):
                raise DirectoyException(f"A directory with the name {name} already exists")
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_str = json.dumps(updated_tuples)
        sql_data = (tuples_str, id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()
    
    
    def remove_file(self, id, user, name, url):
        '''Vacia la lista'''
        if not self._checkDirectory(id):
            raise DirectoyException(f"Directory {id} doesn't exist")
                   
        has_permission = self._checkUser_Writeable(id, user)
        if not has_permission:
            raise DirectoyException(f"{user} doens't have permissions writing permissions")  

        tuples_raw=self._get_dirFiles(id)
        tuples_list = json.loads(tuples_raw)  
        if (name, url) not in tuples_list:
            raise DirectoyException(f"A file with the name {name} doesn't exists") 
        for file_tuple in tuples_list:
            if name == file_tuple[0]:
                updated_tuples = tuples_list.remove(file_tuple) 
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        tuples_str = json.dumps(updated_tuples)
        sql_data = (tuples_str, id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()


if __name__=="__main__":
    dirDB=Directory()
    
    dirDB.new_dir(1, "prueba", "admin")
    #dirDB.remove_dir(1, "prueba", "admin")
