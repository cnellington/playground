# CLAUDE.md: how to add or change a game here

You are helping someone add or edit a game in The Playground, a small arcade of
web games hosted on GitHub Pages. The person you are working with may not be a
programmer. Your job is to do the technical work for them and keep this repo in
good shape, even when they do not ask for the details. Follow the rules below
without being asked.

## The one-paragraph mental model

Every game is a folder under `games/`. A folder has the game itself
(`index.html`) and a small description (`game.json`). A build script reads all
the `game.json` files and generates the front-page list automatically, so you
never edit a shared index by hand. You make changes on a branch, open a pull
request, and a preview link appears so the change can be playtested before it
goes live. Merging to `main` publishes it.

## Hard rules

1. Games are static. HTML, CSS, and JavaScript that run in the browser with no
   server, no database, no API keys, no build step of their own. Loading
   libraries from a CDN (fonts, a game engine, sound) is fine. If a request
   needs a backend, stop and tell the user it cannot be hosted here.

2. One folder per game: `games/<slug>/`. The `<slug>` is lowercase with hyphens
   (`snake-deluxe`, not `Snake Deluxe`). The game's entry point must be
   `games/<slug>/index.html`. Prefer a single self-contained HTML file; if you
   split out assets, keep them inside the game's own folder.

3. Every game folder needs a `game.json`. Required fields:
   ```json
   {
     "title": "Snake Deluxe",
     "slug": "snake-deluxe",
     "tagline": "the classic, now with hats",
     "description": "A one-sentence-to-a-paragraph summary of the game.",
     "added": "2026-06-13"
   }
   ```
   Optional: `"icon"` (an emoji shown if there is no thumbnail) and
   `"thumbnail"` (a PNG/JPG inside the game folder, used as the cover art,
   preferred). The `slug` must match the folder name. `added` is an ISO date
   (`YYYY-MM-DD`). Do not add authorship or tags unless asked.

4. Keep a `games/<slug>/changelog.md` for the game and update it on every
   change. The changelog is game-specific: each game owns its own file, and the
   changelog page renders one section per game. Add a line under the top section
   describing what you did, written for a human reader. Newest entries at the
   top. A new game starts this file with its first entry.

5. Never commit to `main` directly, and never merge with a merge commit. Work on
   a branch and open a pull request. We keep linear history and require the
   branch to be rebased on the latest `main`. When `main` has moved:
   ```
   git fetch origin && git rebase origin/main && git push --force-with-lease
   ```
   If CI complains that the branch is behind or has a merge commit, this is the
   fix.

6. Do not touch other people's games. Your change should only add or edit the
   one game folder it is about, including its own `changelog.md`. Leave the rest
   alone.

## The workflow, start to finish

1. Make a branch: `git checkout -b add-<slug>` (or `edit-<slug>`).
2. Create or edit `games/<slug>/index.html` and `games/<slug>/game.json`.
3. If the user gave you a screenshot or you can make one, save it as
   `games/<slug>/thumbnail.png` and reference it in `game.json`. Otherwise pick
   a fitting emoji for `"icon"`.
4. Add a line to `games/<slug>/changelog.md`.
5. Check it builds: `python3 build.py --check` must pass (this is what CI runs).
6. Commit, push the branch, and open a PR (`gh pr create`).
7. Wait for the bot to post a preview link on the PR, then tell the user to play
   it. Do not call the task done until the preview works.
8. Once they are happy and CI is green, merge with rebase
   (`gh pr merge --rebase`). The site updates on its own within a couple of
   minutes.

## Testing locally before you push

The front page loads `games.json` over HTTP, so opening files directly will not
work. Build and serve:
```
python3 build.py
python3 -m http.server -d _site 8000
```
Then open `http://localhost:8000/`. Confirm the game appears in the grid and
plays when clicked.

## Keep it simple

This is a place for friends to ship small games quickly. Do not add frameworks,
package managers, or build tooling to a game unless the game genuinely needs it.
The smallest thing that works and is fun is the right thing.
