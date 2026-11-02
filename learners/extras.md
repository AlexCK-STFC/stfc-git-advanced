---
title: 'Extras'
---

Everything on this page is **optional**. It's for the curious: how git works underneath, how teams organise their branches, and where to read more about the topics in the workshop.

## How git stores your history

In episode 2 we gave you a model that was *good enough*: a commit is a snapshot with a pointer to its parent, and a branch is a label. If you'd like to go further, these are the best things to read, roughly from the most approachable.

- **[Commits are snapshots, not diffs](https://github.blog/open-source/git/commits-are-snapshots-not-diffs/)** (GitHub Blog). The natural next read after episode 2. It shows how git stores your data, and then uses that to explain *why* `cherry-pick` and `rebase` behave as they do. You can follow along with the commands.
- **[Git's database internals I: packed object store](https://github.blog/open-source/git/gits-database-internals-i-packed-object-store/)** (GitHub Blog). The first of a five-part series that treats git as a database, covering how objects are packed on disk so that large histories stay small. A good read if you like data structures.
- **[Pro Git: Git Internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)**, the free book's chapter on the "plumbing" under the commands we use, and its section on **[Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)**.
- **[Git from the inside out](https://maryrosecook.com/blog/post/git-from-the-inside-out)** (Mary Rose Cook). A long essay that builds a repository up from scratch and explains each part as it appears.
- **[Think Like (a) Git](https://think-like-a-git.net/)**, a short guide to the model in your head when you use git.
- **[Learn Git Branching](https://learngitbranching.js.org)**, an interactive game that draws the graphs as you type commands.

## A short guided peek inside `.git`

Want to see it for yourself? Try this in a **scratch repository**, somewhere that isn't your project. Everything git stores is in the hidden `.git` folder.

```bash
git init scratch
cd scratch
echo "hello" > hello.txt
git add hello.txt
git commit -m "Add hello.txt"
```

**Git stores a commit as a small piece of text**, as we saw in episode 2:

```bash
git cat-file -p HEAD
```

```output
tree aaa96ced2d9a1c8e72c56b253a0e2fe78393feb7
author Sam Scientist <sam@example.org> 1736154000 +0000
committer Sam Scientist <sam@example.org> 1736154000 +0000

Add hello.txt
```

(Your commit's hash will differ, as it depends on your name and the time. But the tree hash above will be **exactly the same** for you. We'll see why in a moment.)

The `tree` line points at a **tree**, which is a listing of the files in that snapshot:

```bash
git cat-file -p 'HEAD^{tree}'
```

```output
100644 blob ce013625030ba8dba906f756967f9e9ca394464a	hello.txt
```

Each file's content is stored as a **blob**, named by a hash of its content. Look inside it:

```bash
git cat-file -p ce01362
git cat-file -t ce01362
```

```output
hello
blob
```

So git has just **three kinds of thing**, which point to each other:

```
commit  --->  tree  --->  blob(s)
(message,     (a folder:   (a file's
 parent)       names)       contents)
```

### Names come from content

A hash is calculated from the content. Prove it, by asking git what the hash of the text `hello` would be, without storing anything:

```bash
echo "hello" | git hash-object --stdin
```

```output
ce013625030ba8dba906f756967f9e9ca394464a
```

The same hash as the blob. That's why the **tree hash was identical for you**: the same filename, and the same content, always give the same tree.

It also means git never stores the same content twice. Copy the file and commit it:

```bash
cp hello.txt copy.txt
git add copy.txt
git commit -m "Add a copy"
git cat-file -p 'HEAD^{tree}'
```

```output
100644 blob ce013625030ba8dba906f756967f9e9ca394464a	copy.txt
100644 blob ce013625030ba8dba906f756967f9e9ca394464a	hello.txt
```

Two files, **one blob**. (This is also why renaming a file is cheap in git: the blob doesn't change, only the name in the tree.)

### Where it lives on disk

The objects are files, in folders named by the first two characters of the hash:

```bash
find .git/objects -type f
```

```output
.git/objects/aa/a96ced2d9a1c8e72c56b253a0e2fe78393feb7
.git/objects/ce/013625030ba8dba906f756967f9e9ca394464a
...
```

And a branch is just a file holding a hash, as episode 2 said. (Look at it now, before the next step.)

```bash
cat .git/refs/heads/main
cat .git/HEAD
```

```output
7e54f9edc6537c60e68928dc87d8aa4fdeacb9d3
ref: refs/heads/main
```

(Your first line will be a different hash. It's the hash of your latest commit.)

### Packing

Thousands of tiny files would be slow, so git occasionally **packs** them together, and compresses them. It does this by itself, but you can ask:

```bash
git gc
find .git/objects -type f
```

```output
.git/objects/pack/pack-c4e0561cce725eb9c99eb33ddf09b8060b7debf3.pack
.git/objects/pack/pack-c4e0561cce725eb9c99eb33ddf09b8060b7debf3.idx
...
```

The loose files are now in one `.pack` file. (Git tidies the branch files at the same time, into `.git/packed-refs`, so `cat .git/refs/heads/main` no longer works. That's the packing too.) The first GitHub Blog post above is all about how this works. When you're done, delete the scratch folder.

*These commands were checked with Git 2.43.*

## Branching models and workflows

Teams organise their branches in different ways. We recommended one simple model in this workshop: **short branches off `main`, pull requests, a straight history, and tags for releases**, with a release branch only if you must patch an old version. It's close to what is usually called **GitHub flow**. Three things worth reading:

- **[GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)**, GitHub's own description of a lightweight, branch-based workflow.
- **[A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)** (Vincent Driessen), the post that introduced **git flow**, with its long-lived `develop` branch and separate release and hotfix branches. It became hugely popular. Notably, the author added a note in 2020 reflecting on it: he suggests that teams who do continuous delivery adopt a much simpler workflow, such as GitHub flow, rather than shoehorning git flow in, but says it may still fit software that is explicitly versioned or that must support multiple versions in the wild. It's worth reading the note, whatever you decide.
- **[Trunk-based development](https://trunkbaseddevelopment.com)**, a related approach where everyone works in very short-lived branches (or directly) on one main branch.

The right choice depends on your project: how often you release, and whether you must support old versions. Most research software is nearer the simple end. For a real example of a project's written workflow, see the [NumPy development workflow](https://numpy.org/devdocs/dev/development_workflow.html).

## More on the topics in the workshop

| Topic | Read |
|---|---|
| Good commit messages | [How to Write a Git Commit Message](https://cbea.ms/git-commit/), and [Conventional Commits](https://www.conventionalcommits.org) if you like prefixes |
| Rebasing | [Pro Git: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing), and the [`git rebase` manual](https://git-scm.com/docs/git-rebase) |
| Remembering conflict resolutions | [Pro Git: Rerere](https://git-scm.com/book/en/v2/Git-Tools-Rerere) |
| The reflog | the [`git reflog` manual](https://git-scm.com/docs/git-reflog) |
| Bisect | the [`git bisect` manual](https://git-scm.com/docs/git-bisect) |
| Comparing two versions of a branch | the [`git range-diff` manual](https://git-scm.com/docs/git-range-diff) |
| Two branches checked out at once | the [`git worktree` manual](https://git-scm.com/docs/git-worktree) |
| Version numbers | [Semantic Versioning](https://semver.org) |
| The basics, again | [Software Carpentry: Version Control with Git](https://swcarpentry.github.io/git-novice/) |

## Tools

- **[GitLens](https://github.com/gitkraken/vscode-gitlens)**, a VS Code extension that adds richer blame, file and line history, and a graphical editor for interactive rebase.
- The built-in `git help <command>` shows the manual for any command, for example `git help rebase`.
