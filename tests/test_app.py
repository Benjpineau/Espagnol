import tempfile
import unittest
from pathlib import Path
import server
from data import conjugate

class AppTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous = server.DB
        server.DB = Path(self.tmp.name) / 'study.sqlite3'
        server.init_db()
    def tearDown(self):
        server.DB = self.previous
        self.tmp.cleanup()
    def test_conjugations_and_indexes(self):
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM conjugations').fetchone()[0],360)
            self.assertEqual(db.execute("SELECT form FROM conjugations WHERE verb='tener' AND pronoun='yo' AND tense='presente'").fetchone()[0],'tengo')
            self.assertEqual(len(db.execute("PRAGMA index_list('conjugations')").fetchall()),3)
        self.assertEqual(conjugate('tener','futuro')[0],'tendré')
        self.assertEqual(conjugate('ir','imperfecto')[3],'íbamos')
        self.assertEqual(conjugate('vivir','presente')[4],'vivís')
        self.assertEqual(conjugate('ser','condicional')[0],'sería')
    def test_restarting_preserves_imports(self):
        with server.connect() as db:
            db.execute("INSERT INTO vocabulary(french,espanol,kind) VALUES ('chat','gato','word')")
        server.init_db()
        with server.connect() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM vocabulary').fetchone()[0],21)
    def test_csv_bom_semicolon_and_quotes(self):
        rows=server.parse_csv('\ufeffespanol;word/expression;french\n"hola; amigo";expression;"salut; ami"\n')
        self.assertEqual(rows,[('salut; ami','hola; amigo','expression')])
        self.assertEqual(server.parse_csv('french,espanol,word/expression\n"bonjour, toi",hola,word\n\n')[0][0],'bonjour, toi')
    def test_reject_invalid_csv(self):
        for text in ['', 'wrong,espanol,word/expression\na,b,word', 'french,espanol,word/expression\na,b,unknown', 'french,espanol,word/expression\na,,word', 'french,espanol,word/expression\na,b,word,extra', 'french,espanol,word/expression\n']:
            with self.subTest(text=text),self.assertRaises(ValueError):
                server.parse_csv(text)
    def test_duplicate_import(self):
        rows=server.parse_csv('french,espanol,word/expression\nchat,gato,word\nchat,gato,word')
        with server.connect() as db:
            before=db.total_changes
            db.executemany('INSERT OR IGNORE INTO vocabulary(french,espanol,kind) VALUES (?,?,?)',rows)
            self.assertEqual(db.total_changes-before,1)

if __name__=='__main__':
    unittest.main()
