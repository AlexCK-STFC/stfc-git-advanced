---
title: "Tooling and Wrap-up"
teaching: 5
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- What small things make these habits quicker?
- Which VS Code features match what we did in the terminal?
- What should I take away and try on Monday?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Create useful git aliases, and know a few settings worth turning on
- Match the commands from the workshop to VS Code's source control features
- Pick one habit to adopt first

::::::::::::::::::::::::::::::::::::::::::::::::

<!--
This episode will probably be SKIMMED, or set as reading afterwards. Nothing later depends on it.
Aliases and settings are deliberately few, commonly used and framed as personal choice (defaults are defaults for a reason).
Tried in a throwaway home directory with Git 2.43: git st, lg, unstage, last, and fetch.prune, rebase.autoStash, merge.conflictStyle zdiff3.
VS Code names come from VS Code's own source control documentation.
-->

## Make the good habits quicker

*This episode is a menu, not a to-do list. Skim it, or read it after the workshop. Everything here is a personal choice.*

An **alias** is a nickname for a git command. Plenty of people use none at all, and typing the full command is perfectly fine. These are some of the ones that are commonly shared, if you'd like a few:

```bash
git config --global alias.st "status -sb"
git config --global alias.lg "log --oneline --graph --decorate"
git config --global alias.unstage "restore --staged"
git config --global alias.last "log -1 --stat"
```

| Type | It runs | You'd use it to |
|---|---|---|
| `git st` | `git status -sb` | a short status, with the branch |
| `git lg` | `git log --oneline --graph --decorate` | see the history as a picture |
| `git unstage <file>` | `git restore --staged <file>` | take a file out of the next commit |
| `git last` | `git log -1 --stat` | see what the last commit changed |

They're stored in your `~/.gitconfig` file. Change them, add your own, and delete the ones you don't use. (VS Code covers a lot of this already, so you may not need any.)

### A word on settings

Git's defaults are the defaults for good reasons, and a lot of the advice about settings online is one person's preference. **Change a setting when you've hit the problem it solves, not before.** The three we asked you to set in the setup
(`pull.rebase`, `rebase.autoSquash` and `push.autoSetupRemote`) suit the workflow in this workshop, but they are preferences too, and many people never change them.

If you want to try something, these three are widely recommended and low-risk:

| Setting | What it does |
|---|---|
| `fetch.prune true` | removes your copies of branches that were deleted on GitHub, so your branch list stays tidy |
| `rebase.autoStash true` | stashes uncommitted changes before a rebase, and puts them back afterwards |
| `merge.conflictStyle zdiff3` | conflict markers also show the *original* version, which makes conflicts easier to understand (needs Git 2.35 or newer) |

Set one with `git config --global <setting> <value>`, and undo it with `git config --global --unset <setting>`.

## VS Code and the terminal

We used both. This table matches what we did to what VS Code offers, so you can use whichever you prefer.

| What we did | In VS Code |
|---|---|
| Stage part of a file (ep 5) | In the diff editor, select lines and use the gutter **Stage** button, or right-click **Stage Selected Ranges** |
| Unstage, or discard changes | the **-** icon, or right-click **Discard Changes** |
| Amend the last commit (ep 5) | the dropdown on the **Commit** button, then **Commit (Amend)** |
| Undo the last commit (ep 5) | **`...`**, then **Commit**, then **Undo Last Commit** |
| Read your branch like a reviewer (ep 7) | the **Source Control Graph**: select a commit, then a file |
| History of one file (ep 10) | the **Timeline** view in the Explorer |
| Blame (ep 10) | **Git: Toggle Git Blame Editor Decoration** in the Command Palette |
| Compare with a branch or tag | right-click a commit in the graph, then **Compare with...** (or **Compare with Merge Base**) |
| Resolve a conflict (ep 9) | **Resolve in Merge Editor**, then **Complete Merge** |
| Stash and restore | **Git: Stash**, **Git: Pop Latest Stash** in the Command Palette |
| Cherry-pick (ep 13) | right-click a commit in the graph, then **Cherry Pick** |
| Give up on a merge, rebase or cherry-pick | **Git: Abort Merge** / **Abort Rebase** / **Abort Cherry Pick** |

And the things that **have no button**, so you use the terminal: `--fixup` commits, **interactive rebase** and `--autosquash`, the **reflog**, **bisect**, `range-diff`, and `--force-with-lease`.
(The **GitLens** extension adds an editor for interactive rebase and more, if you want a graphical version of those.)

## Things we only mentioned

