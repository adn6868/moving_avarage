
import requests
import datetime
import json
import os


class URL_BUILDER:
    def __init__(self, symbol="VNM", start_time=datetime.datetime.today() - datetime.timedelta(days=1), end_time=datetime.datetime.today()):
        self.symbol = symbol
        self.start_time = str(datetime.datetime.timestamp(start_time))
        self.end_time = str(datetime.datetime.timestamp(end_time))
        self.base_url = 'https://iboard.ssi.com.vn/dchart/api/history?resolution=D&symbol=%s&from=%s&to=%s'

    def set_start_time(self, start_time):
        self.start_time = str(datetime.datetime.timestamp(start_time))

    def set_end_time(self, end_time):
        self.end_time = str(datetime.datetime.timestamp(end_time))

    def get_URL(self):
        return self.base_url % (self.symbol, self.start_time, self.end_time)


class STONK_HOADER:
    def __init__(self, symbol="VNM"):
        self.symbol = symbol
        self.time_range = {
            "yesterday": datetime.timedelta(days=1),
            "last_month": datetime.timedelta(days=30),
            "last_year": datetime.timedelta(days=365),
            "five_year": datetime.timedelta(days=365*5)
        }
        self.log_path = 'dat/' + self.symbol + "/"
        self.url_builder = URL_BUILDER(symbol=self.symbol)

    def collecting(self):
        for date_range in self.time_range.keys():
            start_time = datetime.datetime.now() - self.time_range[date_range]
            self.url_builder.set_start_time(start_time)
            try:
                r = requests.get(self.url_builder.get_URL())
                json_return = r.json()
                f = open(self.log_path + self.symbol +
                         "_"+date_range+".json", "w")
                f.write(json.dumps(json_return))
                f.close()
            except:
                print("Unable to collect %s from %s" %
                      (self.symbol, date_range))
            print("Successfully collecting %s with date_range %s" %
                  (self.symbol, date_range))

    def get_URL(self):
        return self.base_url % (self.symbol, self.start_time, self.end_time)


if __name__ == '__main__':
    try:
        os.mkdir('dat')
    except FileExistsError:
        print("Directory ", 'dat',  " already exists")

    vn30 = open('vn30.input', 'r')
    symbol_list = []
    for line in vn30:
        symbol_list.append(line.strip('\n'))
    # symbol_list = ['NRE' , 'VPB' , 'VNM' , 'VJC' , 'VIC' , 'VHM' , 'VCB' , 'TPB' , 'TCH' , 'TCB' , 'STB' , 'SSI' , 'SBT' , 'REE' , 'POW' , 'PNJ' , 'PLX' , 'PDR' , 'NVL' , 'MWG' , 'MSN' , 'MBB' , 'KDH' , 'HPG' , 'HDB' , 'GAS' , 'FPT' , 'CTG' , 'BVH' , 'BID']

    for symbol in symbol_list:
        try:
            os.mkdir('dat/' + symbol)
        except FileExistsError:
            print("Directory ", 'dat/' + symbol,  " already exists")

        S = STONK_HOADER(symbol)
        S.collecting()
