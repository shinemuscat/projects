import json
import datetime
import time
import logging
import telegram  # pip install python-telegram-bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from defs import get_tablebylocation
from defs import get_tablebymenu
from defs import get_menubyweather
from defs import get_menuname
from defs import feel_sum
from defs import get_menu
from defs import get_weather
import train as t
import tel_prac
from defs import get_feeling
from train import chat

feeling = ['좋아', '행복해', '짱이야', '괜찮아', '굿', '유쾌해', '만족해', '사랑해',
           '평화로워', '신나', '즐거워', '뿌듯해', '산뜻해', '설레', '차분해', '고요해',
           '상쾌해', '짜릿해', '편해', '통쾌해', '재밌어', '흐뭇해', '활기차', '슬퍼',
           '우울해', '비참해', '울적해', '침울해', '쓸쓸해', '외로워', '서운해', '울적해',
           '암담해', '불안해', '걱정', '근심', '무서워', '찝찝해', '눈물', '섭섭해', '속상해',
           '후회', '괴로워', '민망해', '쪽팔려', '화나', '짜증나', '빡쳐', '스트레스', '별로',
           '분해', '울화', '극혐', '초조해', '불안해', '긴장', '불쾌해', '성나', '부끄러워',
           '흥분', '역겨워', '후회', '괴로워', '분노', '최악', '민망해', '쪽팔려', '좆같애',
           '엿같애', '힘들어', '지쳤어', '피곤해', '허전해', '허탈해', '멍해', '무기력해',
           '걱정', '근심', '불안해', '무서워', '지겨워', '졸려', '지루해', '무력해', '불편해',
           '찝찝해', '후회', '혼란', '안타까워', '괴로워', '막막', '따분해']
 

kogptqa = ''
sent_tokens = ''
tok = ''
model = ''
vocab = ''
def get_message(bot, update):
    text = update.message.text
    print(text)
    g_m = t.chat2(text, kogptqa, sent_tokens, tok, model, vocab)
    bot.send_message(chat_id=chat_id, text=g_m)

def divide_list(l, n):
    # 리스트 l의 길이가 n이면 계속 반복
    for j in range(0, len(l), n):
        yield l[j:j + n]

def random(menulist):
    import random
    random.shuffle(menulist)
    n = 5
    result = tuple(divide_list(menulist, n))
    return result[0]


# 봇 정보 전달
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Botfather token
token = "1336601123:AAGiyY00Ma_tuhOufGB6uqeWq-njV3y_frk"
chat_id = '1242789121'
bot = telegram.Bot(token=token)




