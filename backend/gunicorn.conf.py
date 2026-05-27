# encoding: UTF-8
from const import BE_URL

workers = 1    # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
bind = BE_URL
threads = 2    # 多线程，2个暂时就够用

debug = False
reload = False
loglevel = 'debug'
pidfile = "logs/gunicorn.pid"
accesslog = "-"  # 输出到容器标准输出，便于 docker logs 查看
errorlog = "-"  # 输出到容器标准错误，便于 docker logs 查看
timeout = 300   # 每个接口的超时时间
daemon = False  # 容器内以前台方式运行，避免主进程退出
