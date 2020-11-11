import requests
import json
import datetime
import time
import logging
import telegram #pip install python-telegram-bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
import os
import scipy.io
import csv
import pymysql
import pandas as pd
from neo4j import GraphDatabase
#봇 정보 전달
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
token = "1336601123:AAGiyY00Ma_tuhOufGB6uqeWq-njV3y_frk"
bb = telegram.Bot(token=token)
chat_id = 1242789121

#장소에따른 데이터프레임
def get_tablebylocation(place):
    df = pd.DataFrame(columns=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r'])
    dong = place.split()[-1]
    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "select * from ourmz.store WHERE store_addr3 like '%{}%'".format(dong)
    curs.execute(sql)
    rows = curs.fetchall()
    #print(rows)
    for i in range(len(rows)):
        a = rows[i]
        df.loc[i] = a
    df = df.loc[df['n'].str.contains(dong)]
    df = df.reset_index(drop=True)
    return df, df['m'][0]
#df1=get_tablebylocation()

def get_menu(menu_input):
    menu=[]
    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "select * from ourmz.menu where menu_name = '{}'".format(menu_input)
    curs.execute(sql)
    rows = curs.fetchone()
    if rows is not None:
    #print(rows[0])
        menuID= rows[0]
        menu.append(menuID)
    else:
        menuID=None
    return menuID

#장소, 메뉴에따른 데이터프레임
def get_tablebymenu(menu_input, df):
    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "select * from ourmz.menu where menu_name = '{}'".format(menu_input)
    curs.execute(sql)
    rows = curs.fetchone()
    #print(rows[0])
    menuID= rows[0]
    want_menu = df.loc[df['b']==menuID]
    return want_menu
# df2=get_tablebymenu()
# df2
def get_weather(gu):
    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "select * from ourmz.gudong WHERE gu like '{}'".format(gu)
    curs.execute(sql)
    rows = curs.fetchall()
    nx=rows[0][2]
    ny=rows[0][3]
    return nx, ny

def get_menubyweather(nx,ny):
    vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst?"

    service_key = "WgdqLLe9BKioZRzKSlzBRo43aFLpDPGWLCYqtn9NPpUU%2FHhv89P2pux0HA%2BPMhpJtxNDVhZTA19rceoGpoxZJA%3D%3D"

    today = datetime.datetime.today()
    base_date = today.strftime("%Y%m%d")  # "20200214" == 기준 날짜
    base_time = "0800"  # 날씨 값

    #     #마포구 위도,경도
    #     nx = str(nx)
    #     ny = str(ny)

    payload = "serviceKey=" + service_key + "&" + \
              "dataType=json" + "&" + \
              "base_date=" + base_date + "&" + \
              "base_time=" + base_time + "&" + \
              "nx=" + nx + "&" + \
              "ny=" + ny

    # 값 요청
    res = requests.get(vilage_weather_url + payload)
    item = res.json().get('response').get('body').get('items')
    # item
    # 강수형태(PTY) 코드 : 없음(0), 비(1), 비/눈(진눈개비)(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7)
    # T3H(3시간 기온)
    # sky 상태
    sky = item['item'][1]['fcstValue']

    # temp 상태
    temp = item['item'][6]['fcstValue']

    if int(temp) <= 16 and sky == '1':
        cond = '0'
        condi = '춥고 비옴'
    if int(temp) <= 16 and sky == '3':
        cond = '1'
        condi = '춥고 눈옴'
    if int(temp) <= 16 and sky == '0':
        cond = '2'
        condi = '추움'
    if int(temp) >= 17 and int(temp) <= 26 and sky == '1':
        cond = '3'
        condi = '비옴'
    if int(temp) >= 17 and int(temp) <= 26 and sky == '0':
        cond = '4'
        condi = '보통'
    if int(temp) >= 27 and sky == '1':
        cond = '5'
        condi = '덥고 비옴'
    if int(temp) >= 27 and sky == '0':
        cond = '6'
        condi = '더움'
    #     print(cond)
    weather_menuID = []
    weather_cnt = cond
    weather_con = condi

    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8')

    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()

    sql = "select * from ourmz.weather where weather = '{}'".format(weather_cnt)
    curs.execute(sql)

    rows = curs.fetchall()
    # print(rows)

    a = rows
    for i in range(len(a)):
        menuID = a[i][1]
        weather_menuID.append(menuID)
    return weather_con, weather_menuID



# from neo4j import GraphDatabase

def feel_sum(word):
    feeling = word
    taste_menu = []
    print("[defs.py] word ={}".format(word))
    # df4 = run_query(get_menubyfeeling(word))

    def run_query(func):
        print("[defs.py] run_query ")
        uri = 'neo4j://localhost:7687'
        user = 'neo4j'
        password = '1234'
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.read_transaction(func)

    def get_menubyfeeling(tx):
        print("[defs.py] get_menubyfeeling ")
        lst = []
        lst1 = []
        lst2 = []
        lst3 = []
        query = """
                   MATCH (a:기쁨단어)
                   RETURN a.기쁨 AS 기쁨단어
                """
        query1 = """
                   MATCH (c:화남단어)
                   RETURN c.화남 AS 화남단어
                """
        query2 = """
                   MATCH (d:지침단어)
                   RETURN d.지침 AS 지침단어
                """
        query3 = """
                   MATCH (b:슬픔단어)
                   RETURN b.슬픔 AS 슬픔단어
                """
        result = tx.run(query)
        result1 = tx.run(query1)
        result2 = tx.run(query2)
        result3 = tx.run(query3)
        for record in result:
            lst.append(record['기쁨단어'])
        for record in result1:
            lst1.append(record['화남단어'])
        for record in result2:
            lst2.append(record['지침단어'])
        for record in result3:
            lst3.append(record['슬픔단어'])
        if feeling in lst:
            feel = '기쁨'
        #         print('기쁨')
        elif feeling in lst1:
            feel = '화남'
        #         print('화남')
        elif feeling in lst2:
            feel = '지침'
        #         print('지침')
        elif feeling in lst3:
            feel = '슬픔'
        #         print('슬픔')
        else:
            feel = 'None'
        #         print('None')
        print(feel)
        #     f.append(feel)

        angry = []
        query = """
                   MATCH (a:감정{기분:'화남'}) - [r:땡긴다] -> (b)
                   RETURN b.종류 AS 맛종류
                """
        result = tx.run(query)

        for record in result:
            angry.append(record['맛종류'])
            #     print(버럭)
        happy = []
        query = """
                   MATCH (a:감정{기분:'기쁨'}) - [r:땡긴다] -> (b)
                   RETURN b.종류 AS 맛종류
                """
        result = tx.run(query)

        for record in result:
            happy.append(record['맛종류'])
            #     print(행복)
        sad = []
        query = """
                   MATCH (a:감정{기분:'슬픔'}) - [r:땡긴다] -> (b)
                   RETURN b.종류 AS 맛종류
                """
        result = tx.run(query)

        for record in result:
            sad.append(record['맛종류'])
        #     print(sad)
        tired = []
        query = """
                   MATCH (a:감정{기분:'지침'}) - [r:땡긴다] -> (b)
                   RETURN b.종류 AS 맛종류
                """
        result = tx.run(query)

        for record in result:
            tired.append(record['맛종류'])
            #     print(tired)

        if feel == "화남":
            #         run_query(get_angry_taste)
            emo = angry
        elif feel == "기쁨":
            #         run_query(get_happy_taste)
            emo = happy
        elif feel == "슬픔":
            #         run_query(get_sad_taste)
            emo = sad
        elif feel == "지침":
            #         run_query(get_tired_taste)
            emo = tired

        #     print(emo)

        짠맛 = []
        query = """
                   MATCH (a:짠맛)
                   RETURN a.메뉴 AS 짠맛
                """
        result = tx.run(query)

        for record in result:
            짠맛.append(record['짠맛'])
        매운맛 = []
        query = """
                   MATCH (a:매운맛)
                   RETURN a.메뉴 AS 매운맛
                """
        result = tx.run(query)

        for record in result:
            매운맛.append(record['매운맛'])
        느끼한맛 = []
        query = """
                   MATCH (a:느끼한맛)
                   RETURN a.메뉴 AS 느끼한맛
                """
        result = tx.run(query)

        for record in result:
            느끼한맛.append(record['느끼한맛'])
        단맛 = []
        query = """
                   MATCH (a:단맛)
                   RETURN a.메뉴 AS 단맛
                """
        result = tx.run(query)

        for record in result:
            단맛.append(record['단맛'])
        신맛 = []
        query = """
                   MATCH (a:신맛)
                   RETURN a.메뉴 AS 신맛
                """
        result = tx.run(query)

        for record in result:
            신맛.append(record['신맛'])
        #         global taste_menu

        for j in emo:
            if j == '짠맛':
                #             run_query(get_짠맛menuID)
                taste_menu.append(짠맛)
            elif j == '느끼한맛':
                #             run_query(get_느끼한맛menuID)
                taste_menu.append(느끼한맛)
            elif j == '매운맛':
                #             run_query(get_매운맛menuID)
                taste_menu.append(매운맛)
            elif j == '단맛':
                #             run_query(get_단맛menuID)
                taste_menu.append(단맛)
            elif j == '신맛':
                #             run_query(get_신맛menuID)
                taste_menu.append(신맛)


    df4 = run_query(get_menubyfeeling)
    return taste_menu


def get_feeling(word):
    feeling = word
    f = []
    print("[defs.py] word ={}".format(word))

    def run_query(func):
        print("[defs.py] run_query ")
        uri = 'neo4j://localhost:7687'
        user = 'neo4j'
        password = '1234'
        driver = GraphDatabase.driver(uri, auth=(user, password))
        with driver.session() as session:
            session.read_transaction(func)

    def feelings(tx):
        print("[defs.py] feeling ")
        lst = []
        lst1 = []
        lst2 = []
        lst3 = []
        query = """
                   MATCH (a:기쁨단어)
                   RETURN a.기쁨 AS 기쁨단어
                """
        query1 = """
                   MATCH (c:화남단어)
                   RETURN c.화남 AS 화남단어
                """
        query2 = """
                   MATCH (d:지침단어)
                   RETURN d.지침 AS 지침단어
                """
        query3 = """
                   MATCH (b:슬픔단어)
                   RETURN b.슬픔 AS 슬픔단어
                """
        result = tx.run(query)
        result1 = tx.run(query1)
        result2 = tx.run(query2)
        result3 = tx.run(query3)
        for record in result:
            lst.append(record['기쁨단어'])
        for record in result1:
            lst1.append(record['화남단어'])
        for record in result2:
            lst2.append(record['지침단어'])
        for record in result3:
            lst3.append(record['슬픔단어'])

        if feeling in lst:
            f.append('기쁨')
        elif feeling in lst1:
            f.append('화남')
        elif feeling in lst2:
            f.append('지침')
        elif feeling in lst3:
            f.append('슬픔')
        else:
            f.append(None)

    df4 = run_query(feelings)
    return f

def get_menuname(menuID_list):
    menu = pd.DataFrame(columns=['menuID','menu_name',])
    conn = pymysql.connect(host='127.0.0.1', user='root', db='ourmz', charset='utf8',password='')
    # Connection 으로부터 Cursor 생성
    curs = conn.cursor()
    sql = "select * from ourmz.menu"
    curs.execute(sql)
    rows = curs.fetchall()
#     print(rows)
    for i in range(len(rows)):
        a = rows[i]
        menu.loc[i] = a
    aa=[]
    for i in menuID_list:
    #     print(i)
        a=menu.loc[menu['menuID']==i,'menu_name'].values[0]
        aa.append(a)
#         print(aa)
    return aa
# df5=get_menuname(df3)
# df5
# df6=get_menuname(taste_menu)
# df6


# 리스트 5개씩 분할

def divide_list(l, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for j in range(0, len(l), n):
        yield l[j:j + n]


def random(menulist):
    import random
    random.shuffle(menulist)
    n = 5
    result = tuple(divide_list(menulist, n))
    result[0]
    return result[0]

# random(df5)
# random(df6)