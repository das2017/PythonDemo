# coding: utf-8
import requests
import re

# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()


class Spider12306:
    def __init__(self):
        self.base_station_info = {}
        pass

    def get_station(self):
        """
        获取12306城市名和城市代码的数据
        :return:
        """
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9018'
        r = requests.get(url, verify=False, timeout=30)
        pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
        result = re.findall(pattern, r.text)
        station = dict(result)
        return station

    def get_train_info_url(self, from_station_name, to_station_name, date):
        """
        查询余票url
        """
        from_station = self.base_station_info[from_station_name]
        to_station = self.base_station_info[to_station_name]
        if len(from_station) == 0 or len(to_station) == 0:
            return ""

        url = (
            'https://kyfw.12306.cn/otn/leftTicket/query?'
            'leftTicketDTO.train_date={}&'
            'leftTicketDTO.from_station={}&'
            'leftTicketDTO.to_station={}&'
            'purpose_codes=ADULT'
        ).format(date, from_station, to_station)
        return url

    def get_train_info(self, url):
        """
        查询余票
        """
        r = requests.get(url, allow_redirects=True, verify=False, timeout=30)
        try:
            raw_trains = r.json()['data']['result']
            return raw_trains
        except Exception as e:
            return None

    def map_train_data(self, s):
        """
        转化余票实体
        """
        return (lambda train_list: {
            "SelectStr": train_list[0],
            "Display": train_list[1],
            "TrainNo": train_list[2],
            "TrainCode": train_list[3],
            "FromStationCode": train_list[6],
            "ToStationCode": train_list[7],
            "DepTime": train_list[8],
            "ArrTime": train_list[9],
            "Duration": train_list[10],
            "CanBook": train_list[11] == 'Y',
            "LeftTicket": train_list[12],
            "StartStationTime": train_list[13],
            "TrainLocation": train_list[15],
            "HighSoftSleep": train_list[21],
            "SoftSleep": train_list[23],
            "SoftSeat": train_list[24],
            "NoSeat": train_list[26],
            "HardSleep": train_list[28],
            "HardSeat": train_list[29],
            "SecondClassSeat": train_list[30],
            "FirstClassSeat": train_list[31],
            "BusinessClassSeat": train_list[32],
            "MovingSeat": train_list[33],
            "SeatType": train_list[34],
            "SeatTypeHave": train_list[35]
        })(s.split('|'))

    def query_train(self, from_station_name, to_station_name, date):
        """
        查询余票对外接口
        """
        if len(from_station_name) == 0 or len(to_station_name) == 0 or len(date) == 0:
            return {"data": None, "success": False, "message": "查询余票：请求参数为空"}

        self.base_station_info = self.get_station()
        url = self.get_train_info_url(from_station_name, to_station_name, date)
        if len(url) == "":
            return {"data": None, "success": False, "message": "查询余票：生成url出错"}

        data = self.get_train_info(url)
        map_data = [self.map_train_data(x) for x in data]
        return {"data": map_data, "success": True, "message": ""}


if __name__ == "__main__":
    q = Spider12306()
    station = q.get_station()
    # print("车站信息：{}".format(station))

    q.base_station_info = station
    url = q.get_train_info_url('上海', '南京', '2019-06-15')
    # print("请求url信息：{}".format(url))

    train_info = q.get_train_info(url)
    # print("请求火车票信息：{}".format(train_info))

    map_data = [q.map_train_data(x) for x in train_info]
    # print('转换后火车票实体')
    # [print("{}\n".format(i)) for i in map_data]
