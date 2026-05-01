import requests
import os
import sys
import time

URLS = [
    ('hotel_tvn.m3u', 'https://iptv-sources-by2.pages.dev/hotel_tvn.m3u'),
    ('youhun.m3u',    'https://iptv-sources-by2.pages.dev/youhun.m3u'),
]

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
}

def download_file(filename, url):
    """下载单个文件，成功返回 True，失败返回 False"""
    try:
        print(f"[↓] 正在下载: {filename} from {url}")
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(resp.content)
        print(f"[✓] 保存完成: {filename} ({len(resp.content)} bytes)")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[✗] 下载失败: {filename} — {e}", file=sys.stderr)
        return False

def main():
    print(f"=== 开始爬取 M3U 播放列表 === {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    success_count = 0
    for filename, url in URLS:
        if download_file(filename, url):
            success_count += 1
        # 两个请求之间稍作停顿，避免被限
        time.sleep(1)
    
    print(f"=== 下载完成：成功 {success_count}/{len(URLS)} === {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 全部成功则退出码 0，否则 1（可触发 workflow 的 failure 通知）
    sys.exit(0 if success_count == len(URLS) else 1)

if __name__ == '__main__':
    main()
