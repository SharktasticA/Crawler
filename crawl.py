import re
from common import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse



# Outputs
QUEUE = "queue.txt"
DONE = "done.txt"
IMGS = "imgs.txt"
DOCS = "docs.txt"
VIDS = "vids.txt"
ZIPS = "zips.txt"

# Patterns
IMG_PATTERN = re.compile(r".*\.(jpg|jpeg|png|gif|bmp|webp|svg|tif|tiff|avif|heif|heic|jp2|ico|psd|exr|hdr|tga|pnm|pbm|pgm|ppm|img)$", re.IGNORECASE)
DOC_PATTERN = re.compile(r".*\.(pdf|doc|docx|ppt|pptx|xls|xlsx|odt|ods|odp|odg|odf|ott|ots|otp|otg|rtf|txt|md|csv|epub|tex)$", re.IGNORECASE)
VID_PATTERN = re.compile(r".*\.(mp4|mov|avi|mkv|mpeg|mpg|webm|flv|wmv|3gp|3g2|ogv|ts|mts|m2ts|asf)(\?.*)?$", re.IGNORECASE)
ZIP_PATTERN = re.compile(r".*\.(zip|7z|rar|tar|gz|bz2|xz|lzma|zst|tar\.gz|tar\.bz2|tar\.xz|tar\.zst|dmg|pkg|cab|jar|war|ear|apk|ipa)(\?.*)?$", re.IGNORECASE)



# Working lists
queue = load_queue(QUEUE)
done = load_set(DONE)
imgs = load_set(IMGS)
docs = load_set(DOCS)
vids = load_set(VIDS)
zips = load_set(ZIPS)

if not queue:
    queue.append(ENTRY)



while queue:
    url = queue.popleft()
    overwrite_file(QUEUE, queue)

    if url in done:
        continue

    # Attempt request
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"ERROR - {url}: {e}")
        continue

    base = response.url

    # Register this URL as visited
    done.add(url)
    append_file(DONE, url)
    done.add(base)
    append_file(DONE, base)

    # Load markup into bs4
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract images from img tags
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        link = urljoin(base, src)

        if link in done:
            continue

        # Ignore if not a sub of entry
        if ENTRY not in link:
            continue

        if IMG_PATTERN.match(link):
            if link not in imgs:
                imgs.add(link)
                append_file(IMGS, link)
                done.add(link)
                append_file(DONE, link)

    # Extract images and documents from a tags
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue

        link = urljoin(base, href)

        if link in done:
            continue

        # Ignore if not full URL
        if "http" not in link:
            continue

        # Ignore if not a sub of entry
        if ENTRY not in link:
            continue

        # Test if document
        if DOC_PATTERN.match(link):
            if link not in docs:
                docs.add(link)
                append_file(DOCS, link)
                done.add(link)
                append_file(DONE, link)
            continue

        # Test if compressed archive
        if ZIP_PATTERN.match(link):
            if link not in zips:
                zips.add(link)
                append_file(ZIPS, link)
                done.add(link)
                append_file(DONE, link)
            continue

        # Test if video
        if VID_PATTERN.match(link):
            if link not in vids:
                vids.add(link)
                append_file(VIDS, link)
                done.add(link)
                append_file(DONE, link)
            continue

        # Test if image
        if IMG_PATTERN.match(link):
            if link not in imgs:
                imgs.add(link)
                append_file(IMGS, link)
                done.add(link)
                append_file(DONE, link)
            continue

        # Save new queue
        if link not in done:
            queue.append(link)
            append_file(QUEUE, link)
