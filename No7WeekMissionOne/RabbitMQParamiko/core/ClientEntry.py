import pika
import uuid
import time


class RemoteServerControlClass(object):

    def __init__(self, hostname):
        self.connection = None
        try:
            print("init connect...")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname))  # 创建连接
            print("init success")
        except Exception as e:
            print(e)
        else:
            self.channel = self.connection.channel()  # 创建通道
            init_queue_result = self.channel.queue_declare(exclusive=True)  # 不允许其它用户访问
            self.callback_queue = init_queue_result.method.queue
            self.channel.basic_consume(self.server_response, no_ack=True,
                                       queue=self.callback_queue)

    def server_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            print("response:", self.response.decode())  # 这里必须要decode bytes转str才能正确显示

    def request(self, cmd):
        self.response = None
        self.corr_id = str(uuid.uuid4())  # 生成一串这样的字符串:ec48ec60-72c9-42c6-8bc3-137ab036ce94
        # exchange使客户端提交的请求消息按照特定的策略转发到Queue存储
        self.channel.basic_publish(exchange='', routing_key='rpc_queue',  # routing_key表示要发送到 的 队列的 名字,如果虚拟主机没有这个队列,则消息被抛弃
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,  # 返回队列
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(cmd))

        if cmd.startswith("check_task"):  # 输入check_task xxx后才去获取任务结果
            while self.response is None:
                self.connection.process_data_events()  # 这里会回调server_response这个方法
        else:
            print("当前任务ID:[%s] 无需等待继续输入指令..." % str(self.corr_id))


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
        print("要做什么操作输入指令吧( >>q 可以退出): ")
        if rpc_client.connection is not None:
            while True:
                # 测试代码
                # cmd = 'ls -all'
                # rpc_client.request(cmd)
                # time.sleep(0.5)
                #####
                cmd = input(">>").strip()
                if cmd == 'q':
                    break
                rpc_client.request(cmd)
                time.sleep(0.2)
        else:
            print("\033[31;0m######connect failed!\033[0m")
