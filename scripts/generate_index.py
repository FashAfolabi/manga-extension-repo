import json
import os
import re

repo_owner = "FashAfolabi"
repo_name = "manga-extension-repo"

base_download_url = f"https://github.com/{repo_owner}/{repo_name}/releases/download/latest"

extensions = []

for apk in os.listdir("apks"):
    if apk.endswith(".apk"):
        name_match = re.search(r'tachiyomi-en\.(.*?)-v', apk)
        version_match = re.search(r'-v([\d\.]+)\.apk', apk)

        if not name_match or not version_match:
            continue

        ext_name = name_match.group(1)
        version = version_match.group(1)
        version_code = int(version.replace(".", ""))

        if "asurascans" in apk:
            display_name = "Tachiyomi: Asura Scans"
            pkg = "eu.kanade.tachiyomi.extension.en.asurascans"
            source_name = "Asura Scans"
            source_id = "6247824327199706550"
            base_url = "https://asuracomic.net"

        elif "allanime" in apk:
            display_name = "Tachiyomi: AllManga"
            pkg = "eu.kanade.tachiyomi.extension.en.allanime"
            source_name = "AllManga"
            source_id = "4709139914729853090"
            base_url = "https://allmanga.to"

        else:
            continue

        extensions.append({
            "name": display_name,
            "pkg": pkg,
            "apk": f"{base_download_url}/{apk}",
            "lang": "en",
            "code": version_code,
            "version": version,
            "nsfw": 0,
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

print("index.json generated successfully.")
