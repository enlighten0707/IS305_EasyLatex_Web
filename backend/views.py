from django.http import HttpResponse
import cv2
from .utils import process
from .utils import models
import numpy as np
import torch
from PIL import Image
from io import BytesIO
import requests
import datetime
import hashlib
import base64
import hmac
import json
import os
import glob

def sketchProcess(request):
    '''
    Get the uploaded image and convert it to sketch, then return the sketch.
    :param request: include the uploaded image
    :return: the sketch generated according to the original image
    '''
    if request.method == 'POST':
        # Read the image and save it to lacal
        file_list = request.FILES.getlist('file')
        file = file_list[0]
        # path = "./backend/utils/imgDir/"
        # img_name = "origin.png"
        # img_dir = path + img_name
        img_dir = "./backend/origin.jpg"
        data = file.file.read()
        # print(data)

        with open(img_dir, 'wb') as f:
            f.write(data)

    return HttpResponse(data, content_type='image/png')


class get_result(object):
    def __init__(self, AudioPath, host="rest-api.xfyun.cn"):
        # 应用ID（到控制台获取）
        self.APPID = "1258fd12"
        # 接口APISercet（到控制台公式识别服务页面获取）
        self.Secret = "MThhNWVhOTRkMzIwNzdkZjhhODk1YzZl"
        # 接口APIKey（到控制台公式识别服务页面获取）
        self.APIKey = "38422a5711755a49a27432a3b3c9ab5d"

        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/itr"
        # 设置url
        # print(host)
        self.url = "https://" + host + self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置测试图片文件
        # self.AudioPath = "./Examples/12.png"
        self.AudioPath = AudioPath

        self.BusinessArgs = {
            "ent": "teach-photo-print",
            "aue": "raw",
        }

    def imgRead(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        # print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        # print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        audioData = self.imgRead((self.AudioPath))
        content = base64.b64encode(audioData).decode(encoding='utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "image": content,
            }
        }
        body = json.dumps(postdata)
        # print(body)
        return body

    def get_content(self, respData):
        # print(respData)
        str = ""
        try:
            for i in range(len(respData['data']['region'])):
                str += respData['data']['region'][i]['recog']['content'] + "\n"
        except:
            return "Error!"

        s1 = 'ifly-latex-begin'
        flag = 1
        while flag == 1:  # 若无子字符串在内则跳出循环
            flag = 0
            if s1 in str:
                str = str.replace(s1, '')
                flag = 1

        s1 = 'ifly-latex-end'
        flag = 1
        while flag == 1:  # 若无子字符串在内则跳出循环
            flag = 0
            if s1 in str:
                str = str.replace(s1, '')
                flag = 1

        s1 = ' '
        flag = 1
        while flag == 1:  # 若无子字符串在内则跳出循环
            flag = 0
            if s1 in str:
                str = str.replace(s1, '')
                flag = 1

        return str

    def call_url(self):
        body = self.get_body()
        headers = self.init_header(body)
        # print(self.url)
        response = requests.post(self.url, data=body, headers=headers, timeout=8)
        status_code = response.status_code

        str = "Error!"
        if status_code != 200:
            # 鉴权失败
            print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
            print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/words/formula-discern/API.html")
        else:
            # 鉴权成功
            respData = json.loads(response.text)
            str = self.get_content(respData)

        return str


# 水平方向投影
def hProject(binary):
    h, w = binary.shape

    # 水平投影
    hprojection = np.zeros(binary.shape, dtype=np.uint8)

    # 创建h长度都为0的数组
    h_h = [0] * h
    for j in range(h):
        for i in range(w):
            if binary[j, i] == 0:
                h_h[j] += 1
    # 画出投影图
    for j in range(h):
        for i in range(h_h[j]):
            hprojection[j, i] = 255

    # cv2.imshow('hpro', hprojection)

    return h_h


def crop_and_store(img_dir):
    img = cv2.imread(img_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 针对不同图需要调整阈值
    ret, th = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

    h, w = th.shape
    h_h = hProject(th)

    start = 0
    h_start, h_end = [], []

    # 根据水平投影获取垂直分割
    zero_cnt = 0
    for i in range(len(h_h)):
        if h_h[i] > 0 and start == 0:
            h_start.append(max(0, i - 5))
            start = 1
            zero_cnt = 0
        if h_h[i] == 0:
            zero_cnt += 1
        if zero_cnt > 10 and start == 1:
            h_end.append(i)
            start = 0

    cropped_dir = "./backend/cropped/"
    if os.path.exists(cropped_dir):
        for path in glob.glob("./backend/cropped/*"):
            os.remove(path)
    else:
        os.makedirs(cropped_dir)
    for i in range(len(h_start)):
        crop = img[h_start[i]: h_end[i]]
        # cv2.imshow('crop_%d' % i, crop)
        cv2.imwrite(os.path.join(cropped_dir, 'crop_%d.jpg' % i), crop)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def XunFeiAPI(request):
    img_dir = "./backend/origin.jpg"

    crop_and_store(img_dir)

    str_all = "\\begin{align} "
    for paths in glob.glob("./backend/cropped/*"):
        # 初始化类
        gClass = get_result(paths)
        str = gClass.call_url()
        str_all += str
        str_all += "\\\\"

    str_all += " \\end{align}"
    return HttpResponse(str_all, content_type='text/plain')

# def expr(request):
#     if request.method == 'POST':
#         # Read the hint and save it to lacal
#         str_expr = request.POST.get('str_expr')
#         print(str_expr)
#         expr = sympify(str_expr)
#
#     return HttpResponse({'str_expr': expr})
