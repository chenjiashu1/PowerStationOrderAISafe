from flask import current_app

from module.disaster_warn.gaode_weather import get_weather_data
from module.power_station_order.power_station_order import find_order, insert_order_operation_log
from utils.aiUtil import call_wanx2, call_qwen_plus, sample_call_i2v, sample_async_call_i2v
from utils.emailUtil import send_email
import asyncio
import threading
def parse_wind_power(wind_power_str):
    """解析风力等级字符串，返回最大风速等级"""
    if "-" in wind_power_str:
        return int(wind_power_str.split("-")[1])
    else:
        return int(wind_power_str)
async def ai_disaster_warn(order, weather_data):
    # 分析天气数据，判断自然灾害等级
    if "forecasts" not in weather_data or not weather_data["forecasts"]:
        return "无法获取天气预报数据"

    forecast = weather_data["forecasts"][0]
    if "casts" not in forecast or not forecast["casts"]:
        return "无法获取详细天气预报"

    # 获取未来一天的天气信息
    daily_forecast = forecast["casts"][0]
    # 风力
    day_power = daily_forecast.get("daypower", "未知")
    night_power = daily_forecast.get("nightpower", "未知")
    # 风向
    day_wind = daily_forecast.get("daywind", "未知")
    night_wind = daily_forecast.get("nightwind", "未知")

    # 解析风力等级
    max_day_power = parse_wind_power(day_power) if day_power != "未知" else 0
    max_night_power = parse_wind_power(night_power) if night_power != "未知" else 0

    # 获取最大风速等级
    max_wind_power = max(max_day_power, max_night_power)
    print(f"ai_disaster_warn-max_wind_power: {max_wind_power},max_support_wind_power:{order.max_support_wind_power}")

    # 判断电站是否有可能遭到破坏
    # 这里可以根据具体需求调整阈值和条件
    if max_wind_power > order.max_support_wind_power:

        # await generate_wind_destroy_future_view(max_wind_power, order)
        await generate_emergency_management_plan(max_wind_power, order)

        return f"预警：正在生成应急管理方案和预测未来一天光伏电站的破坏情况视频，请查看"
    else:
        insert_order_operation_log(order.order_no, "灾情预警", "成功", "电站暂无破坏风险",
                                   "")
        return f"正常：电站暂无破坏风险。"


async def generate_emergency_management_plan(max_wind_power, order):
    prompt1 = f"当前光伏电站可承载的最大风力为{order.max_support_wind_power}，未来一天最大风力{max_wind_power}，为光伏电站梳理出一份完备的应急指挥方案"
    # 异步调用 AI 模型
    emergency_management_plan = call_qwen_plus(prompt1)
    content = (f"应急管理方案:{emergency_management_plan}")
    insert_order_operation_log(order.order_no, "灾情预警", "成功", "超过光伏电站可承载的最大风力",
                               content)
    email_title = f"订单：{order.order_no}应急管理方案"
    send_email(email_title, content)

async def generate_wind_destroy_future_view(max_wind_power, order):

    prompt2 = f"当前光伏电站可承载的最大风力为{order.max_support_wind_power}，未来一天最大风力{max_wind_power}，电站正常照片如图所示，请根据照片预测未来一天光伏电站的破坏情况，视频时长2秒钟"
    sample_async_call_i2v()
    # 异步调用 AI 模型
    wind_destroy_future_view = call_wanx2(prompt2, order.pv_pic)

    content = (f"预测未来一天光伏电站的破坏情况视频:{wind_destroy_future_view}")
    insert_order_operation_log(order.order_no, "灾情预警", "成功", "超过光伏电站可承载的最大风力 ",
                               "")
    email_title = f"订单：{order.order_no}预测未来一天光伏电站的破坏情况视频"

    send_email(email_title, content)


def weather_disaster_warn(order_no):
    order = find_order(order_no)
    print(f"weather_disaster_warn-order={order_no}======: {order}")

    # 获取天气数据
    weather_data = get_weather_data(order.installation_county_code)
    # 分析天气数据
    asyncio.run(ai_disaster_warn(order, weather_data))
    # threading.Thread(target=run_ai_disaster_warn, args=(order, weather_data)).start()

    # 返回分析结果
    print(f"weather_disaster_warn-返回天气")

    return weather_data

# def run_ai_disaster_warn(order, weather_data):
#     asyncio.run(ai_disaster_warn(order, weather_data))