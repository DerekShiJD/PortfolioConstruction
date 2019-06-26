import requests
import time
import datetime
import numpy as np
from bs4 import BeautifulSoup
import bs4


def period_calculator(date):
    period0 = 946706400
    second_num = 24 * 60 * 60

    date0 = time.strptime('2000-01-01', "%Y-%m-%d")
    date = time.strptime(date, "%Y-%m-%d")

    date0 = datetime.datetime(date0[0], date0[1], date0[2])
    date = datetime.datetime(date[0], date[1], date[2])

    add_date1 = str(date - date0)
    i = 0
    temp_date = ''
    while add_date1[i] != ' ':
        temp_date += add_date1[i]
        i += 1
    add_date1 = int(temp_date)
    period = period0 + add_date1 * second_num

    return period


def url_generator(company_id, date1, date2, freq):

    content = ['https://finance.yahoo.com/quote/', '/history?period1=', '&period2=',
               '&interval=1wk&filter=history&frequency=1wk', '&interval=1mo&filter=history&frequency=1mo']

    period1 = period_calculator(date1)
    period2 = period_calculator(date2)

    if freq == 'week':
        url = content[0] + company_id + content[1] + str(period1) + content[2] + str(period2) + content[3]
    elif freq == 'month':
        url = content[0] + company_id + content[1] + str(period1) + content[2] + str(period2) + content[4]
    else:
        return 'error'
    if len(company_id) < 4:
        print('ID: ' + company_id, end='\t\t\t')
    else:
        print('ID: ' + company_id, end='\t\t')
    return url


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error: unable to download data.\n" + url)
        return ""


def filldata(html):
    all_data_list = []
    date_list = []
    useable_flag = True

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={"data-test": 'historical-prices'})

    for tr in table.find('tbody').children:
        temp_week_data = []
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            if len(tds) != 2:
                temp_close_price = tds[4].string
                temp_close_price = temp_close_price.replace(',', '')
                if temp_close_price == '-':
                    # useable_flag = False
                    continue
                temp_week_data.append(float(temp_close_price))
                temp_week_data.append(0.0)
                date_list.append(tds[0].string)
                all_data_list.append(temp_week_data)
            else:
                length = len(all_data_list)
                if length != 0:
                    dividend = tds[1].find("strong")
                    label = tds[1].find("span")
                    if label.string == 'Dividend':
                        if dividend.string != '':
                            all_data_list[length-1][1] = float(dividend.string)
    # print("Completed.", end='\t')
    all_data_list.reverse()
    date_list.reverse()

    for i in range(1, len(all_data_list), 1):
        temp_return = (all_data_list[i][0] + all_data_list[i][1] - all_data_list[i-1][0]) / all_data_list[i-1][0]
        all_data_list[i].append(temp_return)

    if len(date_list) != 0:
        del date_list[0]
        del all_data_list[0]

    return all_data_list, date_list, useable_flag


def filldataSP500(html):
    all_data_list = []
    date_list = []

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={"data-test": 'historical-prices'})
    for tr in table.find('tbody').children:
        temp_week_data = []
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            temp_close_price = tds[5].string
            temp_close_price = temp_close_price.replace(',', '')
            if temp_close_price == '-':
                continue
            temp_week_data.append(float(temp_close_price))
            # temp_week_data.append(0.00)
            date_list.append(tds[0].string)
            all_data_list.append(temp_week_data)

    # print("Completed.", end='\t')
    all_data_list.reverse()
    date_list.reverse()

    for i in range(1, len(all_data_list), 1):
        temp_return = (all_data_list[i][0] - all_data_list[i-1][0]) / all_data_list[i-1][0]
        all_data_list[i].append(temp_return)

    del date_list[0]
    del all_data_list[0]

    return all_data_list, date_list


def save_data(all_data_list, date_list):
    all_data = np.array(all_data_list)
    date_array = np.array(date_list)
    if __name__ == "__main__":
        np.save('testdata/all_company_all_data_array.npy', all_data)
        np.save('testdata/all_company_date_array.npy', date_array)
        print("All data saved in Function folder ('/testdata')")
    else:
        np.save('data_cache/all_company_data_array.npy', all_data)
        np.save('data_cache/all_company_date_array.npy', date_array)
        print("All data saved in Main folder ('/data_cache')")


