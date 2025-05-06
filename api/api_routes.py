from flask import Flask, jsonify

from module.disaster_warn.ai_disaster_warn import weather_disaster_warn
from module.power_station_order.power_station_order import find_order_web, find_order_list
from module.smart_monitoring.ai_smart_monitoring import ai_smart_monitoring
from module.work_inspect.ai_work_inspect import construction_work_inspect

app = Flask(__name__)


@app.route('/test')
def test():
    return jsonify("test")

@app.route('/order_info/<orderNo>')
def order_info(orderNo):
    # 查询订单信息
    return find_order_web(orderNo)

@app.route('/order_list')
def order_list():
    # 查询订单列表
    return find_order_list()


# 工作现场巡查
@app.route('/order/work_inspect/<order_no>')
def work_inspect(order_no):
    return construction_work_inspect(order_no)
# 灾情预警
@app.route('/order/disaster_warn/<order_no>')
def disaster_warn(order_no):
    return weather_disaster_warn(order_no)

# 智慧监控
@app.route('/order/smart_monitoring/<order_no>')
def smart_monitoring(order_no):
    return ai_smart_monitoring(order_no)



if __name__ == '__main__':
    app.run(debug=True)

