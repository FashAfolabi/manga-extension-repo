import json
import os
import re

# ---------------- CONFIG ----------------
apks_folder = "apks"
icons_folder = "icons"

extensions = []

# ---------------- SCAN APKs ----------------
for apk in os.listdir(apks_folder):
    if not apk.endswith(".apk"):
        continue

    name_match = re.search(r'tachiyomi-en\.(.*?)-v', apk)
    version_match = re.search(r'-v([\d\.]+)\.apk', apk)
    if not name_match or not version_match:
        continue

    ext_key = name_match.group(1)
    version = version_match.group(1)
    version_code = int(version.replace(".", ""))

    # ---------------- EXTENSION METADATA ----------------
    if "asurascans" in ext_key:
        display_name = "Tachiyomi: Asura Scans"
        pkg = "eu.kanade.tachiyomi.extension.en.asurascans"
        source_name = "Asura Scans"
        source_id = "6247824327199706550"
        base_url = "https://asuracomic.net"
    elif "allanime" in ext_key:
        display_name = "Tachiyomi: AllManga"
        pkg = "eu.kanade.tachiyomi.extension.en.allanime"
        source_name = "AllManga"
        source_id = "4709139914729853090"
        base_url = "https://allmanga.to"
    else:
        continue

    # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
    # RELATIVE PATHS (this fixes icons + APK 404)
    apk_path = f"{apks_folder}/{apk}"
    icon_path = f"{icons_folder}/{pkg}.png"

    extensions.append({
        "name": display_name,
        "pkg": pkg,
        "apk": apk_path,           # ← changed
        "lang": "en",
        "code": version_code,
        "version": version,
        "nsfw": 0,
        "icon": icon_path,         # ← changed
        "sources": [
            {
                "name": source_name,
                "lang": "en",
                "id": source_id,
                "baseUrl": base_url
            }
        ]
    })

# ---------------- WRITE JSON ----------------
with open("index.json", "w") as f:
    json.dump(extensions, f, indent=2)

with open("index.min.json", "w") as f:
    json.dump(extensions, f, separators=(',', ':'))

print("✅ index.json and index.min.json generated successfully (relative paths).")
