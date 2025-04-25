# 🕶️ ShadowHide

> Effortless Window Management for Power Users – Hide and Restore Any Window with a Hotkey.

![Platform](https://img.shields.io/badge/platform-windows-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-yellow.svg)

## 📚 Sections

- [🔍 Overview](#-overview)
- [✨ Features](#-features)
- [⚠️ Limitations](#️-limitations)
- [📸 Screenshots](#-screenshots)
- [💻 Installation](#-installation)
  - [🔹 Download (Recommended)](#-download-EXE-recommended)
  - [🔹 Run From Source](#-run-from-source)
  - [🔹 Requirements](#-requirements)
- [🛡️ Security & Trust](#%EF%B8%8F-security--trust)
- [🧬 How It Works](#-how-it-works)
- [⚙️ Configuration](#-configuration)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👤 Author](#-author)


---
## 🔍 Overview
**ShadowHide** is a lightweight, digitally signed Windows utility that lets you instantly hide and restore active windows using customizable global shortcuts. Ideal for privacy, productivity, and multitasking, it operates silently in your system tray with dynamic tray icons for every hidden window.

> Whether you're decluttering your screen or hiding a confidential app, ShadowHide is your invisible ally.
---

## ✨ Features

- 🪄 **Instant Window Hiding** with a global keyboard shortcut (default: `Ctrl + Shift + H`)
- 🧊 **Live Tray Icon Titles** that auto-update with the window's current title
- 🛠 **User Configurable Shortcut** stored in `shortcut.json`
- 🔁 **Restore from Tray or GUI** – Click tray icon or use the window list
- 🧵 **Multithreaded Title Monitoring** for non-blocking experience
- 🧼 **Clean Exit**: All hidden windows are restored before exit
- 🔐 **Digitally Signed Executable** to avoid tampering warnings
- 🪟 **List GUI** to choose and hide windows manually

---

## ⚠️ Limitations

- 🚫 **UWP Software Compatibility**: ShadowHide may not work properly with Universal Windows Platform (UWP) apps or certain other software due to API restrictions.
- 🔄 **Future Improvements**: Efforts are underway to enhance compatibility in future updates. For now, please keep this limitation in mind.
- 🛠 **Edge Cases**: Some applications with custom window handling may not respond as expected.
- 🔍 **Antivirus False Positives**: While signed, some antivirus programs may flag the app due to its functionality.

---

## 📸 Screenshots
> Coming soon – we’ll show how ShadowHide appears in action!

---

## 💻 Installation

### 🔹 Download EXE (Recommended)
Grab the latest version [ZIP](https://github.com/Maurya-Nitin/ShadowHide/releases/download/v.1.0.0/ShadowHide.zip) visit [Releases](https://github.com/Maurya-Nitin/ShadowHide/releases) page for more info.

> **Note:** If your antivirus blocks the file, turn off your antivirus temporarily. Please refer to the [🛡️ Security & Trust](#-security-&-trust) section. ShadowHide is digitally self-signed and verified clean by major antivirus vendors. You can safely proceed after reviewing the details.

### 🔹 Run From Source
```bash
# Clone the repository
git clone https://github.com/yourusername/ShadowHide.git
cd ShadowHide

# Install dependencies
pip install -r requirements.txt

# Run the app
python sys.py
```

### 🔹 Requirements
- Windows 10/11
- Python 3.10+
- Dependencies:
  - `pygetwindow`, `pystray`, `keyboard`, `Pillow`, `pywin32`, `tkinter`

---
## 🛡️ Security & Trust

ShadowHide is signed using a personal code-signing certificate. While most antivirus vendors mark it clean (check [VirusTotal](https://www.virustotal.com/gui/file/a9d3fc9123438d00ad3b2285c34c3e624fa5eb6e8407e60edb95c78cd38d97e4) ), **some heuristic engines (e.g., SecureAge APEX)** may falsely flag it due to:

- Embedded Python interpreter (PyInstaller)
- Use of `win32gui` and window manipulation functions

✅ ShadowHide has been thoroughly scanned and verified by leading antivirus vendors, including **Microsoft**, **Bitdefender**, **Kaspersky**, **Avast**, and **Norton**. You can review the detailed scan results on [VirusTotal](https://www.virustotal.com/gui/file/a9d3fc9123438d00ad3b2285c34c3e624fa5eb6e8407e60edb95c78cd38d97e4). Out of 72 vendors, only one flagged it as malware, which has since been confirmed as a **false positive** and updated version shows no worries now 0/72. Rest assured, ShadowHide is safe and secure to use.

> If flagged, please report a false positive with your antivirus vendor.
---

## 🧬 How It Works

ShadowHide uses a Python + Tkinter GUI to list open windows. When triggered:
- It uses `pygetwindow` and `win32gui` to hide the selected window.
- A tray icon is created using `pystray`, with the window’s title.
- A background thread updates the tray title if the window name changes.
- Users can restore any window from the tray.

---

## ⚙️ Configuration

Edit `shortcut.json` to set your preferred hotkey:
```json
{
  "shortcut": "Ctrl+Shift+H"
}
```

> All user configurations are stored in editable plain-text files alongside the EXE.

---

## 🤝 Contributing

Pull requests, feedback, and forks are welcome!
- Report issues via [GitHub Issues](https://github.com/Maurya-Nitin/ShadowHide/issues)
- Feature requests and security reports are welcome

---

## 📜 License

MIT License. See [LICENSE](LICENSE.txt) for full details.

**📜 License Summary (Human-readable)**

**What this license lets you do:**

* **Use it freely:** You can use this software for any purpose, even for commercial projects.
* **Make changes:** You can modify the software to fit your needs.
* **Share it:** You can distribute copies of the original or your modified version.
* **Keep it private:** You don't have to share any changes you make if you don't want to.

**What you need to keep in mind:**

* **Keep the original copyright notice**
* **No guarantees**
* **No liability for misuse**

**Giving credit (Good practice):**

While not legally required, it's appreciated if you credit the original author (Nitin) when using this in your own work — especially commercial projects.

**In simple terms:**

Use it, change it, share it — but don’t blame me if something goes wrong 🙂

---

## 👤 Author

Made with grit and joy by **Nitin** ✨  
[GitHub](https://github.com/Maurya-Nitin) ·

---

> “In the shadows of windows, control is power.”
