import json
import requests
import csv

def requests_web_data(url):
    try:
        headers = {"User-Agent": "", "Cookie": ""}
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        print('requests error!')
    else:
        return r.content

#print(requests_web_data("https://www.eecso.com/test/weibo/apis/getlatest.php"))
def get_weibo_historical_data():
    #latest_time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php'
    #latest_time_id = json.loads(requests_web_data(latest_time_id_url).decode('utf-8'))[0] 
    latest_time_id = 111005
    time_ids = []
    for x in range(96513, 111005 + 1, 180):    # time_id=48438：2020-01-01
        time_id_url = 'https://www.eecso.com/test/weibo/apis/getlatest.php?timeid=' + str(x)
        time_data = json.loads(requests_web_data(time_id_url).decode('utf-8'))
        #print(time_data)
        if time_data is not None:
            time = time_data[1].split(' ')[1].split(':')[0]
            #print(time)
            if time == '00' or time == '12':
                time_ids.append(time_data[0])
                #print(time_ids)
    if time_ids[-1] != latest_time_id:
        time_ids.append(latest_time_id)
    #通过筛选的time_id获取一月份的热搜数据
    weibo_hot_data = []
    for time_id in time_ids:
        historical_data_url = 'https://www.eecso.com/test/weibo/apis/currentitems.php?timeid=' + str(time_id)
        data = json.loads(requests_web_data(historical_data_url).decode('utf-8'))
        weibo_hot_data.append(data)

    #print(weibo_hot_data)
    data_excel = weibo_hot_data
    with open('27MarTopSearch.csv','w',newline='',encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for row in data_excel:
            for each_col in row:    
                writer.writerow(each_col)

    return weibo_hot_data

if __name__ == '__main__':
   get_weibo_historical_data()
