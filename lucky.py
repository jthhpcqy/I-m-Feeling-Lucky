import webbrowser
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QWidget,QApplication,QToolTip,QPushButton,QLineEdit,QTextEdit
from PyQt5.QtGui import QIcon,QFont       #设置窗口图标和字体
from PyQt5.QtCore import QCoreApplication   #使用这里面的功能
from PyQt5 import QtCore
import sys
import re

url_baidu = 'https://www.baidu.com/s?word='
host_baidu = 'www.baidu.com'
url_bing = 'http://cn.bing.com/search?q='
host_bing = 'cn.bing.com'


class Visit(object):
    def __init__(self,Url,Key_Word,Host):
        self.url = Url
        self.key_word = Key_Word
        self.host = Host
        self.msg = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87\
             UBrowser/6.2.3964.2 Safari/537.36',
            'Host' : self.host
        }
    def visit(self):
        res = requests.get(self.url + self.key_word, headers=self.headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        first = soup.find(name='div', id='1')
        second = first.find(name='a', target='_blank')
        third = second.get('href')
        return third

class Bing(Visit):
    def bing(self):
        res = requests.get(self.url+self.key_word,headers = self.headers)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text,'html.parser')
        first = soup.find(name = 'ol',id = 'b_results')
        second = first.find(name = 'a')
        print(second.get('href'))
#=============================
class Translate(object):
    def __init__(self):
        self.url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87\
             UBrowser/6.2.3964.2 Safari/537.36',
            'Host' : 'fanyi.youdao.com',
            'X-Requested-With': 'XMLHttpRequest',
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    def isword(self,words):
        alphabet = 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        is_word = True
        for i in words:
            if i in alphabet:
                pass
            else:
                is_word = False
        return is_word

    def translate(self,keyword):
        self.data = {
            'i':keyword,
            'from':'AUTO',
            'to': 'AUTO',
            'doctype':'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'true',
        }

        res = requests.post(url = self.url, data= self.data, headers = self.headers)
        res.encoding = res.apparent_encoding
        window.text_question.setToolTip(re.findall('"tgt":"(.*)"',res.text)[0])


class Window(QWidget):
    QToolTip.setFont(QFont('Microsoft YaHei', 30))
    def __init__(self):
        super().__init__()
        self.initUI()
        self.addClipbordListener()

    def initUI(self):
        self.text_question = QLineEdit(self)
        self.text_question.setClearButtonEnabled(True)
        #self.text_question.setFrame(False)     #无边框
        self.setWindowOpacity(65/100)           #窗口透明度
        self.text_question.setFont(QFont('Microsoft YaHei', self.text_question.height()));
        self.text_question.setGeometry(5,15,self.width()-55,60)
        self.setFixedSize(600, 90)      #固定窗口大小
        self.text_question.returnPressed.connect(self.search)
        self.setWindowTitle('手气不错')
        desktop = QApplication.desktop()
        self.setGeometry(desktop.width()-self.width(), 400, 600, 90)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def search(self):
        baidu = Visit(url_baidu, Key_Word='', Host=host_baidu)
        baidu.key_word = self.text_question.text()
        if baidu.key_word == "exit": exit()
        try:
            webbrowser.open(url = baidu.visit())
            self.text_question.setText('')
        except:
            pass

    def changeText(self):
        self.text_question.setText(self.clipboard.text())
        if translate.isword(self.clipboard.text()):
            translate.translate(self.clipboard.text())

    def addClipbordListener(self):
        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.changeText)

    def leaveEvent(self, QEvent):
        self.setWindowOpacity(65/100)
    def enterEvent(self, QEvent):
        self.setWindowOpacity(95/100)


bing = Bing(url_bing,Key_Word='',Host=host_bing)

app = QApplication(sys.argv)
app.setWindowIcon(QIcon('luckly_icon.png'))
translate = Translate()
window = Window()
sys.exit(app.exec())
