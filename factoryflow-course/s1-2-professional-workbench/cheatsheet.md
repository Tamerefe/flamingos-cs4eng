# Terminal cheat sheet

**Keep this open in a tab all week.** Everything here works the same on Windows and macOS.

This sheet is the terminal. For the language itself — types, names, lists and dicts, functions, classes, and what the words mean — see [python-primer.md](python-primer.md) next to it.

## Where am I, and how do I move

| Command      | What it does                                  |
| ------------ | --------------------------------------------- |
| `pwd`        | Where am I standing right now                 |
| `ls`         | What is in here                               |
| `cd name`    | Go into the folder called `name`              |
| `cd ..`      | Go back up one                                |
| `cd ~`       | Go to your user folder, from wherever you are |
| `mkdir name` | Make a new folder called `name` here          |

The prompt is a **place**. Most errors in your first hour are being in the wrong one, and `pwd` answers that in one keystroke.

## Three keys that save you an hour

| Key          | What it does                                                                    |
| ------------ | ------------------------------------------------------------------------------- |
| `Tab`        | Completes the name you started typing. Type `fac`, press Tab.                   |
| `↑`          | Brings back the command you ran before. Press it twice for the one before that. |
| `Ctrl` + `C` | Stops whatever is running right now.                                            |

Use Tab for every folder name you type. It is faster and it cannot misspell.

## Paths are addresses

|              |                                                                                          |
| ------------ | -------------------------------------------------------------------------------------- |
| **Absolute** | `C:\Users\anna\cs4eng\factoryflow-legacy` — the full address, from the top of the tree |
| **Relative** | `factoryflow-legacy` — from where you are standing                                     |
| `.`          | here, the folder I am standing in                                                      |
| `..`         | one level up                                                                           |

A path with a space in it needs quotes: `cd "My Documents"`.

Absolute paths are why the script on your screen fails. `C:\Users\mstudent\Desktop\production_data.csv` is a real address on exactly one laptop in the world.

## Copying a file

```
cp <the file> <where it should go>
```

`.` as the destination means "into the folder I am standing in":

```
cd factoryflow-legacy
cp ../factoryflow-course/s1-2-professional-workbench/start/factory_analysis.py .
```

Dragging the file across in VS Code's file tree does exactly the same thing, and it is a fine way to do it. The terminal version is the one you can write down and send to somebody else.

## Running Python today

One line, all three days:

```
uv run --no-project --with "pandas<3" python factory_analysis.py
```

| Part                         | What it is for                                                      |
| ---------------------------- | ------------------------------------------------------------------- |
| `uv run`                     | run this with the Python and the libraries uv manages               |
| `--no-project`               | there is no project file here yet — that arrives on day 1 afternoon |
| `--with "pandas<3"`          | fetch pandas first if it is missing                                 |
| `python factory_analysis.py` | the thing you actually want to run                                  |

**One command per line.** Joining two with `&&` is a parser error in Windows PowerShell.

## Reading a traceback

Python prints the whole route it took to reach the problem. It is long, and almost all of it is inside libraries you did not write. Two lines matter:

```
Traceback (most recent call last):
  File "factory_analysis.py", line 17, in <module>     <-- your file, your line
    df = pd.read_csv(path)
  File "...\pandas\io\parsers\readers.py", line 1026, in read_csv
  ... six more frames inside pandas ...
FileNotFoundError: [Errno 2] No such file or directory:
    'C:\Users\mstudent\Desktop\production_data.csv'     <-- what went wrong
```

- **The last line** says *what* went wrong.
- **The topmost line that names your own file** says *where you caused it*.

Read the last line first, then jump to your file. The rest is scenery.

## What the message is telling you

| What you see                                              | What it means                                           | What to do                                                |
| --------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| `'uv' is not recognized` / `command not found: uv`        | This terminal window was open before uv was installed   | Close the window completely, open a new one               |
| `FileNotFoundError: 'C:\Users\mstudent\...'`              | The path in the code points at somebody else's machine  | Change it to the name of the file next to your script     |
| `FileNotFoundError: 'production_data.csv'`                | The name is right, you are standing in the wrong folder | `pwd`, then `ls`. Is the file in the list?                |
| `ModuleNotFoundError: No module named 'pandas'`           | You ran plain `python`                                  | Use the full `uv run --no-project --with "pandas<3"` line |
| `cd : Cannot find path ...` / `no such file or directory` | Typo, or that folder is one level up                    | `ls` to see the real names, then Tab-complete it          |
| Nothing happens and you get no prompt back                | It is working. This script takes about half a minute    | Wait. `Ctrl` + `C` stops it if you need to                |
| `running scripts is disabled on this system`              | Windows policy blocks the install script                | Use the `winget` command in SETUP.md instead              |

## When you are completely lost

```
pwd
ls
cd ~
```

Three commands, and you are standing somewhere you recognise. Then walk back down.
