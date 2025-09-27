# 📺 YouTubeChatSniper

**YouTubeChatSniper** is a lightweight Python tool that monitors a **YouTube live stream chat** in real time, looking for a **specific keyword**. When the keyword is detected, the tool automatically sends an alert to a **Discord webhook**.

> ⚡ Useful for stream moderators, automated bots, or real-time alert systems during live events.

---

## 🚀 Features

- 🔍 Monitors **live chat** of a YouTube livestream.
- 🎯 Detects a specific **keyword**.
- 📬 Sends matching messages to a **Discord webhook**.
- ⏱️ Includes a **cooldown mechanism** to avoid spamming.
- ⚙️ Uses a `config.json` file for persistent configuration.

---

## 📦 Requirements

- Python 3.7 or higher
- Required Python packages:
  - `pytchat`
  - `requests`
  - `colorama`
  - `termcolor`

Install dependencies:

```bash
pip install -r requirements.txt
