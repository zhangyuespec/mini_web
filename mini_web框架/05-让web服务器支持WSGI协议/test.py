def application(environ,start_response):
    start_response("200 OK",[('Content-Type','text/html;charset=utf-8'),('server','my_web')])
    return 'Hello World!我爱你中国'
