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

`DevMemes.app` is the author's macOS launcher. It runs `run.py` from a fixed path on the author's Mac, so it will not work from a fresh clone without editing.

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
