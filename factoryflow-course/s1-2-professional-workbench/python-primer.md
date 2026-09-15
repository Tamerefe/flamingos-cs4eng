# Python in an hour — the parts you actually need this week

**Keep this open in a tab all week.** It is a reference, and nobody expects you to read it end to end this morning.

Everything here is in `factory_analysis.py`, the script on your screen right now. That is deliberate: this is not a language tour, it is an explanation of the code you are already looking at, and of the code you will read for the next three days.

If you have written MATLAB, VBA, or a formula-heavy Excel sheet, you have done most of this already under other names.

---

## 1 · What a program is made of

Five things. That is the whole list, and every program you see this week is some arrangement of them.

|                |                                      | In the legacy script                   |
| -------------- | ------------------------------------ | -------------------------------------- |
| **Values**     | the data itself                      | `1.7`, `"RUN"`, `0`                    |
| **Names**      | labels you stick on values           | `path`, `df`, `temp2`                  |
| **Decisions**  | do this only if that                 | `if s == "RUN":`                       |
| **Repetition** | do it again for the next one         | `for i in range(len(df)):`             |
| **Calls**      | run something somebody already wrote | `pd.read_csv(path)`, `round(avail, 1)` |

When a file looks impenetrable, it is usually because all five are on the same screen with bad names. It is still only those five.

---

## 2 · Values have a type, and the type decides what happens

Every value in Python is of some type, and the type is what decides whether `+` means *add* or *glue together*.

| Type    | What it is                     | Written as           |
| ------- | ------------------------------ | -------------------- |
| `int`   | a whole number                 | `42`, `0`, `-7`      |
| `float` | a number with a decimal point  | `1.7`, `4.0`, `68.0` |
| `str`   | text, "a string of characters" | `"RUN"`, `'M-01'`    |
| `bool`  | true or false                  | `True`, `False`      |
| `None`  | *nothing is here*              | `None`               |

Text that looks like a number is still text:

```python
"42" + 1        # TypeError — Python refuses to guess
"42" + "1"      # "421"      — two strings glued together
42 + 1          # 43
```

**This is the single most common cause of a wrong number in engineering data.** Your CSV is text. Everything read out of it starts as text, and somebody has to turn it into a number. In the legacy script, that somebody is this line:

```python
t = float(str(row["temperature_c"]).replace(",", "."))
```

Read it inside out: take the temperature, force it to text, swap the German decimal comma for a point, then turn *that* into a float. Written by somebody who opened the file once, saw `21,4`, and fixed it where it hurt.

Two more worth knowing:

- `7 / 2` is `3.5` — division always gives you a float. `7 // 2` is `3`.
- `NaN` ("not a number") is what pandas puts where a value is missing. It is not zero, and any arithmetic touching it gives `NaN` back. You will meet it on day 2 and it is the reason S2.2 exists.

Ask Python what it is holding whenever you are unsure:

```python
type(t)         # <class 'float'>
```

---

## 3 · Names are labels, not boxes

```python
n = 0
n = n + 1       # read the right side first, then move the label
```

`=` means *give this name to that value*. `==` means *are these two the same?* Mixing them up is a rite of passage and Python will tell you.

A name can be re-pointed at anything at any time, which is exactly why bad names are expensive. In the legacy script, `temp` counts warm rows and `temp2` counts hot rows, `l` and `g` are run minutes and planned minutes, and `tempo` holds a quality percentage. Nothing is wrong with the code. It is simply unreadable, and being unreadable is what makes it unfixable.

**That is the whole argument of S1.4 this afternoon.** The names are the documentation.

Conventions this week: `snake_case` for names, `UPPER_CASE` for constants that never change, and names that say what the thing is (`run_minutes`, not `l`).

---

## 4 · Containers: holding more than one thing

| Container | What it is                           | Written as            | Get one out      |
| --------- | ------------------------------------ | --------------------- | ---------------- |
| **list**  | an ordered row of things, changeable | `[1, 2, 3]`           | `things[0]`      |
| **dict**  | labelled drawers, look up by name    | `{"machine": "M-01"}` | `row["machine"]` |
| **tuple** | a list that cannot be changed        | `(48.1, 11.6)`        | `point[0]`       |
| **set**   | unordered, no duplicates             | `{"RUN", "IDLE"}`     | ask `in`         |

