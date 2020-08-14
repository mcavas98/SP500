import requests
import lxml
import pandas as pd
import bs4
alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
base_url = 'https://markets.businessinsider.com/index/components/s&p_500/'
res = requests.get(base_url)
alp2=['a']
'''
soup = bs4.BeautifulSoup(res.text,'lxml')
num_of_corps = (len(soup.select('tr')))-2
corporation = (soup.select('td')[i])#start 6 step 11
price_close = (soup.select('td')[j])#start 7 step 11
three_month_diff_base = (soup.select('.text-right')[k])#start 13 step 8
six_mont_diff_base = (soup.select('.text-right')[l])#8 start 14 step 8 
year_diff = (soup.select('.text-right')[m])#start 15 step 8 
'''

#script
corp_names = []
closes = []
mystr = ''
three_month = ''
six_month =''
for letter in alp2:
    scrape_url = base_url + letter
    res = requests.get(scrape_url)
    soup = bs4.BeautifulSoup(res.text,'lxml')
    num_of_corps = (len(soup.select('tr')))-2
    i=6
    j=7
    k = 13
    l = 14
    m = 15
    for turn in range(0, num_of_corps):
        corporation = (soup.select('td')[i])
        latest_price = (soup.select('td')[j])
        three_month_diff_base = (soup.select('.text-right')[k])
        six_mont_diff_base = (soup.select('.text-right')[l])
        year_diff = (soup.select('.text-right')[m])
        i += 11
        j += 11
        k += 8
        l += 8
        m += 8
        corp_names.append(corporation.getText().strip())
        mystr += latest_price.getText()
        three_month += (three_month_diff_base.getText())
        six_month += (six_mont_diff_base.getText())
#binlik ayıran virgülleri atıyo
mystr = mystr.split()
for n in range(len(mystr)):
    if ',' in mystr[n]:
        mystr[n] = mystr[n].replace(',', '')

previous_closes = []
#sadece last close valuelari ekliyo
for i in range(0,len(mystr)):
    if i%2 != 0:
        previous_closes.append(float(mystr[i]))


#puan degil sadece yuzdelik artış,azalış ve yüzde işaretlerini kaldırma 3 aylık data
three_mo = []
for i in range(0,len(three_month.split())):
    if i%2 != 0:
        three_mo.append(three_month.split()[i])
for i in range(0,len(three_mo)):
    three_mo[i] = float(three_mo[i].replace('%',''))

#puan degil sadece yuzdelik artış,azalış ve yüzde işaretlerini kaldırma 6 aylık data
six_mo = []
for i in range(0,len(six_month.split())):
    if i%2 != 0:
        six_mo.append(six_month.split()[i])
for i in range(0,len(six_mo)):
    six_mo[i] = float(six_mo[i].replace('%',''))


dict = {'Corporation Name':corp_names,'Three Month Change(%)':three_mo,'Six Month Change(%)':six_mo,'Previous Close Value':previous_closes}
df = pd.DataFrame(dict)

df.index=df.index+1
df.to_csv('S&P500 DATA.csv')



import datetime
from datetime import timedelta


def func(months,trend,n):
    if months == 3:
        if trend[0].lower() == 'i':
            df2 =  (df.sort_values(by=['Three Month Change(%)'],ascending=False)[['Corporation Name','Three Month Change(%)','Previous Close Value']].head(n))
            df2 = df2.reset_index(drop=True)
            df2.index += 1
            print("Results from last 3 months starting at:\n", (datetime.datetime.now() - timedelta(days=90)))
            print(f"Companies with the most increase in value over the last {months} months: ")
            pd.set_option("display.max_columns", 3)
            return df2

        elif trend[0].lower() == 'd':
            df2 =  (df.sort_values(by=['Three Month Change(%)'],ascending=True)[['Corporation Name','Three Month Change(%)','Previous Close Value']].head(n))
            df2 = df2.reset_index(drop=True)
            df2.index += 1
            print("Results from last 3 months starting at:\n", (datetime.datetime.now() - timedelta(days=90)))
            print(f"Companies with the most decrease in value over the last {months} months: ")
            pd.set_option("display.max_columns", 3)
            return df2

    elif months == 6:
        if trend[0].lower() == 'i':
            df2 = (df.sort_values(by=['Six Month Change(%)'],ascending=False)[['Corporation Name','Six Month Change(%)','Previous Close Value']].head(n))
            df2 = df2.reset_index(drop=True)
            df2.index += 1
            pd.set_option("display.max_columns", 3)
            print("Results from last 3 months starting at:\n", (datetime.datetime.now() - timedelta(days=90)))
            print(f"Companies with the most increase in value over the last {months} months: ")
            return df2
        elif trend[0].lower() == 'd':
            df2 = (df.sort_values(by=['Six Month Change(%)'],ascending=True)[['Corporation Name','Six Month Change(%)','Previous Close Value']].head(n))
            df2 = df2.reset_index(drop=True)
            df2.index += 1
            pd.set_option("display.max_columns", 3)
            print("Results from last 3 months starting at:\n", (datetime.datetime.now() - timedelta(days=90)))
            print(f"Companies with the most decrease in value over the last {months} months: ")
            return df2




inspect = True
print('Welcome to the S&P500 inspector tool: ')
while inspect == True:
    months = int(input('Would you like to view 3 or 6 month trends? '))
    trend = input('Indicate type of trend. Increasing, Decreasing or Sideways ')
    n = int(input('Enter the number of companies to be displayed: '))
    print('\n',func(months,trend,n))
    q = input('Would you like to continue inspecting: ')
    if q[0].lower() == 'n':
        print('Goodbye')
        break
    else:
        continue
