import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import server

class AppTests(unittest.TestCase):
    def test_game_logging_persistence_validation_and_undo(self):
        with tempfile.TemporaryDirectory() as folder:
            original = server.DB
            try:
                source = sqlite3.connect(original)
                server.DB = Path(folder) / 'test.db'
                target = sqlite3.connect(server.DB)
                source.backup(target)
                target.executescript('DELETE FROM events; DELETE FROM games; DELETE FROM players;')
                target.close()
                source.close()
                def post(path, body):
                    h = server.Handler.__new__(server.Handler)
                    data = json.dumps(body).encode()
                    h.path = '/api/' + path
                    h.headers = {'Content-Length': str(len(data))}
                    h.rfile = io.BytesIO(data)
                    result = []
                    h.send_json = lambda body, status=200: result.append((status, body))
                    h.do_POST()
                    return result[0]
                self.assertEqual(post('players', dict(name='Alex', number=12, position='Setter'))[0], 200)
                status, game = post('games', dict(opponent='Wolves', date='2026-11-06'))
                self.assertEqual(status, 200)
                with server.connect() as db:
                    player_id = db.execute('SELECT id FROM players').fetchone()[0]
                base = dict(game_id=game['id'], player_id=player_id, set_number=1)
                for score in [n/2 for n in range(9)]:
                    self.assertEqual(post('events', dict(base,kind='pass',score=score))[0],200)
                self.assertEqual(post('events', dict(base,kind='pass',score=4.5))[0],400)
                self.assertEqual(post('events', dict(base,kind='serve',score=3.5,made=1))[0],200)
                self.assertEqual(post('events', dict(base,kind='serve',score=0,made=0))[0],200)
                # A new connection reads committed records, as after an app restart.
                with server.connect() as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM events').fetchone()[0],11)
                updated = dict(id=player_id, name='Alex Rivera', number=7, position='Libero')
                self.assertEqual(post('players/update', updated)[0], 200)
                with server.connect() as db:
                    saved = dict(db.execute('SELECT * FROM players WHERE id=?', (player_id,)).fetchone())
                    self.assertEqual(saved, updated)
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM events WHERE player_id=?', (player_id,)).fetchone()[0], 11)
                for invalid in [dict(updated, name=' '), dict(updated, number=100)]:
                    self.assertEqual(post('players/update', invalid)[0], 400)
                self.assertEqual(post('players/update', dict(updated, id=999999))[0], 404)
                with server.connect() as db:
                    self.assertEqual(dict(db.execute('SELECT * FROM players WHERE id=?', (player_id,)).fetchone()), updated)
                post('undo', {'game_id':game['id']})
                with server.connect() as db:
                    self.assertEqual(db.execute('SELECT COUNT(*) FROM events').fetchone()[0],10)
                post('finish', {'game_id':game['id']})
                self.assertEqual(post('events',dict(base,kind='pass',score=3))[0],400)
            finally:
                server.DB = original

if __name__ == '__main__':
    unittest.main()
