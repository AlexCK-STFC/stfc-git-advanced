---
title: 'Instructor Notes'
---

This page is for the people running the workshop. It covers what to prepare, a run-sheet for each day, the solutions and how to rescue someone who is stuck, and how to maintain the lesson. Each episode also has an **Instructor view** box with its own timings, common problems and a bridge to the next episode.

## Before the workshop

**About a week before**

- [ ] **Build and publish the example repository.** Run `python tools/build_starter.py --force`. It builds `build/peakfinder` and checks its own output. Publish only the branches learners need, and **not** the `solution/*` branches:

  ```bash
  cd build/peakfinder
  git remote add origin <the public course repository URL>
  git push origin main background-subtraction colleague/normalise-modes untangle --tags
  ```

  The repository must be **public** (so learners can fork it). Then put its URL in `learners/setup.md`.
- [ ] **Keep the solutions somewhere safe.** Push *everything* (including `solution/*`) to a **private** repository, or keep the `build/` folder on your laptop. Helpers use it to rescue people (see below).
- [ ] **Email learners** the setup page and the self-assessment, and ask them to finish the whole of step 6 (fork, clone, install, tests, push, enable Actions) *before* day 1.
- [ ] **Do a dry run** of both days, on a real GitHub fork, with a colleague as the learner. This is the only way to check the timings and the parts that run on GitHub (the pull request pages, the review buttons and above all the **Actions workflow in episode 12**, which I could check with a linter but not run). Remember to **untick "Copy the default branch only"**.
- [ ] **Prepare for episodes 11 and 12** on your own fork: an example pull request with a few things to comment on (for people without a partner), and the `add-ci` pull request with a **green** run and a **red** run (or screenshots).
- [ ] **Check versions:** Git 2.30 or newer, a current VS Code, and the action versions in the episode 12 workflow (`actions/checkout`, `actions/setup-python`).
- [ ] Add the **feedback link** (episode 14) and the **screenshots** marked `FIXME` (fork page, Source Control, merge editor).
- [ ] **Brief the helpers.** They should read this page, and episodes 6, 7 and 9, and know the rescue commands below. Aim for one helper per 8 learners (online: one per breakout room if you can).

**If you don't use rebase yourself yet.** Many instructors don't, and that's fine. Before teaching it, do the exercises in **episodes 5, 6 and 7** once on your own computer (about an hour), and practise the rescue commands. Everything in the lesson is safe, because of the backup branch and the reflog.

## Day 1 run-sheet

Times assume a 09:00 start and a 15-minute break after episode 4. They come from each episode's own "teaching + exercises" times, so they leave **about 44 minutes of slack** (end 12:16). Follow-along sessions usually run over by a third, so treat the slack as spent.

| Start | Episode | Check before moving on | If you're behind, cut |
|---|---|---|---|
| 09:00 | **01** Welcome and the Story (15 min) | Everyone is on `main` with a clean `git status`; `git branch -r` shows the other branches and `git tag` shows `v0.1.0` and `v0.2.0`; `pytest` passes; `git push` works; partners are collaborators on each other's forks. | Shorten the collaborator-invite walkthrough (email it beforehand). |
| 09:15 | **02** A Mental Model: Snapshots and Labels (22 min) | Nothing to check. Ask: *"what does a branch point at?"* | Skip the `git hash-object` check. |
| 09:37 | **03** Planning and Atomic Commits (23 min) | Everyone has **written down** their list of commits. They need it for episode 6. | Collapse the prefixes callout; shorten the example. |
| 10:00 | **04** The Safety Net: Reflog (15 min) | Everyone ends on `main` with a clean `git status` (no leftover `experiment` branch or README edits). | Skip the knowledge check. |
| 10:30 | *break back (15 min)* | | |
| 10:30 | **05** Shaping a Commit: Staging, Amend, Reset and Restore (27 min) | The `untangle` branch has **two** new commits (`--title`, then the markers), no `DEBUG` print, and `pytest` passes. | Skip the `git add -p` callout and the reset knowledge check. |
| 10:57 | **06** Interactive Rebase: Rewriting a Messy Branch (43 min) | `background-subtraction` has **seven** clean commits; **`main` is unchanged and nobody merged the branch**. | **Don't cut.** If behind, give out the finished todo from the solution earlier. |
| 11:40 | **07** The Daily Loop: Fixup and Autosquash (36 min) | A feature branch (`feature-prominence` or `feature-widths`) is **pushed to the fork**, with three clean commits and no `fixup!`; `main` is unchanged. | Learners watch the short demo instead of typing it. |

## Day 2 run-sheet

A 15-minute break after episode 11. End 12:15, leaving **about 45 minutes of slack**.