```python
a = []                  # an empty list
a.append([m, sh, run])  # add one row to the end
len(a)                  # how many are in it
a[0]                    # the first one
a[-1]                   # the last one
```

**Counting starts at zero.** `a[0]` is the first element and `a[3]` is the fourth. Every off-by-one bug in software has this at the bottom of it, including one of the three you will hunt on Thursday.

A **dict** is the one that clicks last and matters most. It is a lookup table: you ask for a value by its label rather than by its position.

```python
row["machine_state"]     # the value filed under "machine_state"
```

That is why `row["timestamp"]` reads the way it does in the script — each row of the CSV behaves like a dict whose keys are the column headers.

A **DataFrame** (`df`) is pandas' container: a whole table, with named columns, that knows how to do arithmetic on all its rows at once. Day 2 is about that last part.

---

## 5 · Decisions

```python
if state == "RUN":
    ...
elif state == "IDLE":
    ...
else:
    ...
```

`elif` is checked only when the `if` above it was false, and `else` catches everything left. The comparisons are `==`, `!=`, `<`, `>`, `<=`, `>=`, and you join them with `and`, `or`, `not`.

Python also treats some values as false without being `False`:

| Counts as false               | Counts as true          |
| ----------------------------- | ----------------------- |
| `False`, `None`, `0`, `0.0`   | any other number        |
| `""` (empty text)             | any non-empty text      |
| `[]`, `{}` (empty containers) | any non-empty container |

So `if readings:` means *if there are any readings at all*. Convenient, and occasionally a trap: a real measurement of `0.0` is false, which has cost more than one engineer an afternoon.

---

## 6 · Repetition

```python
for row in rows:          # do this once per row
    print(row)
```

Read `for` as *for each*. The name after it is a fresh label pointing at one item per pass.

The legacy script does it the other way round, by position:

```python
for i in range(len(df)):
    row = df.iloc[i]
```

That works. It is also thirty times slower than asking pandas for the whole column at once, which is the day-2 word **vectorisation** and the reason the script takes half a minute to do something a modern machine should do instantly.

`while` repeats until a condition stops being true. You will barely use it this week.

---

## 7 · Indentation is the syntax

```python
if v > 1.7:
    n = n + 1           # inside the if
n = n + 1               # always, regardless
```

Most languages use braces. Python uses the indent itself: four spaces, and everything at that depth belongs to the block above. Get it wrong and the program either refuses to start or quietly does something else. VS Code indents for you — let it.

---

## 8 · Functions: naming a piece of work

```python
def availability(run_minutes, planned_minutes):
    """How much of the planned time the machine was actually running."""
    return run_minutes / planned_minutes * 100
```

| Part                 | What it is                                         |
| -------------------- | -------------------------------------------------- |
| `def`                | "I am defining one"                                |
| `availability`       | the name you call it by later                      |
| `(run_minutes, ...)` | **parameters** — what it needs to do its job       |
| `"""..."""`          | the **docstring**: what it is for, in one sentence |
| `return`             | the answer it hands back                           |

You call it with **arguments**: `availability(1830, 2160)`.

**`return` and `print` are different things**, and confusing them is the most common beginner bug there is. `print` puts characters on your screen and throws them away. `return` hands a value back to whoever asked, so something else can use it. A function that prints instead of returning cannot be tested, reused, or put behind an API — which is three of the next four sessions.

The legacy script computes availability three times, by copy-paste, with the third copy subtly different. Writing it once as a function is S1.4 and it is the whole point of the afternoon.

---

## 9 · Objects, methods and classes

You have been using objects since the first line of the script.

```python
df.sum()            # ask the DataFrame to add itself up
"M-01 ".strip()     # ask the string to trim its own whitespace
a.append(row)       # ask the list to take one more
```

Read the dot as **"of"** or **"belonging to"**. An **object** is a value that carries its own functions around with it. Those attached functions are called **methods**; the values it keeps are its **attributes**.

A **class** is the blueprint a type of object is stamped out of:

