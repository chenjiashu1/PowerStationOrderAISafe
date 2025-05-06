from module.power_station_order.power_station_order import find_construction_work_pic, insert_order_operation_log
from utils.aiUtil import call_qwen_vl
from utils.emailUtil import send_email


def construction_work_inspect(order_no):
    pic_url = find_construction_work_pic(order_no)
    if not pic_url:
        return {"result": "false", "remark": "图片地址未找到"}
    oss_urls = [pic_url]

    # 提示词
    prompt = "根据图片判断施工人员是否穿着工服，佩戴安全帽。符合着装要求:穿着工服且佩戴安全帽，则按如下格式输出{\"result\":\"成功\",\"remark\":\"1.穿着工服;2.佩戴安全帽\",\"ai_remark\":\"无\"}。不符合着装要求,则result=失败，remark中说明:原因，ai_remark中说明:识别结果"


    # 调用 qwen-vl-plus 模型
    response = call_qwen_vl(prompt, oss_urls)
    print(f"construction_work_inspect=======: {response}")

    # 存储返回结果
    insert_order_operation_log(order_no, "施工作业检查", response.get("result"), response.get("remark"), response.get("ai_remark"))
    body = f"检查结果: {response['result']}\n备注: {response['remark']}"
    # 发送邮件
    email_title = f"订单:{order_no}施工作业检查"
    send_email(email_title, body)
    return response