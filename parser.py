from pprint import pp, pprint
from datetime import datetime
import requests
import json
import pytz

def run_status_tracer():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,zh;q=0.5',
        'dnt': '1',
        'if-none-match': 'W/"38b61-um0k4pi+k5bivgZ2mTYMN5mZ3LM"',
        'origin': 'https://livenet.xrpl.org',
        'priority': 'u=1, i',
        'referer': 'https://livenet.xrpl.org/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://data.xrpl.org/v1/network/validator/nHUT6Xa588zawXVdP2xyYXc87LQFm8uV38CxsVzq2RoQJP8LXpJF/reports',
        headers=headers,
    )
    json_response = json.loads(response.text)
    # converting UTC to Kr-Seoul로 변경
    seoul_tz = pytz.timezone('Asia/Seoul')
    for item in json_response['reports']:
        utc_time = datetime.strptime(item['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        seoul_time = utc_time.replace(tzinfo=pytz.utc).astimezone(seoul_tz)
        item['date'] = seoul_time.strftime("%Y-%m-%d %H:%M:%S.%fZ")
    
    sorted_data = sorted(json_response['reports'], key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d %H:%M:%S.%fZ"), reverse=True)
    return sorted_data[0:4]