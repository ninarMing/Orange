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


# 提取文件内容从中国日报
# tag = 1 :格式：<p>中或英文</p> devide =0 不需要分段，1需要分段
# tag = 2 :格式：<p><br/>英文<br/>中文<br/><p>
# tag =3 :从1后进行分段
def find_html_content_from_china_daily(text, tag=1):
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.h1.span.string
    print(title)
    page = soup.select('div #Content p')
    count = len(page)
    j = 0
    article = title+"\n"
    list_sentence = list()
    for i in range(1, count):
        str_text = page[i].getText()
        str_len = len(str_text)
        if str_len <= 1:
            continue
        if str_text.find('来源') != -1:
            break
        if tag == 1:
            j = j + 1
            if j % 2 == 0:
                article = article + str_text + "==="
            else:
                article = article + str_text + "+++"
        elif tag == 2:
            list_text = str(page[i])[8:-4].split('<br/>')
            article = article + divideSegment(list_text)
        elif tag == 3:
            list_sentence.append(str_text)
            if len(list_sentence) == 2:
                article = article + divideSegment(list_sentence)
                list_sentence = list()

    print(article)
    return article


# 句子里进行分段
def divideSegment(list_article):
    list_eng = list_article[0].split('.')
    list_ch = list_article[1].split('。')
    len_eng = len(list_eng)
    len_ch = len(list_ch)
    segment = ''
    if len_eng != len_ch or len_eng <= 2 or len_ch <= 2:
        segment = str(list_article[0]) + "+++" + str(list_article[1]) + "==="
    else:
        for i in range(len_eng-1):
            segment = segment + list_eng[i] + ".+++" + list_ch[i]
            if i < (len_eng-2):
                segment = segment + "。+++"
            else:
                segment = segment + "。==="
    return segment


# 获取每日一译
def get_translate(text):
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
    return article


# 文章写入text文件utf-8编码
# file_tag = 1 是普通的新闻
# file_tag =2 是每日一课
def generate_document_with_text(content, file_tag = 1):
    # 获取今日日期+title作为文件名
    # 写入text文件
    doc_path = 'E:\\Now_Works\\reading_two\\'
    i = datetime.datetime.now()
    date_name = str(i.month)+'.'+str(i.day)
    dir_path = doc_path + date_name+'新闻'
    if file_tag == 1:
        text_path = dir_path +'\\'+date_name+'新闻'
    elif file_tag == 2:
        text_path = dir_path + '\\'+date_name+'每日一译'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    with open(text_path+'.txt', mode='a+', encoding='utf8') as article_file:
        article_file.write(content)


# 获取单篇每日一译
def get_single_translate(translate_url_1):
    page_translate_1 = get_html_text(translate_url_1)
    translate_content_1 = get_translate(page_translate_1)
    generate_document_with_text(translate_content_1, 2)


def getMonthTranslate():
    list_translate_url = ['https://language.chinadaily.com.cn/a/202204/20/WS625fd0cea310fd2b29e58268.html',
                          'https://language.chinadaily.com.cn/a/202204/19/WS625e841ea310fd2b29e57e7b.html',
                          'https://language.chinadaily.com.cn/a/202204/18/WS625d2f66a310fd2b29e57a33.html',
                          'https://language.chinadaily.com.cn/a/202204/15/WS62593c2ba310fd2b29e57499.html',
                          'https://language.chinadaily.com.cn/a/202204/14/WS6257ec89a310fd2b29e57094.html']
    j = 0
    dir_path = 'E:\\Now_Works\\reading_two\\每日一译\\'
    for translate in list_translate_url:
        page_text = get_html_text(translate)
        translate_content = get_translate(page_text)
        j = j+1
        text_path = dir_path + '5.'+str(j)+'每日一译'
        with open(text_path + '.txt', mode='a+', encoding='utf8') as article_file:
            article_file.write(translate_content)


if __name__ == "__main__":
     url_1 = "https://language.chinadaily.com.cn/a/202211/14/WS637225f7a310491754329a05.html"
     url_2 = "https://language.chinadaily.com.cn/a/202205/24/WS628c200aa310fd2b29e5e826.html"

     # translate_url_1 = "https://language.chinadaily.com.cn/a/202205/12/WS627cdbe6a310fd2b29e5c4f3.html"
     page_text_1 = get_html_text(url_1)
     page_content_1 = find_html_content_from_china_daily(page_text_1, 1)
     generate_document_with_text(page_content_1)
















