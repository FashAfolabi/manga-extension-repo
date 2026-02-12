import json
import os
import re

# ---------- CONFIG ----------
repo_owner = "FashAfolabi"
repo_name = "manga-extension-repo"

apks_folder = "apks"
icons_folder = "icons"

# Base URLs
base_icon_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{icons_folder}"

# List to hold extension data
extensions = []

# ---------- SCAN APKs ----------
for apk in os.listdir(apks_folder):
    if not apk.endswith(".apk"):
        continue

    # Extract extension key and version
    name_match = re.search(r'tachiyomi-en\.(.*?)-v', apk)
    version_match = re.search(r'-v([\d\.]+)\.apk', apk)

    if not name_match or not version_match:
        print(f"Skipping invalid APK filename: {apk}")
        continue

    ext_key = name_match.group(1)
    version = version_match.group(1)
    version_code = int(version.replace(".", ""))  # remove dots
    tag_name = f"v{version}"  # release tag

    # ---------- EXTENSION METADATA ----------
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
        print(f"Skipping unknown extension: {apk}")
        continue

    # Construct URLs
    apk_url = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{tag_name}/{apk}"
    icon_url = f"{base_icon_url}/{pkg}.png"

    # Append extension info
    extensions.append({
        "name": display_name,
        "pkg": pkg,
        "apk": apk_url,
        "lang": "en",
        "code": version_code,
        "version": version,
        "nsfw": 0,
        "icon": icon_url,
        "sources": [
            {
                "name": source_name,
                "lang": "en",
                "id": source_id,
                "baseUrl": base_url
            }
        ]
    })

# ---------- WRITE JSON ----------
with open("index.json", "w") as f:
    json.dump(extensions, f, indent=2)

with open("index.min.json", "w") as f:
    json.dump(extensions, f, separators=(',', ':'))

print("✅ index.json and index.min.json generated successfully.")
