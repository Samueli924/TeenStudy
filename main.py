from urllib.request import urlretrieve
import PIL.Image as Image
import io
import requests
import requests.utils
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup

openid = "xxxxxxxxxxxxxxxx"  # 更改为自己的openid


def show_exit(content):
    """
    输出错误原因，辅助退出
    :param content:
    :return:
    """
    input(content)
    exit()


def get_code(s):
    """
    调用API获取最新一期青春学习的CODE
    :return:
    """
    url = "https://h5.cyol.com/special/weixin/sign.json"
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    resp = s.get(url, headers=headers).json()
    return list(resp)[-1]


def get_user(s):
    """
    调用API获取用户的信息
    :return:
    """
    headers = {
        "Host": "api.fjg360.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "*/*",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://api.fjg360.cn/index.php?m=vote&c=index&a=get_members&openid=" + openid
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        return resp.get("h5_ask_member")
    else:
        show_exit("您的OPENID配置有误，请检查后重试")


def get_course(s, code):
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = 'https://h5.cyol.com/special/daxuexi/' + code + '/m.html'
    resp = s.get(url, headers=headers)
    soup = BeautifulSoup(resp.content.decode("utf8"), "lxml")
    course = soup.title.string[7:]
    return course


def save_door(info, course, s):
    """
    调用API提交用户进入页面信息至青春湖北数据库
    :param info:
    :return:
    """
    headers = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
    url += "&username=" + info["name"]
    url += "&phone=" + "未知"
    url += "&city=" + info["danwei1"]
    url += "&danwei2=" + info["danwei3"]
    url += "&danwei=" + info["danwei2"]
    url += "&openid=" + openid
    url += "&num=10"
    url += "&lesson_name=" + course
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        return True
    else:
        show_exit("您的用户信息有误，请检查后重试")


def get_finish_pic(code):
    """
    通过调用dxx青年大学习的公众号服务来获取图片
    :param code:
    :return: None:
    """
    base_url = "https://h5.cyol.com/special/daxuexi/"
    base_url += code
    base_url += "/images/end.jpg"

    urlretrieve(base_url, "finish.jpg")


def get_user_info_pic(course, name, id, company):
    """
    获取用户信息相关截图
    :param id:
    :param name:
    :param course:
    :param company:
    :return: None:
    """
    req_url = "http://124.222.5.227:8080?course="  # 不要更改 这是我服务器上提供的图片生成页面
    req_url += str(course)
    req_url += "&name=" + str(name)
    req_url += "&id=" + str(id)
    req_url += "&company=" + str(company)

    data = {
        'url': req_url,
        'token': 'xxxxxxxxxxx',  # 需替换为自己的screenshotmaster api token
        'width': '828',  # 此大小与青年大学习提供的完成图片大小一致
        'height': '1366',
        'delay': '50',
        'device': 'mobile'
    }

    r = requests.post("https://www.screenshotmaster.com/api/v1/screenshot", data=data)
    print(r.content)

    if r.status_code == 422:
        show_exit("token无效")
    elif r.status_code != 200:
        show_exit("图片获取出错")

    img = Image.open(io.BytesIO(r.content))
    img = img.convert("RGB")
    img.save("personal_info.jpg")


def run():
    s = requests.session()
    code = get_code(s)
    user_info = get_user(s)
    course = get_course(s, code)
    save_door(user_info, course, s)

    get_finish_pic(code)
    get_user_info_pic(course, user_info["name"], user_info["uid"],
                      user_info["danwei1"] + user_info["danwei2"] + user_info["danwei3"])


if __name__ == '__main__':
    run()
