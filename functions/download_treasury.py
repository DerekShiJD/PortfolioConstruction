import requests
import time
import datetime
import numpy as np
from bs4 import BeautifulSoup
import bs4
import matplotlib.pyplot as plt


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Error: unable to download data.\n" + url)
        return ""


def fill_data(html, all_data, all_date):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={"class": 't-chart'})
    temp_num = 0

    a = table.children

    for tr in table.children:
        if temp_num == 0:
            temp_num += 1
            continue
        temp_data = []
        temp_date = []
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            all_date.append(tds[0].string)
            for j in range(1, len(tds), 1):
                if '.' in tds[j].string:
                    temp_data.append(float(tds[j].string))
                else:
                    temp_data.append(0.0)
        all_data.append(temp_data)
    return all_data, all_date


def download_treasury_yield(year1=2019, year2=2019):
    all_data = []
    all_date = []
    url0 = 'https://www.treasury.gov/resource-center/' \
          'data-chart-center/interest-rates/pages/TextView.aspx?data=yieldYear&year='

    for i in range(year1, year2+1, 1):
        t0 = time.time()
        print('\nDownload US treasury yield data: ' + str(i))
        url = url0 + str(i)
        html = getHTMLText(url)
        all_data, all_date = fill_data(html, all_data, all_date)
        print('Loading time: ' + str(round(time.time() - t0, 3)) + 's\n' + '-' * 50 + '\n')

    all_data = np.array(all_data)
    all_date = np.array(all_date)
    one_rate = all_data[all_data.shape[0]-1, 3]

    return all_data, all_date, one_rate


if __name__ == '__main__':
    column_name = ['1Mo', '2Mo', '3Mo',	'6Mo', '1Yr', '2Yr', '3Yr',	'5Yr', '7Yr', '10Yr', '20Yr', '30Yr']
    all_data, all_date, one_rate = download_treasury_yield(2019, 2019)
    x = np.array(range(all_data.shape[0]))

    for i in range(all_data.shape[1]):
        y = all_data[:, i]
        plt.plot(x, y, label=column_name[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=0,
               ncol=4, mode="expand", borderaxespad=0.)
    plt.show()


    a = 1
    # plot data









