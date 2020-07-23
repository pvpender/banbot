from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import time

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
TOKEN = '1264365351:AAH38ocd1resSc_MyQyHLTNjlFUw3hbp4iI'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands= ['start'])
async def st(msg: types.message):
    await msg.answer('Я готов к работе!')

@dp.message_handler(is_chat_admin = True,commands=['ban'])
async def ban(msg: types.message):
    try:
        h = msg.text
        a = time.time()
        try:
            b = h[6:len(h)]
            a = a + int(b)
            if int(b)<32 or int(b) >1314000:
                await msg.answer('Слишком маленький или слишком большой промежуток времени!')
            else:
                await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a)
                await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе на {b} секунд!")
        except:
             await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
             await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе навсегда!")
    except :
        await msg.answer('Ответьте на сообщение пользователя, которого хотите забанить')

'''@dp.message_handler(is_chat_admin = False ,commands=['ban'])
async def ban1(msg: types.message):
    a = time.time()
    a = a + 31
    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a,
                                   can_send_messages=False, can_send_media_messages=False,
                                   can_send_other_messages=False)
    await msg.answer(f"Пользователь @{msg.from_user.username} замучен на 30 секунд! Причина: Тебе не давали права пользоваться ботом!")'''

@dp.message_handler(is_chat_admin = True,commands=['unban'])
async def unban(msg: types.message):
    try:
        await bot.unban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите разбанить')

'''@dp.message_handler(is_chat_admin = False ,commands=['unban'])
async def unban1(msg: types.message):
    a = time.time()
    a = a + 31
    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a,
                                   can_send_messages=False, can_send_media_messages=False,
                                   can_send_other_messages=False)
    await msg.answer(f"Пользователь @{msg.from_user.username} замучен на 30 секунд! Причина: Тебе не давали права пользоваться ботом!")'''

@dp.message_handler(is_chat_admin = True,commands=['mute'])
async def mute(msg: types.message):
   try:
        h = msg.text
        a = time.time()
        try:
            b = h[6:len(h)]
            a = a + int(b)
            if int(b) < 32 or int(b) > 1314000:
                await msg.answer('Слишком маленький или слишком большой промежуток времени!')
            else:
                  await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a, can_send_messages=False, can_send_media_messages=False,
                                                   can_send_other_messages=False)
                  await msg.answer (f"Пользователю @{msg.reply_to_message.from_user.username} запрещено писать в группе на {int(b)} секунд!")
        except:
            await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=False, can_send_media_messages=False,
                                           can_send_other_messages=False)
            await msg.answer(
                f"Пользователю @{msg.reply_to_message.from_user.username} запрещено писать в группе навсегда!")
   except:
       await msg.answer('Ответьте на сообщение пользователя, которого хотите замутить')

'''@dp.message_handler(is_chat_admin = False ,commands=['mute'])
async def mute1(msg: types.message):
    a = time.time()
    a = a + 30
    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a,
                                   can_send_messages=False, can_send_media_messages=False,
                                   can_send_other_messages=False)
    await msg.answer(f"Пользователь @{msg.from_user.username} замучен на 30 секунд! Причина: Тебе не давали права пользоваться ботом!")'''

@dp.message_handler(is_chat_admin = True,commands=['unmute'])
async def unmute(msg: types.message):
    try:
         await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=True, can_send_media_messages=True,
                                        can_send_other_messages=True,can_add_web_page_previews=True)
         await msg.answer('Пользователь размучен!')
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите размутить')


'''@dp.message_handler(is_chat_admin = True ,commands=['unmute'])
async def unmute1(msg: types.message):
    a = time.time()
    a = a + 30
    await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a,
                                   can_send_messages=False, can_send_media_messages=False,
                                   can_send_other_messages=False)
    await msg.answer(f"Пользователь @{msg.from_user.username} замучен на 30 секунд! Причина: Тебе не давали права пользоваться ботом!")'''

@dp.message_handler(commands=['help'])
async def help(msg: types.message):
    await msg.answer("""
    Привет! Я бан-бот! 
Нужно кого-нибудь забанить?
Не вопрос!
Добавте меня в чат и дайте права администратора!
Сделано PVPender
/help - помощь
/ban - Забанить пользователя на x секунд(Если аргумента нет - навсегда)
/unban - Разбанить пользователя
/mute - Замутить пользователя на x секунд(Если аргумента нет - навсегда)
/unmute - Размутить пользователя""")


async def delite(*args, **kwargs):
    msg = args[0]
    await msg.delete()


@dp.message_handler()
@dp.throttled(delite,rate=0.45)
async def nothing(msg: types.message):
    print('')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
