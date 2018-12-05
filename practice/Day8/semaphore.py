import threading, time

def run(n):
    global num
    semaphore.acquire()
    num += 1
    time.sleep(1)
    print("run the thread: %s\n" %n)
    semaphore.release()


if __name__ == "__main__":
    num = 0
    semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
    for i in range(20):
        t = threading.Thread(target=run, args=(i, ))
        t.start()

while threading.active_count() != 1:
    pass
else:
    print("----all threads done-----")
    print(num)


def Hello(init_time):
    print("after %d seconds Hello,world!" % (time.time() - init_time))
current_time = time.time()
t = threading.Timer(5.0, Hello, (current_time, ))
t.start()
