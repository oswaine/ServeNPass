# Serve & Pass

A local volleyball team stat tracker with a responsive dashboard, player roster, game history, courtside logging, undo, player summaries, and CSV export.

## Run

Requires Python 3. No packages or accounts needed.

```sh
python3 server.py
```

Open http://localhost:8000. Add players in Team roster, create a game, then select a player and log touches. Passing uses 0–4 in 0.5 increments. Serving uses make/miss plus a 0–4 receive difficulty rating in 0.5 increments. Missed serves count toward serve success but are excluded from average serve difficulty. Each touch belongs to a game and set. Finish a game to keep its summary in history.

Data is saved in `data/volleyball.db` (SQLite), independently of browser storage. Back up that file while the app is stopped. The app binds to localhost and is intended for one local team workspace. Use `PORT=8001 python3 server.py` to choose a different port.

The interface uses optional Google Fonts with system fallbacks. All stats and application behavior work without external services.
