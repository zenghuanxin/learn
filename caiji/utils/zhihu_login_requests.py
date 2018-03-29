import requests
try:
    import http.cookiejar as cookielib
except:
    print('无法加载该模块')

import re
session = requests.session()

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
}

def get_xsrf():
    #获取xsrf code
    response = session.get('https://www.zhihu.com/explore',headers=header)
    xsrf = re.search('<input type="hidden" name="_xsrf" value="(.*?)"/>',response.text)
    if xsrf:
        return xsrf.group(1)
    else:
        return ""

def zhihu_login(account,passwd):
    #知乎登录
    if re.match("^1\d{10}",account):
        print('手机号码登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            # '_xsrf':get_xsrf(),
            'phone_num': account,
            'password': passwd,
            'remember_me': True
        }
    response = session.post(post_url,data=post_data,headers=header)
    print(response.text)

zhihu_login('18659328891','zhx18659328891..')