**Stash.** Real work gets interrupted. You're halfway through an edit, and a colleague asks you to look at something on another branch. You can't switch branches with half-finished changes in the way, and you don't want to make a messy commit. **Stash** puts your uncommitted changes in a drawer and gives you a clean working directory:

```bash
git stash push -m "README scratch note"     # put them away, with a label
git stash list                              # what's in the drawer?
git switch main                             # do the other thing...
git switch my-feature                       # ...and come back
git stash pop                               # take the changes out again
```

```output
Saved working directory and index state On my-feature: README scratch note
stash@{0}: On my-feature: README scratch note
```

Some variations: `git stash push -u` also stashes new, untracked files, `git stash apply` is like `pop` but keeps the stash in the drawer, and `git stash drop` throws one away.
In VS Code, run **Git: Stash** (it asks for an optional message) and **Git: Pop Latest Stash** from the Command Palette. **Git: Stash Staged** stashes *only* what's staged, which is `git stash push --staged` and needs Git 2.35 or newer.

**Worktrees.** Sometimes you want two branches checked out at once, such as a release branch for a quick fix while your feature is in the middle of a change. Instead of stashing and switching, make
a second folder for the same repository:

```bash
git worktree add ../peakfinder-hotfix release/0.2
```

You get a new folder with `release/0.2` checked out. Work there, commit, and delete it when you're finished (`git worktree remove ../peakfinder-hotfix`). VS Code can manage worktrees too.

**The merge base.** The *merge base* of two branches is the commit where they diverged: `git merge-base main my-feature`. It's what `git range-diff` and VS Code's **Compare with Merge Base** compare against.

## Take-aways

Nobody does all of this at once. Here are the habits we've covered, roughly in order of how much they give back:

1. **Plan** the change, then the commits.
2. Make commits **atomic**, with messages that say *why*.
3. Use **fixup** for mistakes in earlier commits, and **autosquash** before you share.
4. **Rebase** onto `main` rather than merging `main` into your branch. Push with `--force-with-lease`.
5. Review **your own** branch first, then ask for review.
6. Let **CI** check what a person shouldn't have to.

::::::::::::::::::::::::::::::::::::: challenge

## Challenge: your first step

1. If you like, add an alias or two from the list above, and try them in your `peakfinder` clone. (Or skip this: it's optional.)
2. Decide **one habit** from the take-aways that you'll try on your own work next week. Tell your partner, and say what might get in the way.

Keep it small. One habit that you actually use is worth more than six that you don't.

:::::::::::::::::::::::: solution

There's no single answer. A popular first choice is **fixup and autosquash**, because you can start with it today, on any branch, without anyone else changing what they do.

If you're not sure, try this on your next piece of work: write the commit plan first, make each commit one idea, and run `git lg` before you ask for review to check that it reads like a story.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Where next

- **Pro Git**, the free book, at [git-scm.com/book](https://git-scm.com/book). Chapters 3 (branching), 7 (tools) and 10 (internals) go deeper on everything here.
- **Learn Git Branching**, an interactive game that draws the graphs as you type: [learngitbranching.js.org](https://learngitbranching.js.org).
- **Conventional Commits**, if you want a commit message convention: [conventionalcommits.org](https://www.conventionalcommits.org).
- The [reference page](reference.html) in this lesson has a cheat sheet of the commands and a glossary.
- Come back to the **extras**. We skipped how git stores files (blobs, trees and packfiles). If you're curious, `git cat-file -p` and the "Git Internals" chapter of Pro Git are the place to start.

## Thank you

We'd love to hear what worked and what didn't. <!-- FIXME: add the feedback form link here. -->

::::::::::::::::::::::::::::::::::::: instructor

**This episode is a menu.** It's fine to skip most of it, or to tell people it's there to read afterwards. If you do one thing, do the take-aways and the "one habit" challenge.

**The challenge** is also a quiet way to end. Ask two or three people to share their chosen habit.

**Before you finish:** point people to the reference page, remind them their forks and branches are theirs to keep, and share the feedback link.

**Optional extras for a longer session or a follow-up:** how git stores files (objects, trees, packfiles), `git bisect` with a script on a bigger history, `git rerere` in action, worktrees as an exercise, and a look at a real project's pull requests.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Aliases and settings are personal choices: git's defaults are fine, and you only need to change what's bothering you
- VS Code covers staging, amending, history, blame, conflicts, stash and cherry-pick. Fixup, interactive rebase, the reflog, bisect and `range-diff` need the terminal
- Pick one habit to adopt first. Atomic commits and fixup with autosquash give the most for the least effort

::::::::::::::::::::::::::::::::::::::::::::::::
