# The Playground

A little arcade of web games we make for fun, hosted free on GitHub Pages.

Play: https://cnellington.github.io/playground/

## Add a game

Read [CONTRIBUTING.md](CONTRIBUTING.md). The short version: describe your game
to an AI coding agent in a clone of this repo, and it builds the game, opens a
pull request, and hands you a link to play it before it goes live. You do not
need to know how any of the plumbing works.

## How it works

- Each game is a self-contained static folder under `games/<slug>/` with an
  `index.html` and a `game.json` describing it.
- `build.py` reads every `game.json` and generates the front-page grid, so no
  one edits a shared list by hand.
- Pull requests get a live preview at
  `.../playground/pr-preview/pr-<N>/` for playtesting.
- Merging to `main` publishes the site. History is kept linear (rebase only) so
  rollbacks are easy.

The deeper rules for agents working in this repo are in [CLAUDE.md](CLAUDE.md).

## Local development

```
python3 build.py                      # build into _site/
python3 -m http.server -d _site 8000  # serve it
```

Then open http://localhost:8000/. No dependencies beyond Python 3.
