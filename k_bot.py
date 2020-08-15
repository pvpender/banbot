from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ContentTypes
from aiogram.utils.markdown import hide_link, hlink
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


# dp.middleware.setup(LoggingMiddleware())


class CheckFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return ((member.can_restrict_members == self.is_admin) or (member.status == 'creator')) and \
               (member.is_chat_admin() is True or member.is_chat_admin() is None)


dp.filters_factory.bind(CheckFilter)


class CheckFilter(BoundFilter):
    key = 'chat_id'

    def __init__(self, chat_id):
        self.chat_id = chat_id

    async def check(self, message: types.Message):
        return message.chat.id == self.chat_id


dp.filters_factory.bind(CheckFilter)


class CheckFilter(BoundFilter):
    key = 'is_chat_idd'

    def __init__(self, is_chat_idd):
        self.is_chat_idd = is_chat_idd

    async def check(self, message: types.Message):
        return message.chat.id == self.is_chat_idd


dp.filters_factory.bind(CheckFilter)


@dp.message_handler(commands=['start'])
async def st(msg: types.message):
    await msg.answer('Я готов к работе!')


@dp.message_handler(is_chat_idd=-1001490191998, content_types=ContentTypes.NEW_CHAT_MEMBERS)
async def hello(msg: types.message):
    user = f"https://t.me/{msg.new_chat_members[0].username}"
    user1 = hlink(f"{msg.new_chat_members[0].full_name}", user)
    gip = hlink("правилами", "https://telegra.ph/Prpvila-G%C3%98T-Mafia-07-24")
    chat = hlink("Ссылка на чат", "https://t.me/mafgot")
    chat1 = hlink("Чат Family GØT", "https://t.me/bsgot")
    await msg.answer(f"""🗡Приветствую, {user1}️!

🔫Ты попал в чат любителей игры
Мафия,располагайся)

‼️Перед началом игры,ознокомься с базовыми знаниями игры,а  также нашими правилами {gip}‼️

🔫{chat}
🐉{chat1}""", disable_web_page_preview=True, parse_mode='HTML')


@dp.message_handler(is_chat_idd=-1001279094011, content_types=ContentTypes.NEW_CHAT_MEMBERS)
async def hello(msg: types.message):
    user = f"https://t.me/{msg.new_chat_members[0].username}"
    user1 = hlink(f"{msg.new_chat_members[0].full_name}", user)
    await msg.answer(f"""🗡Приветствую, {user1}️!
Добро пожаловать!""", disable_web_page_preview=True, parse_mode='HTML')


async def delite(*args, **kwargs):
    msg = args[0]
    await msg.delete()


@dp.message_handler(is_admin=True, commands=['ban'])
async def ban(msg: types.message):
    try:
        h = msg.text
        a = time.time()
        try:
            b = h[5:len(h)]
            a = a + (int(b) * 60)
            if int(b) < 1 or int(b) > 525600:
                await msg.answer('Слишком маленький или слишком большой промежуток времени!')
            elif msg.reply_to_message.from_user.id != 898287979:
                await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a)
                await msg.answer(
                    f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе на {b} минут!")
        except:
            await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
            await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе навсегда!")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите забанить')


@dp.message_handler(is_admin=False, commands=['ban'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав банить пользователей!')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['ban'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(is_admin=True, commands=['unban'])
async def unban(msg: types.message):
    try:
        await bot.unban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
        await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} разбанен!")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите разбанить')


@dp.message_handler(is_admin=False, commands=['unban'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав разбанивать пользователей!')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['unban'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(is_admin=True, commands=['mute'])
async def mute(msg: types.message):
    try:
        h = msg.text
        a = time.time()
        try:
            b = h[6:len(h)]
            a = a + (int(b) * 60)
            if int(b) < 1 or int(b) > 525600:
                await msg.answer('Слишком маленький или слишком большой промежуток времени!')
            elif msg.reply_to_message.from_user.id != 898287979:
                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a,
                                               can_send_messages=False, can_send_media_messages=False,
                                               can_send_other_messages=False)
                await msg.answer(
                    f"Пользователю @{msg.reply_to_message.from_user.username} запрещено писать в группе на {int(b)} минут!")
        except:
            await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=False,
                                           can_send_media_messages=False,
                                           can_send_other_messages=False)
            await msg.answer(
                f"Пользователю @{msg.reply_to_message.from_user.username} запрещено писать в группе навсегда!")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите замутить')


@dp.message_handler(is_admin=False, commands=['mute'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав мутить пользователей!')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['mute'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(is_admin=True, commands=['unmute'])
async def unmute(msg: types.message):
    try:
        await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=True,
                                       can_send_media_messages=True,
                                       can_send_other_messages=True, can_add_web_page_previews=True)
        await msg.answer('Пользователь размучен!')
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите размутить')


@dp.message_handler(is_admin=False, commands=['unmute'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав размучивать пользователей!')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['unmute'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(is_chat_idd=-1001490191998, commands=['report'])
async def report(msg: types.message):
    if msg.reply_to_message:
        text = msg.text
        if len(text) > 7:
            why = text[7:len(text)]
        else:
            why = 'Причина не указана'
        link = f"https://t.me/{msg.chat.username}/{msg.reply_to_message.message_id}"
        await msg.answer('Жалоба на пользователя отправлена!')
        await bot.send_message(-1001389125426, text=f"""Новая жалоба от @{msg.from_user.username}!
Жалоба на сообщение пользователя: @{msg.reply_to_message.from_user.username}
Текст сообщения: {msg.reply_to_message.text}
Причина жалобы: {why}
Ссылка на сообщение: {link}
""", disable_web_page_preview=True)
        await bot.send_message(-1001283141945, text=f"""Новая жалоба от @{msg.from_user.username}!
Жалоба на сообщение пользователя: @{msg.reply_to_message.from_user.username}
Текст сообщения: {msg.reply_to_message.text}
Причина жалобы: {why}
Ссылка на сообщение: {link}
""", disable_web_page_preview=True)
    else:
        await msg.answer('Ответьте на сообщение пользователя на которого хотите пожаловаться')


@dp.message_handler(commands=['help'])
async def help(msg: types.message):
    await msg.answer("""
    Привет! Я бан-бот! 
Нужно кого-нибудь забанить?
Не вопрос!
Добавте меня в чат и дайте права администратора!
Сделано PVPender
/help - помощь
/ban - Забанить пользователя на x минут(Если аргумента нет - навсегда)
/unban - Разбанить пользователя
/mute - Замутить пользователя на x минут(Если аргумента нет - навсегда)
/unmute - Размутить пользователя""")


@dp.message_handler(commands=['chatid'])
async def get_chat_id(msg: types.message):
    await msg.answer(f"{msg.chat.id}")


@dp.message_handler()
@dp.throttled(delite, rate=0.45)
async def nothing(msg: types.message):
    print('')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
