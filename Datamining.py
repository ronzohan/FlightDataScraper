import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import threading
import time
import smtplib

def numberForText(text):
    non_decimal = re.compile(r'[^\d.]+')
    return non_decimal.sub('', text)

def formattedDateStringForDate(date):
    return date.strftime('%b %d %Y, %H:%M %p')

def lowestFareForCebuPac(date):
    origin1 = 'CEB'
    destination1 = 'CGY'
    
    url = 'https://beta.cebupacificair.com/Flight/InternalSelect?o1=' + origin1 + '&d1=' + destination1 + '&o2=&d2=&dd1=' + date +'&ADT=1&CHD=0&INF=0&s=true&mon=true'
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html5lib")
    samples = soup.find_all('label', class_="fare-amount")

    values = []

    for sample in samples:
        value = sample.getText().strip()
        values.append(numberForText(value))

    lowestFare = min(values, key=float)
    now = formattedDateStringForDate(datetime.now())
    print('Lowest fare on ' + date + ': ' + lowestFare + ' (' + now +')')

def sendEmail(email):
    return requests.post(
        "https://api.mailgun.net/v3/samples.mailgun.org/messages",
        auth=("api", "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"),
        data={"from": "Excited User <excited@samples.mailgun.org>",
              "to": [email],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomeness!"})

if __name__ == '__main__':
    while True:
        '''
        lowestFareForCebuPac('2017-12-20')
        lowestFareForCebuPac('2017-12-21')
        lowestFareForCebuPac('2017-12-22')
        lowestFareForCebuPac('2017-12-23')
        lowestFareForCebuPac('2017-12-24')
        lowestFareForCebuPac('2017-12-25')
        lowestFareForCebuPac('2017-12-26')
        print('-------------------------')
        print('-------------------------')
        print('-------------------------')
        time.sleep(100)
        '''
        print(sendEmail('ron.zohan@gmail.com').content)
