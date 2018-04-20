# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests, time

from qqbot.basicqsession import BasicQSession, qHash, bknHash
from qqbot.utf8logger import ERROR, INFO

qq, password, nick, driverType = '???', '???', '???', '???'

class NewBasicQSession(BasicQSession):

    def Login(self, conf):
        try:
            INFO('正在使用“用户名-密码”登录，请耐心等待 1 ~ 3 分钟......')
            try:
                self.newLogin(conf)
            except:
                self.newLogin(conf)
        except Exception as e:
            ERROR('用户名-密码登录失败，原因：%s', e, exc_info=True)
            INFO('开始使用“手工扫码”登录......')
            BasicQSession.Login(self, conf)
    
    def newLogin(self, conf):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        
        wait = WebDriverWait(driver, 30)
        driver.get('http://m.qzone.com')
        wait.until(EC.presence_of_element_located((By.ID, "go")))
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(qq)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(password)
        driver.find_element_by_id('go').click()
        wait.until(EC.element_to_be_clickable((By.ID, 'header')))
        driver.get('http://web2.qq.com')
        try:
            driver.switch_to_frame('ptlogin')
            time.sleep(2)
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'face'))).click()
        except:
            pass

        driver.get('http://web2.qq.com')

        self.session = requests.session()
        for item in driver.get_cookies():
            self.session.cookies.set(item['name'], item['value'])

        driver.get('http://web2.qq.com')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))
        driver.get('http://web2.qq.com')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))
        driver.get('http://web2.qq.com')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'container')))
        time.sleep(2)

        self.ptwebqq = driver.execute_script('return mq.ptwebqq')
        self.vfwebqq = driver.execute_script('return mq.vfwebqq')
        self.psessionid = driver.execute_script('return mq.psessionid')

        driver.close()
        time.sleep(2)
        
        self.uin = int(qq)
        self.qq = qq
        self.hash = qHash(self.uin, self.ptwebqq)
        self.bkn = bknHash(self.session.cookies['skey'])        
        self.clientid = 53999199
        self.msgId = 6000000
        self.lastSendTime = 0
        self.nick = nick
        
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64; rv:38.0) '
                           'Gecko/20100101 Firefox/38.0 Iceweasel/38.7.1')
        })
        
        try:
            self.TestLogin()
        except:
            self.TestLogin()

        t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        self.dbbasename = '%s-%s-contact.db' % (t, self.qq)
        self.dbname = conf.absPath(self.dbbasename)
        conf.SetQQ(self.qq)

def onInit(bot):
    global qq, password, nick, driverType

    d = bot.conf.pluginsConf.get(__name__, {})
    qq = d.get("qq", qq)
    password = d.get("password", password)
    nick = d.get("nick", nick)
    driverType = d.get("driverType", driverType)

    import qqbot.qsession
    from qqbot.groupmanager import GroupManagerSession
    class QSession(NewBasicQSession, GroupManagerSession):
        pass
    qqbot.qsession.QSession = QSession