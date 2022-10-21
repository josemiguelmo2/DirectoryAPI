#!/usr/bin/env python3

import unittest, json
import restdir.directory as rd

class TestDirImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        mydir = rd.Directory()
        self.assertTrue(mydir._checkDirectory(1))

    def test_newdir(self):
        '''Test append item'''
        mydir = rd.Directory() 
        parent=1
        new_name="prueba"
        user="admin"

        len_bef = len(json.loads(mydir._get_dirChilds(parent)))
        mydir.new_dir(parent, new_name, user)
        len_aft = len(json.loads(mydir._get_dirChilds(parent)))
        self.assertEqual(len_aft, len_bef+1)
        self.assertNotEqual(mydir._get_UUID_dir(parent, new_name), False)

    def test_removedir(self):
        '''Test remove item'''
        mydir = rd.Directory() 
        parent=1
        name="prueba"
        user="admin"

        len_bef = len(json.loads(mydir._get_dirChilds(parent)))
        mydir.remove_dir(parent, name, user)
        len_aft = len(json.loads(mydir._get_dirChilds(parent)))
        self.assertEqual(len_aft, len_bef-1)
        self.assertEqual(mydir._get_UUID_dir(parent, name), False)

    def test_adduser_readable(self):
        '''Test add user readable'''
        mydir = rd.Directory()
        id = 1
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_readableBy(id))
        mydir.add_user_readable(id, user, owner)
        len_aft = len(mydir._get_readableBy(id))
        self.assertEqual(len_aft, len_bef+1)

    def test_removeuser_readable(self):
        '''Test add user readable'''
        mydir = rd.Directory()
        id = 1
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_readableBy(id))
        mydir.remove_user_readable(id, user, owner)
        len_aft = len(mydir._get_readableBy(id))
        self.assertEqual(len_aft, len_bef-1)

    def test_adduser_writeable(self):
        '''Test add user readable'''
        mydir = rd.Directory()
        id = 1
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_writeableBy(id))
        mydir.add_user_writeable(id, user, owner)
        len_aft = len(mydir._get_writeableBy(id))
        self.assertEqual(len_aft, len_bef+1)

    def test_removeuser_writeable(self):
        '''Test add user readable'''
        mydir = rd.Directory()
        id = 1
        user = "tobias"
        owner = "admin"

        len_bef = len(mydir._get_writeableBy(id))
        mydir.remove_user_writeable(id, user, owner)
        len_aft = len(mydir._get_writeableBy(id))
        self.assertEqual(len_aft, len_bef-1)
        
    def test_add_file(self):
        mydir = rd.Directory()
        id=1
        user="admin"
        name="file1"
        url="root/file1/"
        
        len_bef = len(json.loads(mydir._get_dirFiles(id)))
        mydir.add_file(id, user, name, url)
        len_aft = len(json.loads(mydir._get_dirFiles(id)))
        self.assertEqual(len_aft, len_bef+1)
        
    def test_remove_file(self):
        mydir = rd.Directory()
        id=1
        user="admin"
        name="file1"
        url="root/file1/"
        
        len_bef = len(json.loads(mydir._get_dirFiles(id)))
        mydir.remove_file(id, user, name, url)
        len_aft = len(json.loads(mydir._get_dirFiles(id)))
        self.assertEqual(len_aft, len_bef-1)