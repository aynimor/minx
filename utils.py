import time


def paser_x_www_form_urlencoded(data):
    pass


def parse_content_type(content_type):
    data = content_type.split("; ")
    parameters = ""
    content_type = data[0]
    if len(data) == 2:
        parameters = data[1]
    return content_type, parameters
    

def parse_form_data(body, boundary):
    # TODO: 实现文件上传解析
    pass


def log(*args, **kwargs):
    formatstr = time_format()
    print(formatstr, *args, **kwargs)


def time_format(unix_time=None):
    if unix_time is None:
        unix_time = time.time()
    localtime = time.localtime(unix_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", localtime)
