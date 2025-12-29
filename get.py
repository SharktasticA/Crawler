from pathlib import Path
from common import *
import random
import urllib.request
import time



# Outputs
DOWNLOADED = "downloaded.txt"
E404S = "404s.txt"
dir = Path(FILES.replace(".txt", ""))
dir.mkdir(exist_ok=True)



# Working lists
files = load_list(FILES)
e404s = load_list(E404S)
downloaded = load_list(DOWNLOADED)



random.shuffle(files)

for file in files:
    if file in downloaded:
        continue

    # Output file name 
    filename = file.replace(ENTRY, "").replace("/", "_").replace(" ", "_").replace("%20", "_")
    out_path = dir / filename

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": parent_url(file),
    }

    req = urllib.request.Request(sanitise_url(file), headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            out_path.write_bytes(response.read())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            e404s.append(file)
            append_file(E404S, file)
            continue
    except Exception as e:
        print(f"ERROR - {file}: {e}")
        continue

    downloaded.append(file)
    append_file(DOWNLOADED, file)

    time.sleep(random.uniform(0.8, 1.6))
