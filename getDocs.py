import requests
import pandas as pd

# 1. 配置API参数
KEY = "45002ad6ac7fcb281606d3758078a5d6"  # 替换为实际密钥
region = "成都"  # 目标城市
keywords = "旅游景点"  # 搜索关键词
citylimit = "true"  # 限定城市内搜索
show_fields = "business" # 需要返回的字段
page_size = 20  # 每页返回结果数
# page_num = 1  # 页码
page_tot = 6  # 总页数



data = []
for page_num in range(1, page_tot):
    url = f"https://restapi.amap.com/v5/place/text?key={KEY}&keywords={keywords}&region={region}&citylimit={citylimit}&page_size={page_size}&page_num={page_num}&show_fields={show_fields}"
    
    # 2. 发送请求并解析数据
    response = requests.get(url).json()
    if response["status"] != "1":
        raise Exception("API请求失败，错误信息：" + response.get("info", "未知错误"))
    pois = response["pois"]  # 景点列表

    # 3. 提取关键信息（过滤无用字段）
    for index, poi in enumerate(pois):
        data.append({
            "city": region, # 城市
            "type": poi["type"],  # 数据类型：景点
            "name": poi["name"],  # 景点名
            "address": poi["address"],  # 地址
            "tel": poi.get("business", "无").get("tel", "无"),  # 电话
            "price": poi.get("business", "无").get("cost","以现场为准"),  # 门票价格
            "open_time": poi.get("business", "无").get("opentime_today", "以现场为准"),  # 开放时间
            "rating": poi.get("business", "无").get("rating", "无"),  # 评分
        })
        now = index+(page_num-1)*page_size
        data[now]['content'] = f"{poi['name']}位于{poi['address']}，门票{data[now]['price']}，开放时间{data[now]['open_time']}"  # 检索用的文本内容
        # print(f"已处理景点：{data[index]['price']}")
# 4. 保存为CSV（后续用于构建向量库）
df = pd.DataFrame(data)
df.to_csv("data/chengdu_attractions.csv", index=False, encoding="utf-8")
