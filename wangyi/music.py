#!/usr/bin/python3

import urllib3


csrf_token = '7af8197a31123355e4d369346920181d'
request_url = 'https://music.163.com/weapi/v3/playlist/detail?csrf_token=' + csrf_token
cookie = 'usertrack=c+xxC1n1sY1eZ7INC0sUAg==; _ntes_nnid=74c6b4dd078a7c4cbf0092d7fc1aa3a4,1509349137971; ' \
         '_ntes_nuid=74c6b4dd078a7c4cbf0092d7fc1aa3a4; Province=021; City=021; _ga=GA1.2.339051942.1509519294; ' \
         'vjuids=-b83542f9b.160648da6a8.0.9fdf45f0b46aa; vjlast=1513515493.1513515493.30; ne_analysis_trace_id=1513515493050; ' \
         'vinfo_n_f_l_n3=aafac4a74c465148.1.0.1513515493054.0.1513515511594; s_n_f_l_n3=aafac4a74c4651481513515493055; ' \
         'JSESSIONID-WYYY=6SVD8a%2FAxqvP40%2BI%5CfoXHPKwBGPOb0iUucfXBqpJxSIWEyK95wMdWf4sYaZ5Y0ZecV0%2BPwj6xsdFmH8y6gt9QOczshtYz%2F%5' \
         'CZFW0nAKrM8NOdz8Oe%5CcRzV15%2B%2Fax%5C%5CISI6VGRFEcB6pNSKG03Wya%5CYUqXXHKs6pp%2BZUSIhVVJxjhXy1CP%3A1513680198706; ' \
         '_iuqxldmzr_=32; __remember_me=true; MUSIC_U=9de0b492647e4661004c6c240edeeb00b058e52201e8175a0e09ab75c9510f062fe10894' \
         'd85fe38e3c2938c79a7097d703e236a71b078ae15e04a48d0b02b5ac91ced7312b15c66a; __csrf=e90d63825df4fa0a308e5d2b4821d2bb; ' \
         '__utma=94650624.1305228059.1509349138.1512453920.1513678400.4; __utmb=94650624.4.10.1513678400; __utmc=94650624; ' \
         '__utmz=94650624.1513678400.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)'

url = 'https://music.163.com/#/my/m/music/playlist?id=143590877'

http = urllib3.PoolManager()
try:
    header=[{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'},
            {'Origin':'https://music.163.com'},
            {'Referer':'https://music.163.com/my/'},
            {}]
    r = http.request('GET', url, headers=header)
