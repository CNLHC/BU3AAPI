# coding:u8
import requests
from bs4 import BeautifulSoup


def Verification(Username='', Password=''):
    '''通过e.buaa.edu.cn 检测统一认证账号是否合法。
    @Input:
        Username:统一认证账号
        Password:统一认证密码
    @Output:
        True:合法
        False:不合法'''
    def get_token(page):
        soup = BeautifulSoup(page, 'lxml')
        token = soup.find(
            'input', attrs={'name': 'authenticity_token'}).get("value")
        return token
    response = requests.get('https://e.buaa.edu.cn')
    cookies = response.cookies
    page = response.text
    paylode = {
        'utf8': '✓',
        'authenticity_token': get_token(page),
        'user[login]': Username,
        'user[password]': Password,
        'commit': '登录 / Login',
    }
    return True if len(requests.post('https://e.buaa.edu.cn/users/sign_in', data=paylode, cookies=cookies).history) > 0 else False


print (Verification(Username='@TODO', Password='@TODO'))
