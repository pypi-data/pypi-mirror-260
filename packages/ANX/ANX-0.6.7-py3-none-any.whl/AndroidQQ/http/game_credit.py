import time
from urllib.parse import urlparse, parse_qs

import requests
from box import Box

from AndroidQQ.http import User_Agent


def query_common_credit():
    try:
        response = requests.get(
            url="https://gamecredit.qq.com/api/qq/proxy/query_common_credit",
            headers={
                "Host": "gamecredit.qq.com",
                "Connection": "keep-alive",
                "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/x-www-form-urlencoded",
                "sec-ch-ua-mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "sec-ch-ua-platform": "\"macOS\"",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://gamecredit.qq.com/static/web/index.html",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cookie": "gs_code=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiQ0NCOEZCNTVENTM1QzM1OEQ2ODYyRTAyQjYyMkI5NEYiLCJhcHBpZCI6IjEwMjA1MzYyMCIsImV4cCI6MTcxNzA4MzM0MCwiaXNzIjoiYXV0aC5nc3BsYXQuY29tIiwibG9naW5fdHlwZSI6IlFRIiwic2lnbiI6ImJBSGFGTkdKdllYM2ItSjlIbDJxYkJHblQ4TTZSSGpCU280Q2JlVVVEa2ciLCJ0b2tlbiI6IjY2MDYyNEYzQzEyRTc3NzdGMjk3OEJENjc5RjMyMEZFIn0.bib1ldrRuL_ceAmNQbmvleLCnafTUpppjTXPGM_KsQDGfwW_umZmaeCHXRiyFIl-De2EuCX2rOu6ouYaF-jtXgiNggcSr99Y2Bh9Cnd0hFEGxFspvL0dvvkldLGs0byWAl4NqIPcF7yCUMzhJcql6AKWCotL_gkiLVt-GL6jiAtkKt7zaJZSA1Q5TzvGvsr8tmi-1wcI3C5-Oj9GgGWKapBiq8Te-kpfYSlcoRljh7XvFPP0WdotVpw86nsl2ICKMyhgXj_iDcCqZmbN8eDllmB03mSB-oSmO_f1IFI7M5EVCN_zEgY0dbMXMpRmV0JbK_h3oph5kbfkASA2boFWBA",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


class credit_score:

    def __init__(self, uin, clientkey):
        # self.uin = '3484129139'
        # self.clientkey = '9f2677a5c3c9dd3571f4c14c3a796f06cd54ade8e7983f68b2e8bdb557e65eabc849b9b87cf8a6ed69f2a3e4b99d2dde'
        #
        self.gs_code = None
        self.uin = uin
        self.clientkey = clientkey
        self.get_gs_code()

    def get_gs_code(self):
        try:
            response = requests.get(url="https://ssl.ptlogin2.qq.com/jump",
                                    params={
                                        "keyindex": "19",
                                        "clientuin": self.uin,
                                        "clientkey": self.clientkey,
                                        "u1": "https://connect.qq.com",
                                        "pt_report": "1",
                                        "pt_aid": "716027609",
                                        "daid": "383",
                                        "style": "35",
                                        "pt_ua": "B0BFB00844CA89BF32B35D60533238A2",
                                        "pt_browser": "Chrome",
                                        "pt_3rd_aid": "102053620",
                                        "pt_openlogin_data": f"appid=716027609&pt_3rd_aid=102053620&daid=383&pt_skey_valid=0&style=35&s_url=https%3A%2F%2Fconnect.qq.com&refer_cgi=authorize&which=&sdkp=pcweb&sdkv=v1.0&time={str(int(time.time()))}&loginty=3&h5sig=G_tqev5eSttaANNnVgcw5gCN25vuzK7ef9fUPcYGmUY&state=qqconnect_1&client_id=102053620&response_type=code&scope=all&redirect_uri=https%3A%2F%2Fgamecredit.qq.com%2Flogin-ui%2Findex.html%3FcPageName%3Dmiddle%26type%3DQQ%26backUrl%3Dreload%26appId%3D102053620&pt_flex=1&loginfrom=&h5sig=G_tqev5eSttaANNnVgcw5gCN25vuzK7ef9fUPcYGmUY&loginty=3&",
                                    }
                                    ,
                                    allow_redirects=False)
            Location = response.headers['Location']

            if Location is None:
                return {'status': False, 'message': '没找到Location'}
            parsed_url = urlparse(Location)
            query_params = parse_qs(parsed_url.query)
            code = query_params.get('code')[0]
            response = requests.get(url=f'https://gamecredit.qq.com/connect?code={code}&appId=102053620&atype=QQ',
                                    allow_redirects=False
                                    )
            self.gs_code = response.cookies.get('gs_code')
            if self.gs_code is None:
                return {'status': False, 'message': '没找到gs_code'}
            return {'status': True, 'cookie': self.gs_code}
        except Exception as e:
            return {'status': False, 'message': f'获取gs_code异常:{e}'}

    def query_common_credit(self):
        if not self.gs_code:
            return {'status': False, 'message': 'gs_code为空', 'score': 0}

        try:
            response = requests.get(
                url="https://gamecredit.qq.com/api/qq/proxy/query_common_credit",
                headers={
                    "Host": "gamecredit.qq.com",
                    "Connection": "keep-alive",
                    "Accept": "application/json, text/plain, */*",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "sec-ch-ua-mobile": "?0",
                    "User-Agent": User_Agent,
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://gamecredit.qq.com/static/web/index.html",
                    "Accept-Encoding": "gzip, deflate, br, zstd",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": "gs_code=" + self.gs_code,
                },
            )
            data = response.json().get('data', {})
            score = data.get('score', -1)
            return {'status': True, 'score': score, 'data': data}
        except requests.exceptions.RequestException:
            return {'status': False, 'score': 0, 'message': '请求失败'}


if __name__ == '__main__':
    pass
    # print(credit_score().query_common_credit())
    # query_common_credit()
#
# ptui_qlogin()

# send_request()
# connect()

# query_common_credit()
