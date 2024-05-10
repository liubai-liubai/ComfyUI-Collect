import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
import json

# 设置GitHub API的URL和参数
url = "https://api.github.com/search/repositories"
page = 1
params = {
    "q": "comfyui",
    "sort": "stars",
    "order": "desc",
    "per_page": 100,
    "page": page
}

# 读取config.json文件中的token
with open('config.json') as f:
    config = json.load(f)
    token = config['token']

headers = {
    "Authorization": f"token {token}"
}

# 存储所有项目的信息
data = []

print("data长度为" + str(len(data)))

while True:
    # 发送请求到GitHub API
    
    response = requests.get(url, params=params, headers=headers)
    print("请求的url为："+response.url)
    response_json = response.json()

    # 判断下获取的数据是否为空  如果为空就跳出循环  否则继续获取数据
    if "items" not in response_json or len(response_json["items"]) == 0:
        print("items为空,跳出循环")    
        break
    else:
        print("items不为空,继续获取数据")    
        # 解析返回的JSON数据
        for item in response_json["items"]:
            data.append({
                "作者": item["owner"]["login"],
                "项目名称": item["name"],
                "stars数量": item["stargazers_count"],
                "网址": item["html_url"]
            })

            print("序号:" + str(len(data)) + "     | " + "stars数量:" + str(item["stargazers_count"]) + "     | " + "作者:" + str(item["owner"]["login"])+  "     | 项目名称为:" + item["name"] )
            # with open('output.txt', 'a') as f:
            #     # f.write("序号:" + str(len(data)) + "     | " + "stars数量:" + str(item["stargazers_count"]) + "     | " + "作者:" + str(item["owner"]["login"])+  "     | 项目名称为:" + item["name"] + '\n')
            #     f.write(f"序号: {len(data):<5} | stars数量: {item['stargazers_count']:<7} | 作者: {item['owner']['login']:<20} | 项目名称为: {item['name']}\n")
            #  # 更新page参数以获取下一页的数据
            

        # 如果没有下一页，就跳出循环
    if 'link' in response.headers:
        params["page"] += 1
    else:
        print("没有link下一页了")
        break

# 将数据存储到pandas DataFrame中
df = pd.DataFrame(data)

# 将DataFrame写入Excel文件
df.to_excel("github_repos.xlsx", index=False)