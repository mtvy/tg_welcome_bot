#/==================================================================\#
# bot.py                                              (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Tuple
from telebot       import TeleBot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove as rmvKb
#------------------------\ project modules /-------------------------#
from back  import *
from front import *
from front.vars import BOT_KB
from setup import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
bot = TeleBot(TOKEN)
#\------------------------------------------------------------------/#

ADMINS = ['281321076', '923118950']

BOT_FUNC = {'Добавить'      : add_group,
            'Редактировать' : edit_group,
            'Удалить'       : del_group, 
            'Показать'      : show_group}


#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)
    if _id in ADMINS:
        send_msg(bot, _id, 'Бот для управления рассылкой сообщений.', set_kb(BOT_KB))
    else:
        send_msg(bot, _id, 'Нет доступа', rmvKb())
#\------------------------------------------------------------------/#

users_sub = {}

#\------------------------------------------------------------------/#
@bot.message_handler(content_types=["new_chat_members"])
def new_group_user(msg : Message):
    global users_sub

    _id  = str(msg.chat.id)
    u_id = str(msg.from_user.id)

    group : Tuple = get_info(_id)

    if group:
        send_msg(bot, _id, group[1], set_inline_kb({'Подтвердить' : u_id}))
        users_sub[_id] = {u_id : False}
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:
    global users_sub
    

    _id  = str(msg.chat.id)
    u_id = str(msg.from_user.id)
    
    txt : str = msg.text

    if _id in ADMINS and txt in BOT_FUNC.keys():
        BOT_FUNC[txt](bot, _id)
    elif _id in users_sub.keys() and \
            u_id in users_sub[_id] and not users_sub[_id][u_id]:
        del_msg(bot, _id, msg.message_id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.callback_query_handler(func=lambda call: True)
@logging()
def callback_inline(call : CallbackQuery):
    global users_sub


    _id  = str(call.message.chat.id)
    u_id = str(call.from_user.id)

    data   : str = call.data
    l_name : str = call.from_user.first_name
    f_name : str = call.from_user.first_name
    msg_id : int = call.message.message_id

    if _id in users_sub.keys() and \
            u_id in users_sub[_id] and not users_sub[_id][u_id]:
        users_sub[_id][u_id] = True
        del_msg(bot, _id, msg_id)
        


#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    bot.polling(none_stop=True)
#\==================================================================/#