| Start | Episode | Check before moving on | If you're behind, cut |
|---|---|---|---|
| 09:00 | **08** Day 2 Recap and Warm-up (9 min) | State check passed: clean tree, feature branch present on the fork. Standing rules said aloud (own fork; Rebase and merge). | Skip the quiz; do the state check only. |
| 09:09 | **09** Rebase vs Merge, and Resolving Conflicts (35 min) | Feature rebased onto `main` (straight line), pushed with `--force-with-lease`, and **one test still fails** (the colleague's). Nobody typed the merge demo. | Skip the merge demo (the diagrams show the double back). |
| 09:44 | **10** Tracking Down a Bug: Blame and Bisect (30 min) | The fix is on `main` (fast-forwarded and pushed), the feature is rebased onto it, and **all tests pass**. | Skip the by-hand bisect demo, then the `log -S/-L` callout. |
| 10:14 | **11** Pull Requests: Authoring and Reviewing (30 min) | A pull request is open **on the learner's own fork** (not the course repo), reviewed by the partner, and a fixup pushed. Finishing is optional. | Skip the Finishing section (squash and merge). |
| 10:59 | *break back (15 min)* | | |
| 10:59 | **12** Catching Problems Early: Shift Left and CI (26 min) | Actions enabled; the `add-ci` pull request has gone green, then red, then green again (or the fallback demo has been shown). | Do the exercise as a demo, or use the fallback. |
| 11:25 | **13** Releases: Versions, Tags and Cherry-pick (35 min) | `release/0.2` and tag `v0.2.1` pushed, with the fix cherry-picked. | Skip the optional GitHub release. |
| 12:00 | **14** Tooling and Wrap-up (15 min) | Each person has named one habit to try. | Read-afterwards: do only the take-aways. |

**The standing rules for day 2** (said once, in episode 8): every pull request is on the learner's **own fork**, and you merge with **Rebase and merge**.

## Solutions

Every exercise has a **solution** box in the episode. The ones people most often need:

| Exercise | Where the answer is | End state to check |
|---|---|---|
| 03 smell test | the solution box (a 7-commit list) | learners wrote their own list |
| 05 untangle | the solution box (VS Code and command line) | `git log --oneline -3` shows two new commits; `git grep DEBUG` is empty |
| 06 rebase 1 and 2 | the solution boxes give the **finished todo lists** | `git log --oneline main..` shows seven commits; `git diff --stat backup/background-subtraction` shows only `scratch_smoothing.py` |
| 07 features A/B | the solution box | three commits, no `fixup!`, `pytest` passes |
| 09 rebase and conflict | the solution box gives the **resolved `find_peaks`** for A and B | straight line, one failing test left |
| 10 the fix | the solution box | `pytest` passes after the second rebase |
| 12 CI | the solution box, and the workflow file in the episode | green, red, then green |
| 13 release | the solution box | tag `v0.2.1` on `release/0.2` |

## Rescuing someone who is stuck

First, the general tools, which cover most problems:

- **`git status`** says what git thinks is happening and what to do next.
- **`git rebase --abort`** (or `git merge --abort`, `git cherry-pick --abort`) puts everything back.
- **`git reflog`** finds a lost commit (episode 4).
- **`git reset --hard origin/<branch>`** puts a branch back to what's on their fork. Use it with care: it throws away local changes.

For specific exercises, helpers need the solutions repository as a remote:

```bash
git remote add solutions <the private solutions repository URL>
git fetch solutions
```

| Problem | Rescue |
|---|---|
| Episode 6: badly tangled, no backup | `git switch -C background-subtraction origin/background-subtraction` starts again from the messy branch. Or, to give them the *finished* branch: `git switch -C background-subtraction solutions/solution/background-subtraction` |
| Episode 7: a lost feature branch | `git switch -C feature-prominence solutions/solution/feature-prominence` (or `feature-widths`) |
| Episode 9: stuck in the conflict | `git rebase --abort`, then redo it, pasting the resolved `find_peaks` from the episode's solution box |
| Episode 10: missed the fix | `git switch main`, then `git cherry-pick solutions/solution/fix-normalise` |
| Their `main` has stray commits | `git switch main`, then `git reset --hard origin/main` (check `origin/main` is the right one) |
| No tags in their fork | They ticked "Copy the default branch only". Re-fork with it unticked, or `git fetch <original repository URL> --tags` |
| Pull request opened against the course repository | Close it, and open it again on their own fork |

## Online delivery

- Put people in **pairs in breakout rooms** for the exercises, and have helpers visit the rooms. Create the rooms before you need them, and keep a list of who is with whom.
- Share your **VS Code with the terminal visible**, at a large font, as people follow your commands.
- Use the chat for **"done" reactions** after each step, so you can see who is behind without stopping.
- Pairs that lose a partner can review the prepared pull request (episode 11) and follow the prepared Actions run (episode 12).

## Looking after the lesson

- **Rebuild the example repository** with `python tools/build_starter.py --force`. It checks that the tests pass and fail where the episodes expect, that the example features conflict with the colleague's work, and that the fix cherry-picks cleanly.
- **Any change under `tools/` changes every commit hash**, even a name or a date. After a rebuild, run `python tools/remap_hashes.py <old hashes file>` to update the hashes quoted in the episodes (the steps are in its docstring).
- **Check the diagrams** with `node tools/check_diagrams/check.mjs` (add `--render <folder>` to draw images). It needs `npm install` once.
- **Check the lesson** with `sandpaper::validate_lesson(".")` in R, and preview it with `sandpaper::serve()`.
