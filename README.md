# Crawler

A simple Python-based website crawler and asset downloader. I put this together to download media from a part of a website from the Wayback Machine for analysis and research.

## Files

`crawl.py` is the crawler that finds files to later download. Possible media files discovered are recorded in several text files: `docs.txt`, `imgs.txt`, `vids.txt` and `zips.txt`. `done.txt` and `queue.txt` are used during the crawling process.

`get.py` downloads all of one media type at a time. A directory for the media type will be created (for example, `imgs`), and all downloaded files will be recorded in `downloaded.txt`. Any 404s will also be recorded in a `404s.txt` file.

## Usage

To get started, you just need to create a `.env` with an entry point (`ENTRY`) and a target text file (`FILES`) variable set. Run `crawl.py` first, then `get.py` once complete.