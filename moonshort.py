# import json
# import time
# from openai import OpenAI
# from openpyxl import load_workbook

# # 读取config.json文件中的token
# with open('config.json') as f:
#     config = json.load(f)
#     api_key = config['api_key']

# # 替换为您的 Moonshot AI API 密钥
# client = OpenAI(
#     api_key=f"{api_key}",
#     base_url="https://api.moonshot.cn/v1",
# )


# # 加载 Excel 文件
# wb = load_workbook('github_repos.xlsx')
# ws = wb.active

# user_input = ""

# # 初始化计数器
# counter = 0

# # 遍历除第一行之外的每一行
# for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
#     if row[4].value is not None:
#         continue
#     url = row[3].value  # 获取第4列的值（即网址）

#     # 准备对话历史和用户输入
#     history = [
#     {
#         "role": "system",
#         "content": "你是一个总结者，针对发送给你的网址进行访问，总结网址内项目的要点，要点不超过100字且标题为概述，然后详细分析网址中项目的主要的作用，旨在让我明白这个项目是干啥用的，有哪些功能，这个不限字数。其他废话不要多说。",
#         "role": "user",
#         "content": "https://github.com/ZHO-ZHO-ZHO/ComfyUI-Workflows-ZHO ",
#         "role": "assistant",
#         "content": "概述：\
#             ComfyUI-Workflows-ZHO 是一个集合了多种 ComfyUI 工作流的 GitHub 仓库，由用户 ZHO-ZHO-ZHO 创建和维护，提供了丰富的自定义工作流和节点，以增强 ComfyUI 的功能。\
# \
#             主要功能节点和每个节点的功能：\
#             1. **ComfyUI Assistant**：一个专门为 ComfyUI 使用而创建的智能助手，帮助用户创建和解释自定义节点或工作流。\
#             2. **Stable Cascade**：包含六个工作流，涉及标准的稳定级联、Canny ControlNet、Inpainting ControlNet、Img2Img、ImagePrompt Standard 和 ImagePrompt Mix。\
#             3. **3D**：提供三个与3D相关的工作流，包括 CRM Comfy 3D、Sketch to 3D 和 LayerDIffusion + TripoSR V1.0。\
#             4. **LLM + SD**：结合大型语言模型（LLM）和稳定扩散（SD）的工作流，共六个，如 Qwen-VL V1.0、Gemini-pro 等。\
#             5. **Differential Diffusion**：两个工作流，包括简单的 DD 重绘和文生图 + DD 重绘。\
#             6. **YoloWorld-EfficientSAM**：提供图片检测+分割和视频检测+分割的工作流。\
#             7. **Portrait Master 简体中文版**：四个工作流，为 SD1.5 或 SDXL 设计的 Portrait Master 版本。\
#             8. **ArtGallery | Prompt Visualization**：一个用于提示可视化的工作流。\
#             9. **InstantID-ZHO**：三个工作流，包括 InstantID_pose_ref + ArtGallery、自动下载 huggingface hub 和 InstantID_locally_pose_ref。\
#             10. **PhotoMaker-ZHO**：五个工作流，如 Disney-Character_PhotoMaker + DragNUWA、lora + batch 等。\
#             11. **SVD-ZHO**：一个正在进行中（WIP）的工作流 SVD1.1。\
#             12. **I2VGenXL**：两个版本，标准版和基础版。\
#             13. **More Models**：包括 PixArtAlpha Standard V1.0 和 SegMoE。\
#             14. **TravelSuite-ZHO**：提供 Latent_travel_workflow【Zho】.json 和 Latent_travel_compare2composite_workflow【Zho】.json。\
#             15. **WordCloud**：一个 WordCloud 工作流。\
#             16. **APISR in ComfyUI**：两个工作流，APISR 图像或视频批量处理和迭代处理。\
#             17. **SDXS**：一个 SDXS-512-0.9 工作流。\
#             18. **CosXL & CosXL Edit**：包括 CosXL Edit + ArtGallery 1.0。\
#             19. **Stable Diffusion 3 API**：一个 V1.0 SD3 API 工作流。\
#             20. **Phi-3-mini in ComfyUI**：两个工作流 Phi-3-mini-4k + CosXL【Zho】和 Phi-3-mini-4k Chat【Zho】。\
#             \
#             此外，该仓库还包含了作者的社交媒体链接、联系方式、支持作者的方式、以及一个更新日志，记录了仓库的更新历史和新添加的工作流。"
#     }
# ]


#     user_input = f"总结最后面发给你得网址包含的项目作用，根据网址中的描述总结项目所包含的主要功能，不用分析文件，网址为：{url}"
#     print(user_input)
#     # 发送请求
#     completion = client.chat.completions.create(
#         model="moonshot-v1-32k",
#         messages=history + [{"role": "user", "content": user_input}],
#         temperature=0.1,
#     )

#     # 获取响应
#     response = completion.choices[0].message.content
#     print(response)
#      # 将响应写入到第5列
#     ws.cell(row=i, column=5, value=response)

#      # 增加计数器
#     counter += 1

#      # 如果计数器达到10，保存 Excel 文件并重置计数器
#     if counter == 5:
#         wb.save('github_repos.xlsx')
#         counter = 0

#     time.sleep(0.3)
# # 保存 Excel 文件
# wb.save('github_repos.xlsx')