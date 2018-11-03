import requests
from selenium import webdriver
import time
import os
import json
from store import PretreatMgr

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'}


def login(username, password):
    browser = webdriver.PhantomJS('phantomjs')
    # browser=webdriver.Firefox()
    browser.get(
        'https://passport.weibo.cn/signin/login?entry=mweibo&amp;res=wel&amp;wm=3349&amp;r=http%3A%2F%2Fm.weibo.cn%2F')
    browser.set_page_load_timeout(10)
    time.sleep(5)
    browser.find_element_by_id('loginName').send_keys(username)
    browser.find_element_by_id('loginPassword').send_keys(password)
    browser.find_element_by_id('loginAction').click()
    time.sleep(5)
    cookies = browser.get_cookies()
    result = {}
    for item in cookies:
        try:
            result[item['name']] = item['value']
        except:
            continue
    f = open('cookies', 'w')
    f.write(str(result))
    f.close()
    return result


def weibo():
    if os.path.isfile('cookies'):
        cookies = eval(open('cookies', 'r').read())
    else:
        cookies = login('626591833@qq.com', '1913805949')
    session = requests.session()
    session.cookies = requests.utils.cookiejar_from_dict(cookies)
    html = session.get('http://m.weibo.cn', headers=headers).text
    html = session.get('http://m.weibo.cn/index/feed?format=cards&page=1', headers=headers).text
    data = json.loads(html)[0]['card_group']
    result = []
    for item in data:
        user = item['mblog']['user']['screen_name']
        text = item['mblog']['text']
        result.append({'user': user, 'text': text})
    get_comments(session, '4302336342422693')


def get_comments(session, weiboid):
    page = 1
    datas = []
    while True:
        html = session.get(
            'http://m.weibo.cn/single/rcList?format=cards&id={weiboid}&type=comment&hot=0&page={page}'.format(
                weiboid=weiboid, page=page), headers=headers).text
        js = json.loads(html)[-1]
        if 'card_group' in js:
            data = js['card_group']
            datas.append(data)
            PretreatMgr.save(weiboid=weiboid, datas=datas)
            print(data)
            time.sleep(5)
            page += 1
        else:
            break
    return datas


if __name__ == '__main__':
    weibo()
