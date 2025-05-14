from tkinter import messagebox

from openai import OpenAI
import time
import json
from config import ALI_ACCESS_KEY
from dashscope import VideoSynthesis
from http import HTTPStatus

# 设置通义千问 API Key（通过 OpenAI 兼容模式）
client = OpenAI(
    api_key=ALI_ACCESS_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
# 调用 qwen - vl - plus 模型（支持多图片输入）
def call_qwen_vl(prompt, image_urls):
    print(f"call_qwen_vl-url=======: {image_urls}")
    start_time = time.time()  # 记录开始时间
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            *[{"type": "image_url", "image_url": {"url": url}} for url in image_urls]
        ]
    }]

    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=messages,
            response_format= {"type": "json_object"},
            temperature=0.7  # 控制输出随机性，0.7 为适中
        )
        end_time = time.time()  # 记录结束时间
        print(f"call_qwen_vl耗时: {end_time - start_time} 秒")  # 输出耗时
        print(f"call_qwen_vl-response=======: {response}")
        try:
            response_json = json.loads(response.choices[0].message.content)
            return response_json
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 解析失败", f"无法解析返回内容为 JSON：{str(e)}")
            return None
    except Exception as e:
        messagebox.showerror("call_qwen_vl模型调用失败", f"请检查网络1或 API Key：{str(e)}")
        return None


def sample_async_call_i2v():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    rsp = VideoSynthesis.async_call(
        model='wanx2.1-i2v-turbo',
                                    prompt='一只猫在草地上奔跑',
                                    img_url='https://cdn.translate.alibaba.com/r/wanx-demo-1.png')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print("task_id: %s" % rsp.output.task_id)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # get the task information include the task status.
    status = VideoSynthesis.fetch(rsp)
    if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)  # check the task status
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # wait the task complete, will call fetch interval, and check it's in finished status.
    rsp = VideoSynthesis.wait(rsp)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
def sample_call_i2v():
    # call sync api, will return the result
    print('please wait...')
    rsp = VideoSynthesis.call(model='wanx2.1-i2v-turbo',
                              prompt='一只猫在草地上奔跑',
                              img_url='https://cdn.translate.alibaba.com/r/wanx-demo-1.png')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.video_url)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

def call_wanx2(prompt,img_url):
    print(f"call_wanx2-start=======")

    start_time = time.time()  # 记录开始时间

    try:
        response = VideoSynthesis.call(model='wanx2.1-t2v-turbo',
                                  prompt=prompt,
                                  img_url=img_url)
        end_time = time.time()  # 记录结束时间
        print(f"call_wanx2 耗时: {end_time - start_time} 秒")  # 输出耗时花了84.99245738983154 秒才生成，生成出来的结果差强人意
        print(f"call_wanx2-response=======: {response}")
        if response.status_code == HTTPStatus.OK:
            return response.output.video_url
    except Exception as e:
        messagebox.showerror("call_wanx2模型调用失败", f"请检查网络1或 API Key：{str(e)}")
        return None


# from urllib.parse import urlparse, unquote
# from pathlib import PurePosixPath
# import requests
# from dashscope import ImageSynthesis
#
# def call_wanx_v1(prompt,img_url):
#     print(f"call_wanx_v1-start=======")
#     start_time = time.time()  # 记录开始时间
#     rsp = ImageSynthesis.call(api_key=ALI_ACCESS_KEY,
#                               model=ImageSynthesis.Models.wanx_v1,
#                               prompt=prompt,
#                               n=1,
#                               style='<watercolor>',
#                               size='1024*1024')
#     print('response: %s' % rsp)
#     if rsp.status_code == HTTPStatus.OK:
#         # 在当前目录下保存图片
#         for result in rsp.output.results:
#             file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
#             with open('./%s' % file_name, 'wb+') as f:
#                 f.write(requests.get(result.url).content)
#     else:
#         print('sync_call Failed, status_code: %s, code: %s, message: %s' %
#               (rsp.status_code, rsp.code, rsp.message))


def call_qwen_plus(prompt):
    try:
        start_time = time.time()  # 记录开始时间
        completion = client.chat.completions.create(
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            model="qwen-plus",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
                ]
        )
        end_time = time.time()  # 记录结束时间
        print(f"call_qwen_plus 耗时: {end_time - start_time} 秒")  # 输出耗时
        print(f"call_qwen_plus-response=======: {completion}")
        return completion.choices[0].message.content
    except Exception as e:
        messagebox.showerror("call_qwen_plus模型调用失败", f"请检查网络1或 API Key：{str(e)}")
        return None

def call_deepseek(prompt):
    try:
        start_time = time.time()  # 记录开始时间
        completion = client.chat.completions.create(
            model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        end_time = time.time()  # 记录结束时间
        print(f"call_deepseek-耗时: {end_time - start_time} 秒")  # 输出耗时
        print(f"call_deepseek-response=======: {completion}")
        return completion.choices[0].message.content
    except Exception as e:
        messagebox.showerror("call_deepseek-模型调用失败", f"请检查网络1或 API Key：{str(e)}")
        return None
def call_ocr(prompt,img_url):
    completion = client.chat.completions.create(
        model="qwen-vl-ocr-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": img_url
                    },
                      # qwen-vl-ocr-latest支持在以下text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                     # 如调用qwen-vl-ocr-1028，模型会使用固定Prompt：Read all the text in the image.不支持用户在text中传入自定义Prompt
                    {"type": "text",
                     "text": prompt},
                ]
            }
        ])

    print(f"============={completion.choices[0].message.content}")
    print(f"============={completion}")

def call_qwen_vl(prompt, image_urls):
    print(f"call_qwen_vl-url=======: {image_urls}")
    start_time = time.time()  # 记录开始时间
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            *[{"type": "image_url", "image_url": {"url": url}} for url in image_urls]
        ]
    }]

    try:
        response = client.chat.completions.create(
            model="qwen-vl-plus",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7  # 控制输出随机性，0.7 为适中
        )
        end_time = time.time()  # 记录结束时间
        print(f"call_qwen_vl耗时: {end_time - start_time} 秒")  # 输出耗时
        print(f"call_qwen_vl-response=======: {response}")
        try:
            response_json = json.loads(response.choices[0].message.content)
            return response_json
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON 解析失败", f"无法解析返回内容为 JSON：{str(e)}")
            return None
    except Exception as e:
        messagebox.showerror("call_qwen_vl模型调用失败", f"请检查网络1或 API Key：{str(e)}")
        return None