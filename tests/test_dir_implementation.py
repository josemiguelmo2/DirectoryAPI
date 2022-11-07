#!/usr/bin/env python3

import unittest, json
import restdir.directory as rd
from restdir.server import server
from restdir.client import DirectoryService,DirectoryException

BD_PATH="./db/data.db"
ADMIN="admin"
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

    def test_dirinfo(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id = ROOT_ID
        user = ADMIN
        parent, childs = mydir.get_dir_info(id, user) 
        self.assertEqual(parent, "0")
        self.assertIsNotNone(childs)

    def test_dirchilds(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        parent = "0"
        name = "/"
        user = ADMIN
        childs = mydir.get_dir_childs(parent, name, user)
        self.assertIsNotNone(childs)

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

    def test_dirfiles(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id = ROOT_ID
        user = ADMIN
        files = mydir.get_dir_files(id, user)
        self.assertIsNotNone(files)  
    
    def test_fileurl(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id = ROOT_ID
        filename = "file1"
        user = ADMIN
        url = mydir.get_file_url(id, filename, user)
        self.assertNotEqual(url, "")

    def test_remove_file(self):
        mydir = rd.Directory(BD_PATH,ADMIN)
        id=ROOT_ID
        user="admin"
        name="file1"
        
        len_bef = len(json.loads(mydir._get_dirFiles(id)))
        mydir.remove_file(id, user, name)
        len_aft = len(json.loads(mydir._get_dirFiles(id)))
        self.assertEqual(len_aft, len_bef-1)
