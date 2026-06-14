# Adding a game to The Playground

You do not need to be a programmer to add a game here. The easiest path is to
let an AI coding agent (like Claude Code) do the technical parts while you
describe the game you want. This repo is set up so that an agent reads its
instructions automatically and follows the right steps.

## The fastest way: describe it to an agent

1. Get access. Ask Caleb to add you as a collaborator on the repo. This matters:
   it lets your preview links work (see the note at the bottom).
2. Clone the repo and open it with an AI coding agent:
   ```
   git clone https://github.com/cnellington/playground.git
   cd playground
   ```
3. Tell the agent what you want, for example:
   > "Add a new game called Snake Deluxe. It's the classic snake game but the
   > snake wears a different hat each level. Make it playable with arrow keys."
4. The agent will create the game, open a pull request, and give you a preview
   link. Open the link and play it.
5. If something is off, tell the agent what to change. It will update the same
   pull request and the preview refreshes.
6. When you are happy, the agent merges it and the game goes live at
   `https://cnellington.github.io/playground/` within a couple of minutes.

The agent follows the rules in [`CLAUDE.md`](CLAUDE.md) so you do not have to
learn them. If you are curious what it is doing, that file is readable.

## What can be hosted here

Anything that runs in a web browser with no server: HTML, CSS, and JavaScript.
Single-player or hot-seat multiplayer, pixel art, text games, toys. Loading
libraries from the internet (fonts, a game engine) is fine.

What does not work: anything that needs a backend, a login, a database, or
secret keys. If your idea needs those, the page cannot host it as-is.

## How it is organized

```
playground/
├── index.html          the front page (a grid of all games), generated, do not hand-edit the list
├── changelog.html      shows each game's changelog, grouped by game
├── games/
│   └── <your-game>/
│       ├── index.html   your game
│       ├── game.json    its title, tagline, description, etc.
│       ├── changelog.md what changed in this game (optional, newest at the top)
│       └── thumbnail.png optional cover image
└── build.py             assembles the site; CI runs it
```

Each game is fully self-contained in its own folder, including its own
`changelog.md`. You only ever add or edit your own folder, so changes never
collide with anyone else's.

## Doing it by hand (optional)

If you do want to do it yourself:

1. `git checkout -b add-<your-game>`
2. Create `games/<your-game>/index.html` (your game) and
   `games/<your-game>/game.json` (copy an existing one and edit the fields).
3. Add a line to `games/<your-game>/changelog.md` describing the change.
4. Check it: `python3 build.py --check`
5. Preview it locally:
   ```
   python3 build.py
   python3 -m http.server -d _site 8000
   ```
   then open `http://localhost:8000/`.
6. Commit, push, and open a pull request. A preview link will appear on it.
7. When CI is green and you have playtested the preview, merge with rebase.

## Two things CI will insist on

- Your `game.json` must have all its fields and its `slug` must match the folder
  name. The build check tells you exactly what is missing.
- Your branch must be rebased on the latest `main`, with no merge commits. If CI
  says you are behind, ask your agent to "rebase my branch on the latest main,"
  or run:
  ```
  git fetch origin && git rebase origin/main && git push --force-with-lease
  ```
  This keeps history clean so that rolling back a bad change is painless.

## A note on preview links and forks

Preview links are built by a GitHub Action that needs write access, which GitHub
only grants to branches inside this repo, not to forks. So push your branch to
this repo (this is why you want to be a collaborator) rather than working from a
fork. If you only have a fork, your pull request still works, but the automatic
preview link will not appear.
