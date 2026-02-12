import json
import os
import re

repo_owner = "FashAfolabi"
repo_name = "manga-extension-repo"

apks_folder = "apks"
icons_folder = "icons"

base_apk_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{apks_folder}"
base_icon_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{icons_folder}"

extensions = []

for apk in os.listdir(apks_folder):
    if not apk.endswith(".apk"):
        continue

    # Extract extension key and version
    name_match = re.search(r'tachiyomi-en\.(.*?)-v', apk)
    version_match = re.search(r'-v([\d\.]+)\.apk', apk)
    if not name_match or not version_match:
        continue

    ext_key = name_match.group(1)
    version = version_match.group(1)
    version_code = int(version.replace(".", ""))

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

    apk_url = f"{base_apk_url}/{apk}"
    icon_url = f"{base_icon_url}/{pkg}.png"

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

with open("index.json", "w") as f:
    json.dump(extensions, f, indent=2)

with open("index.min.json", "w") as f:
    json.dump(extensions, f, separators=(',', ':'))

print("✅ index.json and index.min.json generated successfully.")
