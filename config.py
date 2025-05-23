import os

import dashscope

DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost/pv_station')
# API_KEY = os.getenv('API_KEY', 'your_api_key_here')

ALI_ACCESS_KEY = "sk-77e9f67bb6454269a7b695b3a7f226d6"

GAODE_ACCESS_KEY ="a27fb67760d05b94310381ebf65cfb5f"

dashscope.api_key = ALI_ACCESS_KEY


DIFY_BASE_URL = "http://localhost"
# DIFY_BASE_URL = "http://host.docker.internal"
DATASET_ID = "95319f14-0a6d-438f-95cf-82f9aaca49da"  # 替换为你的知识库ID
DIFY_KNOEWLEDGE_KEY = "dataset-rBfmZMxGAN1oQ2oveUcw9a3Q"  # 替换为你的API Key


prompt = f"""
        你是一个专业的 HTML 到 Markdown 转换器。
        请将以下 HTML 内容整理为清晰、简洁的 Markdown 格式。要求如下：
        - 移除所有 HTML 标签
        - 保留标题、段落和列表结构
        - 提供简洁明了的内容总结
        - 输出格式应为标准 Markdown

        HTML 内容如下：
        """