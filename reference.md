---
title: 'Reference'
---

## The daily loop

The working style from this workshop, in nine steps:

1. **Plan.** What is the overall change? What steps are needed along the way? Those are your commits.
2. **Start from a fresh `main`**, on a new branch: `git switch main`, `git pull`, `git switch -c my-branch`.
3. **Commit small and often**, each commit one idea. Stage just the right lines (VS Code gutter **Stage**).
4. **Spot a mistake in an earlier commit?** `git commit --fixup <hash>`.
5. **Keep up with `main`.** `git fetch`, then `git rebase main`. Don't merge `main` into your branch.
6. **Before you share:** `git rebase -i --autosquash main`. Fold in the fixups, and reword, reorder, drop or edit until it reads well.
7. **Read your own branch** the way a reviewer will (Source Control Graph, or `git log --oneline main..`).
8. **Push** and open a pull request. CI runs. After a rebase: `git push --force-with-lease`.
9. **Respond to review** with fixups. When approved, autosquash, then **Rebase and merge**.

## Command cheat sheet

### Looking

| I want to... | Command |
|---|---|
| see the history as a picture | `git log --oneline --graph --decorate` |
| see what a commit contains | `git show <hash>` |
| see which commits are on my branch | `git log --oneline main..` |
| print a commit as git stores it | `git cat-file -p <hash>` |
| see where `HEAD` has been | `git reflog` |
| see who last changed each line | `git blame <file>` |
| search for text that was added or removed | `git log -S"text" -- <file>` |
| see the history of one function | `git log -L :<function>:<file>` |
| compare two versions of a series of commits | `git range-diff <old>...<new>` |
| find where two branches diverged | `git merge-base <a> <b>` |

### Shaping commits

| I want to... | Command |
|---|---|
| stage part of a file | VS Code diff gutter, or `git add -p <file>` |
| unstage a file | `git restore --staged <file>` |
| discard my edits to a file (lost for good) | `git restore <file>` |
| change the last commit's message or add to it | `git commit --amend` |
| undo the last commit, keep the changes staged | `git reset --soft HEAD^` |
| undo the last commit, keep the changes unstaged | `git reset HEAD^` |
| undo the last commit and throw its changes away | `git reset --hard HEAD^` |
| leave a note to fix an earlier commit later | `git commit --fixup <hash>` |
| tidy up a branch | `git rebase -i --autosquash <base>` |

In the interactive rebase todo list: `pick`, `reword`, `edit`, `squash`, `fixup`, `drop`. Move lines to reorder them. `git rebase --abort` gives up.

### Moving work around

| I want to... | Command |
|---|---|
| move my branch onto the latest `main` | `git rebase main` |
| finish a rebase after resolving a conflict | `git add <file>`, then `git rebase --continue` |
| push after a rebase | `git push --force-with-lease` |
| move `main` forward to another branch (no merge commit) | `git merge --ff-only <branch>` |
| copy one commit onto my branch | `git cherry-pick -x <hash>` |
| put unfinished work aside | `git stash push -m "message"` (add `-u` to include new files) |
| see what's put aside | `git stash list` |
| get it back, and remove it from the list | `git stash pop` |
| get it back, and keep it in the list | `git stash apply` |
| throw the newest one away | `git stash drop` |
| make a second folder with another branch | `git worktree add <folder> <branch>` |

### Finding a bug and releasing

| I want to... | Command |
|---|---|
| find the commit where a test starts failing | `git bisect start <bad> <good>`, then `git bisect good` or `bad` |
| let git run the test for me | `git bisect run pytest -q` |
| leave bisect | `git bisect reset` |
| make a release tag | `git tag -a v1.2.3 -m "message"` |
| send a tag to GitHub | `git push origin v1.2.3` |
| make a branch from a tag | `git switch -c release/1.2 v1.2.0` |

### When it goes wrong

| Situation | What to do |
|---|---|
| a merge, rebase or cherry-pick has gone wrong | `git merge --abort`, `git rebase --abort`, or `git cherry-pick --abort` |
| I lost a commit | `git reflog`, then `git reset --hard <hash>` or `git branch <name> <hash>` |
| I merged by mistake | `git reset --hard ORIG_HEAD` |
| I deleted a branch | `git reflog`, then `git branch <name> <hash>` |
| my push was rejected after a rebase | `git push --force-with-lease` (don't `git pull`) |

## VS Code

| Task | Where |
|---|---|
| Stage lines | diff editor gutter **Stage**, or right-click **Stage Selected Ranges** |
| Amend | **Commit** button dropdown, **Commit (Amend)** |
| Undo last commit | **`...`**, **Commit**, **Undo Last Commit** |
| Branch history | **Source Control Graph** |
| File history | **Timeline** view (Explorer) |
| Blame | Command Palette: **Git: Toggle Git Blame Editor Decoration** |
| Resolve conflicts | **Resolve in Merge Editor**, then **Complete Merge** |
| Stash | Command Palette: **Git: Stash**, **Git: Pop Latest Stash** |
| Cherry-pick | right-click a commit in the graph, **Cherry Pick** |
| Abort | Command Palette: **Git: Abort Merge**, **Abort Rebase**, **Abort Cherry Pick** |

## Glossary

atomic commit
:   A commit that does one logical thing and leaves the project working.

autosquash
:   `git rebase -i --autosquash`: moves each `fixup!` commit under the commit it corrects, and folds it in.

base
:   The commit your branch starts from. Rebasing moves it.

bisect
:   A binary search through history for the first commit where something goes wrong.

blame
:   Shows which commit last changed each line of a file.

branch
:   A movable label that points at a commit.

cherry-pick
:   Copy one commit's change onto another branch, as a new commit.

CI (continuous integration)
:   Automatically running the build and checks on every change, on a clean machine.

commit
:   A snapshot of the whole project, with a message, an author, and a pointer to its parent.

conflict
:   Two sets of changes touch the same lines, so git can't combine them without help.

detached HEAD
:   `HEAD` points straight at a commit rather than at a branch.

fast-forward
:   Moving a branch label forward along a straight line of commits, without creating a merge commit.

fixup
:   A commit marked `fixup!` that is meant to be folded into an earlier commit later.

force with lease
:   `git push --force-with-lease`: overwrite the remote branch, but only if it's still what you last saw.

hash
:   A commit's ID, calculated from its contents and its parent, so changing a commit changes its hash.

`HEAD`
:   A label for where you are now. Usually it points at a branch.

hook
:   A script git runs at certain moments, such as just before a commit.

merge
:   Join two branches with a commit that has two parents.

merge base
:   The commit where two branches diverged.

rebase
:   Replay your commits, one at a time, on top of a new starting point. They become new commits.

reflog
:   Git's private, local diary of where `HEAD` and branches have been.

range-diff
:   Compares two versions of a series of commits, for example before and after a rebase.

squash
:   Combine commits into one. In a rebase, `squash` keeps both messages and `fixup` discards the later one.

staging area
:   Where you assemble the next commit. Also called the index.

stash
:   A drawer for uncommitted changes, so you can set them aside.

tag
:   A label on a commit that never moves. Used for releases.

working tree
:   The files on disk that you're editing.
