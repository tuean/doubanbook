
import random
import time
import urllib3

headerPool = [
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
    {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}
]


def download( url, retrys=2,  delayFlag = True):
    html = None
    if delayFlag:
        sleepSec = random.randint(0, 10) * 0.25
        time.sleep(sleepSec)
        print("延时" + str(sleepSec) + "s")
    else:
        time.sleep(0.1)
        print("延时 0.1s")
    http = urllib3.PoolManager()
    try:
        header = random.choice(headerPool)
        r = http.request('GET', url, headers=header)
        if 200 == r.status:
            html = str(r.data, encoding="utf-8")
        else:
            print(r.status)
            if retrys > 0 and r.status != 404:
                return download(url, retrys - 1, False)
            elif r.status == 403:
                html = "ip"
            else:
                html = None
    except Exception as e:
        print(e.reason)
    return html