from telebot import types


def keyboard_1_7():
    markup_1_7 = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Երկուշաբթի', callback_data="d1")
    button_2 = types.InlineKeyboardButton(text='Երեքշաբթի', callback_data="d2")
    button_3 = types.InlineKeyboardButton(text='Չորեքշաբթի', callback_data="d3")
    button_4 = types.InlineKeyboardButton(text='Հինգշաբթի', callback_data="d4")
    button_5 = types.InlineKeyboardButton(text='Ուրբաթ', callback_data="d5")
    button_6 = types.InlineKeyboardButton(text='Շաբաթ', callback_data="d6")
    button_7 = types.InlineKeyboardButton(text='Կիրակի', callback_data="d7")
    markup_1_7.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)
    return markup_1_7


def keyboard_1_7_update():
    markup_1_7 = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Երկուշաբթի', callback_data="u1")
    button_2 = types.InlineKeyboardButton(text='Երեքշաբթի', callback_data="u2")
    button_3 = types.InlineKeyboardButton(text='Չորեքշաբթի', callback_data="u3")
    button_4 = types.InlineKeyboardButton(text='Հինգշաբթի', callback_data="u4")
    button_5 = types.InlineKeyboardButton(text='Ուրբաթ', callback_data="u5")
    button_6 = types.InlineKeyboardButton(text='Շաբաթ', callback_data="u6")
    button_7 = types.InlineKeyboardButton(text='Կիրակի', callback_data="u7")
    markup_1_7.add(button_1, button_2, button_3, button_4, button_5, button_6, button_7)
    return markup_1_7
