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

import exclog, os

from traceback import format_exc
from dotenv import load_dotenv
load_dotenv('./setup/.env')
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
bot = TeleBot(os.getenv('TOKEN'))
#\------------------------------------------------------------------/#

ADMINS = ['281321076', '923118950']

BOT_FUNC = {'Добавить'      : add_group,
            'Редактировать' : edit_group,
            'Удалить'       : del_group, 
            'Показать'      : show_group}

#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@exclog.logging()
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

    group : Tuple = get_info(_id)

    if group:
        u_id = str(msg.from_user.id)
        
        txt    : str = group[1] 
        f_name : str = msg.from_user.first_name
        l_name : str = msg.from_user.last_name
        u_name : str = msg.from_user.username

        if '@user' in txt:
            txt = txt.replace('@user', f_name if f_name else l_name \
                    if l_name else u_name \
                        if u_name else '')
        
        msg = send_msg(bot, _id, txt, set_inline_kb({'Подтвердить' : u_id}))
        users_sub[_id] = {u_id : [False, msg.message_id, False]}
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@exclog.logging()
def input_keyboard(msg : Message) -> None:
    global users_sub
    
    _id  = str(msg.chat.id)
    u_id = str(msg.from_user.id)
    
    txt : str = msg.text

    if _id in ADMINS and txt in BOT_FUNC.keys():
        BOT_FUNC[txt](bot, _id)
    elif _id in users_sub.keys() and \
            u_id in users_sub[_id].keys() and not users_sub[_id][u_id][0]:
        del_msg(bot, _id, msg.message_id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.callback_query_handler(func=lambda call: True)
@exclog.logging()
def callback_inline(call : CallbackQuery):
    global users_sub

    _id  = str(call.message.chat.id)
    u_id = str(call.from_user.id)

    if _id in users_sub.keys() and \
            u_id in users_sub[_id].keys() and not users_sub[_id][u_id][0]:
        users_sub[_id][u_id][0] = True
        users_sub[_id][u_id][2] = True
        if del_msg(bot, _id, users_sub[_id][u_id][1]):
            users_sub[_id][u_id][1] = None
#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    try:
        proc = init_proc(handle_mems, [])
        start_proc(proc)
        bot.polling(allowed_updates="chat_member")
    except:
        print(f"Polling Error! {format_exc()}")
#\==================================================================/#