```python
class Machine:
    def __init__(self, machine_id, line):
        self.machine_id = machine_id     # the data this one carries
        self.line = line

    def label(self):                      # something it can do
        return f"{self.machine_id} on line {self.line}"

m = Machine("M-01", "A")                  # one instance, made from the blueprint
m.machine_id                              # "M-01"
m.label()                                 # "M-01 on line A"
```

- `__init__` runs once when the object is made; it is where the data goes in.
- `self` is the object talking about itself. Every method gets it first.
- `Machine` is the class. `m` is an **instance** of it.

**How much of this do you need?** You will *use* objects constantly this week and *write* a class twice — in S2.3, where the shape of every API response is declared as one:

```python
class Machine(BaseModel):
    machine_id: str
    line: str
```

Five lines, and FastAPI uses them to validate the data, generate the documentation, and produce the JSON. That is the honest case for classes: when data and the rules about that data belong together, put them together.

---

## 10 · Modules, packages and libraries

```python
import pandas as pd           # the whole library, under a short name
from datetime import datetime # one specific thing out of it
```

| Word                    | What it means                                          |
| ----------------------- | ------------------------------------------------------ |
| **module**              | one `.py` file                                         |
| **package**             | a folder of modules that imports as one thing          |
| **library**             | a package somebody else wrote and published            |
| **dependency**          | a library your code cannot run without                 |
| **virtual environment** | a box holding exactly the libraries this project needs |

`pandas` is a library. `pd.read_csv` is a function inside it. The `as pd` is a nickname, and it is a convention rather than a rule — everyone writes `pd`.

The reason one of the two demo laptops said `ModuleNotFoundError` this morning is that the library was not in the box that machine was using. Making the box reproducible is S1.5, at four o'clock.

---

## 11 · Type hints: reading the signature

From day 2 onwards, every function you read looks like this:

```python
def quality(readings: pd.DataFrame) -> float:
```

Read it as a sentence: *quality takes a DataFrame called readings and gives back a float.* The `:` annotates what goes in, the `->` says what comes out.

| Hint            | Means                                  |
| --------------- | -------------------------------------- |
| `x: int`        | a whole number goes here               |
| `-> float`      | a decimal number comes back            |
| `float \| None` | a float, **or** nothing at all         |
| `list[dict]`    | a list, and every item in it is a dict |

Python does not enforce any of it. They are there for the person reading, and for the editor, which uses them to catch your mistake before you run anything. **You will read a great many of these and write very few.**

---

## 12 · When it goes wrong

An **exception** is Python stopping because it cannot continue. The **traceback** is the route it took to get there: read the last line first (*what* went wrong), then find the topmost line naming your own file (*where you caused it*). The rest is scenery inside somebody else's library.

You can catch one deliberately:

```python
try:
    t = float(row["temperature_c"])
except ValueError:
    t = 0.0                     # a sensible fallback, chosen on purpose
```

The legacy script does this instead:

```python
try:
    ts = datetime.datetime.strptime(row["timestamp"], "%Y-%m-%dT%H:%M:%S")
except:
    pass
```

`except:` with nothing after it means *if anything whatsoever goes wrong, do nothing and carry on*. Every bad row in that file is silently skipped, nobody is ever told, and the report still prints a confident number at the end.

**A program that hides its failures is worse than one that crashes**, because a crash is information and a wrong number is not. Thursday morning is ninety minutes on exactly this.

---

## 13 · Three ways to write the same program

You will hear these words. They describe *styles*, and Python lets you mix all three in one file.

| Style                        | The idea                                                   | Where you see it this week                                     |
| ---------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| **Procedural**               | a list of steps, in order: do this, then this              | `factory_analysis.py`, top to bottom                           |
| **Object-oriented**          | things that carry their own data and know what they can do | the pydantic models in S2.3; a DataFrame                       |
| **Functional / declarative** | describe the result you want, let the library work out how | `df.groupby("shift").sum()` — and every SQL query ever written |

The same job in all three:

```python
total = 0                          # procedural
for row in rows:
    total = total + row["units"]

total = readings["units"].sum()    # declarative — pandas does the loop
```

Neither is more correct. The second is shorter, faster, and says *what* rather than *how*, which is why day 2 spends a morning on it.