def save_dataSP500(all_data_list, date_list):
    all_data = np.array(all_data_list)
    date_array = np.array(date_list)
    if __name__ == "__main__":
        np.save('testdata/SP500_data_array.npy', all_data)
        np.save('testdata/SP500_date_array.npy', date_array)
        print("S&P500 data saved in Function folder ('/testdata')")
    else:
        np.save('data_cache/SP500_data_array.npy', all_data)
        np.save('data_cache/SP500_date_array.npy', date_array)
        print("S&P500 data saved in Main folder ('/data_cache')")


def print_data(company_list):
    if __name__ == "__main__":
        all_date = np.load('testdata/date_array.npy')
        all_data = np.load('testdata/all_data_array.npy')
    else:
        all_date = np.load('data_cache/date_array.npy')
        all_data = np.load('data_cache/all_data_array.npy')

    print('\n\n' + '================' + '===================='*len(company_list) + '\nCompany ID\t|\t', end='')
    for i in range(len(company_list)):
        print(company_list[i] + '\t'*5, end='')
    print('\n----------------' + '--------------------' * len(company_list))
    print('Date \t\t|\t' + 'Pep\t\tDiv\t\t\t' * len(company_list))
    print('================' + '====================' * len(company_list))
    for i in range(all_date[0].shape[0]):
        time.sleep(0.25)
        print(all_date[0][i]+'|\t', end='')
        for j in range(len(company_list)):
            if all_data[j, i, 1] == all_data[0, 0, 1]:
                print(all_data[j, i, 0] + '\t' + all_data[j, i, 1] + '\t\t\t', end='')
            else:
                print(all_data[j, i, 0] + '\t' + all_data[j, i, 1] + '\t\t', end='')
        print()
    print('================' + '====================' * len(company_list))


def main():
    company_list = ['BA', 'MMM', 'PEP', 'CAT', 'DIS', 'HP']
    time1 = '2018-01-01'
    time2 = '2019-01-01'

    all_data = []
    all_date = []

    print("**********************" * 2)

    for cid in company_list:
        t0 = time.time()
        url = url_generator(cid, time1, time2)
        html = getHTMLText(url)
        temp_data, temp_date, useable_flag = filldata(html)
        all_data.append(temp_data)
        all_date.append(temp_date)
        print('Loading time: ' + round(time.time() - t0, 3) + 's')

    save_data(all_data, all_date)
    print_data(company_list)


def downloaddata(company_list, time1, time2, freq):
    flag_download = True
    SP500data = []
    SP500date = []
    all_data = []
    all_date = []

    print("===== Downloading data from Yahoo Finance =====")

    # S&P500 index
    t0 = time.time()
    url = url_generator('%5EGSPC', time1, time2, freq)
    if url == 'error':
        flag_download = False
        return flag_download
    html = getHTMLText(url)
    if html == '':
        flag_download = False
        return flag_download
    temp_data, temp_date = filldataSP500(html)
    SP500data.append(temp_data)
    SP500date.append(temp_date)
    print('Loading time: ' + str(round(time.time() - t0, 3)) + 's')
    # save_dataSP500(SP500data, SP500date)

    # All companies
    for cid in company_list:
        t0 = time.time()
        url = url_generator(cid, time1, time2, freq)
        if url == 'error':
            flag_download = False
            return SP500data, SP500date, all_data, all_date, flag_download
        html = getHTMLText(url)
        if html == '':
            flag_download = False
            return SP500data, SP500date, all_data, all_date, flag_download
        temp_data, temp_date, useable_flag = filldata(html)
        if len(temp_date) == 0:
            continue
        if useable_flag == False:
            continue
        all_data.append(temp_data)
        all_date.append(temp_date)
        print('Loading time: ' + str(round(time.time() - t0, 3)) + 's')

    # save_data(all_data, all_date)

    # SP500data = np.array(SP500data)
    # SP500date = np.array(SP500date)
    # all_data = np.array(all_data)
    # all_date = np.array(all_date)

    return SP500data, SP500date, all_data, all_date, flag_download


if __name__ == "__main__":
    # execute only if run as a script
    company_list = ['MMM', 'ADBE', 'BDX', 'CVX']
    # main()
    # print_data(company_list)
    SP500data, SP500date, all_data, all_date, flag_download = downloaddata(company_list, '2017-01-13', '2018-01-12', 'week')
    a = 1

