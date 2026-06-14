#!/usr/bin/env python3
"""Assemble the static site into _site/.

What it does, in order:
  1. Validate every games/<slug>/game.json against a small required-field schema.
  2. Aggregate them into _site/games.json (the manifest the library page reads).
  3. Copy the library shell (index.html, changelog.html, assets/, CHANGELOG.md)
     and every game folder into _site/.

No third-party dependencies: this runs anywhere Python 3 runs, including a
contributor's laptop and CI, with no install step. Run it with:

    python3 build.py            # build into _site/
    python3 build.py --check    # validate only, do not write _site/

A non-zero exit means a game is malformed; CI blocks the merge in that case.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
GAMES_DIR = ROOT / "games"
SITE_DIR = ROOT / "_site"

# Fields every game.json must define. Keep this list short so the barrier to
# adding a game stays low for non-technical contributors.
REQUIRED_FIELDS = ["title", "slug", "tagline", "description", "added"]
ISO_DATE_LEN = len("YYYY-MM-DD")


def fail(msg: str) -> None:
    print(f"  ERROR: {msg}", file=sys.stderr)


def validate_game(game_dir: Path) -> dict | None:
    """Return the parsed, validated manifest for one game, or None on error."""
    slug = game_dir.name
    manifest_path = game_dir / "game.json"
    entry_path = game_dir / "index.html"
    ok = True

    if not manifest_path.exists():
        fail(f"{slug}: missing game.json")
        return None
    if not entry_path.exists():
        fail(f"{slug}: missing index.html (the game itself)")
        ok = False

    try:
        meta = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{slug}: game.json is not valid JSON ({e})")
        return None

    for field in REQUIRED_FIELDS:
        if field not in meta or meta[field] in ("", [], None):
            fail(f"{slug}: game.json is missing required field '{field}'")
            ok = False

    if meta.get("slug") != slug:
        fail(f"{slug}: game.json slug '{meta.get('slug')}' must match folder name '{slug}'")
        ok = False

    added = meta.get("added", "")
    if not (isinstance(added, str) and len(added) == ISO_DATE_LEN and added[4] == "-" and added[7] == "-"):
        fail(f"{slug}: 'added' must be an ISO date like 2026-06-13 (got '{added}')")
        ok = False

    # A thumbnail is optional, but if named it must exist so the grid never 404s.
    thumb = meta.get("thumbnail")
    if thumb and not (game_dir / thumb).exists():
        fail(f"{slug}: thumbnail '{thumb}' is named in game.json but the file is missing")
        ok = False

    if not ok:
        return None

    # Surface the path the library page links to; keep manifest self-contained.
    meta["path"] = f"games/{slug}/"

    # Per-game changelog: an optional changelog.md in the game's own folder. Each
    # game owns its history (no shared file for contributors to collide on) and
    # gets its own changelog page next to the game. The card links to it when one
    # exists; the flag tells the library whether to show that link.
    changelog_path = game_dir / "changelog.md"
    meta["hasChangelog"] = changelog_path.exists() and bool(changelog_path.read_text().strip())

    return meta


def collect_games() -> list[dict]:
    if not GAMES_DIR.exists():
        return []
    manifests = []
    had_error = False
    for game_dir in sorted(p for p in GAMES_DIR.iterdir() if p.is_dir()):
        meta = validate_game(game_dir)
        if meta is None:
            had_error = True
        else:
            manifests.append(meta)
    if had_error:
        print("\nBuild failed: fix the errors above. See CONTRIBUTING.md.", file=sys.stderr)
        sys.exit(1)
    # Newest first so the library shows fresh games at the top.
    manifests.sort(key=lambda m: m["added"], reverse=True)
    return manifests


def build(manifests: list[dict]) -> None:
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Library shell + shared assets.
    shutil.copy2(ROOT / "index.html", SITE_DIR / "index.html")
    if (ROOT / "assets").exists():
        shutil.copytree(ROOT / "assets", SITE_DIR / "assets")

    # The aggregated manifest the library page fetches at runtime.
    (SITE_DIR / "games.json").write_text(json.dumps(manifests, indent=2))

    # Every game folder, verbatim.
    if GAMES_DIR.exists():
        shutil.copytree(GAMES_DIR, SITE_DIR / "games")

    # Drop a per-game changelog page next to each game that has a changelog.md.
    template = (ROOT / "templates" / "game-changelog.html").read_text()
    for meta in manifests:
        if meta["hasChangelog"]:
            (SITE_DIR / "games" / meta["slug"] / "changelog.html").write_text(template)

    print(f"Built _site/ with {len(manifests)} game(s): {', '.join(m['slug'] for m in manifests)}")


def main() -> None:
    check_only = "--check" in sys.argv
    print("Validating games ...")
    manifests = collect_games()
    print(f"  {len(manifests)} game(s) valid.")
    if check_only:
        return
    build(manifests)


if __name__ == "__main__":
    main()
