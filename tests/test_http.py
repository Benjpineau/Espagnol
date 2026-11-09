import json
import threading
import tempfile
from pathlib import Path
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import server

class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous = server.DB
        server.DB = Path(self.tmp.name) / "study.sqlite3"
        server.init_db()
        self.http = ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
        self.thread = threading.Thread(target=self.http.serve_forever,daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.http.server_port}'
    def tearDown(self):
        self.http.shutdown()
        self.http.server_close()
        self.thread.join()
        server.DB = self.previous
        self.tmp.cleanup()
    def test_http_data_and_import(self):
        with urlopen(self.url+'/api/data') as response:
            self.assertEqual(len(json.load(response)['conjugations']),360)
        request=Request(self.url+'/api/vocabulary/import',data='french,espanol,word/expression\nchat,gato,word'.encode(),method='POST')
        with urlopen(request) as response:
            self.assertEqual(json.load(response),{'added':1,'duplicates':0})
        with urlopen(self.url+'/api/data') as response:
            self.assertEqual(len(json.load(response)['vocabulary']),21)
        with urlopen(self.url+'/') as response:
            self.assertIn(b'lang="fr"',response.read())
    def test_invalid_import_is_atomic_and_cross_origin_blocked(self):
        body=b'french,espanol,word/expression\nchat,gato,word\nbad,,word'
        with self.assertRaises(HTTPError) as result:
            urlopen(Request(self.url+'/api/vocabulary/import',data=body,method='POST'))
        self.assertEqual(result.exception.code,400)
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM vocabulary').fetchone()[0],20)
        with self.assertRaises(HTTPError) as result:
            urlopen(Request(self.url+'/api/vocabulary/import',data=body,headers={'Origin':'https://example.com'},method='POST'))
        self.assertEqual(result.exception.code,403)
