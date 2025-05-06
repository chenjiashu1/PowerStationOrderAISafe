import requests
from config import GAODE_ACCESS_KEY

# 高德api文档：https://lbs.amap.com/api/webservice/guide/api/weatherinfo/#t1

def get_weather_data(installation_county_code):
    # 高德天气 API 地址
    url = f"https://restapi.amap.com/v3/weather/weatherInfo"
    # 参数字典
    params = {
        "key": GAODE_ACCESS_KEY,
        "city": installation_county_code,
        # "extensions": "base"  # 返回实况天气
        "extensions": "all"  # 返回预报天气
    }
    response = requests.get(url, params=params)
    print(f"get_weather_data-response=======: {response.json()}")

    return response.json()
