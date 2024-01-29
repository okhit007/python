# coding:utf8
import requests, json, time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import urllib.parse
import hmac
import hashlib
import base64

# 第三方 SMTP 服务
mail_host="smtp.qq.com"  #设置服务器
mail_user=""    #用户名
mail_pass=""   #口令 
sender = ''
receivers = ['11@qq.com', '22@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# 多少秒刷新一次接口
s = 120

url = "https://XXXXX.XXXXX.com.cn/api/bus/ticketlist"

payload_yingdong = json.dumps({
	"depCode": "84",
	"hospitalCode": "2220",
	"docCode": "3799"
})

payload_yunfeng = json.dumps({
	"depCode":"84",
	"hospitalCode":"2220",
	"docCode":"2251"
})

files = [
]
headers = {
  'Content-Type': 'application/json'
}

payload={'month': '2024-01',
'busid': '13',
'lineid': '13'}

headers = {
'Cookie':''
}

def dingding_send(msg):
	timestamp = str(round(time.time() * 1000))
	secret = ''
	secret_enc = secret.encode('utf-8')
	string_to_sign = '{}\n{}'.format(timestamp, secret)
	string_to_sign_enc = string_to_sign.encode('utf-8')
	hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
	sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

	url = 'https://oapi.dingtalk.com/robot/send?access_token=XXXXX&timestamp={}&sign={}'.format(timestamp, sign)
	HEADERS = {
	"Content-Type": "application/json ;charset=utf-8 "
	}
	String_textMsg = {\
	"msgtype": "text",\
	"text": {"content": msg}}
	String_textMsg = json.dumps(String_textMsg)
	res = requests.post(url, data=String_textMsg, headers=HEADERS)
	print(res.text)

while True:
	time.sleep(s)
	response_yingdong = requests.request("POST", url, headers=headers, data = payload, files = files)
	# response_yunfeng = requests.request("POST", url, headers=headers, data = payload_yunfeng, files = files)
	response = response_yingdong.json()
	# time.sleep(2)
	# response1 = response_yunfeng.json()
	# print ("123", response)

	for i in response['rows']:
		if i['date'] == '2024-01-22' and i['state'] != 5:
			msg = '%s:有票了！！当前时间：%s'  %(i['date'], time.ctime())
			print("状态", msg)
			dingding_send(msg)
		else:
			print('运行中，无票!' + time.ctime())

def send_email(msg):
	message = MIMEText('' + str(msg) , 'plain', 'utf-8')
	message['From'] = Header('sender', 'utf-8')
	message['To'] =  Header('receivers', 'utf-8')
	subject = '放号了，冲啊！！！'
	message['Subject'] = Header(subject, 'utf-8')
	try:
		smtpObj = smtplib.SMTP() 
		smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
		smtpObj.login(mail_user,mail_pass)  
		# smtpObj.sendmail(sender, receivers, message.as_string())
		print ("邮件发送成功")
	except smtplib.SMTPException:
		print ("Error: 无法发送邮件")



