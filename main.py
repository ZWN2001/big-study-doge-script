import requests
import re

openids = ['----']
printHistory = False
proxies = {"https": 'https://127.0.0.1:7890'}


def getHistory(current_version, openid):
    url = "http://qndxx.youth54.cn/SmartLA/dxx.w?method=queryPersonStudyRecord"
    headers = {
        "Origin": "http://qndxx.youth54.cn",
        "Cookie": "JSESSIONID=277C3E9C8D096A7A5025C8395A58A25D",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; ELS-AN00 Build/HUAWEIELS-AN00; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4365 MMWEBSDK/20221012 Mobile Safari/537.36 "
                      "MMWEBID/6920 MicroMessenger/8.0.30.2260(0x28001E55) WeChat/arm64 Weixin NetType/WIFI "
                      "Language/zh_CN ABI/arm64",
        "Connection": "keep-alive",
        "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=enterIndexPage&fxopenid=&fxversion=",
        "Host": "qndxx.youth54.cn",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en-US;q=0.7,en;q=0.6",
        "Content-Length": "35",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    data = f"openid={openid}"
    response = requests.post(url, data=data, headers=headers, verify=False, timeout=5, proxies=proxies)

    done = False
    if response.status_code == 200:
        # 解析数据
        obj = re.compile(r"{\"tzzmc\":\".*?\",\"xm\":\".*?\",\"dtsj\":\".*?\",\"sjhm\":\".*?\","
                         r"\"parent_version\":(?P<parentVersion>\d+),\"version\":\"(?P<version>.*?)\","
                         r"\"versionname\":\"(?P<versionName>.*?)\",\"fulltzzmc\":\".*?\"}", re.S)
        result = obj.finditer(response.text)

        if printHistory:
            print("dxx History:")
        for it in result:
            if printHistory:
                print("-----------------------------")
                print("     parentVersion:" + it.group("parentVersion"))
                print("     version:" + it.group("version"))
                print("     versionName:" + it.group("versionName"))
                print("-----------------------------")
            if it.group("version") == current_version:
                done = True

    else:
        print("error")

    return done


def getNewestVersionInfo():
    url = "http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo"

    headers = {
        "Origin": "http://qndxx.youth54.cn",
        "Cookie": "JSESSIONID=A0B36BB8AC5782093C96170306EECFD4",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, "
                      "like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Connection": "keep-alive",
        "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=enterIndexPage&fxopenid=&fxversion=",
        "Host": "qndxx.youth54.cn",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Content-Length": "0",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5, proxies=proxies)
        # print(f"getNewestVersionInfo Status {response.status_code}")
        if response.status_code == 200:
            version = response.json()
            return version["version"]
        return ""
    except:
        return ""


def passInfo():
    url = "http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=studyLatest"
    headers = {
        "Cookie": "JSESSIONID=551858919D81B6E40C56261D4F7ABA2E",
        "Origin": "http://qndxx.youth54.cn",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        "Referer": "http://qndxx.youth54.cn/SmartLA/dxx.w?method=enterIndexPage&fxopenid=&fxversion=",
        "Connection": "close",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Site": "same-origin",
        "Host": "qndxx.youth54.cn",
        "Accept-Encoding": "gzip, deflate",
        "Dnt": "1",
        "Sec-Fetch-Mode": "cors",
        "Te": "trailers",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Length": "48",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    info = getNewestVersionInfo()
    openidsWithoutRepate = list(set(openids))
    for openid in openidsWithoutRepate:
        done = getHistory(info, openid)

        if not done:
            version = info
            # TODO:抓包，"http://qndxx.youth54.cn/SmartLA/dxxjfgl.w?method=getNewestVersionInfo"等url内都可以找到openID字段
            data = f"openid={openid}&version={version}"
            try:
                response = requests.post(url, data=data, headers=headers, verify=False, timeout=5, proxies=proxies)
                if response.status_code == 200 and response.json()["errcode"] == "0":
                    print(f"{openid}: Success ")
            except:
                print(f"{openid}:error")
                pass
        else:
            print(f"{openid} have done this term")


if __name__ == "__main__":
    passInfo()
