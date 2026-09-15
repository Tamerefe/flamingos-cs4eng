# S1.2 — The workbench, and the language

**Day 1 · 09:30–11:00 · Your own machine, with your partner next to you.**

You installed everything weeks ago. Today you find out what it is all for: you take a script that came out of somebody else's folder, put it in a folder of your own, and make it run. That is most of the session, and it is the move you repeat at the start of every session for three days. The last ten minutes are about what that script is actually made of.

Everything you need is on screen. Two files sit next to this one, and both are yours for the whole week — open them in tabs now and leave them there:

| [cheatsheet.md](cheatsheet.md)       | every terminal command you need, and what each error message means                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [python-primer.md](python-primer.md) | what the code is made of: types, names, containers, functions, classes, and the words people will say in front of you all week |

You do not have to read the primer today. It is a reference, it is written for somebody who has never written a line of Python, and §17 at the end says which part of it matters before which session.

## Your workbench

One VS Code window, one terminal panel inside it, two folders side by side:

```
cs4eng/                        the folder you cloned into before the workshop
  factoryflow-course/          mine. Read-only. You never write in here.
  factoryflow-legacy/          yours. You make it in step 2.
```

Open VS Code on the folder that holds **both** — `File → Open Folder`, pick `cs4eng` — then open a terminal inside it with ``Ctrl + ` ``(macOS: ``Cmd + ` ``). The terminal opens standing in that folder, which is exactly where you want to be.

> Your folder may have a different name. It is wherever `factoryflow-course` ended up when you cloned it. If you cannot find it: `cd ~`, then `ls`, and look for a name you recognise.

## 0 · Does the workbench work? (5 minutes, everybody)

Three commands. Type them one per line.

```bash
uv --version
pwd
ls
```

You should see a version number, the folder you are standing in, and `factoryflow-course` in the listing.

**Anything missing — say so now, out loud.** This is the one moment today where being stuck costs you nothing, because the rest of the session has not started.

## 1 · Read it before you run it

In the file tree, open:

`factoryflow-course/s1-2-professional-workbench/start/factory_analysis.py`

Two minutes, no talking, just read it. Then tell your partner **one thing about it that would worry you** if you had to change it next week. You do not need to understand the code to answer that.

Nobody expects you to follow this file. It is a couple of hundred lines written by a student in a hurry in 2024, and finding it hard to read is the correct response — that is what the whole of day 1 is about.

## 2 · Make your own folder

First check where you are standing. This is the one mistake worth avoiding today:

```bash
pwd
```

If what it prints **ends in `factoryflow-course`**, you are inside my folder. Step out of it with `cd ..` before you go on. Your folder belongs *next to* mine.

```bash
mkdir factoryflow-legacy
cd factoryflow-legacy
pwd
```

`pwd` now ends in `factoryflow-legacy`. You are standing inside your own folder, and everything from here happens in it.

> This folder is a workbench, and it is not your project. Your project is the repository you create after the break, with a name you pick.

## 3 · Copy the two files in

You are standing in `factoryflow-legacy`. Reach up one level with `..` and pull the files across. `.` at the end means "to here".

```bash
cp ../factoryflow-course/s1-2-professional-workbench/start/factory_analysis.py .
cp ../factoryflow-course/s1-2-professional-workbench/start/production_data.csv .
ls
```

Press `Tab` after every few letters instead of typing those folder names out.

`ls` shows both files. They are now yours — the copies in the course folder stay untouched, and that is the point of copying.

## 4 · Run it

```bash
uv run --no-project --with "pandas<3" python factory_analysis.py
```

**It fails.** That is the exercise. Do not fix anything yet.

## 5 · Read the error

Python prints a wall of text. Almost all of it is inside pandas, which you did not write. Find these two lines:

- the **last line** — what went wrong
- the **topmost line naming `factory_analysis.py`** — where you caused it

Say both out loud to your partner in your own words before you touch the code.

## 6 · Fix it

The script is looking for its data at an address on a laptop that is not yours. The same file is sitting right next to the script, in your folder.

| **Hint 1** | The problem is on one line, near the top of the file. The error message quotes it.      |
| ---------- | --------------------------------------------------------------------------------------- |
| **Hint 2** | `ls` lists the data file. That name is all the script needs to find it.                 |
| **Hint 3** | A path with no folders in it means "next to me". Replace everything between the quotes. |

## 7 · Run it again

```bash
uv run --no-project --with "pandas<3" python factory_analysis.py
```

It takes about half a minute and prints nothing while it works. That is normal.

### Checkpoint

Numbers on your screen, and these three match:

```
134176
Shift A
  Availability   84.3 %
...
Warnings vibration over 1.7: 38578
```

**Say it out loud: the numbers are up.**

Nothing yet, or an error you cannot get past — **say that out loud too**. It is information, and it gets you help faster.

## 8 · What you were just looking at

Ten minutes, together, with the file on the screen. Five things make up every program ever written:

| **Values**     | the data itself — `1.7`, `"RUN"`, `0`                   |
| -------------- | ------------------------------------------------------- |
| **Names**      | labels you put on values — `path`, `df`, `temp2`        |
| **Decisions**  | do this only if that — `if s == "RUN":`                 |
| **Repetition** | now do it for the next one — `for i in range(len(df)):` |
| **Calls**      | run something somebody else wrote — `pd.read_csv(path)` |

That is the whole list. A file looks impenetrable when all five are on one screen with bad names, and it is still only those five.

The rest of it — why `"42" + 1` is an error, what a list and a dict are, what the dot in `df.sum()` means, what a function is for, what a class is, what happens when it breaks — is in [**python-primer.md**](python-primer.md), in plain English, with every example taken from the file in front of you.

**Read §1 to §6 tonight if any of this was new.** Twenty minutes, and tomorrow morning stops being a foreign language.

## Stuck for ten minutes?

Say so out loud. Ten minutes is the limit today. There is a prepared cloud environment that works identically, and moving to it costs you nothing.

## Finished early?

Three things, in this order.

1. **Look at shift C.** One of the four numbers it prints is impossible for a factory. Find it. You do not have to fix it — Thursday afternoon is about exactly that.
2. **Open <!---->**[**python-primer.md**](python-primer.md)**<!----> at §1** and find one example of each of the five in `factory_analysis.py`. Two minutes, and it makes the next session shorter.
3. **You are your table's helper**, with one rule: **hands off other people's keyboards.** Ask them what `pwd` says.
