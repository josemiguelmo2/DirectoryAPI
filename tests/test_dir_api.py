#!/usr/bin/env python3

import unittest, json
import restdir.directory as rd
from restdir.server import server
from restdir.client import DirectoryService,DirectoryException

BD_PATH="./db/data.db"
ADMIN="admin"
ROOT_ID="root"
URI_AUTH='1234'
URI_DIR = "http://127.0.0.1:3002"

class TestDirApi(unittest.TestCase):


    def test_info(self):
        dir=DirectoryService(URI_DIR, URI_AUTH)
        self.assertRaises(Exception,dir.get_root,"spoofer")
    
    def test_new_dir(self):
        dir=DirectoryService(URI_DIR,URI_AUTH)
        root = dir.get_root(ADMIN)
        root.new_directory("dirTest")
        info=json.loads(root.self_info())  
        self.assertIn("dirTest", info['childs'])  

    def test_remv_dir(self):
        dir=DirectoryService(URI_DIR,URI_AUTH)
        root = dir.get_root(ADMIN)
        root.remove_directory("dirTest")
        info=json.loads(root.self_info())  
        self.assertNotIn("dirTest",info['childs'])

    def test_new_file(self):
        dir=DirectoryService(URI_DIR,URI_AUTH)
        root = dir.get_root(ADMIN)
        root.new_file("test.txt","/root/text.txt")
        info=json.loads(root.list_files())
        self.assertIn("test.txt",str(info['files']))  

    def test_remv_file(self):   
        dir=DirectoryService(URI_DIR,URI_AUTH)
        root = dir.get_root(ADMIN)
        root.remove_file("test.txt")
        info=json.loads(root.list_files())  
        print(info['files'])
        self.assertNotIn("test.txt",str(info['files']))
        
    

        