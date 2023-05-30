import json
import requests
import os


key = os.environ.get("KEY")
url = "https://api.github.com/user/starred"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {key}",
    "X-GitHub-Api-Version": "2022-11-28",
}
fp = open("./3.md", "w", encoding="utf-8")
fp.writelines("# ALL repo\n\n")
fp.writelines("这里显示我所有star的repo\n\n")
fp.writelines("| Num | Name |  auther   | Description  | Stars | Last update |\n")
fp.writelines("|-------|------|-------------|----------|-------|----|\n")
i = 1
while True:
    r = requests.get(url, headers=headers, params={"per_page": 1, "page": i})
    if r.status_code == 200:
        if len(r.content) != 2:
            a = r.json()
            print(i, a[0]["full_name"])
            print("\t", a[0]["description"])
            desc = a[0]["description"]
            if a[0]["description"] == None:
                print("aaa")
                desc = "None"
            elif len(str(a[0]["description"])) > 100:
                desc = a[0]["description"][:100] + "..."
            fp.writelines(
                "| "
                + str(i)
                + " |["
                + a[0]["name"]
                + "]("
                + a[0]["html_url"]
                + ") | ["
                + a[0]["owner"]["login"]
                + "]("
                + a[0]["owner"]["html_url"]
                + ") | "
                + desc
                + " | "
                + str(a[0]["stargazers_count"])
                + " | "
                + a[0]["pushed_at"][:10]
                + " |\n"
            )
        else:
            print("end")
            break
    else:
        fp.close()
        break
    i += 1


print("fin")
