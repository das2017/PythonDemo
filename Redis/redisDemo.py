# coding: utf-8

import redis
import pickle


class RedisClient:
    def __init__(self):
        """
        初始化
        """     
        self.host = "139.198.13.12"
        self.port = 4125
        self.password="uuid845tylabc123"
        self.redis = redis.Redis(host=self.host, port=self.port, decode_responses=True, password=self.password)

    def getRedis(self):
        return self.redis


if __name__ == '__main__':
    rc = RedisClient().getRedis()

    rc.set('number', 123)
    num = rc.get('number')
    print('数字类型数据__存储和读取结果：{}，读取结果类型：{}'.format(num, type(num)))

    rc.set('string', '我是字符串类型')
    str = rc.get('string')
    print('字符串类型数据__存储和读取结果：{}，读取结果类型：{}\n'.format(str, type(str)))

    rc.set('dict', pickle.dumps({"num": 100, "string": "字符串", 'bool': True}, 0).decode())
    dic = rc.get('dict')
    dic_data = pickle.loads(dic.encode())
    print('字典类型数据__存储和读取结果：{}，读取结果类型：{}'.format(dic_data, type(dic_data)))
