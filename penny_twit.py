from twython import TwythonStreamer
from pandas import DataFrame
import pandas as pd
import re, dateutil, datetime

def write_data(new_data, data):
    today = datetime.datetime.now().strftime('%m/%d/%Y')
    print today
    if data['Date'][len(data)-1].strftime('%m/%d/%Y') != today:
        zero_list = []
        for j in range(len(data.T)):
            zero_list.append(0)
        zero_list[0] = dateutil.parser.parse(today)

        temp = DataFrame(zero_list).T
        temp.columns = data.columns
        data = pd.concat([data,temp]).reset_index(drop=True)

    for i in new_data:
        if i not in list(data.columns):
            data[i] = 0
        data[i][len(data)-1] += 1
        data.to_csv('data.csv', sep=',', index=False)

        print data.ix[len(data)-1,:].tail()

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        self.counter += 1
        print self.counter
        if 'text' in data:
            regex = '[A-Z]{2,5}'
            pattern = re.compile(regex)
            temp = re.findall(pattern, data['text'].encode('utf-8'))
            new_data = []

            for i in range(len(temp)):
                if temp[i] in symbols:
                    new_data.append(temp[i])
            if len(new_data) > 0:
                print new_data
                write_data(new_data, self.data)

    def on_error(self, status_code, data):
        print status_code

fi = open('OTCBB.txt')
symbols = []
for i in fi:
    symbols.append(i.strip())
fi.close()

data = pd.read_csv('data.csv')
date_list = []
for i in data['Date']:
    date_list.append(dateutil.parser.parse(i))
data['Date'] = date_list

stream = MyStreamer(app_key = 'JAwwpso9dTLGOCk80uBSpZpzf', app_secret = 'cif8ZMIUHqMvv6SLf2wTRhJ5vwd7fK2sokaIZkdtPxkyV7XPH3', oauth_token='55765343-140U0dHF4XyItd1vyVLcxoTRC2mgr5ivHO8Ggdr54', oauth_token_secret='2SG13ejh4MbQTjzr4z4YuwIFd2493L2v94uIRgtYomuYk')
stream.symbols = symbols
stream.data = data
stream.counter = 0
stream.statuses.filter(track='stock')