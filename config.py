import os

import dashscope

DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:root@localhost/pv_station')
# API_KEY = os.getenv('API_KEY', 'your_api_key_here')

ALI_ACCESS_KEY = "sk-77e9f67bb6454269a7b695b3a7f226d6"

GAODE_ACCESS_KEY ="a27fb67760d05b94310381ebf65cfb5f"

dashscope.api_key = ALI_ACCESS_KEY


