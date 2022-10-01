#/==================================================================\#
# bot.py                                              (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------/ installed libs  \------------------------\#
from typing        import Any, Callable, Dict
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove as rmvKb
#------------------------\ project modules /-------------------------#
from back  import *
from front import *
from front.vars import BOT_KB
from setup import *
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
bot = TeleBot(TOKEN)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(commands=['start'])
@logging()
def start(msg : Message) -> None:
    """### Bot begin actions """
    _id = str(msg.chat.id)

    send_msg(bot, _id, 'Бот для управления рассылкой сообщений.', set_kb(BOT_KB))
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.message_handler(content_types=['text'])
@logging()
def input_keyboard(msg : Message) -> None:

    BOT_FUNC   =  {'Добавить'      : add_group,
                   'Редактировать' : edit_group,
                   'Удалить'       : del_group, 
                   'Показать'      : show_group}

    _id = str(msg.chat.id)
    txt : str = msg.text

    if txt in BOT_FUNC.keys():
        BOT_FUNC[txt](bot, _id)
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@bot.callback_query_handler(func=lambda call: True)
@logging()
def callback_inline(call):
    data   : str = call.data
    _id    : int = call.message.chat.id
    msg_id : int = call.message.message_id

    if data.isdigit():
        #send_call_resp(bot, _id, data, msg_id)
        pass

#\------------------------------------------------------------------/#


#\==================================================================/#
if __name__ == "__main__":
    bot.polling(none_stop=True)
#\==================================================================/#
