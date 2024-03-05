import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler
from json import dumps as js_dumps, loads as js_loads
from socket import gethostbyname, gethostname
from orionTools.utils.str_op import dict_contain_key
from functools import wraps


class HttpTools:
    def __init__(self):
        self.routes = {}
        self.request_info = None
        self.req = None

    def analysis_request(self, request_url, request_data=None):
        self.request_info = {"path": "", "params": {}}
        try:
            url = request_url.split("?")
            if request_data is None:
                params = url[1].split("&")
                for i in params:
                    key_and_value = i.split("=")
                    self.request_info["params"][key_and_value[0]] = key_and_value[1]
            else:
                self.request_info["params"] = request_data
            self.request_info['path'] = url[0][1:]
        except Exception as e:
            print(e, traceback.format_exc())
        return self.request_info

    def get(self, request_info):
        try:
            method = self.routes[request_info['path']]
            result = method(**request_info['params'])
        except Exception as e:
            print(e, traceback.format_exc())
            result = str(e)
        return result

    def register(self, my_module, pre_path=None):
        module_dir = dir(my_module)
        for item in module_dir:
            em = getattr(my_module, item)
            if '__flag__' in dir(em) and '__route__' in dir(em):
                if em.__flag__ == 'my_route':
                    route_path = em.__route__
                    if pre_path is not None:
                        route_path = pre_path + route_path
                    self.routes[route_path] = em

    def set_req(self, req):
        self.req = req


ht = HttpTools()


class MyHttpRequest(BaseHTTPRequestHandler):
    my_routes = {}
    server_version = "orion"
    sys_version = "python/3"
    timeout = 60

    def req_all(self):
        return {
            "headers": self.headers,
            "client_address": self.client_address,
            "path": self.path,
            "monthname": self.monthname
        }

    def do_GET(self):
        ht.set_req(self.req_all())
        request_info = ht.analysis_request(self.path)
        result = ht.get(request_info)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        res = js_dumps(result).encode()
        self.end_headers()
        self.wfile.write(res)

    def do_POST(self):
        req_data = self.rfile.read(int(self.headers['content-length']))
        request_data = js_loads(req_data)
        ht.set_req(self.req_all())
        request_info = ht.analysis_request(self.path, request_data)
        result = ht.get(request_info)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(js_dumps(result).encode())


class MyHttpServer:
    def __init__(self, host=None):
        self.server = None
        self.ip = host['ip'] if dict_contain_key(host, 'ip') else gethostbyname(gethostname())
        self.port = host['port'] if dict_contain_key(host, 'port') else "18090"

    def start(self):
        mhr = MyHttpRequest
        mhr.my_routes = ht.routes
        self.server = HTTPServer((self.ip, int(self.port)), mhr)
        print(f"HTTP Server Starting On {self.ip}:{self.port}")
        self.server.serve_forever()


def router(route):
    """
    请求路由器
    :param route: 路由地址
    :return: 原函数
    """

    def out_wrapper(func):
        func.__route__ = route  # 添加路由属性
        func.__flag__ = 'my_route'  # 添加路由标识

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return out_wrapper
