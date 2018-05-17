import pika
import uuid


class RemoteServerControlClass(object):

    def __init__(self, hostname):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))  # 创建连接
        except RuntimeError as e:
            raise e
        self.channel = self.connection.channel()  # 创建通道
        init_queue_result = self.channel.queue_declare(exclusive=True)  # 不允许其它用户访问
        self.callback_queue = init_queue_result.method.queue
        self.channel.basic_consume(self.server_response, no_ack=True,
                                   queue=self.callback_queue)

    def server_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self, cmd):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # exchange使客户端提交的请求消息按照特定的策略转发到Queue存储
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',  # routing_key表示要发送到 的 队列的 名字,如果虚拟主机没有这个队列,则消息被抛弃
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,  # 返回队列
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(cmd))

        if cmd.startswith("check_task"):  # 输入check_taks xxx后才去获取任务结果
            while self.response is None:
                self.connection.process_data_events()  # 这里会回调server_response这个方法
            return int(self.response)


def main():
    notice = """
        基于RabbitMQ rpc实现的主机管理系统
    """
    print(notice)
    while True:
        host = input("请输入要远程管理的机器地址(q:退出): ").strip()
        if host == 'q':
            exit()
        rpc_client = RemoteServerControlClass(host)
        if rpc_client.connection is not None:
            cmd = input("要做什么操作输入指令吧: ").strip()
            rpc_client.request(cmd)
        else:
            print("\033[31;0m连接异常![0m\033")
