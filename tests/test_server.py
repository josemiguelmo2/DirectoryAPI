
import unittest, json
from restdir.directory import Directory 
from restdir.server import server
from restdir.client import DirectoryService,DirectoryException

BD_PATH="./db/data.db"
ADMIN="admin"
ROOT_ID="root"
URI_AUTH='1234'
URI_DIR = "http://127.0.0.1:3002"

class TestDirServer(unittest.TestCase):


    def test_dir_info(self):
        app = Flask("restdir")
        DIR = Directory(BD_PATH, ADMIN) 
        server_api = server(app, DIR)
        server_api.dir_info()
    