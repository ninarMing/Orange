# 每个月运行一次生成一个文件夹
# 文件夹命名为： 年+月份+每日一译
# 文章命名：月份+日期+每日一译
# 文章篇数跟月份天数变化而变化
# 每次文件生成后需要添加每日一译图片素材
# 网址：https://language.chinadaily.com.cn/trans_collect/page_3.html
# 1页网址15篇文章
# 先获取该页的15篇文章
# 待做 to do
import requests
from bs4 import BeautifulSoup
import datetime
import os
''' 
 page_text_2 = getHtmlText(url_2)
 page_content_2 = "\n"*6 + findHtmlContentFromChinaDaily(page_text_2, 1)
 generateDocumentWithText(page_content_2)'''
# 获取网页内容
def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "error"


# 获取每日一译
def getTranslate(text):
    soup = BeautifulSoup(text, 'html.parser')
    article = "译："+soup.h1.span.string[5:]+"\n"
    generator_page = soup.find('figure').next_siblings
    flag = 0
    for i in generator_page:
        un_text = str(i)
        text = un_text.replace('\n', '')
        if len(text) <= 0:
            continue
        if text.find('Editor') != -1:
            break
        if text.find('例句') != -1:
            flag = 1
            article = article+str(i.getText())+"\n"
            # print(article)
            continue
        if flag == 1:
            # print("list_text="+text)
            list_text = (text[3:-4]).split('<br/>')
            count = 0
            for k in list_text:
                if len(k) > 0:
                    count = count+1
                    if count % 2 == 0:
                        article = article + k + "==="
                    else:
                        article = article + k + "+++"
        else:
            article = article + i.getText()+'\n'
    print(repr(article))
    return article+'\n\n\n'



def getPageUrl(content):
    soup = BeautifulSoup(content, 'html.parser')
    div_all = soup.find_all('a', attrs={'class', 'gy_box_img'})
    list_href = []
    for div in div_all:
        list_href.append('https:'+div.get('href'))
    return list_href


def getMonthTranslate(list_translate_url):
    j = 0
    dir_path = 'E:\\Now_Works\\reading_two\\每日一译\\'
    i = datetime.datetime.now()
    date_name = str(i.month)
    text_path = dir_path + date_name + '月每日一译'
    for translate in list_translate_url:
        page_text = getHtmlText(translate)
        translate_content = getTranslate(page_text)
        j = j+1
        with open(text_path + '.txt', mode='a+', encoding='utf8') as article_file:
            article_file.write(translate_content)


if __name__ == '__main__':
    url = "https://language.chinadaily.com.cn/trans_collect/page_3.html"
    text = getHtmlText(url)
    list_url = getPageUrl(text)
    getMonthTranslate(list_url)
    print('end')
