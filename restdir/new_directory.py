import sqlite3
import uuid

BD_PATH = "./db/data.db"
ADMIN="admin"
PERMISSION_ERR = 0
DIR_NOTFOUND_ERR = 1 
ALREADYEXISTS_ERR = 2
DOESNOTEXIST_ERR = 3

'''
    Interfaces para el acceso al servicio de directorio
'''

class DirectoyException(Exception):
    '''Errores causados por fallos de la persistencia'''
    def __init__(self, message='unknown', code='uknown'):
        self.msg = message
        self.code = code

    def __str__(self):
        return f'DirestoryError: {self.msg}'


class DirectoryService:
    '''Cliente de acceso al servicio de directorio'''
    
    def __init__(self):
        try:
            self.bd_con = sqlite3.connect(BD_PATH)
            cur = self.bd_con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS directories(uuid text PRIMARY KEY, uuid_parent text, name text, childs text [], tuples text [], readable_by text [], writeable_by text [])")  
            cur.execute("SELECT * FROM directories")   
            if not cur.fetchall():
                self.init_root(cur)

            cur.execute("SELECT * FROM directories")  
            root=cur.fetchone() 
            self.root_obj=Directory(root[0],root[1],root[2],root[3],root[4],root[5],root[6],root[7])

            self.bd_con.commit()
            self.bd_con.close()
        except Exception as Error:
            print(Error)
    
    def init_root(self, cur): 
        cur = self.bd_con.cursor()
   
        id=1
        uuid_parent=0
        name="/"
        readable_by = list()
        writeable_by =list()
        files=list()
        childs=list()
        
        sql_data=(str(id), uuid_parent, name, str(childs), str(files), str(readable_by.append(ADMIN)), str(writeable_by.append(ADMIN)))
        sql_sentence=("INSERT INTO directories(uuid, uuid_parent, name, childs, tuples, readable_by, writeable_by) VALUES(?,?,?,?,?,?,?)")
        cur.execute(sql_sentence, sql_data)      
    
    def get_root(self, user):
        '''Obtiene el directorio raiz'''
        self.root_obj._set_actual_user(user)
        return self.root_obj

