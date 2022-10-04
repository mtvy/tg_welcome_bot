#/==================================================================\#
# handle.py                                           (c) Mtvy, 2022 #
#\==================================================================/#
#                                                                    #
# Copyright (c) 2022. Mtvy (Matvei Prudnikov, m.d.prudnik@gmail.com) #
#                                                                    #
#\==================================================================/#

#/-----------------------------/ Libs \-----------------------------\#
import traceback
from back.database import get_db, update_db
from back.utility  import logging
from setup.config import TOKEN
from front.utility import del_msg, send_msg
from time            import sleep
from telebot         import TeleBot
from typing          import Callable
from multiprocessing import Process
from schedule        import every       as set_delay
from schedule        import run_pending as proc_run
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
@logging()
def init_proc(_func : Callable, _args) -> Process:
    return Process(target=_func, args=_args)


@logging()
def start_proc(proc : Process) -> Process:
    proc.start()
    return proc

@logging()
def kill_proc(proc : Process) -> Process:
    proc.kill()
    return proc
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
def timer_msg(_id : str | int, txt : str) -> None:
    try:
        bot = TeleBot(TOKEN)
        msg = send_msg(bot, _id, txt)
        sleep(15)
        del_msg(bot, _id, msg.message_id)
    except:
        pass
#\------------------------------------------------------------------/#


#\------------------------------------------------------------------/#
exc = False
def handle_mems() -> None:
    global exc

    def _send_req(bot : TeleBot) -> None:
        global exc

        try:
            for grp in get_db('groups_tb'):
                if len(grp[3]) > 13:
                    l_len = int(grp[4])
                    try:
                        p_len = bot.get_chat_member_count(grp[3])
                    except:
                        send_msg(bot, 281321076, 'get_chat_member_count')
                        #p_len = l_len
                        #sleep(5)
                        #p_len = bot.get_chat_member_count(grp[3])
                        #send_msg(bot, 281321076, f'{traceback.format_exc()}')
                    if l_len < p_len:
                        proc = init_proc(timer_msg, [grp[3], grp[2]])
                        start_proc(proc)
                        update_db(f"UPDATE groups_tb SET mems='{p_len}' WHERE tid='{grp[3]}'", 'groups_tb')
                    elif l_len > p_len:
                        update_db(f"UPDATE groups_tb SET mems='{p_len}' WHERE tid='{grp[3]}'", 'groups_tb')
        except:
            send_msg(bot, 281321076, '__send_req')
            exc = f'{traceback.format_exc()}'


    bot = TeleBot(TOKEN)

    set_delay(20).seconds.do(_send_req, bot)
        
    while not exc:
        proc_run()
        sleep(1)

    if exc:
        send_msg(bot, 281321076, exc)
#\------------------------------------------------------------------/#
