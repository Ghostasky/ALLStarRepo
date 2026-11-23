import os
import sys
import time

import requests

key = os.environ.get("KEY")
url = "https://api.github.com/user/starred"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {key}",
    "X-GitHub-Api-Version": "2022-11-28",
}

rows = []
num = 1  # README 行号
page = 1  # API 翻页号，与行号分开
session = requests.Session()
while True:
    # 每页 100 条；拿满一页翻页，空页即结束
    for attempt in range(3):
        r = session.get(
            url, headers=headers, params={"per_page": 100, "page": page}, timeout=30
        )
        if r.status_code in (403, 429, 500, 502, 503, 504) and attempt < 2:
            time.sleep(5 * (attempt + 1))
            continue
        break
    if r.status_code != 200:
        print(f"fetch failed: {r.status_code} {r.text[:200]}")
        sys.exit(1)
    items = r.json()
    if not items:
        break
    for a in items:
        desc = a["description"]
        if desc is None:
            desc = "None"
        elif len(str(desc)) > 100:
            desc = desc[:100] + "..."
        print(num, a["full_name"])
        rows.append(
            "| "
            + str(num)
            + " |["
            + a["name"]
            + "]("
            + a["html_url"]
            + ") | ["
            + a["owner"]["login"]
            + "]("
            + a["owner"]["html_url"]
            + ") | "
            + desc
            + " | "
            + str(a["stargazers_count"])
            + " | "
            + a["pushed_at"][:10]
            + " |\n"
        )
        num += 1
    page += 1

if not rows:
    print("no starred repos returned, refuse to overwrite README")
    sys.exit(1)

# 全部抓完再一次性写盘：中途失败不会留下被截断的 README
with open("./README.md", "w", encoding="utf-8") as fp:
    fp.writelines("# ALLStarRepo\n\n")
    fp.writelines("这里显示我所有star的repo\n\n")
    fp.writelines("| Num | Name |  auther   | Description  | Stars | Last update |\n")
    fp.writelines("|-------|------|-------------|----------|-------|----|\n")
    fp.writelines(rows)

print("fin")
