from django.shortcuts import render
from django.http import HttpResponse
import cv2
from .utils import process
from .utils import models
import numpy as np
import torch
from PIL import Image
from io import BytesIO
import base64
from sympy import *
import requests
import datetime
import hashlib
import base64
import hmac
import json


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
        path = "./backend/utils/imgDir/"
        img_name = "origin.png"
        img_dir = path + img_name
        data = file.file.read()
        # print(data)

        with open(img_dir, 'wb') as f:
            f.write(data)
        #
        # # Initialize config
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # with torch.no_grad():
        #     netC2S = models.Color2Sketch(input_nc=3,
        #                                  output_nc=1,
        #                                  norm='IN',
        #                                  SN=True,
        #                                  activation='relu',
        #                                  residual=False,
        #                                  ckpt_path='./backend/utils/checkpoint/color2sketch.pth').to(device)
        #     netS2C = models.Colorizenet(input_nc=4,
        #                                 output_nc=3,
        #                                 norm='IN',
        #                                 SN=True,
        #                                 activation='relu',
        #                                 residual=True,
        #                                 ckpt_path='./backend/utils/checkpoint/sketch2color.pth').to(device)
        #
        #     netC2S.eval()
        #     netS2C.eval()
        #
        # # Iamge process
        # img = cv2.imread(img_dir, cv2.IMREAD_COLOR)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.resize(img, dsize=(512, 512), interpolation=cv2.INTER_AREA)
        # with torch.no_grad():
        #     img_ = process.ForwardNet(img, netC2S, device)
        # img_ = img_ * 255
        # img_ = img_.astype(np.uint8)
        # img_ = np.broadcast_to(img_, img.shape)
        #
        # # Save sketch
        # img_name_ = "sketch.png"
        # img_dir_ = path + img_name_
        # img_ = Image.fromarray(img_)
        # img_.save(img_dir_)
        #
        # # Generate stream
        # stream = BytesIO()
        # img_.save(stream, "png")
        # data = stream.getvalue()
        data = base64.b64encode(data).decode()

    return HttpResponse(data, content_type='image/png')


def colorization(request):
    '''
    Get the sketch and convert it to colored image, then return.
    :param request: include the sketch
    :return: the image generated according to the original sketch
    '''
    if request.method == 'POST':
        # Read the hint and save it to lacal
        file = request.POST.get('hint')
        data = file.split(",")[-1]
        data = base64.b64decode(data)
        path = "./backend/utils/imgDir/"
        img_name = "hint.png"
        img_dir = path + img_name
        with open(img_dir, 'wb') as f:
            f.write(data)

        # Initialize config
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        with torch.no_grad():
            netS2C = models.Colorizenet(input_nc=4,
                                        output_nc=3,
                                        norm='IN',
                                        SN=True,
                                        activation='relu',
                                        residual=True,
                                        ckpt_path='./backend/utils/checkpoint/sketch2color.pth').to(device)
            netS2C.eval()

        # Iamge process
        hint = cv2.imread(path + 'hint.png', cv2.IMREAD_COLOR)
        hint = cv2.cvtColor(hint, cv2.COLOR_BGR2RGB)
        sketch = cv2.imread(path + 'sketch.png', cv2.IMREAD_GRAYSCALE).reshape(512, 512, 1)
        input_array = np.concatenate([sketch, hint], axis=2)
        with torch.no_grad():
            result = process.ForwardNet(input_array, netS2C, device)
        result = result * 255
        result = result.astype(np.uint8)

        # Save result
        result_dir = path + "result.png"
        result = Image.fromarray(result)
        result.save(result_dir)

        # Generate stream
        stream = BytesIO()
        result.save(stream, "png")
        data = stream.getvalue()
        data = base64.b64encode(data).decode()

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
        str = ""
        for i in range(len(respData['data']['region'])):
            str += respData['data']['region'][i]['recog']['content']+"\n"

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

        if status_code != 200:
            # 鉴权失败
            print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
            print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/words/formula-discern/API.html")
        else:
            # 鉴权成功
            respData = json.loads(response.text)
            str = self.get_content(respData)

        return str


def XunFeiAPI(request):
    path = "./backend/utils/imgDir/"
    img_name = "origin.png"
    img_dir = path + img_name

    # 初始化类
    gClass = get_result(img_dir)
    str = gClass.call_url()
    return HttpResponse(str, content_type='text/plain')

# def expr(request):
#     if request.method == 'POST':
#         # Read the hint and save it to lacal
#         str_expr = request.POST.get('str_expr')
#         print(str_expr)
#         expr = sympify(str_expr)
#
#     return HttpResponse({'str_expr': expr})
