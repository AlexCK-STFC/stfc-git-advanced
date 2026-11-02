---
title: Setup
---

This workshop is hands-on. You will type every command yourself, so please
work through this page **before the first session**. It takes about 30 minutes,
longer if you need to install things.

If you get stuck, email us and we will help you before the day. You will
also have time at the start of the first session, but we'd rather spend it on git.

## Is this workshop for you?

This is a follow-up to a beginner course and goes quicker. Read through these
statements. You should be able to say **yes to most of them**.

- [ ] I have used git on my own in the last month (not just in a workshop).
- [ ] I can create a repository (`git init`) or clone one (`git clone`).
- [ ] I can stage and commit changes (`git add`, `git commit`) and know what the staging area is for.
- [ ] I can read `git status` and understand what it tells me.
- [ ] I can look at history with `git log` (and `git diff`).
- [ ] I can create a branch and switch between branches.
- [ ] I have pushed to a remote such as GitHub and pulled from it.
- [ ] I have opened a pull request on GitHub.
- [ ] I have merged one branch into another.
- [ ] I have seen a merge conflict (you don't need to be good at fixing them!).

**Not sure about a few of them?** That's fine. Pick up the ones you missed in the
[Software Carpentry git lesson](https://swcarpentry.github.io/git-novice/), which
takes a couple of hours, and then come back.

**Already comfortable with all of that, and with some rebasing?** You're welcome too.
You will still pick up new tricks, and we like having experienced people in the room.

You do **not** need to have used `git rebase` before. Most people haven't, and that
is what we will learn.

## What you need

Tick these off as you go.

### 1. Git

- [ ] Git is installed, **version 2.30 or newer**. Check with:

```bash
git --version
```

::::::::::::::::: spoiler

### Windows

Install [Git for Windows](https://gitforwindows.org/). It comes with **Git Bash**, which is the
terminal we will use. Leave the default options selected, **except**: if it asks about the
default editor, choose *Visual Studio Code* (once you have installed it, below).

:::::::::::::::::::::::::

::::::::::::::::: spoiler

### macOS

Open Terminal and run `git --version`. If git isn't installed, macOS offers to install
the command line developer tools. Say yes. Or, if you use Homebrew: `brew install git`.

:::::::::::::::::::::::::

::::::::::::::::: spoiler

### Linux

Install it with your package manager, for example `sudo apt install git`.

:::::::::::::::::::::::::

### 2. Visual Studio Code

We will use VS Code as our editor, our terminal and for a graphical view of git.

- [ ] VS Code is installed ([download](https://code.visualstudio.com/)).
- [ ] The `code` command works in your terminal. Check with:

```bash
code --version
```

::::::::::::::::: spoiler

### If `code` isn't found

- **Windows:** re-run the VS Code installer and make sure *Add to PATH* is ticked. Then open a new terminal.
- **macOS:** open VS Code, press `Cmd+Shift+P`, type "shell command", and choose
  *Shell Command: Install 'code' command in PATH*. Then open a new terminal.
- **Linux:** this is normally set up by the installer. If not, reinstall from the `.deb`/`.rpm`.

:::::::::::::::::::::::::

- [ ] You can open a terminal *inside* VS Code (`Ctrl+\``, or *Terminal > New Terminal*).
  On Windows, use the dropdown next to the `+` to choose **Git Bash**. We will work from here.

### 3. Python

`peakfinder`, the project we'll work on, is a small Python package that finds peaks in
spectra. You don't need to be a Python expert, and we won't be writing anything clever.

- [ ] Python **3.10 or newer** is installed:

```bash
python --version
```

(Some systems call it `python3`.) If you don't have it, we recommend
[uv](https://docs.astral.sh/uv/getting-started/installation/), which installs Python for you
and is what we use. Conda works as well.

### 4. A GitHub account

- [ ] You have a [GitHub](https://github.com/) account, and you can sign in.
- [ ] You can **push** from your computer to GitHub. This is the step that catches people out.
  GitHub no longer accepts your password on the command line. You need one of:
  - the [GitHub CLI](https://cli.github.com/): install it, then run `gh auth login` and follow the prompts (easiest), or
  - an [SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), or
  - a [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) used as your password.

You will test this in step 6.

### 5. Configure git

Run these commands once. They are settings that make the commands we use in the workshop
work smoothly. We'll explain what each does in the workshop itself. They are **preferences, not rules**: many people use git's defaults, so you don't need to keep
them afterwards, though you may find you want to.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main

git config --global core.editor "code --wait"
git config --global pull.rebase true
git config --global rebase.autoSquash true
git config --global push.autoSetupRemote true
```

Use the same email address as your GitHub account (or your GitHub
[no-reply address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address)).

- [ ] Those commands ran without errors.
- [ ] `git config --global --list` shows your name, email and the settings above.

The `core.editor` line matters. Without it git opens a terminal editor called **vim**, which
is hard to leave if you've never used it. If that ever happens, type `:q!` and press Enter.

### 6. Get the project

<!-- FIXME: replace with the real repository URL once published. -->

- [ ] Fork the workshop repository on GitHub: **FIXME-ORG/peakfinder** (use the *Fork* button, top right).

  **Important:** on the "Create a new fork" page, make sure **"Copy the `main` branch only" is UNTICKED**.
  It is ticked by default. We need the other branches (and the tags) for the exercises.

  <!-- FIXME: add a screenshot of the fork page once the real repo exists (learners/fig/fork-untick.png) -->
- [ ] Clone **your fork** (not the original). Replace `YOUR-USERNAME`:

```bash
git clone https://github.com/YOUR-USERNAME/peakfinder.git
cd peakfinder
code .
```

- [ ] Check you got all the branches and tags. You should see several `origin/` branches
  (including `origin/background-subtraction` and `origin/colleague/normalise-modes`) and two tags:

```bash
git branch -r
git tag
```

```output
v0.1.0
v0.2.0
```

  If you only see `origin/main`, your fork copied just one branch. The quickest fix is to delete the fork
  (*Settings* > *Delete this repository*, at the bottom) and make it again with the box unticked.

- [ ] Turn on GitHub Actions for your fork. Forks start with Actions switched off. Open the **Actions** tab of your
  fork and click **"I understand my workflows, go ahead and enable them"**. (There's nothing to run yet. We'll
  need this on day 2.)
- [ ] Create a virtual environment and install the requirements:

::::::::::::::::: spoiler

### With uv (recommended)

```bash
uv venv
source .venv/bin/activate        # on Windows Git Bash: source .venv/Scripts/activate
uv pip install -r requirements.txt
```

:::::::::::::::::::::::::

::::::::::::::::: spoiler

### With python and pip

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
```

On Debian or Ubuntu you may first need `sudo apt install python3-venv`.

:::::::::::::::::::::::::

::::::::::::::::: spoiler

### With conda

```bash
conda create -n peakfinder python=3.12
conda activate peakfinder
pip install -r requirements.txt
```

:::::::::::::::::::::::::

- [ ] The tests pass:

```bash
pytest
```

```output
============================= test session starts ==============================
...
============================== 6 passed in 0.8s ===============================
```

- [ ] You can see a plot. This should open a window with a spectrum and red dots on it:

```bash
python -m peakfinder.cli data/example_spectrum.csv --plot
```

If no window appears (for example you are on a remote machine) save the plot instead,
and open the image file in VS Code:

```bash
python -m peakfinder.cli data/example_spectrum.csv --save-plot spectrum.png
```

- [ ] You can **push to your fork**. Make sure authentication works by running:

```bash
git push
```

It should say `Everything up-to-date`. If it asks for a password, or says authentication
failed, go back to step 4.

## Check you're ready

You should be able to say yes to all of these:

- [ ] `git --version` prints 2.30 or newer
- [ ] `code --version` prints a version
- [ ] `git config --global core.editor` prints `code --wait`
- [ ] You've cloned **your fork** of `peakfinder`, and `git tag` shows `v0.1.0` and `v0.2.0`
- [ ] GitHub Actions is enabled on your fork
- [ ] `pytest` passes in your clone
- [ ] `git push` works without errors

## Troubleshooting

**My fork only has the `main` branch.**
You left "Copy the `main` branch only" ticked when forking. Delete the fork and make it again.

**I'm stuck in a strange editor in the terminal (vim).**
Press `Esc`, then type `:q!` and press Enter. Then set `core.editor` as in step 5.

**`code` isn't found, or git doesn't wait for VS Code.**
See step 2. The `--wait` in `core.editor` is what makes git wait until you close the tab.

**`pytest` says `ModuleNotFoundError`.**
Your virtual environment probably isn't active. Run the `source .venv/bin/activate` line again.
You should see `(.venv)` at the start of your terminal prompt.

**My laptop is locked down and I can't install things.**
Tell us in advance. We are working on an alternative, so you can use a hosted environment instead.

<!-- FIXME: decide the fallback (JupyterHub / Git Bash only) and describe it here -->