# 버튼 메뉴 설정
def build_box(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

time.sleep(0.3)
show_list = []
show_list.append(InlineKeyboardButton('맛집 추천받기', callback_data='맛집 추천받기'))
show_list.append(InlineKeyboardButton('머먹찌랑 대화하기', callback_data='머먹찌랑 대화하기'))
show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
bot.sendMessage(chat_id=chat_id, text="난 맛집추천봇 머먹찌야!" + "\n" "나랑 뭐할래?!" + "\n" + "처음으로 돌아가고 싶다면" + "\n" +" *머먹찌* 라고 쳐줘!", reply_markup=show_markup,parse_mode = "Markdown")

def weather_button(bot, update, df4):
    t = "오늘같은 날씨에는 이런 메뉴들이 생각나~~"
    bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton(df4[0], callback_data=df4[0]))
    show_list.append(InlineKeyboardButton(df4[1], callback_data=df4[1]))
    show_list.append(InlineKeyboardButton(df4[2], callback_data=df4[2]))
    show_list.append(InlineKeyboardButton(df4[3], callback_data=df4[3]))
    show_list.append(InlineKeyboardButton('없어', callback_data='없어'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
    update.message.reply_text("이 메뉴들 어때? 맘에 드는게 있으면 선택하고 없으면 '없어'를 눌러줘", reply_markup=show_markup)

def feeling_button(bot, update,df4):
    t = "그런감정에는 이런 메뉴들이 생각나~~"
    bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    # bot.send_photo(chat_id=update.message.chat_id,
    #                photo='https://lolstatic-a.akamaihd.net/frontpage/apps/prod/rg-champion-reveal-neeko/en_US/325b98f79271c28b8748a6af3474938dc4cfe1df/assets/img/content/neeko/wallpaper/neeko-splash.jpg')
    # time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton(df4[0], callback_data=df4[0]))
    show_list.append(InlineKeyboardButton(df4[1], callback_data=df4[1]))
    show_list.append(InlineKeyboardButton(df4[2], callback_data=df4[2]))
    show_list.append(InlineKeyboardButton(df4[3], callback_data=df4[3]))
    show_list.append(InlineKeyboardButton('없어', callback_data='없어'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
    update.message.reply_text("이 메뉴들 어때? 맘에 드는게 있으면 선택하고 없으면 '없어'를 눌러줘", reply_markup=show_markup)

def more_button(update):
    # t = "ddd"
    # bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton('더보기', callback_data='더보기'))
    show_list.append(InlineKeyboardButton('이제 됐어', callback_data='이제 됐어'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, 1))  # make markup
    update.message.reply_text("더 보고싶다면 '더보기'를 눌러줘~!", reply_markup=show_markup)

def gu_request(update):
    # t = "그런감정에는 이런 메뉴들이 생각나~~"
    # bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton('강남구 신사동', callback_data='강남구 신사동'))
    show_list.append(InlineKeyboardButton('관악구 신사동', callback_data='관악구 신사동'))
    show_list.append(InlineKeyboardButton('은평구 신사동', callback_data='은평구 신사동'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
    update.message.reply_text("이중에 어디야?", reply_markup=show_markup)

def feedback(update):
    # t = "내 추천 어땟니???"
    # bot.sendMessage(chat_id=update.message.chat_id, text=t)
    time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton('좋아', callback_data='좋아'))
    show_list.append(InlineKeyboardButton('별로야', callback_data='별로야'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, 1))  # make markup
    update.message.reply_text("내 추천 어땠어???ㅎㅎ", reply_markup=show_markup)

def gpt_button(bot, update):
    # t = "나랑 머하까?!"
    # bot.sendMessage(chat_id=update.message.chat_id, text=t)
    bot.sendMessage(chat_id=chat_id,
                    text="난 맛집추천봇 머먹찌야!" + "\n" "나랑 뭐할래?!" + "\n" + "처음으로 돌아가고 싶다면" + "\n" + " *머먹찌* 라고 쳐줘!",
                    parse_mode="Markdown")
    time.sleep(0.3)
    show_list = []
    show_list.append(InlineKeyboardButton('맛집 추천받기', callback_data='맛집 추천받기'))
    show_list.append(InlineKeyboardButton('머먹찌랑 대화하기', callback_data='머먹찌랑 대화하기'))
    show_markup = InlineKeyboardMarkup(build_box(show_list, len(show_list) - 1))  # make markup
    update.message.reply_text("나랑 뭐할래?!", reply_markup=show_markup)



gu_list=[]
addrs=[]
menus=[]
nope=[]
callquery = []
def handler1(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id
    print('gpt')
    mm = get_menu(text)
    if callquery[0] == '맛집 추천받기':
        if mm is not None :
            menus.append(text)
            bot.send_message(chat_id=chat_id,
                             text=text + ' 먹고싶구나?! 추천해줄게!' + '\n' + '맛집 리스트를 가져오고 있어~' + '\n' + '조금만 기다려줘~')
            print(menus)
            df1,gu = get_tablebylocation(addrs[0])
            df2 = get_tablebymenu(menus[0], df1)

            df2 = df2.values.tolist()
            print(df2)
            # df2를 랜덤으로 5개씩 묶어 놓는 함수 만들기 OK

            userlist = [2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17]
            if len(df2) == 0:
                bot.send_message(chat_id=chat_id, text='미안.. 아직 내 데이터상에는'+'\n'+' 이 지역에 ' + text + ' 맛집은 없어ㅜ.ㅜ' + '\n' + '다시 처음부터 적어줘!')
                # Stringmessage_text = "<b>" + update.getMessage().getFrom().getFirstName() + "</b>" + " Said what? \n" + update.getMessage().getText();

                menus.clear()
                addrs.clear()
                gu_list.clear()
                bot.sendMessage(chat_id=chat_id,
                                text=emojize(
                                    "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",
                                    use_aliases=True))
                # 처음으로 돌아가기 구현. OK

            else:
                df3 = tuple(divide_list(df2, 5))
                print(df3)
                print(len(df3))
                if len(df3) >= 2:
                    df3 = df3[0]
                    for i in range(len(df3)):
                        txt = ''
                        for j in userlist:
                            txt = txt + str(df3[i][j]) + '\n'
                        # print('txt',txt)
                        bot.send_message(chat_id=chat_id, text=txt)

                        # addrs.clear()
                    # 더보기
                    more_button(update)
                else:
                    df3 = df3[0]
                    for i in range(len(df3)):
                        txt = ''
                        for j in userlist:
                            txt = txt + str(df3[i][j]) + '\n'
                        # print('txt',txt)
                        bot.send_message(chat_id=chat_id, text=txt)
                    menus.clear()
                    addrs.clear()
                    gu_list.clear()
                    bot.send_message(chat_id=chat_id, text='내가 준비한건 여기까지!')
                    bot.sendMessage(chat_id=chat_id,
                                    text=emojize(
                                        "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",
                                        use_aliases=True))



        elif text in feeling:
            print(text)
            bot.send_message(chat_id=chat_id, text='그렇구나 '+'*'+text+'*'+' 감정이구나..',parse_mode = "Markdown")
            # taste_menu=[]
            ff = feel_sum(text)
            print('[newchatbot5]: {}'.format(ff))
            # print(ff)
            ff = sum(ff, [])
            ff = set(ff)
            ff = list(ff)
            print(len(ff))
            df4 = get_menuname(ff)
            df5 = random(df4)
            feeling_button(bot, update, df5)


        elif text == '머먹찌':
            gpt_button(bot, update)
            callquery.clear()

        elif text == '없어':
            nope.append(text)
            bot.send_message(chat_id=chat_id, text='그렇다면 *날씨 기반*으로 메뉴를 추천해줄게!',
                             parse_mode = "Markdown")
            nx, ny = get_weather(gu_list[0])
            w_con,df3 = get_menubyweather(nx,ny)
            print(w_con)
            bot.send_message(chat_id=chat_id,text='오늘은 '+'*'+w_con+'*'+'의 날씨야!',parse_mode = "Markdown")
            print(len(df3), df3)
            df4 = get_menuname(df3)
            print(len(df4), df4)
            df5 = random(df4)
            print(df5)
            weather_button(bot, update, df5)


        elif mm is None:
            if text =='하이':
                bot.sendMessage(chat_id=chat_id,
                                text=emojize(
                                    "안녕! 나는 머먹찌야!:hamster:", use_aliases=True))
            elif text=='꺼져':
                bot.send_message(chat_id=chat_id,text='욕하지 마셈!')
            elif text=='신사동':
                bot.send_message(chat_id=chat_id,text='신사동은 여러곳에 있어! ')
                gu_request(update)
            elif text!= '슬퍼':
                df1,gu = get_tablebylocation(text)
                if len(df1) > 0 and len(text)>1:
                    gu_list.append(gu)
                    addrs.append(text)
                    bot.send_message(chat_id=chat_id,
                                     text=text + '에서 먹을거구나!' + '\n'+ text + '에서 먹고 싶은 메뉴가 있어?' + '\n' + '있으면 메뉴를 적어줘!' + '\n' + '없으면 "없어"라고 적어줘!',
                                     parse_mode = "Markdown")
                    print(addrs)
                    print(gu_list)

                else:
                    bot.send_message(chat_id=chat_id,
                                     text='그 말은 아직 내가 몰라..ㅠㅠ')
    else:
        get_message(bot, update)
        print('bot')
        if text=='머먹찌':
            gpt_button(bot,update)
            callquery.clear()



# callback
more_num=[]

def callback_get(bot, update):
    print("callback")
    print(update.callback_query.data)
    callquery.append(update.callback_query.data)

    if update.callback_query.data == '맛집 추천받기':
        bot.sendMessage(chat_id=chat_id,
                        text=emojize("안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!",
                                     use_aliases=True))
    if update.callback_query.data == "강남구 신사동" or update.callback_query.data == "관악구 신사동" or update.callback_query.data == "은평구 신사동":
        Gu=update.callback_query.data.split()[0]
        Dong=update.callback_query.data.split()[1]
        df1, gu = get_tablebylocation(Dong)
        gu_list.append(Gu)
        addrs.append(update.callback_query.data)
        bot.send_message(chat_id=chat_id,
                         text=update.callback_query.data + '에서 먹을거구나!' + '\n' + update.callback_query.data + '에서 먹고 싶은 메뉴가 있어?' + '\n' + '있으면 메뉴를 적어줘!' + '\n' + '없으면 "없어"라고 적어줘!',
                         parse_mode="Markdown")
        print(addrs)
        print(gu_list)
    if update.callback_query.data == "더보기":
        more_num.append(1)
        df1,gu = get_tablebylocation(addrs[0])
        # print('11111111111111111111111',df1)
        df2 = get_tablebymenu(menus[0], df1)

        df2 = df2.values.tolist()
        # print('222222222222222222222222222222', df2)
        # df2를 랜덤으로 5개씩 묶어 놓는 함수 만들기 OK

        userlist = [2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17]

        df3 = tuple(divide_list(df2, 5))
        # print(df3)
        index=len(more_num)
        df3 = df3[index]
        for i in range(len(df3)):
            txt = ''
            for j in userlist:
                txt = txt+str(df3[i][j])+'\n'
            # print('txt',txt)
            bot.send_message(chat_id=chat_id, text=txt)
            print(len(more_num))
            # addrs.clear()
        # test2(update)
        menus.clear()
        addrs.clear()
        gu_list.clear()
        bot.send_message(chat_id=chat_id, text='내가 준비한건 여기까지!')
        bot.sendMessage(chat_id=chat_id,
                        text=emojize(
                            "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",
                            use_aliases=True))


    if update.callback_query.data == "이제 됐어":
        bot.sendMessage(chat_id=chat_id,
                        text=emojize(
                            "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",
                            use_aliases=True))

    if update.callback_query.data != "없어" and update.callback_query.data != "더보기" and update.callback_query.data != "이제 됐어" and update.callback_query.data != "강남구 신사동" and update.callback_query.data != "관악구 신사동" and update.callback_query.data != "은평구 신사동" and update.callback_query.data != "맛집 추천받기" and update.callback_query.data != "머먹찌랑 대화하기":
        bot.edit_message_text(text=update.callback_query.data+" 좋은 선택이야!", chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
        menus.append(update.callback_query.data)
        df1,gu = get_tablebylocation(addrs[0])
        # print('11111111111111111111111',df1)
        df2 = get_tablebymenu(menus[0], df1)

        df2 = df2.values.tolist()
        # print('222222222222222222222222222222', df2)
        # df2를 랜덤으로 5개씩 묶어 놓는 함수 만들기 OK

        userlist = [2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17]
        if len(df2) == 0:
            bot.send_message(chat_id=chat_id, text='미안.. 아직 내 데이터상에는'+'\n'+' 이 지역에 ' + update.callback_query.data + ' 맛집은 없어ㅜ.ㅜ' + '\n' + '다시 처음부터 적어줘!')

            menus.clear()
            addrs.clear()
            gu_list.clear()
            bot.sendMessage(chat_id=chat_id,
                            text=emojize(
                                "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",parse_mode = "Markdown", use_aliases=True))
            # 처음으로 돌아가기 구현. OK

        else:
            df3 = tuple(divide_list(df2, 5))
            # print(df3)
            df3 = df3[0]
            for i in range(len(df3)):
                txt = ''
                for j in userlist:
                    txt = txt+str(df3[i][j])+'\n'
                # print(txt)
                bot.send_message(chat_id=chat_id, text=txt)
            menus.clear()
            addrs.clear()
            gu_list.clear()
            bot.send_message(chat_id=chat_id, text='내가 준비한건 여기까지!')
            bot.sendMessage(chat_id=chat_id,
                            text=emojize(
                                "다시 안녕! 나는 머먹찌야:hamster:" + "\n" + "맛집을 추천해줄게!" + "\n" + "어디서 먹을건지 지역을 적어줘!" + "\n" + "예)을지로",
                                use_aliases=True))


    if update.callback_query.data == "없어":
        bot.edit_message_text(
            text=emojize("그렇다면 너의 *현재 기분*에따라 메뉴를 추천해줄게" + "\n" + "지금 기분이 어때?:hamster:", use_aliases=True),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,parse_mode = "Markdown")

    if update.callback_query.data == '머먹찌랑 대화하기':
        bot.edit_message_text(
            text=emojize("그래! 나랑 얘기하고 놀자!:hamster:", use_aliases=True),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id)




# error 처리
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# command & function 활성화 하기
def main():
    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handler1))
    dp.add_handler(CallbackQueryHandler(callback_get))

    # log all errors
    dp.add_error_handler(error)
    #dp.add_handler(MessageHandler(Filters.text, get_message))
    # polling시작, 걸리는 시간 최대치 정해줌 너무 낮은 경우는 poll이 제대로 작동이 안됨
    # clean=true 기존의 텔레그램 서버에 저장되어있던 업데이트 사항 지우기
    updater.start_polling(timeout=1)
    # idle은 updater가 종료되지 않고 계속 실행
    updater.idle()

if __name__ == '__main__':
    kogptqa, sent_tokens, tok, model, vocab = t.chat1()
    main()