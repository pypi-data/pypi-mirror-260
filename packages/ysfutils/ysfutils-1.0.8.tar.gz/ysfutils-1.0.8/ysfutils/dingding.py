import copy
import json

import requests


class SendMsg:
    """ 调用自己的dingding服务发送消息 """

    __header = {'Content-Type': 'application/json; charset=utf-8'}
    __txt_msg_template = {
        "webhook": "",
        "secret": "",
        "pcSlide": False,
        "failNotice": False,
        "msgType": "text",
        "msgContent": {
            "isAtAll": False,
            "isAutoAt": True,
            "atMobiles": [
                ""
            ],
            "atUserIds": None,
            "text": ""
        }
    }

    @staticmethod
    def send_txt_msg(server_url: str, webhook: str, secret: str, mobiles: list, text: str):
        msg = copy.deepcopy(SendMsg.__txt_msg_template)
        msg['webhook'] = webhook
        msg['secret'] = secret
        msg['msgContent']['text'] = text
        msg['msgContent']['atMobiles'] = mobiles
        requests.post(server_url, headers=SendMsg.__header, data=json.dumps(msg))
