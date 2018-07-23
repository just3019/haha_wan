# -*- coding: utf-8 -*-
# python3.6

# 易码短信服务平台开放接口范例代码
# 语言版本：python版
# 官方网址：www.51ym.me
# 技术支持QQ：2114927217
# 发布时间：217-12-11
import json
from urllib import parse, request
import time
import re


def logs(s):
    f1.write('%s\n' % s)


header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

# 登陆/获取TOKEN
# username = 'ye907182374'  # 账号
# password = 'baobao1515'  # 密码
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=login&username=' + username + '&password=' + password
# TOKEN1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
# if TOKEN1.split('|')[0] == 'success':
#     TOKEN = TOKEN1.split('|')[1]
#     print('TOKEN是' + TOKEN)
# else:
#     print('获取TOKEN错误,错误代码' + TOKEN1 + '。代码释义：1001:参数token不能为空;1002:参数action不能为空;1003:参数action错误;
# 1004:token失效;1005:用户名或密码错误;1006:用户名不能为空;1007:密码不能为空;1008:账户余额不足;1009:账户被禁用;1010:参数错误;1011:
# 账户待审核;1012:登录数达到上限')

TOKEN = '00499849cbf687835af75182698438eb3c2ccdf4'  # 输入TOKEN
# 获取账户信息
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getaccountinfo&token=' + TOKEN + '&format=1'
# ACCOUNT1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
# if ACCOUNT1.split('|')[0] == 'success':
#     ACCOUNT = ACCOUNT1.split('|')[1]
#     print(ACCOUNT)
# else:
#     print('获取TOKEN错误,错误代码' + ACCOUNT1)

# 获取手机号码
# ITEMID = '7982'  # 项目编号
# EXCLUDENO = ''  # 排除号段170_171
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getmobile&token=' + TOKEN + '&itemid=' + ITEMID + '&excludeno=' + EXCLUDENO
# MOBILE1 = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
# if MOBILE1.split('|')[0] == 'success':
#     MOBILE = MOBILE1.split('|')[1]
#     print('获取号码是:\n' + MOBILE)
# else:
#     print('获取TOKEN错误,错误代码' + MOBILE1)
#
# # 获取短信，注意线程挂起5秒钟，每次取短信最少间隔5秒
# TOKEN = TOKEN  # TOKEN
# ITEMID = ITEMID  # 项目id
# MOBILE = MOBILE  # 手机号码
# WAIT = 61  # 接受短信时长60s
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=getsms&token=' + \
#       TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE + '&release=1'
# text1 = request.urlopen(request.Request(
#     url=url, headers=header_dict)).read().decode(encoding='utf-8')
# print('text1======>', text1)
# TIME1 = time.time()
# TIME2 = time.time()
# ROUND = 1
# while (TIME2 - TIME1) < WAIT and not text1.split('|')[0] == "success":
#     time.sleep(5)
#     text1 = request.urlopen(request.Request(
#         url=url, headers=header_dict)).read().decode(encoding='utf-8')
#     TIME2 = time.time()
#     ROUND = ROUND + 1
#
# ROUND = str(ROUND)
# if text1.split('|')[0] == "success":
#     text = text1.split('|')[1]
#     TIME = str(round(TIME2 - TIME1, 1))
#     print('短信内容是' + text + '\n耗费时长' + TIME + 's,循环数是' + ROUND)
# else:
#     print('获取短信超时，错误代码是' + text1 + ',循环数是' + ROUND)
#
# # 释放号码
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=release&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
# RELEASE = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
# if RELEASE == 'success':
#     print('号码成功释放')
#
# # 拉黑号码
# url = 'http://api.fxhyd.cn/UserInterface.aspx?action=addignore&token=' + TOKEN + '&itemid=' + ITEMID + '&mobile=' + MOBILE
# BLACK = request.urlopen(request.Request(url=url, headers=header_dict)).read().decode(encoding='utf-8')
# if BLACK == 'success':
#     print('号码拉黑成功')

