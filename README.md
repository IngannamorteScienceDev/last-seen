# Last Seen

**Last Seen** is an offline VK dialog viewer that converts a downloaded VK message archive into a fully browsable local chat — with messages, media, search, and a clean UI.  
No internet connection, no VK API, no authentication required.

---

## ✨ Features

- 📄 Parse VK HTML message archives into structured JSON
- 🖼 Download and store media attachments locally (photos, voice messages)
- 💬 Offline dialog viewer with chat-style layout
- 👤 Message authors and timestamps
- 📅 Grouping messages by day
- 🔍 Instant client-side message search with highlighting
- 🌙 Light / dark theme toggle (saved locally)
- ⬇️ User-controlled autoscroll and jump-to-bottom
- 🖥 Fully offline — works without internet access

---

## 🧠 How It Works

1. You download your VK data archive
2. Last Seen parses message HTML pages
3. Attachments are downloaded and saved locally
4. Messages are exported into a normalized JSON format
5. A static HTML viewer displays the dialog offline

All processing happens **locally on your machine**.

---

## 📁 Project Structure

```text
last-seen/
├── lastseen/          # Core package
│   ├── cli.py         # Command-line interface
│   ├── parser/        # VK HTML parsing logic
│   ├── downloader/    # Media downloader
│   └── exporter/      # JSON export
├── viewer/            # Offline HTML viewer
├── inspector/         # Archive inspection utilities
├── tests/             # Tests
├── samples/           # Example dialogs (optional)
├── export/            # Generated output (JSON, media)
├── requirements.txt
└── README.md
````

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/last-seen.git
cd last-seen
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### Parse a dialog and export messages

```bash
python -m lastseen.cli -i samples/<DIALOG_ID>
```

### Skip media downloading

```bash
python -m lastseen.cli -i samples/<DIALOG_ID> --no-media
```

### Open the viewer

Start a local HTTP server:

```bash
python -m http.server 8000
```

Then open in your browser:

```
http://localhost:8000/viewer/index.html
```

---

## ⚙️ CLI Options

| Flag            | Description            |
| --------------- | ---------------------- |
| `-i`, `--input` | Path to dialog folder  |
| `--no-media`    | Skip media downloading |

---

## 🎛 Viewer Controls

* 🌙 Toggle light / dark theme
* 🔍 Search messages by text
* 📅 Messages grouped by day
* ⬇️ Autoscroll toggle (open dialog at the end)
* ⬇️⬇️ Double-click jump to last message

All viewer preferences are stored locally in the browser.

---

## 📎 Supported Attachments

Last Seen supports detection and offline handling of the following attachment types:

* Photos
* Voice messages
* Videos (links)
* Files
* Stickers (metadata)
* Forwarded messages
* Wall posts
* Playlists
* Calls (metadata)
* Stories (metadata)

Attachment support depends on availability in the original VK archive.

---

## 🧠 Design Philosophy

Last Seen is designed to be **local-first**, simple, and transparent.

* No background services
* No external APIs
* No accounts or authentication
* No hidden network activity

Your data stays on your machine — always.

---

## 🔒 Privacy

* No VK API usage
* No authentication
* No external requests (except local files)
* No tracking or telemetry

Last Seen is built for **personal archives and private analysis**.

---

## 🗺 Roadmap

Possible future improvements (no guarantees):

* Improved viewer performance for very large dialogs
* Optional analytics and statistics
* Additional export formats

---

## 🧪 Status

Current version: **v0.3.0**

The project is stable and fully usable.
Future versions may extend the viewer UI or export formats.

---

## 📜 License

This project is licensed under a **Personal Use License**.

You are allowed to use the software for personal purposes,
but copying, modifying, or reusing the source code is not permitted.

See the `LICENSE` file for full terms.

---

## 👤 Author

**Arsenij Ingannamorte**

---

## ⭐ Why Last Seen?

Last Seen is not just a parser — it is a way to **revisit conversations as they were**, fully offline, without platforms, accounts, or servers.

A local memory.
Nothing more. Nothing less.
