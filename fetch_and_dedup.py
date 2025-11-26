import requests
import os

TRACKER_LIST_FILE = "TrackersListCollection.txt"
OUTPUT_FILE = "out.txt"

def fetch_online_files(file_list_path):
    urls = []
    with open(file_list_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def fetch_and_merge(urls):
    all_lines = set()
    for url in urls:
        try:
            response = requests.get(url, timeout=20)
            if response.ok:
                # 逐行分割并去重
                lines = set(
                    line.strip()
                    for line in response.text.strip().splitlines()
                    if line.strip()
                )
                all_lines.update(lines)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return sorted(all_lines)

def main():
    if not os.path.exists(TRACKER_LIST_FILE):
        print(f"{TRACKER_LIST_FILE} not found.")
        return
    urls = fetch_online_files(TRACKER_LIST_FILE)
    merged_list = fetch_and_merge(urls)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in merged_list:
            f.write(line + "\n")
    print(f"[Done] Wrote {len(merged_list)} unique lines to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
