
import requests
import json
import os

sys_path = os.path.dirname(os.path.realpath(__file__))

def get_github_token():
    try:
        config_path = os.path.join(sys_path, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        token = config["token"]
    except:
        print("Error: token is required")
        return ""
    return token



class lb_collect:
    def __init__(self):
        pass
    CATEGORY = "LB-LB"

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "keywords": ("STRING", {"default": "ComfyUI", "placeholder": "请输入要搜索的关键词","multiline": False}),
                "order_number": ("INT",{
                    "default": 100,  # 默认
                    "min": 1,
                    "max": 1000,
                    "step": 1,  # 步长
                    "display": "order-number"}),
            },
            "optional": {
                
                "author": ("BOOLEAN", {"default": True}),
                "project_name": ("BOOLEAN", {"default": True}),     
                "stars_count": ("BOOLEAN", {"default": True}), 
                "project_url": ("BOOLEAN", {"default": True}),
            },
        }

    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "collect"

    def collect(self,keywords,order_number,author,project_name,stars_count,project_url):
        # 1加载模型========================================================================
        # 设置GitHub API的URL和参数
        url = "https://api.github.com/search/repositories"
        page = 1
        params = {
            "q": keywords,
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        # 读取config.json文件中的token
    
        token = get_github_token()

        headers = {
            "Authorization": f"token {token}"
        }

        # 存储所有项目的信息
        data = []

        output = ""
        
        while True:
            # 发送请求到GitHub API
            response = requests.get(url, params=params, headers=headers)
            response_json = response.json()

            # 判断下获取的数据是否为空  如果为空就跳出循环  否则继续获取数据
            if "items" not in response_json or len(response_json["items"]) == 0:
                print("items为空,跳出循环")    
                break
            else:
                print("items不为空,继续获取数据")    
                # 解析返回的JSON数据
                # 如果获取的数据大于等于order_number，就跳出循环
                if len(data) >= order_number:
                    print("获取的数据大于等于order_number，跳出循环")
                    break
                for item in response_json["items"]:
                    if len(data) >= order_number:
                        print("获取的数据大于等于order_number，跳出循环")
                        break
                    else:
                        data.append({
                            "author": item["owner"]["login"],
                            "project_name": item["name"],
                            "stars_count": item["stargazers_count"],
                            "project_url": item["html_url"]
                        })

                # 如果没有下一页，就跳出循环
            if 'link' in response.headers:
                params["page"] += 1
            else:
                print("没有link下一页了")
                break
            
            # 将Data中的数据按一定格式输出
            
        for i in range(len(data)):
            output += f"order: {i+1:<5} "
            if author:
                output += f"author: {data[i]['author']:<20} "
            if stars_count:
                output += f"stars: {data[i]['stars_count']:<7} "    
            if project_name:
                output += f"name: {data[i]['project_name']:<25} "
            if project_url:
                output += f"url: {data[i]['project_url'] } "
            output += "\n"
            
        return (output,)


# value为类名称
NODE_CLASS_MAPPINGS = {
    # wechat
    "LB-test":lb_collect,

}

# 映射节点名称，显示在节点的左上角
# value为节点上显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    # wechat
    "LB-test":"collect",

}