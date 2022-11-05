#!/usr/bin/env python3
from flask import Flask
import unittest, json
import restdir.directory as rd
from restdir.server import server
from restdir.client import DirectoryService,DirectoryException
import threading
BD_PATH="./db/data.db"
ADMIN="1234"
ROOT_ID="root"

URI = "http://127.0.0.1:3002"

class TestDirImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        mydir = rd.Directory(BD_PATH,ADMIN)
        self.assertTrue(mydir._checkDirectory(ROOT_ID))

    def test_newdir(self):
        '''Test append item'''
        mydir = rd.Directory(BD_PATH,ADMIN) 
        parent=ROOT_ID
        new_name="prueba"
        user="admin"

        len_bef = len(json.loads(mydir._get_dirChilds(parent)))
        mydir.new_dir(parent, new_name, user)
        len_aft = len(json.loads(mydir._get_dirChilds(parent)))
        self.assertEqual(len_aft, len_bef+1)
        self.assertNotEqual(mydir._get_UUID_dir(parent, new_name), False)

    def test_removedir(self):
        '''Test remove item'''
        mydir = rd.Directory(BD_PATH,ADMIN) 
        parent=ROOT_ID
        name="prueba"
        user="admin"

        len_bef = len(json.loads(mydir._get_dirChilds(parent)))
        mydir.remove_dir(parent, name, user)
        len_aft = len(json.loads(mydir._get_dirChilds(parent)))
        self.assertEqual(len_aft, len_bef-1)
        self.assertEqual(mydir._get_UUID_dir(parent, name), False)

    def test_adduser_readable(self):
        '''Test add user readable'''
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_readableBy(id))
        mydir.add_user_readable(id, user, owner)
        len_aft = len(mydir._get_readableBy(id))
        self.assertEqual(len_aft, len_bef+1)

    def test_removeuser_readable(self):
        '''Test add user readable'''
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_readableBy(id))
        mydir.remove_user_readable(id, user, owner)
        len_aft = len(mydir._get_readableBy(id))
        self.assertEqual(len_aft, len_bef-1)

    def test_adduser_writeable(self):
        '''Test add user readable'''
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_writeableBy(id))
        mydir.add_user_writeable(id, user, owner)
        len_aft = len(mydir._get_writeableBy(id))
        self.assertEqual(len_aft, len_bef+1)

    def test_removeuser_writeable(self):
        '''Test add user readable'''
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_writeableBy(id))
        mydir.remove_user_writeable(id, user, owner)
        len_aft = len(mydir._get_writeableBy(id))
        self.assertEqual(len_aft, len_bef-1)
        
    def test_add_file(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user="admin"
        name="file1"
        url="root/file1/"
        
        len_bef = len(json.loads(mydir._get_dirFiles(id)))
        mydir.add_file(id, user, name, url)
        len_aft = len(json.loads(mydir._get_dirFiles(id)))
        self.assertEqual(len_aft, len_bef+1)
        
    def test_remove_file(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user="admin"
        name="file1"
        
        len_bef = len(json.loads(mydir._get_dirFiles(id)))
        mydir.remove_file(id, user, name)
        len_aft = len(json.loads(mydir._get_dirFiles(id)))
        self.assertEqual(len_aft, len_bef-1)
    

    def test_server_info(self):
        #app = Flask("test-suite")
        # DIR = rd.Directory(BD_PATH, ADMIN) 
        # server(app, DIR)
        # app.run(host="0.0.0.0", port=3002, debug=True)
        # t1=threading.Thread(target=app.run,kwargs={'host':"0.0.0.0", 'port':3002, 'debug':True})
        # t1.run()
        dir=DirectoryService(URI)
        self.assertRaises(DirectoryException,dir.get_root,"spoofer")
        #  t1.setDaemon(True)