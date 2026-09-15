# S1.3 — Git

**Day 1 · 11:30–13:00 · You work in pairs, on one machine at a time. Swap every 15 minutes.**

By 13:00 you own a repository. It has your name on it, it lives on your GitHub
account, and it remembers everything you did to it.

## The two folders

For the next three days you have exactly two folders:

```text
~/dev/
  factoryflow-course/       mine. Read-only. One folder per session, and every
                            session's starting files come out of it. You never
                            edit inside it.

  <your-repo-name>/         YOURS. Created today. Every commit you make for
                            three days lands here.
```

Files move from the first to the second by being copied, and then committed by
you.

## 1 · Name it (5 minutes, hard stop)

Pick a name for your repository. You keep it after Friday.

- Lowercase letters, numbers and hyphens. No spaces, no umlauts.
- A name you would be happy to show someone.

At 5 minutes, whatever you have is the name.

## 2 · Make the repository

```bash
mkdir ~/dev/<your-repo-name>
cd ~/dev/<your-repo-name>
git init
```

## 3 · Bring the code in

First the script you read this morning, exactly as it reached you:

```bash
cd ~/dev/factoryflow-course/s1-2-professional-workbench/start
cp factory_analysis.py production_data.csv ~/dev/<your-repo-name>/

cd ~/dev/<your-repo-name>
git status                  # git can see them
git add -A
git commit -m "Add the legacy script as we received it"
```

Then the skeleton the rest of the week is built in:

```bash
cd ~/dev/factoryflow-course/s1-3-git/start
cp .gitignore .python-version pyproject.toml README.md SETUP.md ~/dev/<your-repo-name>/
cp -r src tests data ~/dev/<your-repo-name>/

cd ~/dev/<your-repo-name>
git add -A
git commit -m "Add the project skeleton"
```

Those files came out of someone else's folder and are now in yours. **Every
handout for three days arrives exactly this way** — copy, `git status`, commit.

## 4 · Change, look, commit

```bash
# change something small in the script, then:
git diff                    # exactly what you changed
git add -A
git commit -m "..."
git log --oneline           # your history so far
```

Do this until you have **at least three commits**.

### What goes in a commit message

It answers **what changed and why**. The what is already in the diff, so spend
the message on the why.

| | |
| --- | --- |
| Weak | `update`, `fix`, `changes` |
| Strong | `Extract yield calculation into a function — it was duplicated 3x and one copy differed` |

## 5 · Break it on purpose

This is the part that matters. Do it for real.

```bash
# Delete half the script in your editor. Save the file. Look at it.
git restore factory_analysis.py
# Look again.
```

## 6 · Try an idea on a branch

```bash
git switch -c try-different-availability
# change the availability formula, then commit it
git switch main             # look at the file — your change is gone
git merge try-different-availability
```

A branch is a scenario analysis. If the idea is bad, you delete the branch and
lose nothing.

## 7 · Put it on GitHub

1. GitHub → **New repository** → your name → **Private**.
2. Follow the "push an existing repository" lines GitHub shows you.
3. **Settings → Collaborators → Add people →** the facilitator's handle
   (it is on the flipchart).
4. Write your **repository name and URL on the register sheet** on the wall,
   and tick the invite column.

The register is how anyone finds your repo again. Nobody guesses a name like
`bierdeckel-analytics`.

## The six commands that are all of today

| | |
| --- | --- |
| `git status` | What is going on? Type it constantly. |
| `git add` | Choose what goes into the next commit |
| `git commit -m "..."` | Make the save point |
| `git log --oneline` | The history |
| `git diff` | What did I change? |
| `git restore <file>` | Undo my changes to that file |

## Checkpoint

Your repo has ≥ 3 commits, you have recovered a file you destroyed, you have
made and merged a branch, it is on GitHub as private, the facilitator is
invited, and you are on the register.
