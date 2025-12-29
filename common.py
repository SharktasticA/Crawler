from dotenv import load_dotenv
import os
from collections import deque
from urllib.parse import urlsplit, urlunsplit, quote



load_dotenv()
ENTRY = os.getenv("ENTRY")
FILES = os.getenv("FILES")


USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64; rv:146.0) Gecko/20100101 Firefox/146.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.8.2 Chrome/122.0.6261.171 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
]



def load_list(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_set(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())
    
def load_queue(filename):
    if not os.path.exists(filename):
        return deque()
    with open(filename, "r", encoding="utf-8") as f:
        return deque(line.strip() for line in f if line.strip())
    
def append_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def overwrite_file(filename, items):
    with open(filename, "w", encoding="utf-8") as f:
        for item in items:
            f.write(item + "\n")



def parent_url(url):
    parts = urlsplit(url)
    parent = parts.path.rsplit("/", 1)[0] + "/"
    return urlunsplit((parts.scheme, parts.netloc, parent, "", ""))

def sanitise_url(url):
    parts = urlsplit(url)
    encoded_path = quote(parts.path, safe="/%")
    return urlunsplit((parts.scheme, parts.netloc, encoded_path, parts.query, parts.fragment))
