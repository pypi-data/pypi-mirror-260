"""
定义服务返回信息列表
"""


class MyRes:
    """
    支持响应自定义
    """

    def __init__(self, code_list=None):
        """
        初始化
        :param code_list: 自定义的响应码与响应信息列表
        """
        self.code_list = {
            '0000': 'Accepted',
            '2000': 'Success',
            '4000': 'Not Found',
            '5000': 'Error'
        }
        if code_list is not None and type(code_list) == 'dict':
            self.code_list.update(code_list)

    def get_code_message(self, code):
        """
        返回码值对应的信息
        :param code: 码值
        :return: 码值信息
        """
        try:
            msg = self.code_list[code]
        except Exception as e:
            print(e)
            msg = 'None'
        return msg

    def res(self, data=None, code='0000', msg=None):
        """
        响应处理
        :param data: 响应体
        :param code: 响应码
        :param msg: 相应描述
        :return: 响应信息
        """
        if msg is None:
            msg = self.get_code_message(code)
        return {
            'code': code,
            'message': msg,
            'data': data
        }

    def success(self, data=None, code='2000'):
        """
        成功的返回
        :param data: 返回数据
        :param code: 返回码
        :return: 统一返回格式
        """
        return {
            'code': code,
            'message': self.get_code_message(code),
            'data': data
        }

    def error(self, data=None, code='5000'):
        """
        错误的返回
        :param data: 返回数据
        :param code: 返回码
        :return: 统一返回格式
        """
        return {
            'code': code,
            'message': self.get_code_message(code),
            'data': data
        }
