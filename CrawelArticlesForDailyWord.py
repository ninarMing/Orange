import re

import requests
from bs4 import BeautifulSoup
import datetime
import os


# 获取网页内容
def get_html_text(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return "error"


# 获取标题
def get_title_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.h1.span.string
    index = title.find(' ')
    title = title[3:] + "\n" + title[index+1:] + "+++" + title[5:index]+"==="
    title = title.replace('∣', '：')
    return title


# 获取图片前的文章
def get_previous_data(content):
    soup = BeautifulSoup(content, 'html.parser')
    # <p></p><figure>前的p里的内容
    previous_text = soup.find('figure').previous_siblings
    article = ''
    count = 0
    for sibling in previous_text:
        text_previous = sibling.getText().replace('\n', '')
        if len(text_previous) > 0:
            # print(text_previous)
            article = article + text_previous
            count = count+1
            if count % 2 == 0:
                article = article + "==="
            else:
                article = article + "+++"
        # print(repr(sibling))
    # print(article)
    return article


# 获取主体内容
def get_important_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    next_text = soup.find('figure').next_siblings
    article = ''
    tag = 0
    list_instruction = []
    list_word = []
    for sibling in next_text:
        text_next = sibling.getText().replace('\n', '').replace('\xa0', '')
        if len(text_next) > 0:
            if text_next.find('【知识点】') != -1:
                article = article + "【知识点】"+"\n"
                tag = 1
                continue
            elif text_next.find('【重要') != -1:
                article = article +text_next + "\n"
                tag = 2
                continue
            elif text_next.find('【相关词汇】') != -1:
                article = article + "【相关词汇】" + "\n"
                tag = 3
                continue
            if tag == 1:
                article = article + text_next + '\n'
            elif tag == 2:
                list_instruction.append(text_next)
                len_instruction = len(list_instruction)
                if len_instruction == 3:
                    # 需要分段
                    article = article + divideSegment(list_instruction) + '\n' + list_instruction[2] + '==='
                    list_instruction.clear()
            elif tag == 3:
                list_word.append(text_next)
                len_word = len(list_word)
                if len_word == 2:
                    article = article + list_word[1] + '+++' + list_word[0] + '==='
                    list_word.clear()
    # print(article)
    return article


# 段落里进行分句
def divideSegment(list_article):
    list_eng = list_article[1].split('.')
    list_ch = list_article[0].split('。')
    len_eng = len(list_eng)
    len_ch = len(list_ch)
    segment = ''
    if len_eng != len_ch or len_eng <= 2 or len_ch <= 2:
        segment = str(list_article[1]) + "+++" + str(list_article[0])
    else:
        for i in range(len_eng-1):
            segment = segment + list_eng[i] + ".+++" + list_ch[i]
            if i < (len_eng-2):
                segment = segment + "。+++"
            else:
                segment = segment + "。"
    return segment


# 写入文件
def generate_document_with_text(content):
    # 获取今日日期+title作为文件名
    # 写入text文件
    doc_path = 'E:\\Now_Works\\reading_two\\'
    i = datetime.datetime.now()
    date_name = str(i.month)+'.'+str(i.day)
    dir_path = doc_path + date_name+'新闻'
    text_path = dir_path + '\\'+date_name+'每日一词'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(text_path+'.txt', mode='a+', encoding='utf8') as article_file:
        article_file.write(content)

'''
def get_page_url(content):
    soup = BeautifulSoup(content, 'html.parser')
    div_all = soup.find_all('a', attrs={'class', 'gy_box_img'})
    list_href = []
    for div in div_all:
        list_href.append('https:'+div.get('href'))
    return list_href
'''


if __name__ == '__main__':
    # url = "https://language.chinadaily.com.cn/trans_collect/"
    # text = getHtmlText(url)
    # list_url = getPageUrl(text)
    list_url =["https://language.chinadaily.com.cn/a/202211/04/WS6364d5bca3105ca1f22741dc.html", "https://language.chinadaily.com.cn/a/202211/03/WS63638569a310fd2b29e80256.html", "https://language.chinadaily.com.cn/a/202211/02/WS636233e8a310fd2b29e7fec5.html", "https://language.chinadaily.com.cn/a/202211/01/WS6360e13ca310fd2b29e7fb42.html", "https://language.chinadaily.com.cn/a/202210/31/WS635fbfe7a310fd2b29e7f829.html"]
    content = ''
    for url_page in list_url:
        text = get_html_text(url_page)
        # content = content + get_title_data(text)
        content = content + get_title_data(text) + get_previous_data(text) + get_important_content(text) +'\n\n\n'
        print(content)
    # print(repr(content))
    generate_document_with_text(content)
    print('end')


