import json, sqlite3, os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
BASE = Path(__file__).resolve().parent
DB = BASE / 'data' / 'volleyball.db'
DB.parent.mkdir(exist_ok=True)
def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    return db
with connect() as db:
    db.executescript('''CREATE TABLE IF NOT EXISTS players(id INTEGER PRIMARY KEY, name TEXT NOT NULL, number INTEGER NOT NULL, position TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS games(id INTEGER PRIMARY KEY, opponent TEXT NOT NULL, date TEXT NOT NULL, location TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT 'live');
    CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, game_id INTEGER REFERENCES games(id), player_id INTEGER REFERENCES players(id), kind TEXT NOT NULL, score REAL NOT NULL, made INTEGER, set_number INTEGER NOT NULL DEFAULT 1, created_at TEXT DEFAULT CURRENT_TIMESTAMP);''')
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(BASE/'static'),**kw)
    def send_json(self, data, status=200):
        body=json.dumps(data).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path == '/api/state':
            with connect() as db: self.send_json({t:[dict(r) for r in db.execute('SELECT * FROM '+t)] for t in ['players','games','events']})
        else: super().do_GET()
    def do_POST(self):
        try:
            d=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
            with connect() as db:
                if self.path == '/api/players':
                    name=str(d['name']).strip(); number=int(d['number']); position=str(d['position'])
                    if not name or not 0<=number<=99: raise ValueError('Enter a name and jersey number from 0 to 99.')
                    db.execute('INSERT INTO players(name,number,position) VALUES(?,?,?)',(name,number,position))
                elif self.path == '/api/games':
                    opponent=str(d['opponent']).strip(); date=str(d['date'])
                    if not opponent or not date: raise ValueError('Opponent and date are required.')
                    cur=db.execute('INSERT INTO games(opponent,date,location) VALUES(?,?,?)',(opponent,date,str(d.get('location',''))))
                    self.send_json({'id':cur.lastrowid}); return
                elif self.path == '/api/events':
                    score=float(d['score']); kind=d['kind']; made=d.get('made'); set_number=int(d['set_number'])
                    if kind not in ['pass','serve'] or score not in [i/2 for i in range(9)] or not 1<=set_number<=5 or (kind=='serve' and made not in [0,1]): raise ValueError('Invalid stat.')
                    if not db.execute("SELECT id FROM games WHERE id=? AND status='live'",(d['game_id'],)).fetchone(): raise ValueError('Game is finished.')
                    db.execute('INSERT INTO events(game_id,player_id,kind,score,made,set_number) VALUES(?,?,?,?,?,?)',(d['game_id'],d['player_id'],kind,score,made,set_number))
                elif self.path == '/api/undo': db.execute('DELETE FROM events WHERE id=(SELECT MAX(id) FROM events WHERE game_id=?)',(d['game_id'],))
                elif self.path == '/api/finish': db.execute("UPDATE games SET status='finished' WHERE id=?",(d['game_id'],))
                else: self.send_json({'error':'Not found'},404); return
            self.send_json({'ok':True})
        except (ValueError,KeyError,sqlite3.Error) as e: self.send_json({'error':str(e)},400)
if __name__=='__main__':
    port=int(os.environ.get('PORT',8000)); print(f'Serve & Pass running at http://localhost:{port}',flush=True); ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
