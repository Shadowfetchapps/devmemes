# DevMemes

A desktop meme generator for developers and startup workers. 140 handcrafted jokes across 6 categories — one click generates a ready-to-post meme.

---

## Features

- **140 dev/startup jokes** across Debugging, Git, Meetings, Startup Life, Stack Overflow, and Deployment
- **28 classic meme templates** — Drake, This Is Fine, Expanding Brain, Change My Mind, Epic Handshake, and more
- **One-click generation** — Random Meme picks a template and joke together
- **New Joke** — keep the same template, swap the joke
- **Fully editable text** — tweak any text before generating
- **Copy to clipboard** — paste straight into Slack, Twitter/X, Discord
- **Save as PNG** — exports to `~/Downloads/DevMemes/`
- **Browse tab** — search the Imgflip template catalog (needs internet)
- **Dark theme** PyQt6 desktop UI

---

## Setup

```bash
git clone https://github.com/Shadowfetchapps/devmemes.git
cd devmemes
pip3 install -r requirements.txt
```

## Run

From Terminal:

```bash
python3 run.py
```

### macOS app

`DevMemes.app` runs `run.py` from the folder it sits in, so it works from any clone location. It uses `.venv/bin/python3` in the repo folder if that exists, otherwise `python3` from your login shell. Set up the venv once:

```bash
cd devmemes
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Then double-click `DevMemes.app` in the repo folder. Keep the app inside the repo folder; it looks for `run.py` next to itself. Output goes to `~/Library/Logs/DevMemes.log`. If Python or the requirements are missing, the app shows a dialog with the setup commands.

The app is ad-hoc signed, not notarized. A `git clone` launches directly. If you downloaded the repo as a ZIP, macOS blocks the first launch: right-click the app and choose Open (on macOS 15 and later, try to open it once, then click Open Anyway in System Settings > Privacy & Security), or run `xattr -dr com.apple.quarantine DevMemes.app` in the repo folder.

---

## Templates

A selection of the 28 built-in templates:

| Template | Best for |
|---|---|
| Drake Hotline Bling | "You should do X but you do Y" |
| This Is Fine | Everything is on fire but whatever |
| One Does Not Simply | Impossible things in software |
| Two Buttons | Hard choices with no good answer |
| Change My Mind | Spicy dev opinions |
| Expanding Brain | Escalating irrationality |
| Surprised Pikachu | Predictable consequences of bad choices |
| Mocking SpongeBob | Repeating bad advice sarcastically |
| Waiting Skeleton | Anything that takes forever |
| Success Kid | Small victories that feel massive |
| Disaster Girl | Controlled chaos energy |
| Epic Handshake | Both sides agreeing on something dumb |
| Ancient Aliens | Blaming inexplicable things on forces unknown |
| Y U No | Frustrated demands |
| First World Problems | Developer luxoproblems |

---

## Categories

- **Debugging** — bugs, console.log, missing semicolons, cosmic rays
- **Git** — force push, commit messages, merge conflicts, PR reviews
- **Meetings** — standups, sprint planning, this-could-have-been-an-email
- **Startup Life** — unlimited PTO nobody takes, equity, AI washing, pivot fatigue
- **Stack Overflow** — copy-paste, duplicate questions, 2009 answers
- **Deployment** — Friday deploys, prod fires, CI/CD pipelines, config changes

---

## Project structure

```
devmemes/
├── memegen/
│   ├── jokes.py      # 140 memes + template definitions
│   ├── generator.py  # PIL image rendering (downloads + caches templates)
│   └── app.py        # PyQt6 dark-theme UI
├── cache/            # Downloaded template images (auto-created)
├── DevMemes.app      # Double-clickable macOS launcher
├── requirements.txt
└── run.py
```

---

## License

MIT. See [LICENSE](LICENSE).