class Directory:
    '''Cliente de acceso a un directorio'''
    
    def __init__(self, id, uuid_parent, directory_name, readable_by, writeable_by, files, childs):
        self.id = id 
        self.uuid_parent = uuid_parent
        self.directory_name = directory_name
        self.readable_by = readable_by
        self.writeable_by = writeable_by
        self.files = files
        self.childs = childs       
    
    def _set_actual_user(self, user):
        self.actual_user = user
       
    def _set_id(self, id):
        self.id = id
        
    def _set_id_parent(self, id_parent):
        self.uuid_parent = id_parent
    
    def _get_name(self, name):
        self.directory_name = name    
    
    def _set_readableby(self, readableby):
        self.readable_by = readableby
        
    def _set_writeableby(self, writeableby):
        self.writeable_by = writeableby
        
    def _set_files(self, files):
        self.files = files
    
    def _set_childs(self, childs):
        self.childs = childs
        
    def _get_id(self):
        return self.id
    
    def _get_id_parent(self):
        return self.uuid_parent
    
    def _set_name(self):
        return self.directory_name
    
    def _get_readableby(self):
        return self.readable_by
    
    def _get_writeableby(self):
        return self.writeable_by
    
    def _get_files(self):
        return self.files
    
    def _get_childs(self):  
        return self.childs

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

    def _checkUser_Writeable(self,user):
        writeable = False
        if user in self.writeable_by:
            writeable= True
        return writeable
    
    def _checkUser_Readable(self,user):
        readable = False
        if user in self.readable_by:
            readable= True
        return readable
    
    def list_directories(self):
        '''Obtiene una lista de todos los subdirectorios del directorio'''
        return self.childs


    def new_directory(self, directory_name):
        '''Crea un nuevo subdirectorio en el directorio'''
        
        has_permission = self._checkUser_Writeable(self.actual_user)

        if not has_permission:
            raise DirectoyException(f"User {self.actual_user} doesn't have writing permissions", PERMISSION_ERR)

        '''Añade nuevo child al parent'''
        childs = self.files
        if directory_name in childs:
                raise DirectoyException(f'Another child with the name {directory_name} in current directory', ALREADYEXISTS_ERR)
        
        childs.append(directory_name)
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()

        sql_data3 =(str(childs), self.id,)
        sql_sentence3  = ("UPDATE directories SET childs=? WHERE uuid=?")
        
        '''Añade el directorio a la BD'''
        cur.execute(sql_sentence3, sql_data3)
        self.bd_con.commit()
        
        id=uuid.uuid1()
        readable_by = list()
        writeable_by =list()
        files=list()
        childs=list()
        new_dir = Directory(id, directory_name, readable_by.append(self.actual_user), writeable_by.append(self.actual_user), files, childs)       

        sql_data=(new_dir._get_id(), new_dir._get_id_parent(), new_dir._get_name(), str(new_dir._get_childs()), str(new_dir._get_files()), str(new_dir._get_readableby()), str(new_dir._get_writeableby()),)
        sql_sentence = ("INSERT INTO directories(uuid, uuid_parent, name, childs, tuples, readable_by, writeable_by) VALUES(?,?,?,?,?,?,?)")
        
        cur.execute(sql_sentence, sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
        
    def remove_directory(self, directory_name):
        '''Elimina un subdirectorio del directorio'''

        childs = self.childs
        if directory_name not in childs:
            raise DirectoyException(f"It doesn't exist a directory with the name {directory_name}", DOESNOTEXIST_ERR)

        childs.remove(directory_name)

        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
                raise DirectoyException(f"User {self.actual_user} doesn't have writing permissions", PERMISSION_ERR)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        
        '''Eliminar este directorio del array de hijos del padre'''
        sql_data3 = (str(childs), self.id,)
        sql_sentence3 = ("UPDATE directories SET childs=? WHERE uuid=?")    

        cur.execute(sql_sentence3, sql_data3)
        self.bd_con.commit()

        sql_data = (self._get_UUID_dir(self.id, directory_name),)
        sql_sentence = ("DELETE FROM directories WHERE uuid=?")
        
        cur.execute(sql_sentence, sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        
        raise NotImplementedError()


    def list_files(self):
        '''Obtiene una lista de ficheros del directorio'''
        return self._get_files()

    def new_file(self, filename, blob_id):
        '''Crea un nuevo fichero a partir de un blob'''
        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
                raise DirectoyException(f"User {self.actual_user} doesn't have writing permissions", PERMISSION_ERR)

        for file_tuple in files:
            if filename == file_tuple[0]:
                raise DirectoyException(f"A file with the name {filename} already exists", 0)

        files=self.files.append((filename,blob_id)) 
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        sql_data = (str(files), self.id,)
        
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()

        return blob_id


    def remove_file(self, filename):
        '''Elimina un fichero del directorio'''

        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
            raise DirectoyException(f"{self.actual_user} doens't have permissions writing permissions", PERMISSION_ERR)  

        files=self.childs
        found=False
        for file_tuple in files:
            if filename == file_tuple[0]:
                files.remove(file_tuple) 
                found = True
    
        if not found:
            raise DirectoyException(f"A file with the name {filename} doesn't exists", DOESNOTEXIST_ERR) 
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
            
        sql_data = (str(files), self.id,)
        sql_sentence= ("UPDATE directories SET tuples=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)
    
        self.bd_con.commit()
        self.bd_con.close()       


    def add_read_permission_to(self, user):
        '''Permite al usuario dado leer el blob'''
        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
                raise DirectoyException(f"User {self.actual_user} doesn't have writing permissions")

        readers=self.readable_by
        readers.append(user)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data=(str(readers), self.id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        

    def revoke_read_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de lectura'''
        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
                raise DirectoyException(f"User {self.actual_user} doesn't have writing permissions")
        
        readers=self.readable_by 
        if user not in readers:
            raise DirectoyException(f'Error while removing user writeable, user {user} not in writeable_by list')
        elif user==ADMIN:
            raise DirectoyException(f'Error while removing user writeable, ADMIN user is UNALTERABLE')

        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        readers.remove(user)
        
        sql_data=(str(readers), self.id,)
        sql_sentence=("UPDATE directories SET readable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()


    def add_write_permission_to(self, user):
        '''Permite al usuario dado escribir el blob'''
        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
            raise DirectoyException(f'{self.actual_user} has not permissions to add user writeable')

        writers=self.writeable_by
        writers.append(user)
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        sql_data=(str(writers), self.id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
        

    def revoke_write_permission_to(self, user):
        '''Elimina al usuario dado de la lista de permiso de escritura'''
        has_permission = self._checkUser_Writeable(self.actual_user)
        if not has_permission:
            raise DirectoyException(f'{self.actual_user} has not permissions to remove user writeable')
        
        writers=self.writeable_by
        if user not in writers:
            raise DirectoyException(f'Error while removing user writeable, user {user} not in writeable_by list')

        elif user==ADMIN:
            raise DirectoyException(f'Error while removing user writeable, ADMIN user is UNALTERABLE')
        
        self.bd_con = sqlite3.connect(BD_PATH)
        cur = self.bd_con.cursor()
        writers.remove(user)
        
        sql_data=(str(writers), self.id,)
        sql_sentence=("UPDATE directories SET writeable_by=? WHERE uuid=?")

        cur.execute(sql_sentence,sql_data)

        self.bd_con.commit()
        self.bd_con.close()
