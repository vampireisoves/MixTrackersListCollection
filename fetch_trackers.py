import requests

def read_links(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        links = {line.strip() for line in f if line.strip()}
    return list(links)

def fetch_and_collect(links):
    result = set()
    for url in links:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            lines = set(
                line.strip()
                for line in resp.text.splitlines()
                if line.strip()
            )
            result.update(lines)
        except Exception as e:
            print(f"链接获取失败: {url}，错误: {e}")
    return result

def save_to_file(txt_path, data):
    with open(txt_path, 'w', encoding='utf-8') as f:
        for line in sorted(data):
            f.write(f"{line}\n")

if __name__ == "__main__":
    links = read_links("TrackersListCollection.txt")
    print(f"读取到 {len(links)} 个唯一链接。")
    all_trackers = fetch_and_collect(links)
    print(f"共收集到 {len(all_trackers)} 个唯一条目。")
    save_to_file("out.txt", all_trackers)
    print("结果已保存到 out.txt")
