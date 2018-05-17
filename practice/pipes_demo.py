from multiprocessing import Process, Pipe


def f(conn):
    conn.send([42, None, 'Hello'])
    conn.close()

if __name__ == "__main__":
    """
    新建一个Pipe(duplex)的时候，如果duplex为True，那么创建的管道是双向的;
    如果duplex为False，那么创建的管道是单向的。
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, ))
    p.start()
    print(parent_conn.recv())
    p.join()
