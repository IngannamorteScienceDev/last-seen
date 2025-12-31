# Last Seen

## Overview

**Last Seen** is a tool for building a complete offline mirror of VKontakte dialogs from the official VK data archive.

It converts exported HTML message files into a self-contained local viewer that preserves messages and attachments and can be opened without an internet connection.

---

## Input

Last Seen works with the **official VK data archive** provided by the user.

Expected structure:
```

vk_archive/
└── messages/
└── dialog_XXXX/
├── messages.html
├── messages_2.html
└── ...

```

No VK API access is required.

---

## Output

The tool generates a local, self-contained archive:
```

export/
├── index.html
├── data/
├── media/
└── assets/

```

Opening `index.html` displays the dialog offline.

---

## Purpose

Last Seen is designed for **offline access, preservation, and readable storage** of VK dialogs.

The project is read-only and does not modify message content.

---

## Project Status

🚧 Early development
