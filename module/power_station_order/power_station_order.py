from database.db_connection import session
from database.models import PowerStationInfo, OrderOperationLog, PvStationDailyMonitor  # 导入模型
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


def find_order(order_no):
    try:
        # 查询订单信息
        order = session.query(PowerStationInfo).filter_by(order_no=order_no).first()
        return order
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常


def find_order_web(order_no):
    try:
        # 查询订单信息
        order = find_order(order_no)
        if order:
            return jsonify(order.to_dict())
        else:
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常


def find_construction_work_pic(order_no):
    try:
        # 查询订单信息
        order = find_order(order_no)
        return order.construction_work_pic
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常


def insert_order_operation_log(order_no, operation_name, operation_result, operation_description, ai_remark):
    # 创建新的操作日志记录
    try:
        new_log = OrderOperationLog(
            order_no=order_no,
            operation_name=operation_name,
            operation_result=operation_result,
            operation_description=operation_description,
            ai_remark=ai_remark
        )
        session.add(new_log)
        session.commit()
        return jsonify({"message": "Operation log inserted successfully"}), 201
    except Exception as e:
        session.rollback()  # 发生异常时回滚
        return jsonify({"error": str(e)}), 500201


def find_pv_station_monitor_by_order_no(order_no: str):
    try:
        return (session.query(PvStationDailyMonitor)
                .filter_by(order_no=order_no)
                .order_by(PvStationDailyMonitor.record_time.desc())
                .limit(10)
                .all())
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常


def find_pv_station_monitor_by_order_no_web(order_no: str):
    result = find_pv_station_monitor_by_order_no(order_no)
    if result:
        # 将日志记录转换为字典列表，并使用 jsonify 进行序列化
        return jsonify([item.to_dict() for item in result])
    else:
        return jsonify({"error": "No pv run data found for the order"}), 404


def find_order_list():
    try:
        order_list = session.query(PowerStationInfo).all()
        return jsonify([order.to_dict() for order in order_list])
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常


def find_order_operation_log(order_no):
    try:
        # 查询订单信息
        logs = (session.query(OrderOperationLog).filter_by(order_no=order_no)
                .order_by(OrderOperationLog.operation_time.desc())
                .all())
        if logs:
            # 将日志记录转换为字典列表，并使用 jsonify 进行序列化
            return jsonify([log.to_dict() for log in logs])
        else:
            return jsonify({"error": "No logs found for the order"}), 404
    except Exception as e:
        session.rollback()
        raise  # 可根据业务决定是否重新抛出异常
