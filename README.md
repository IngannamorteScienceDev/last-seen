# Last Seen

**Last Seen** is a Python tool for creating a complete offline mirror of VKontakte dialogs using the official VK data archive.

The project converts exported VK HTML message files into a normalized, machine-readable format and prepares them for offline viewing, media downloading, and analysis — without requiring VK API access or an internet connection.

---

## ✨ Key Features

- 📦 Works with the **official VK data archive**
- 🧠 Parses **all message pages** in a dialog
- 🗂 Normalizes message structure and attachments
- 📊 Exports the full dialog into a single JSON file
- 📈 Provides clean console logs and progress bars
- 🔌 No VK API, no authentication, no internet required

---

## 📥 Input Data

Last Seen expects a dialog folder from the official VK archive.

Typical structure:

```

vk_archive/
└── messages/
└── <DIALOG_ID>/
├── messages.html
├── messages50.html
├── messages100.html
├── ...

```

Each `messages*.html` file contains up to 50 messages.

---

## 📤 Output Data

After processing, Last Seen produces a normalized JSON file:

```

export/
└── messages.json

````

Each message contains:

```json
{
  "id": 5762123,
  "author": {
    "role": "other",
    "name": "User Name",
    "vk_id": 123456789
  },
  "datetime": "2022-05-05T01:30:12",
  "edited": false,
  "text": "Message text",
  "attachments": []
}
````

Attachments are normalized using an internal taxonomy
(photo, voice_message, sticker, link, forwarded_messages, etc.).

---

## 🛠 Installation

Python **3.10+** is required.

Install dependencies:

```bash
pip install -r requirements.txt
```

or (if using `pyproject.toml`):

```bash
pip install .
```

---

## 🚀 Usage

Basic usage via CLI:

```bash
python -m lastseen.cli
```

By default, the tool:

1. Parses all `messages*.html` files in a dialog folder
2. Shows progress bars during parsing
3. Exports the result to `export/messages.json`

---

## 📊 Console Output Example

```
[INFO] Parsing dialog folder: samples/<DIALOG_ID>
[INFO] Found 624 HTML pages
Parsing message pages: 100%|██████████████| 624/624
[INFO] Total messages parsed: 31160
[INFO] Exporting 31160 messages to export/messages.json
[INFO] Export completed successfully
```

---

## 🧩 Project Structure

```
last-seen/
├── lastseen/
│   ├── attachments/     # Attachment taxonomy
│   ├── parser/          # HTML parsing logic
│   ├── downloader/      # Media downloader (planned)
│   ├── exporter/        # JSON export
│   ├── cli.py           # CLI entry point
│   └── logging.py       # Logging setup
├── inspector/           # Archive inspection tool
├── tests/               # Parsing tests
├── samples/             # Example VK archive data
└── export/              # Generated output
```

---

## 🧠 Design Principles

* **No guessing** — attachment types are derived from real archive inspection
* **Separation of concerns** — parsing, exporting, downloading, viewing
* **Deterministic output** — same input → same JSON
* **Offline-first** — everything works without internet access

---

## 🚧 Project Status

**Stable core pipeline implemented**
(Current stage: CLI improvements and UX refinements)

Planned next steps:

* CLI arguments (`--input`, `--output`, `--no-media`)
* Media downloader (photos, voice messages)
* Offline HTML viewer
* Search and analytics utilities

---

## 👤 Author

**Arsenij Ingannamorte**

---

## ⚠️ Disclaimer

This project works only with data that the user has legally obtained from VKontakte via the official data export mechanism.

Last Seen does not bypass VK restrictions and does not access private data without user consent.
