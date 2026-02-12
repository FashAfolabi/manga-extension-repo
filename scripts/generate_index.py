import json
import os
import re

# GitHub repo info
repo_owner = "FashAfolabi"
repo_name = "manga-extension-repo"

# Base URLs
base_download_url = f"https://github.com/{repo_owner}/{repo_name}/releases/download"
base_icon_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/icons"

extensions = []

for apk in os.listdir("apks"):
    if not apk.endswith(".apk"):
        continue

    # Extract package key and version from filename
    name_match = re.search(r'tachiyomi-en\.(.*?)-v', apk)
    version_match = re.search(r'-v([\d\.]+)\.apk', apk)

    if not name_match or not version_match:
        print(f"Skipping invalid APK filename: {apk}")
        continue

    ext_key = name_match.group(1)
    version = version_match.group(1)
    version_code = int(version.replace(".", ""))  # remove dots for code
    tag_name = f"v{version}"  # GitHub release tag

    # Determine extension metadata
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

    # Construct APK and icon URLs
    apk_url = f"{base_download_url}/{tag_name}/{apk}"
    icon_url = f"{base_icon_url}/{pkg}.png"

    # Append extension JSON
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

# Write JSON files
with open("index.json", "w") as f:
    json.dump(extensions, f, indent=2)

with open("index.min.json", "w") as f:
    json.dump(extensions, f, separators=(',', ':'))

print("index.json and index.min.json generated successfully.")
