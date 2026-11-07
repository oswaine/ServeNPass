# Serve & Pass

A local volleyball team stat tracker with a dashboard, player roster, game history, courtside logging, undo, player summaries, and CSV export.

Runs on **Windows, macOS, and Linux** with Python 3 and a web browser. No extra Python packages, database installation, or app account required.

## 1. Get the app

1. Open [the ServeNPass repository](https://github.com/oswaine/ServeNPass). If the repository is private, sign in with a GitHub account that has access.
2. Click **Code → Download ZIP**.
3. Extract the ZIP into a folder you can keep, such as Documents. On Windows, right-click the ZIP and choose **Extract All**. Run the app from the extracted folder, not from inside the ZIP.

If you already use Git, you can clone it instead:

```sh
git clone https://github.com/oswaine/ServeNPass.git
cd ServeNPass
```

## 2. Install or check Python

### Windows

Install Python 3 from [python.org](https://www.python.org/downloads/). If the installer offers **Add Python to PATH**, enable it. Close and reopen your terminal after installation.

Open PowerShell or Windows Terminal and check:

```powershell
py --version
```

If `py` is unavailable, try `python --version`. Use `python` in place of `py` in the Windows commands below if that works.

### macOS

Open **Terminal** (Applications → Utilities) and check:

```sh
python3 --version
```

If Python 3 is missing, install it from [python.org](https://www.python.org/downloads/macos/), reopen Terminal, and run the check again.

### Linux

Open a terminal and check:

```sh
python3 --version
```

If it is missing, install Python 3 with your distribution's package manager. For example:

```sh
# Ubuntu / Debian
sudo apt update
sudo apt install python3
```

```sh
# Fedora
sudo dnf install python3
```

## 3. Start the app

Open a terminal in the extracted project folder: the folder containing `server.py` and `README.md`.

- **Windows:** Open the folder in File Explorer, right-click an empty area, and select **Open in Terminal**. Alternatively, open PowerShell and use `cd` as shown below.
- **macOS / Linux:** Open a terminal and use `cd` to enter the folder. Replace the example path with the actual location of your download.

**Windows (PowerShell):**

```powershell
cd "C:\Users\YourName\Documents\ServeNPass-main"
py server.py
```

**macOS:**

```sh
cd "$HOME/Documents/ServeNPass-main"
python3 server.py
```

**Linux:**

```sh
cd "$HOME/Documents/ServeNPass-main"
python3 server.py
```

If you opened the terminal directly in the project folder, skip the `cd` command. If you cloned the repository, the folder will normally be named `ServeNPass` instead of `ServeNPass-main`.

Leave the terminal running, then open **http://localhost:8000** in your browser. You must start the Python server; opening `index.html` directly will not work.

To stop the app, press **Ctrl+C** in the terminal. To use it again, run the same start command and open the same browser address. Your saved stats will still be there.

## 4. Log your first game

1. Open **Team roster** and add each player's name, jersey number, and position. Use **Edit** on a player card to update these details later; their recorded stats stay attached to the same player.
2. Select **New game**, enter the opponent, date, and optional location, then start the game.
3. Choose the set and player, then select **Passing** or **Serving**.
4. For passing, choose a quality score from **0 to 4 in 0.5 increments** and click **Log pass**.
5. For serving, select **Made** or **Missed**. For a made serve, also choose its difficulty to receive from **0 to 4 in 0.5 increments**, then log the serve.
6. Use **Undo** to remove the most recently logged touch in that game.
7. Select **Finish game** when you are done. Its summary stays in game history; finished games no longer accept new stats.

The dashboard shows overall stats and passing leaders. Each game includes a player breakdown and **Export CSV** for downloading its touch-by-touch records.

Passing averages include all logged passes. Serve success is made serves divided by all serves. Average serve difficulty includes only made serves; misses are excluded from that average.

## Saved data and backups

Stats save automatically after each touch in **`data/volleyball.db`**, a SQLite database created inside the project folder on first launch. Closing the browser or restarting the app does not erase them.

- Keep the project folder in a location where your user account can write files.
- To back up your stats, stop the server with **Ctrl+C**, then copy `data/volleyball.db` to a safe location.
- To move to another computer, stop the server and copy the project folder, including `data/volleyball.db`. Install Python on the new computer and follow the start instructions above.
- When updating the app, keep your existing `data` folder. A fresh download has no copy of your saved stats.
- The database is excluded from Git. Pushing code to GitHub does **not** back up your team data.

The app runs on your computer and is intended for one local team workspace. It does not sync between devices. Internet access is needed to download the app and Python; logging stats works locally afterward. The interface uses optional Google Fonts and falls back to system fonts without internet.

## Troubleshooting

**“Python was not found” or “command not found”**

Install Python using the instructions above and reopen the terminal. On Windows, try `python` if `py` is unavailable. On macOS and Linux, use `python3`.

**“Can't open file … server.py”**

Your terminal is in the wrong folder. Use `cd` to enter the extracted folder containing `server.py`. Put paths containing spaces inside quotation marks.

**The browser cannot connect**

Make sure the server is still running without an error in its terminal. Open `http://localhost:8000`, using `http` rather than `https`. If you choose a different port below, use that port in the browser too.

**Port 8000 is already in use**

Choose another port, such as 8001:

Windows PowerShell:

```powershell
$env:PORT = "8001"
py server.py
```

Windows Command Prompt:

```bat
set PORT=8001
py server.py
```

macOS / Linux:

```sh
PORT=8001 python3 server.py
```

Then open **http://localhost:8001**. The alternate-port setting lasts for that terminal session on Windows; on macOS and Linux, the command applies it only to that launch.

**Permission denied or database is read-only**

Extract or move the app to a writable folder, such as Documents, and start it there. Make sure your user account can write to the project folder and its `data` folder.
