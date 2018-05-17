from gevent import monkey; monkey.patch_all()
import gevent
from urllib.request import urlopen


def f(url):
    print(("GET: %s" % url))
    resp = urlopen(url)
    data = resp.read()
    print("%d bytes received from %s." % (len(data), url))

gevent.joinall([
    gevent.spawn(f, "http://192.168.40.215/DevSuite/#home"),
    gevent.spawn(f, "https://github.com/")
])
