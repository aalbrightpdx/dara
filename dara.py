#!/usr/bin/python3

import argparse
import json
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path("./config.json")
LOG_PATH = Path("./dara.log")
MAX_LOG_LINES = 500  # Limit the number of log lines to keep

# --- Load configuration ---
def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("Config file not found. Please run configure.py first.")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

# --- Log to file and trim if necessary ---
def log_message(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {entry}\n"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)

    # Trim log file if it grows too large
    with open(LOG_PATH, "r") as log_file:
        lines = log_file.readlines()
    if len(lines) > MAX_LOG_LINES:
        with open(LOG_PATH, "w") as log_file:
            log_file.writelines(lines[-MAX_LOG_LINES:])

# --- Helper: Run a shell command and get output ---
def run_check(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return ""

# --- Speak output ---
def speak(text, engine="gtts", mute=False):
    if mute:
        return
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        temp_path = tmp.name
    try:
        if engine == "gtts":
            from gtts import gTTS
            tts = gTTS(text)
            tts.save(temp_path)
            subprocess.run(["ffplay", "-nodisp", "-autoexit", "-af", "atempo=1.15", temp_path])
        else:
            subprocess.run(["espeak-ng", text])
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

# --- Build the status message ---
def build_message(config):
    now = datetime.now()
    date = now.strftime("%B %d, %Y")
    clock = now.strftime("%I:%M %p").lstrip("0")
    user = os.getenv("USER", "User")

    spoken_year = " ".join(str(now.year))
    spoken_day = " ".join(f"{now.timetuple().tm_yday:03}")
    stardate = f"{spoken_year} point {spoken_day}"

    time_of_day = now.hour
    if 5 <= time_of_day < 12:
        time = "morning"
    elif 12 <= time_of_day < 17:
        time = "afternoon"
    elif 17 <= time_of_day < 21:
        time = "evening"
    else:
        time = "nightwatch"

    weather = ""
    if config["enabled_modules"].get("weather"):
        try:
            zip_code = config.get("weather_zip", "97045")
            weather_json = run_check(f"curl -s 'wttr.in/{zip_code}?format=j1&u'")
            import json as jsonlib
            data = jsonlib.loads(weather_json)
            temp_f = data["current_condition"][0]["temp_F"]
            desc = data["current_condition"][0]["weatherDesc"][0]["value"]
            high = data["weather"][0]["maxtempF"]
            low = data["weather"][0]["mintempF"]
            weather = f"The ambient temperature is {temp_f}F with {desc.lower()}. High {high}, low {low}."
        except Exception as e:
            weather = "Weather unavailable."
            log_message(f"[WARN] Failed to fetch weather: {e}")

    status = "All systems nominal."
    # (Placeholder: Add real checks later)

    return config["greeting_template"].format(
        time=time,
        user=user,
        stardate=stardate,
        date=date,
        clock=clock,
        weather=weather,
        status=status
    )

# --- Main entry point ---
def main():
    parser = argparse.ArgumentParser(description="DARA System Assistant")
    parser.add_argument("command", nargs="?", default="greet", choices=["greet", "status", "start", "stop", "mute", "unmute"], help="Command to run")
    args = parser.parse_args()

    config = load_config()
    mute = args.command == "mute"

    if args.command in ("greet", "status", "mute", "unmute"):
        message = build_message(config)
        print("[DARA MESSAGE]", message)
        log_message(f"[{args.command.upper()}] {message}")

        # Play startup chime if configured
        if config.get("startup_chime", False):
            chime_path = os.path.expanduser(config.get("chime_path", ""))
            if chime_path and os.path.exists(chime_path):
                try:
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", chime_path])
                    log_message("[INFO] Startup chime played.")
                except Exception as e:
                    log_message(f"[WARN] Startup sound failed: {e}")
            else:
                log_message("[INFO] Startup chime enabled but file missing or invalid.")

        speak(message, engine=config.get("voice_engine", "gtts"), mute=mute)

    elif args.command == "start":
        print("[DARA] Daemon start functionality not implemented yet.")
        log_message("[INFO] Daemon start requested")
    elif args.command == "stop":
        print("[DARA] Daemon stop functionality not implemented yet.")
        log_message("[INFO] Daemon stop requested")

if __name__ == "__main__":
    main()

