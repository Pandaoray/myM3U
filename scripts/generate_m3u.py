#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_m3u.py
---------------
本脚本用于自动下载并筛选 IPTV m3u 频道列表，适合非技术用户和自动化场景（如 GitHub Actions）。
功能：
- 下载指定的 m3u 源文件
- 按自定义关键词模糊筛选频道
- 输出标准 m3u 文件，便于 IPTV 播放器使用

Python 版本：3.11+
"""

import os
import sys

try:
    import requests
except ImportError:
    print("缺少 requests 库，请先运行：pip install requests")
    sys.exit(1)

# 源 m3u 文件 URL
M3U_URLS = [
    "https://iptv-org.github.io/iptv/countries/cn.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u"
]

# 自定义黑名单关键词列表（频道名或 URL 命中任一关键词将被排除，优先于白名单，支持自定义）
BLACKLIST = ["测试", "广告"]

# 自定义白名单关键词列表（仅频道名或 URL 命中任一关键词才会保留，黑名单优先）
KEYWORDS = ["CCTV", "新闻", "台", "视", "频道", "CNN", "BBC", "FOX"]

# 输出文件路径
OUTPUT_PATH = os.path.join("output", "custom.m3u")

def download_m3u(url):
    """
    下载 m3u 文件内容
    :param url: m3u 文件的 URL
    :return: 文本内容（str），如失败则返回 None
    """
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except Exception as e:
        print(f"下载失败：{url}\n原因：{e}")
        return None

def parse_and_filter_m3u(m3u_text, keywords, blacklist):
    """
    解析 m3u 内容，先按黑名单关键词排除频道，再按白名单关键词筛选。
    黑名单优先级高于白名单：频道名或 URL 只要命中黑名单关键词，则无论是否命中白名单，均被排除；
    否则再按白名单关键词筛选，只有命中白名单关键词的频道才会保留。

    :param m3u_text: m3u 文件内容
    :param keywords: 白名单关键词列表
    :param blacklist: 黑名单关键词列表
    :return: 符合条件的频道条目列表，每项为 (extinf, url)
    """
    lines = m3u_text.splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            extinf = line
            # 查找下一个非注释且非空行作为 URL
            j = i + 1
            while j < len(lines):
                url_line = lines[j].strip()
                if url_line and not url_line.startswith("#"):
                    break
                j += 1
            else:
                i += 1
                continue
            url = url_line
            extinf_lower = extinf.lower()
            url_lower = url.lower()
            # 黑名单优先：命中黑名单关键词直接排除
            if any(kw.lower() in extinf_lower or kw.lower() in url_lower for kw in blacklist):
                i = j
                i += 1
                continue
            # 白名单关键词匹配
            if any(kw.lower() in extinf_lower or kw.lower() in url_lower for kw in keywords):
                result.append((extinf, url))
            i = j
        i += 1
    return result

def main():
    # 创建输出目录
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    all_entries = []
    for url in M3U_URLS:
        print(f"正在下载：{url}")
        m3u_text = download_m3u(url)
        if not m3u_text:
            print(f"跳过：{url}")
            continue
        entries = parse_and_filter_m3u(m3u_text, KEYWORDS, BLACKLIST)
        print(f"已筛选 {len(entries)} 条频道")
        all_entries.extend(entries)
    # 去重（按 EXTINF+URL 唯一）
    seen = set()
    unique_entries = []
    for extinf, url in all_entries:
        key = (extinf, url)
        if key not in seen:
            unique_entries.append((extinf, url))
            seen.add(key)
    # 写入输出文件
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for extinf, url in unique_entries:
            f.write(f"{extinf}\n{url}\n")
    print(f"已生成自定义 m3u 文件：{OUTPUT_PATH}，共 {len(unique_entries)} 条频道")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"脚本运行出错：{e}")
        sys.exit(2)