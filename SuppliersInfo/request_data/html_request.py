import re
import time

import requests

from OtherWork.QiYeHuangYe.request_data.Constant import Headers

my_session = requests.session()
my_session.headers.update(Headers)
res = my_session.get(
    "http://www.tianyancha.com/tongji/2546208953.json?random=" + str(round(time.time(), 3)).replace(".", ""))
content = res.content
random_json = eval(content)
data_v = random_json["data"]["v"]

token = re.match(r".*?token=(.*?);.*?", str(bytes(eval(data_v)))).group(1)
print(token)



