# DARA
**Daily Assistant: Readout Announcer**

DARA is a modular, voice-ready personal assistant script that greets the user at GNOME login, reads system status, gives weather updates, and can optionally play a startup chime. She’s designed to run as a CLI tool and will soon support daemon-mode for continuous monitoring.

---

## 🚀 Features
- 🌤️ Weather announcements via `wttr.in`
- 🖥️ System greeting with time, date, and stardate
- 🔊 Spoken output using `gTTS` or `espeak-ng`
- 🔔 Optional startup chime support
- 🧪 Logging to `dara.log` (auto-trims to 500 lines)
- 🔕 `mute` and `unmute` CLI modes
- 🛠️ Interactive configuration wizard
- 🗃️ Configurable via `config.json`

---

## 📦 Installation
```bash
pipx install .
```

Or just run manually:
```bash
./configure.py       # First-time setup
./dara.py greet      # Speak and show the message
./dara.py status     # Same as greet
./dara.py mute       # Show message without speaking
./dara.py unmute     # Speak even if previously muted
```

---

## 🔧 Configuration
All settings are stored in `config.json` (created by `configure.py`). This includes:
- Greeting template
- Weather ZIP code
- Startup chime toggle and path
- Voice engine preference
- Enabled modules (weather, system checks, stardate, etc.)

You can re-run the wizard at any time:
```bash
python3 configure.py
```

---

## 🧭 Plan / Roadmap
- [x] CLI interface with `greet`, `mute`, `status`
- [x] Logging and log rotation
- [x] Weather and basic system info
- [ ] System health checks (disk, mounts, failures)
- [ ] Daemon mode: background system monitor
- [ ] Task reminders (from local file)
- [ ] Google Calendar / Tasks integration (optional)
- [ ] GTK or tray UI module (stretch goal)
- [ ] Auto-start via `.desktop` file for GNOME

---

## 📝 License
MIT License — customize, extend, or build your own command deck on top of DARA 💫

---

## 💬 Example
```
Good morning, Aaron. You have arrived at the DARA Command Interface. 
Stardate 2 0 2 5 point 1 3 3. Earth date: May 13, 2025, 09:12 AM. 
The ambient temperature is 53F with light rain. High 57, low 47. 
All systems nominal.
```

---
