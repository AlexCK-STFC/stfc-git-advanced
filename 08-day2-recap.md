---
title: "Day 2 Recap and Warm-up"
teaching: 5
exercises: 4
---

:::::::::::::::::::::::::::::::::::::: questions

- What did we cover yesterday?
- Is everyone ready to start?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Recall the main ideas from day 1
- Check your branch and your fork are as we left them

::::::::::::::::::::::::::::::::::::::::::::::::

<!--
Keep this SHORT (about 10 minutes). The aim is a warm-up and a state check, not a re-teach.
If people are missing their day-1 branch, point them to the fallback below rather than debugging for long.
-->

## Yesterday in one minute

Yesterday we were the **author**. We learned:

- A commit is a **snapshot** with a pointer to its parent, and a branch is just a **label**. Changing a commit makes a *new* one.
- The **reflog** remembers where `HEAD` has been, so we can recover from mistakes.
- Good commits are **atomic**: one logical change, with the project working at every step.
- We can shape commits with the **staging area**, `--amend` and `reset`, and rewrite a branch with **interactive rebase**.
- In our **daily loop** we commit as we go, leave `--fixup` notes for mistakes in earlier commits, and tidy up with
  `git rebase -i --autosquash` before sharing.

Today we're a **collaborator**. Other people's work is landing in the same project as ours, and we need to work with it.

## Warm-up quiz

Try these on your own for a minute or two, then we'll go through them together.

::::::::::::::::::::::::::::::::::::: challenge

## Quiz

1. When you make a new commit, what happens to the branch label?
2. Why does `git commit --amend` give you a different hash?
3. You made a `fixup!` commit for something three commits back. How do you fold it into the right commit?
4. You lost a commit after a mistake. Where do you look to find it?
5. Why do we try to make each commit atomic? Give one reason.

:::::::::::::::::::::::: solution

1. It **moves forward** to the new commit. A branch is just a label that follows the newest commit.
2. A commit's hash is calculated from its contents, including the message and its parent. Change any of that and you get a new
   commit with a new hash.
3. `git rebase -i --autosquash main` (or just `git rebase -i main` if `rebase.autoSquash` is on). It moves the fixup under its
   target and folds it in.
4. The **reflog**: `git reflog`. Find the hash, then `git reset --hard <hash>` or `git branch <name> <hash>`.
5. Any of: it's easier to review one idea at a time; you can revert just the bad change; you can cherry-pick just the fix;
   `git bisect` finds a small, specific commit; each commit passes the tests.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Check your state

Make sure you're ready for today. In your `peakfinder` clone, with your virtual environment active:

```bash
git status
git switch main
git log --oneline -1
git branch
git log --oneline main..feature-prominence      # or feature-widths
```

You should see:

- `git status`: `nothing to commit, working tree clean`
- `main` still at `Add plotting of the spectrum and its peaks` (hash `1e81f27`). If `main` has any extra commits of your own, you can put it
  right with `git reset --hard origin/main`.
- Your feature branch listed, with **three** clean commits and no `fixup!`.

Then check your work is on GitHub. Open your fork in the browser, switch to your feature branch, and check that you can see the three
commits. Ask your partner to look too.

::::::::::::::::::::::::::::::::::::: callout

## If you're missing your feature branch

If your branch is missing, or in a bad state, don't spend long on it. Ask a helper, or build a quick replacement:

```bash
git switch main
git switch -c feature-prominence
```

and redo the three commits from episode 7 (it's fast now that you've done it before). The helpers can also give you a ready-made branch.

::::::::::::::::::::::::::::::::::::::::::::::::

## Today's story

While you were working on your feature, a colleague was working on the same project, and their work has now been approved and merged into `main`.

Today we'll:

1. bring that work into our branch, and deal with the conflict between their changes and ours (episode 9)
2. find out why a test is now failing, and which change caused it (episode 10)
3. have our work reviewed by our partner (episode 11)
4. set up automatic checks (episode 12)
5. release a fix (episode 13)

### Two rules for today

- **Every pull request is on your own fork**, never on the course repository. GitHub proposes the original repository by default, so we'll remind you where it matters.
- **Merge pull requests with "Rebase and merge"**, so your carefully made commits stay exactly as you wrote them.

::::::::::::::::::::::::::::::::::::: instructor

Keep this to about 10 minutes. The quiz can be done by a show of hands, or by cold-calling. Don't let it turn into a lecture.

**State check.** The point is to find the people with a broken day-1 state *before* they hit episode 9. Common problems:

- `main` has local commits, because they committed to it by mistake. `git reset --hard origin/main` fixes it.
- The feature branch still contains `fixup!` commits, so they never ran the autosquash. They can do it now:
  `git rebase -i --autosquash main`.
- They never pushed. `git push`.
- The fork is missing the colleague's branch (they forked with the default-branch-only option). Tomorrow's story needs
  `colleague/normalise-modes`. They can fetch it from the original repository (`git remote add upstream <url>`,
  `git fetch upstream`) and push it to their fork, but it's often quicker to re-fork.

**Fallback branches.** Have a ready-made `feature-prominence` and `feature-widths` available for anyone who lost theirs. These aren't published
to the learners' forks, so give the helpers a way to hand them out.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Day 1 was about producing good history: snapshots, atomic commits, rewriting and the daily loop
- Day 2 is about sharing it and working alongside other people's changes
- Check your branch and your fork are in order before starting

::::::::::::::::::::::::::::::::::::::::::::::::
