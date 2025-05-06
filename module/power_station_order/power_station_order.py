from database.db_connection import session
from database.models import PowerStationInfo, OrderOperationLog, PvStationDailyMonitor  # 导入模型
from flask import jsonify


def find_order(order_no):
    # 查询订单信息
    order = session.query(PowerStationInfo).filter_by(order_no=order_no).first()
    return order

def find_order_web(order_no):
    # 查询订单信息
    order = session.query(PowerStationInfo).filter_by(order_no=order_no).first()
    if order:
        return jsonify(order.to_dict())
    else:
        return jsonify({"error": "Order not found"}), 404


def find_construction_work_pic(order_no):
    # 查询订单信息
    order = find_order(order_no)
    return order.construction_work_pic

def insert_order_operation_log(order_no, operation_name, operation_result, operation_description, ai_remark):
    # 创建新的操作日志记录
    new_log = OrderOperationLog(
        order_no=order_no,
        operation_name=operation_name,
        operation_result=operation_result,
        operation_description=operation_description,
        ai_remark=ai_remark
    )

    # 添加到会话并提交
    session.add(new_log)
    session.commit()

    return jsonify({"message": "Operation log inserted successfully"}), 201


def find_pv_station_monitor_by_order_no(order_no: str):
    return (session.query(PvStationDailyMonitor)
            .filter_by(order_no=order_no)
            .order_by(PvStationDailyMonitor.record_time.desc())
            .limit(50)
            .all())

def find_order_list():
    order_list = session.query(PowerStationInfo).all()
    return jsonify([order.to_dict() for order in order_list])
