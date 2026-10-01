bind = '0.0.0.0:5003'
backlog = 2048
proc_name = 'trainer'
restart = True
deamon = True

workers = 1
worker_class = 'sync'
timeout = 30
keepalive = 2

errorlog = '-'
accesslog = '-'