str = '【飞凡】短信验证码 498820 ，欢迎注册飞凡会员。如需帮助，请关注微信号“飞凡逛街”联系在线客服。'
print(str[str.find('，') - 8: str.find('，')])
# 提取短信内容中的数字验证码
pat = "[0-9]+"
IC = 0
IC = re.search(pat, str)
if IC:
    print("验证码是:\n" + IC.group())
else:
    print("请重新设置表达式")

a = '{"status":"0000","message":"成功","data":[{"memberCode":"228167255530831872","name":"","mobileNo":"14726502729","rating":"普通","ratingId":"1","points":0,"regDate":1532328913000,"regTime":1532328913000,"fromOrg":"东营万达广场","expandingType":"引流","expandingChannel":"新媒体小程序","expandingTypeCode":"drainage","expandingChannelCode":"20","salesUserName":null,"memberStatus":"NORMAL","sex":"","certificateType":"","certificateCode":"","consumeAmountSum":null,"createUserName":null,"refereeUserName":null,"descRuleVO":null,"plazaId":"1000985","plazaName":null,"storeId":null,"lastConsumeTime":1532328922000,"firstLoginTime":"2018-07-23 14:55:13","couponType":null,"couponBusiness":null,"useTime":null,"tinyOrgId":"1000985","tinyOrgName":"东营万达广场"}],"_metadata":{"totalCount":1,"pageIndex":0,"pageSize":0}}'
b = json.loads(a)
print(b['_metadata']['totalCount'])


# if __name__ == '__main__':
#     # global f1
#     # f1 = open('%s.txt' % time.strftime("%Y%m%d%H%M"), 'a')
#     # logs('sfa')
#     a = '{"status":200,"message":"\u6210\u529f","data":{"orderId":"51898425408154","memberId":"15000000369748154","status":"PAY_SUCCESS","createTime":1532323775,"createTimeYmd":"2018\u5e7407\u670823\u65e5","createTimeHi":"13:29","payTime":0,"orderAmt":"0.00","realPay":"0","orderCode":7010,"tradeCode":7010,"orderCodeName":"\u4f18\u60e0\u5238","usePoint":"0","usePointDiscount":"0","paySequenceNo":null,"orderSrc":2030,"payOrderNo":null,"usePointFlag":0,"useCouponFlag":0,"refund":"","reBuy":1,"currentStatus":"\u4ed8\u6b3e\u6210\u529f","product":[{"orderNo":"51898425408154","productId":"20180514141349","productCount":1,"productPrice":"0","productCode":"7010","merchantId":"10045938","productInfo":{"parentId":"20180514141349","saleStartTime":1526278492,"title":"\u5c0f\u7a0b\u5e8f\u4e13\u5c5e\u4e34\u65f6\u505c\u8f66\u724c","price":"0.00","pic":"T1CuhgB7Jg1RCvBVdK","saleEndTime":1532948281},"title":"\u5c0f\u7a0b\u5e8f\u4e13\u5c5e\u4e34\u65f6\u505c\u8f66\u724c","picture":"T1CuhgB7Jg1RCvBVdK","applyRefundFlag":0,"refundFinishedFlag":0,"realPayAmt":"0","couponNo":null}],"track":[{"logTime":1532323776146,"logInfo":"\u5546\u54c1\u5df2\u53d1\u9001","operator":"\u7cfb\u7edf"},{"logTime":1532323776004,"logInfo":"\u8ba2\u5355\u5df2\u4ed8\u6b3e","operator":"\u7cfb\u7edf"},{"logTime":1532323775887,"logInfo":"\u8ba2\u5355\u5df2\u63d0\u4ea4","operator":"\u5ba2\u6237"}],"store":[],"buyType":1,"couponList":[],"priceDetail":{"orderAmt":"0.00","usePoint":"0","memberPromotion":0,"combinationpromotion":0,"userYouHui":0,"userDuiHuan":0,"realpayAmt":"0"},"dispatching":"","promotionList":[],"operateCode":[],"payType":""}}';
#     result = json.loads(a)
#     if result['data']['product'][0]['couponNo'] is None:
#         print(1)
