import telebot
import requests
from telebot.types import Message
from telebot import types
#from bot_token import TOKEN

from db import init_db, add_reg_info_in_db, update_schedule, update_name, update_surname, update_mail
from db import admin_check, mail, mail_check, admin, fromCompanyId_adminCheck, update_telephone
from keyboard import keyboard_1_7, keyboard_1_7_update

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import re

TOKEN = '   '

bot = telebot.TeleBot(TOKEN)

CompanyID = 0
name = ''
surname = ''

day = ""
start_time = ""
end_time = ""
telephone = ""
content = ''
message_in_mail = ''
schedule = ''
bonus_quantity = 0
bonus_id = 0
coupon_id = 0
purchase_price = 0

@bot.message_handler(commands=['start'])
def keyboard(message):
    start_keyboard = types.InlineKeyboardMarkup()
    start_register = types.InlineKeyboardButton(text='Գրանցվել', callback_data='register')
    start_last_data = types.InlineKeyboardButton(text='Վերջին տվյալներ', callback_data='lastData')
    start_support = types.InlineKeyboardButton(text='Օգնություն/Support', callback_data='support')
    start_report = types.InlineKeyboardButton(text='Ստանալ ամբողջական հաշվետվություն', callback_data='report')
    start_change_settings = types.InlineKeyboardButton(text="Փոփոխել կարգավորումները", callback_data="change_settings")
    start_add_new_bonus = types.InlineKeyboardButton(text="Գրանցել նոր բոնուս", callback_data="add_new_bonus")
    start_add_new_purchase = types.InlineKeyboardButton(text="Գրանցել նոր գնում", callback_data="add_new_purchase")
    start_confirm_coupon = types.InlineKeyboardButton(text="Հաստատել կուպոն", callback_data="confirm_coupon")
    start_keyboard.add(start_register, start_last_data, start_support, start_report,
                       start_change_settings, start_add_new_bonus, start_add_new_purchase, start_confirm_coupon)
    bot.send_message(message.from_user.id, 'Ընտրեք գործողությունը', reply_markup=start_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def Call_Back(call):
    global day
    if call.data == "register":
        bot.send_message(call.message.chat.id, "Մուտքագրեք Ձեր անունը։ ")
        bot.register_next_step_handler(call.message, registerName)
    elif call.data == "lastData":
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Դիտել Կայքում', url='https://www.facebook.com/allin.pr.group')
        markup.add(btn_my_site)
        bot.send_message(call.message.chat.id, "Վերջին տվյալները մեր կայքում", reply_markup=markup)
    elif call.data == "support":
        markup = types.InlineKeyboardMarkup()
        btn_call = types.InlineKeyboardButton(text='Զանգ', callback_data='call')
        btn_sendmail = types.InlineKeyboardButton(text='Ուղարկել նամակ', callback_data='sendMail')
        markup.add(btn_call, btn_sendmail)
        bot.send_message(call.message.chat.id, "Ընտրեք կապի միջոցը", reply_markup=markup)
    elif call.data == "call":
        bot.send_message(call.message.chat.id, "+37499471603")
    elif call.data == "sendMail":
        bot.send_message(call.message.chat.id, "Գրեք հաղորթագրությունը",)
        bot.register_next_step_handler(call.message, sendMail1, call)
    elif call.data == "add_new_bonus":
        bot.send_message(call.message.chat.id, "Գրեք բոնուսի քանակը", )
        bot.register_next_step_handler(call.message, bonus, call)
    elif call.data == "confirm_coupon":
        bot.send_message(call.message.chat.id, "Գրեք կուպոնի id-ն")
        bot.register_next_step_handler(call.message, id_of_coupon, call)
    elif call.data == "change_settings":
        markup = types.InlineKeyboardMarkup()
        basic_settings = types.InlineKeyboardButton(text='հիմնական կարգավորումներ',
                                                    url='https://www.facebook.com/allin.pr.group')
        telegram_info = types.InlineKeyboardButton(text='Տելեգրամի տվյալներ', callback_data='telegram_info')
        markup.add(basic_settings, telegram_info)
        bot.send_message(call.message.chat.id, text="Ընտրել կարգավորումը", reply_markup=markup)
    elif call.data == "telegram_info":
        markup = types.InlineKeyboardMarkup()
        schedule_start_end = types.InlineKeyboardButton(text='Գրաֆիկի սկիզբ/ավարտ', callback_data="schedule_start_end")
        change_name = types.InlineKeyboardButton(text='Փոխել անունը', callback_data='change_name')
        change_surname = types.InlineKeyboardButton(text='Փոխել ազգանունը', callback_data='change_surname')
        change_mail = types.InlineKeyboardButton(text='Փոխել էլ․հասցեն', callback_data='change_mail')
        change_telephone = types.InlineKeyboardButton(text="Փոխել հեռախոսահամարը", callback_data="change_telephone")
        markup.add(schedule_start_end, change_name, change_surname, change_mail, change_telephone)
        bot.send_message(call.message.chat.id, text="Ընտրել կարգավորումը", reply_markup=markup)
        """գրաֆիկի օրերի ընտրություն"""
    elif call.data in ["d1", "d2", "d3", "d4", "d5", "d6", "d7"]:
        day = call.data[1]
        bot.send_message(call.message.chat.id, "Ներմուծեք աշխատաժամի սկիզբը։ ")
        bot.register_next_step_handler(call.message, register_work_start_time)
    elif call.data in ["u1", "u2", "u3", "u4", "u5", "u6", "u7"]:
        day = call.data[1]
        bot.send_message(call.message.chat.id, "Ներմուծեք աշխատաժամի սկիզբը։ ")
        bot.register_next_step_handler(call.message, update_work_start_time)
    elif call.data == "change_name":
        bot.send_message(call.message.chat.id, text="Մուտքագրեք Ձեր անունը։ ")
        bot.register_next_step_handler(call.message, change_name_1)
    elif call.data == "change_surname":
        bot.send_message(call.message.chat.id, text="Մուտքագրեք Ձեր ազգանունը։ ")
        bot.register_next_step_handler(call.message, change_surname_1)
    elif call.data == "schedule_start_end":
        bot.send_message(call.message.chat.id, text="Ընտրեք գրաֆիկի օրը։ ", reply_markup=keyboard_1_7_update())

    elif call.data == "report":
        global mail
        mail = mail_check(chat_id=call.message.chat.id)
        if (mail):
            markup = types.InlineKeyboardMarkup()
            btn_yes = types.InlineKeyboardButton(text='այո', callback_data='yes')
            btn_no = types.InlineKeyboardButton(text='ոչ', callback_data='no')
            markup.add(btn_yes, btn_no)
            bot.send_message(call.message.chat.id, f"Ձեր {mail}-ին ուղարկե՞նք", reply_markup=markup)
        elif(not mail):
            bot.send_message(call.message.chat.id, "Գրեք Ձեր մեյլը ")
            bot.register_next_step_handler(call.message, change_mail_1, call)

    elif call.data == "yes":
        sendMail(mail, call, "Hello, \nThis is a test mail. \nIn this mail we are sending random text. \nThe mail is sent using Python SMTP library. \nThank You")

    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Գրեք այլ մեյլ ")
        bot.register_next_step_handler(call.message, change_mail_1, call)

    class ClassWithGlobalFunction:
        global sendMailAfterRegister
        def sendMailAfterRegister(mail, content): sendMailFromUser(mail, call, content)


@bot.callback_query_handler(func=lambda call: True)
def sendMail(mail, call, content):
    admin = admin_check(chat_id=call.message.chat.id)

    if(admin == 1):
        mail_content = content

        sender_address = 'test@allin.am'
        sender_pass = 'j700Q0YFgt8#'
        receiver_address = mail

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'A test mail sent by Python. It has an attachment.'

        if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
            message.attach(MIMEText(mail_content))

            session = smtplib.SMTP_SSL("mail.allin.am", 465)

            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            print("mail sent")
            bot.send_message(call.message.chat.id, "Ուղարկված է")

        else:
            bot.send_message(call.message.chat.id, "not valid mail")

    else:
        bot.send_message(call.message.chat.id, "you are not admin")

#Մեյլ ուղարկող առանց ադմին ստուգելու
def sendMailFromUser(mail, call, content):
    mail_content = content

    sender_address = 'test@allin.am'
    sender_pass = 'j700Q0YFgt8#'
    receiver_address = mail

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'

    if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        message.attach(MIMEText(mail_content))

        session = smtplib.SMTP_SSL("mail.allin.am", 465)


        session.login(sender_address, sender_pass)
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print("mail sent")
    else:
        bot.send_message(call.message.chat.id, "not valid mail")


def registerName(message: Message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Գրեք Ձեր ազգանունը։")
    print(message.chat.id)
    bot.register_next_step_handler(message, register_surname)


def register_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Ընտրեք շաբաթվա օրը։ ", reply_markup=keyboard_1_7())

#-------------------------------------------------------------------------------------------------


def register_work_start_time(message: Message):
    global start_time
    start_time = message.text
    bot.send_message(message.from_user.id, "Ներմուծեք աշխատաժամանակի ավարտը։ ")
    bot.register_next_step_handler(message, register_work_end_time)


def register_work_end_time(message: Message):
    global end_time
    end_time = message.text
    bot.send_message(message.from_user.id, "Ներմուծեք ընկերության համարը(ID): ")
    bot.register_next_step_handler(message, registerID)

#-------------------------------------------------------------------------------------------------


def registerID(message: Message):
    global CompanyID
    CompanyID = int(message.text)
    bot.send_message(message.from_user.id, "Ներմուծեք հեռախոսահամարը: ")
    bot.register_next_step_handler(message, telephone_n)


def telephone_n(message: Message):
    global telephone
    telephone = int(message.text)
    init_db()
    add_reg_info_in_db(chat_id=message.chat.id, company_id=CompanyID, name=name, surname=surname,
                       telephone=telephone, day=day, start_time=start_time, end_time=end_time)
    bot.send_message(message.from_user.id, "Ձեր անձնական տվյալներն են \n\n Անուն : " + name + "\n Ազգանուն : " +
                     surname + "\n Կազմակերպության ID : " + str(CompanyID) + "\n Աշխատանքային գրաֆիկ : " + day + " " +
                     start_time + "-" + end_time +
                     "\n Հեռախոսահամար ։ 0" + str(telephone))


    whole_info = "Նոր գրանցում \n\n Անուն : " + name + "\n Ազգանուն : " + surname + "\n Կազմակերպության ID : " + str(CompanyID) + "\n Աշխատանքային գրաֆիկ : " + "\n Հեռախոսահամար ։ 0" + str(telephone)
    mail = fromCompanyId_adminCheck(company_id=CompanyID)
    if(mail):
        sendMailAfterRegister(mail, whole_info)
    else:
        print("something happened, we didn't send")


def update_work_start_time(message):
    global start_time
    start_time = message.text
    bot.send_message(message.from_user.id, "Ներմուծեք աշխատաժամի ավարտը: ")
    bot.register_next_step_handler(message, update_work_end_time)


def update_work_end_time(message):
    global end_time
    end_time = message.text
    update_schedule(chat_id=message.chat.id, day=day, start_time=start_time, end_time=end_time)
    bot.send_message(message.from_user.id, "Ինֆորմացիան հաջողությամբ խմբագրված է ։")


def change_name_1(message: Message):
    global name
    name = message.text
    print(message.chat.id)
    update_name(chat_id=message.chat.id, name=name)
    bot.send_message(message.from_user.id, "Ինֆորմացիան հաջողությամբ խմբագրված է ։")


def change_surname_1(message: Message):
    global surname
    surname = message.text
    print(message.chat.id)
    update_surname(chat_id=message.chat.id, surname=surname)
    bot.send_message(message.from_user.id, "Ինֆորմացիան հաջողությամբ խմբագրված է ։")


def change_telephone_1(message: Message):
    global telephone
    telephone = message.text
    print(message.chat.id)
    update_telephone(chat_id=message.chat.id, telephone=telephone)
    bot.send_message(message.from_user.id, "Ինֆորմացիան հաջողությամբ խմբագրված է ։")


def change_mail_1(message: Message, call):
    global mail
    mail = message.text
    print(message.chat.id)
    update_mail(chat_id=message.chat.id, mail=mail)
    sendMail(mail, call, "Hello, \nThis is a test mail. \nIn this mail we are sending random text. \nThe mail is sent using Python SMTP library. \nThank You")


#==================================================================================================================
#Հետադարձ կապի համար ֆունկցիաններ
def change_mail_2(message: Message, call, mail, messageInMail):#էս հտադարձ կապի համար,առանց գրանցման նամակ ուղարկելու

    global message_in_mail
    mail = message.text
    print(message.chat.id)
    update_mail(chat_id=message.chat.id, mail=mail)
    sendMail2(message, call, messageInMail)


def sendMail1(message: Message, call):#էս հետադարձ կապի համարա
    global message_in_mail
    mail = mail_check(chat_id=call.message.chat.id)
    messageInMail = message.text
    message_in_mail = messageInMail + "   \n" + "Հաղորդագրությունը ուղարկված է " + str(mail) + " -ից"
    allInMail = 'danieldavtyan99@gmail.com'  # stex test@allin.am - na linelu
    if (mail):
        sendMailFromUser(allInMail, call, message_in_mail)
    if (not mail):
        bot.send_message(message.chat.id, "Գրեք Ձեր մեյլը ")
        bot.register_next_step_handler(message, change_mail_2, call, mail, messageInMail)


    #global message_in_mail
    # mail = mail_check(chat_id=call.message.chat.id)
    # messageInMail = message.text
    # message_in_mail = messageInMail + "   \n" + "Հաղորդագրությունը ուղարկված է " + str(mail) + " -ից"
    # allInMail = 'danieldavtyan99@gmail.com'  # stex test@allin.am - na linelu
    # if (mail):
    #     sendMailFromUser(allInMail, call, message_in_mail)
    # if (not mail):
    #     bot.send_message(message.chat.id, "Գրեք Ձեր մեյլը ")
    #     bot.register_next_step_handler(message, change_mail_2, call, mail, messageInMail)


def sendMail2(message : Message, call, messageInMail):


    mail = mail_check(chat_id=call.message.chat.id)
    message_in_mail = messageInMail + "   \n" + "Հաղորդագրությունը ուղարկված է " + str(mail) + " -ից"
    allInMail = 'danieldavtyan99@gmail.com'
    sendMailFromUser(allInMail, call, message_in_mail)
#=======================================================================================================

def bonus(message: Message, call):
    global bonus_quantity
    bonus_quantity = message.text
    bot.send_message(call.message.chat.id, "Գրեք բոնուսի ID-ն",)
    bot.register_next_step_handler(call.message, bonus_id, call)


def bonus_id(message: Message, call):
    global bonus_id
    bonus_id = message.text
    bot.send_message(call.message.chat.id, "Շնորհակալություն")
    payload = {'bonus_id': bonus_id,
               'bonus_quantity': bonus_quantity}
    r = requests.post('https://api.allin.am/telegram', data = payload)
    print(r.json())

    print(bonus_id, bonus_quantity)

#========================================================================================================

def id_of_coupon(message:Message, call):
    global coupon_id
    coupon_id = message.text
    bot.send_message(call.message.chat.id, "Գրեք գնման արժեքը")
    bot.register_next_step_handler(call.message, purchase, call)

def purchase(message: Message, call):
    global purchase_price
    purchase_price = message.text
    bot.send_message(call.message.chat.id, "Շնորհակալություն")
    print(coupon_id, purchase_price)

    payload2 = {'coupon_id': coupon_id,
               'purchase_price': purchase_price}
    r2 = requests.post('https://api.allin.am/telegram', data=payload2)
    print(r2.json())

bot.polling()