

from back.database import delete_db, get_db, insert_db, update_db
from back.utility import logging
from front.utility import send_msg, set_kb, wait_msg
from telebot       import TeleBot
from telebot.types import Message, ReplyKeyboardRemove  as rmvKb

from front.vars import *


@logging()
def add_group(bot : TeleBot, _id : str | int) -> None:


    @logging()
    def __add_group(msg : Message, bot : TeleBot, _id : str | int, name : str) -> None:
        if (insert_db(f"INSERT INTO groups_tb (name, msg) VALUES ('{name}', {msg.text})", 'groups_tb')):
            send_msg(bot, _id, f'Добавлена группа {name} с текстом:\n{msg.text}', set_kb(BOT_KB))
        else:
            send_msg(bot, _id, f'Не добавлена группа {name} с текстом:\n{msg.text}.', set_kb(BOT_KB))


    @logging()
    def __add_msg(msg : Message, bot : TeleBot, _id : str | int) -> None:
        wait_msg(bot, _id, __add_group, ADD_GROUP_MSG, rmvKb(), [bot, _id, msg.text])


    wait_msg(bot, _id, __add_msg, ADD_GROUP, rmvKb(), [bot, _id])


@logging()
def edit_group(bot : TeleBot, _id : str | int) -> None:


    @logging()
    def __edit_group(msg : Message, bot : TeleBot, _id : str | int, name : str) -> None:
        if (update_db(f"UPDATE groups_tb SET msg='{msg.text}' WHERE name='{name}'", 'groups_tb')):
            send_msg(bot, _id, f'Группа {name} обновлена с текстом:\n{msg.text}', set_kb(BOT_KB))
        else:
            send_msg(bot, _id, f'Не обновлена группа {name} с текстом:\n{msg.text}.', set_kb(BOT_KB))


    @logging()
    def __edit_msg(msg : Message, bot : TeleBot, _id : str | int) -> None:
        wait_msg(bot, _id, __edit_group, EDIT_GROUP_MSG, rmvKb(), [bot, _id, msg.text])

    groups_kb = [it[1] for it in get_db('groups_tb')]
    wait_msg(bot, _id, __edit_msg, EDIT_GROUP, set_kb(groups_kb), [bot, _id])


@logging()
def del_group(bot : TeleBot, _id : str | int) -> None:


    @logging()
    def __del_group(msg : Message, bot : TeleBot, _id : str | int) -> None:
        if (delete_db(f"name='{msg.text}'", 'groups_tb')):
            send_msg(bot, _id, f'Группа {msg.text} удалена.', set_kb(BOT_KB))
        else:
            send_msg(bot, _id, f'Группа {msg.text} не удалена.', set_kb(BOT_KB))


    wait_msg(bot, _id, __del_group, DELETE_GROUP, rmvKb(), [bot, _id])


@logging()
def show_group(bot : TeleBot, _id : str | int) -> None:


    @logging()
    def __show_group(msg : Message, bot : TeleBot, _id : str | int) -> None:
        if (delete_db(f"name='{msg.text}'", 'groups_tb')):
            send_msg(bot, _id, f'Группа {msg.text} удалена.', set_kb(BOT_KB))
        else:
            send_msg(bot, _id, f'Группа {msg.text} не удалена.', set_kb(BOT_KB))


    wait_msg(bot, _id, __show_group, EDIT_GROUP, rmvKb(), [bot, _id])
