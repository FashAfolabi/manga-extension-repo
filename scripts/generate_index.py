import os
import json

# Base URL for GitHub Releases
repo_url = "https://github.com/FashAfolabi/manga-extension-repo/releases/latest/download/"

apk_folder = "apks"
extensions = []

for apk in os.listdir(apk_folder):
    if apk.endswith(".apk"):
        # Generate a friendly name
        name = apk.replace(".apk", "").replace("tachiyomi-en.", "").replace("-", " ").title()
        
        # Hardcode sourceId and versionCode for your two extensions
        if "allanime" in apk:
            source_id = 4709139914729853090
            version_code = 10
            version = "1.4.10"
        elif "asurascans" in apk:
            source_id = 6247824327199706550
            version_code = 52
            version = "1.4.52"
        else:
            source_id = 0
            version_code = 1
            version = "1.0.0"

        extensions.append({
            "name": f"Tachiyomi: {name}",
            "pkg": f"eu.kanade.tachiyomi.extension.en.{apk.split('-')[1].split('.')[0]}",
            "apk": repo_url + apk,
            "lang": "en",
            "version": version,
            "versionCode": version_code,
            "nsfw": 0,
            "sources": [
                {
                    "name": name,
                    "lang": "en",
                    "id": source_id
                }
            ]
        })

# Write index.json
with open("index.json", "w") as f:
    json.dump(extensions, f, indent=2)

# Write index.min.json
with open("index.min.json", "w") as f:
    json.dump(extensions, f, separators=(",", ":"))
