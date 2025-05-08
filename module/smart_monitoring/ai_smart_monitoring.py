from database.models import list_to_string
from module.power_station_order.power_station_order import find_pv_station_monitor_by_order_no, \
    insert_order_operation_log
from utils.aiUtil import call_deepseek
from utils.emailUtil import send_email
from utils.fileUtil import markdown_to_pdf2
import re
import threading


def ai_smart_analysis(order_no):
    order_daily_monitors = find_pv_station_monitor_by_order_no(order_no);
    print(f"ai_smart_monitoring-order_daily_monitors: {order_daily_monitors}")

    tableInfo = "CREATE TABLE pv_station_daily_monitor ( id int NOT NULL AUTO_INCREMENT, order_no varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '订单编号', record_time datetime NOT NULL COMMENT '记录时间', voltage decimal(10,2) DEFAULT NULL COMMENT '电压 (V)', current decimal(10,2) DEFAULT NULL COMMENT '电流 (A)', max_module_temp decimal(5,2) DEFAULT NULL COMMENT '最大组件温度 ()', avg_module_temp decimal(5,2) DEFAULT NULL COMMENT '平均组件温度 ()', avg_ambient_temp decimal(5,2) DEFAULT NULL COMMENT '平均环境温度 ()', power_ratio decimal(5,2) DEFAULT NULL COMMENT '功率比 (%)1.1~1.3（超配比）', work_hour_count decimal(6,2) DEFAULT NULL COMMENT '等效利用小时数 (h)', power_generation decimal(10,2) DEFAULT NULL COMMENT '实际发电量 (kWh)', theoretical_power decimal(10,2) DEFAULT NULL COMMENT '理论发电量 (kWh)', system_efficiency decimal(5,2) GENERATED ALWAYS AS (round(((power_generation / theoretical_power) * 100),2)) STORED COMMENT '系统效率 (%)75%~85%', PRIMARY KEY (id) ) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='光伏电站日常数据监测表';"
    format = (
        "markdown\n" "### 可视化报表\n" "\n" "以下是对订单编号为“5”的光伏电站日常数据监测表的分析，生成多种维度的图表和总结分析。\n" "\n" "---\n" "\n" "#### 电压与电流的变化趋势仪表盘图\n" "\n"
        "gauge\n"
        "    title 电压与电流的变化趋势\n"
        "\n" "描述: 上图展示了电压和电流随时间的变化趋势。从图中可以看出，电压和电流在一天内的波动较为平稳，但存在一定的峰值和谷值。\n" "\n" "---\n" "\n" "#### 最大组件温度与平均组件温度对比横向条形图\n" "\n"
        "bar\n"
        "    title 最大组件温度与平均组件温度对比横向条形图\n"
        "")

    prompt = (f"订单：{order_no}的最近运行数据如下：\n\n{list_to_string(order_daily_monitors)}"
              f"\n\n来源于光伏电站日常数据监测表，表结构为：{tableInfo}"
              f"\n您是光伏电站运维专家，帮我分析上述订单数据，输出可视化图形报表，内容要求：纯markdown格式，不能有url"
              # f"报表内容包含：电流/电压仪表盘图；温度散点图+颜色梯度图；发电量-时间变化折线图；电站效率条形图"
              # f"格式如下：{format}"
              )
    print(f"ai_smart_monitoring-prompt: {prompt}")

    # 异步调用 AI 模型
    smart_monitoring_md = call_deepseek(prompt)
    # 提取 markdown 部分内容
    smart_monitoring_md = extract_markdown_content(smart_monitoring_md)
    insert_order_operation_log(order_no, "智慧监控", "成功", "分析光伏电站日常运行数据", "正在生成报表并抄送邮件")
    threading.Thread(target=sendMarkdown, args=(order_no, smart_monitoring_md)).start()

    return "成功"


def convertMarkdownToPdfAndSend(order_no, smart_monitoring_md):
    pdf_file_path = markdown_to_pdf2(smart_monitoring_md)
    email_title = f"订单:{order_no}智慧监控"
    send_email(email_title, smart_monitoring_md, pdf_file_path)


def sendMarkdown(order_no, smart_monitoring_md):
    # 2. 新增：保存为 .md 文件
    md_file_path = f"report_order_{order_no}.md"
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(smart_monitoring_md)

    # 3. 邮件主题和内容
    email_title = f"订单:{order_no}智慧监控"

    # 4. 发送邮件时附带两个文件：PDF 和 Markdown
    send_email(email_title, "", md_file_path)


def extract_markdown_content(content):
    # 去除首尾的 ```markdown 和 ```
    if content.startswith("```markdown") and content.endswith("```"):
        return content[len("```markdown"):-len("```")].strip()
    else:
        print("未找到 markdown 内容块")
        return None