The finished FactoryFlow application you build this week is mostly plain functions, with classes at the edges where data crosses the network, and declarative pandas in the middle. That mixture is normal professional Python.

---

## 14 · How code grows up

The three days follow this ladder exactly, one rung at a time.

|                 | What it is                                                       | When                         |
| --------------- | ---------------------------------------------------------------- | ---------------------------- |
| **script**      | one file you run by hand                                         | what you have at 09:30 today |
| **module**      | one file with named functions, importable by others              | S1.4, this afternoon         |
| **package**     | a folder of modules, installable, with its dependencies declared | S1.5, at 16:00               |
| **application** | a package with an interface — a CLI, an API, a dashboard         | day 2                        |
| **service**     | an application somebody else can run, anywhere, with tests       | day 3                        |

Nothing on that ladder is more *clever* than the rung below it. Each one adds a specific thing that the rung below could not do.

---

## 15 · Small things that save you an hour

| **f-strings**                      | `f"Shift {name}: {value:.1f} %"` — put values inside text. Far better than the `"a" + str(b)` glue in the legacy script.                                            |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Comments**                       | `#` to the end of the line. Say *why*, never *what* — the code already says what.                                                                                   |
| **Docstrings**                     | `"""..."""` under a `def`. What it is for, in one sentence.                                                                                                         |
| **`None` vs `0` vs `""` vs `NaN`** | *nothing here* · *a measured zero* · *empty text* · *missing number*. Four different facts. Confusing them is how a factory reports 0 % quality on an idle machine. |
| **Case matters**                   | `Row` and `row` are two different names, always.                                                                                                                    |
| **Text is immutable**              | `"M-01 ".strip()` hands back a new string. The original is unchanged unless you re-assign it.                                                                       |
| **`in`**                           | `if state in ("RUN", "IDLE"):` — reads exactly as it sounds.                                                                                                        |
| **`if __name__ == "__main__":`**   | *only do this when the file is run directly, not when it is imported*. You will meet it in S1.4.                                                                    |
| **`Ctrl` + `C`**                   | stops a running program.                                                                                                                                            |
| **The empty line**                 | Python does not care. Your reader does.                                                                                                                             |

---

## 16 · The words, in one table

People will use these in front of you all week without stopping to define them.

| Word             | Plain English                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------- |
| **variable**     | a name pointing at a value                                                                  |
| **expression**   | anything that produces a value: `2 + 2`, `df["units"].sum()`                                |
| **statement**    | one instruction: an assignment, an `if`, a call                                             |
| **block**        | the indented lines under an `if`, a `for`, or a `def`                                       |
| **call**         | running a function: the `()` is the calling                                                 |
| **argument**     | the value you hand a function when you call it                                              |
| **parameter**    | the name the function knows that value by, inside                                           |
| **return value** | what the function hands back                                                                |
| **method**       | a function belonging to an object: `df.sum()`                                               |
| **attribute**    | a value belonging to an object: `df.columns`                                                |
| **instance**     | one object made from a class                                                                |
| **iterable**     | anything a `for` loop can walk through                                                      |
| **mutable**      | can be changed after it is made (a list is; text is not)                                    |
| **exception**    | the error Python raises when it cannot continue                                             |
| **library**      | code somebody else wrote that you import                                                    |
| **API**          | the set of calls a piece of software offers you. Also, on day 2, a URL you can ask for data |

---

## 17 · Where each of these turns up

| Session          | What you will actually need from here                             |
| ---------------- | ----------------------------------------------------------------- |
| **S1.2** (now)   | §1–§6. Enough to read the script without flinching                |
| **S1.4** (14:00) | §3 names, §8 functions. The whole session is those two            |
| **S1.5** (16:00) | §10 packages and the environment                                  |
| **S2.2**         | §4 containers, §6 repetition and why vectorisation beats the loop |
| **S2.3**         | §9 classes, §11 type hints                                        |
| **S3.2**         | §12 exceptions, and why a silent failure is the expensive kind    |

---

**One last thing.** Nobody holds all of this in their head. Professionals look up the same four things every week and the good ones are simply fast at looking them up. Being able to read code, know what kind of thing you are looking at, and ask the right question about it is the skill — and after three days you will have it.
