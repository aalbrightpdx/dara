#!/usr/bin/python3

import json
import os
from pathlib import Path

DEFAULT_CONFIG_PATH = Path("./config.json")

DEFAULTS = {
    "greeting_template": "Good {time}, {user}. You have arrived at the DARA Command Interface. Stardate {stardate}. Earth date: {date}, {clock}. {weather} {status}",
    "weather_zip": "97045",
    "status_frequency": "login_only",  # login_only / login_hourly / login_4h / login_8h / on_error / never
    "voice_engine": "gtts",  # gtts / espeak-ng
    "startup_chime": True,
    "chime_path": "~/Music/startup_chime.mp3",
    "enabled_modules": {
        "weather": True,
        "system_checks": True,
        "stardate": True,
        "tasks": False,
        "calendar": False
    }
}

def prompt_with_default(prompt, default):
    response = input(f"{prompt} (Default: {default})\n> ").strip()
    return response if response else default

def prompt_boolean(prompt, default):
    response = input(f"{prompt} [Y/n] (Default: {'Y' if default else 'n'})\n> ").strip().lower()
    return default if response == "" else response.startswith("y")

def run_config_wizard():
    print("\n🧠 Welcome to the DARA configuration wizard!\n")

    config = {}
    config["greeting_template"] = prompt_with_default(
        "Enter your preferred greeting format",
        DEFAULTS["greeting_template"]
    )

    config["weather_zip"] = prompt_with_default(
        "Enter your ZIP code for weather (or leave blank to disable)",
        DEFAULTS["weather_zip"]
    )

    print("\nHow often should DARA give you a system status update?")
    print("  1. On GNOME login only")
    print("  2. On login + hourly")
    print("  3. On login + every 4 hours")
    print("  4. On login + every 8 hours")
    print("  5. On login + only when system issues are detected")
    print("  6. Never")
    choice = input("Choose an option [1-6] (Default: 1):\n> ").strip()
    status_freq_options = {
        "1": "login_only",
        "2": "login_hourly",
        "3": "login_4h",
        "4": "login_8h",
        "5": "on_error",
        "6": "never"
    }
    config["status_frequency"] = status_freq_options.get(choice, "login_only")

    config["voice_engine"] = prompt_with_default(
        "Preferred voice engine? [gtts / espeak-ng]",
        DEFAULTS["voice_engine"]
    )

    config["startup_chime"] = prompt_boolean(
        "Enable startup chime?",
        DEFAULTS["startup_chime"]
    )

    if config["startup_chime"]:
        config["chime_path"] = prompt_with_default(
            "Path to startup chime MP3 (or leave default)",
            DEFAULTS["chime_path"]
        )
    else:
        config["chime_path"] = ""

    print("\n🔌 Enable optional modules:")
    config["enabled_modules"] = {
        "weather": prompt_boolean("- Weather announcements?", DEFAULTS["enabled_modules"]["weather"]),
        "system_checks": prompt_boolean("- System checks?", DEFAULTS["enabled_modules"]["system_checks"]),
        "stardate": prompt_boolean("- Include stardate?", DEFAULTS["enabled_modules"]["stardate"]),
        "tasks": prompt_boolean("- Local task reminders?", DEFAULTS["enabled_modules"]["tasks"]),
        "calendar": prompt_boolean("- Google calendar integration (future)?", DEFAULTS["enabled_modules"]["calendar"])
    }

    print("\n✅ Configuration complete. Saving to:", DEFAULT_CONFIG_PATH)
    with open(DEFAULT_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print("\nYou can rerun this wizard anytime using: `python3 configure.py`\n")

if __name__ == "__main__":
    run_config_wizard()

