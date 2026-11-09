#!/usr/bin/env python3
"""Local-only Spanish study app, Python 3.10+, no third-party packages."""
import argparse
import csv
import io
import json
import os
import sqlite3
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from data import VERBS, TENSES, PRONOUNS, VOCABULARY, GRAMMAR, conjugate

ROOT = Path(__file__).resolve().parent
DB = Path(os.environ.get('ESPAGNOL_DB', ROOT / 'data' / 'espagnol.sqlite3'))

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS conjugations (
            verb TEXT NOT NULL, pronoun TEXT NOT NULL, tense TEXT NOT NULL, form TEXT NOT NULL,
            PRIMARY KEY (verb, pronoun, tense));
        CREATE INDEX IF NOT EXISTS conjugations_by_tense ON conjugations(tense, verb, pronoun);
        CREATE INDEX IF NOT EXISTS conjugations_by_pronoun ON conjugations(pronoun, tense, verb);
        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY, french TEXT NOT NULL, espanol TEXT NOT NULL,
            kind TEXT NOT NULL CHECK(kind IN ('word','expression')),
            UNIQUE(french, espanol, kind));
        CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT);
        ''')
        if not db.execute("SELECT 1 FROM metadata WHERE key='seeded'").fetchone():
            for verb in VERBS:
                for tense in TENSES:
                    db.executemany('INSERT OR IGNORE INTO conjugations VALUES (?,?,?,?)',
                        [(verb, pronoun, tense, form) for pronoun, form in zip(PRONOUNS, conjugate(verb, tense))])
            db.executemany('INSERT OR IGNORE INTO vocabulary(french,espanol,kind) VALUES (?,?,?)', VOCABULARY)
            db.execute("INSERT INTO metadata VALUES ('seeded','1')")

def parse_csv(text):
    text = text.lstrip('\ufeff')
    if not text.strip():
        raise ValueError('Le fichier CSV est vide.')
    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=',;\t')
    except csv.Error:
        dialect = csv.excel
    reader = csv.reader(io.StringIO(text, newline=''), dialect)
    header = [v.strip().lower() for v in next(reader)]
    if set(header) != {'french', 'espanol', 'word/expression'} or len(header) != 3:
        raise ValueError('En-têtes attendus : french,espanol,word/expression')
    result = []
    for number, row in enumerate(reader, 2):
        if not row or not any(v.strip() for v in row):
            continue
        if len(row) != 3:
            raise ValueError(f'Ligne {number} : trois colonnes attendues.')
        item = dict(zip(header, [v.strip() for v in row]))
        kind = item['word/expression'].lower()
        if not item['french'] or not item['espanol'] or kind not in ('word', 'expression'):
            raise ValueError(f'Ligne {number} : traductions requises et type word ou expression.')
        if any(len(v) > 2000 for v in row):
            raise ValueError(f'Ligne {number} : texte trop long (2 000 caractères maximum).')
        result.append((item['french'], item['espanol'], kind))
    if not result:
        raise ValueError('Le fichier ne contient aucun mot.')
    return result

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'static'), **kwargs)

    def json_response(self, value, status=200):
        payload = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if urlparse(self.path).path == '/api/data':
            with connect() as db:
                self.json_response({'verbs':VERBS, 'tenses':TENSES, 'pronouns':PRONOUNS,
                    'conjugations':[dict(r) for r in db.execute('SELECT * FROM conjugations')],
                    'vocabulary':[dict(r) for r in db.execute('SELECT * FROM vocabulary ORDER BY id')],
                    'grammar':GRAMMAR})
        elif self.path.startswith('/api/'):
            self.json_response({'error':'Page introuvable'}, 404)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != '/api/vocabulary/import':
            return self.json_response({'error':'Page introuvable'}, 404)
        # Only same-origin browser requests may change the local database.
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
            return self.json_response({'error':'Origine non autorisée'}, 403)
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host', ''):
            return self.json_response({'error':'Origine non autorisée'}, 403)
        try:
            size = int(self.headers.get('Content-Length', 0))
            if not 0 < size <= 2_000_000:
                raise ValueError('Le fichier doit faire moins de 2 Mo.')
            rows = parse_csv(self.rfile.read(size).decode('utf-8-sig'))
            with connect() as db:
                before = db.total_changes
                db.executemany('INSERT OR IGNORE INTO vocabulary(french,espanol,kind) VALUES (?,?,?)', rows)
                added = db.total_changes - before
            self.json_response({'added':added, 'duplicates':len(rows)-added})
        except (ValueError, UnicodeError, csv.Error) as exc:
            self.json_response({'error':str(exc)}, 400)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    init_db()
    print(f'Espagnol → http://localhost:{args.port} (Ctrl+C pour arrêter)', flush=True)
    try:
        ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\nÀ bientôt !')
