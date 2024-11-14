import requests

# url = "https://www.xiaohongshu.com/explore/670a543c000000002603606d?xsec_token=ABb38uWmvUCplnJbQN14KPPJLcUoNHONqhmBe6Y1JCemo=&xsec_source=pc_search&source=unknown"

payload = { 'api_key': '3c8002cb0d731b4bf7c1d2e72ae9d819', 'url': 'https://www.xiaohongshu.com/explore/67263d09000000003c015936?xsec_token=ABwGWue-nfrp-R-eZwBczzzosJQpLGhuCOZOPqga1G43s=&xsec_source=pc_search&source=unknown', 'follow_redirect': 'false' }
r = requests.get('https://api.scraperapi.com/', params=payload)
print(r.text)
