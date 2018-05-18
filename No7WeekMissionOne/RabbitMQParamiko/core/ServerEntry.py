import pika
import os

result_record = {}


def on_request(ch, method, props, body):
    cmd = body.decode()
    print("请求的指令是: ", cmd)
    if cmd.startswith("check_task"):
        task_id = cmd.strip().split(' ')[1]
        response = search_result(task_id)
    else:
        response = process_cmd(cmd, props.correlation_id)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # else:
    # process_cmd(cmd, props.correlation_id)


def process_cmd(cmd, task_id):
    """执行操作指令"""
    result = ""
    result = os.popen(cmd).readlines()
    print("执行结果: %s" % result)
    record_result(task_id, result)
    return result


def search_result(task_id):
    """根据task_id去搜索对应的结果"""
    response = ""
    if task_id in result_record:
        """说明有这个task_id"""
        response = result_record.get(task_id)
    return response


def record_result(task_id, content):
    """记录操作的结果"""
    if task_id not in result_record:
        result_record[task_id] = content


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='rpc_queue')
    channel.basic_qos(prefetch_count=1)  # 是否需要均衡负载?
    channel.basic_consume(on_request, queue='rpc_queue')
    channel.start_consuming()
