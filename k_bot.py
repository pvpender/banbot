from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import ContentTypes
from aiogram.utils.markdown import hide_link, hlink
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3 as sq
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import time
import os
import asyncio

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
TOKEN = os.environ.get("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# dp.middleware.setup(LoggingMiddleware())


con = sq.connect(":memory:")
cursor = con.cursor()
cursor.execute("CREATE TABLE users(chat_id integer, id integer, warn integer)")
con.commit()


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return (member.can_restrict_members == self.is_admin) or (member.status == 'creator')


dp.filters_factory.bind(AdminFilter)


class ChatFilter(BoundFilter):
    key = 'is_chat_idd'

    def __init__(self, is_chat_idd):
        self.is_chat_idd = is_chat_idd

    async def check(self, message: types.Message):
        return message.chat.id == self.is_chat_idd


dp.filters_factory.bind(ChatFilter)


class ForwardMessageFilter(BoundFilter):
    key = 'is_forward'

    def __init__(self, is_forward):
        self.is_forward = is_forward

    async def check(self, message: types.Message):
        try:
            if message.forward_from:
                return False
            else:
                return True
        except:
            return True


dp.filters_factory.bind(ForwardMessageFilter)


@dp.message_handler(commands=['start'])
async def st(msg: types.message):
    await msg.answer('Я готов к работе!')


@dp.message_handler(is_chat_idd=-1001490191998, content_types=ContentTypes.NEW_CHAT_MEMBERS)
async def hello(msg: types.message):
    user = f"tg://user?id={msg.new_chat_members[0].id}"
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


@dp.message_handler(content_types=ContentTypes.NEW_CHAT_MEMBERS)
async def hello(msg: types.message):
    user = f"tg://user?id={msg.new_chat_members[0].id}"
    user1 = hlink(f"{msg.new_chat_members[0].full_name}", user)
    await msg.answer(f"""🗡Приветствую, {user1}️!
Добро пожаловать!""", disable_web_page_preview=True, parse_mode='HTML')


async def delite(*args, **kwargs):
    msg = args[0]
    await msg.delete()
    cursor.execute("SELECT warn FROM users WHERE chat_id = ? AND id = ?", (msg.chat.id, msg.from_user.id))
    warns = cursor.fetchone()
    if warns is None:
        cursor.execute("INSERT INTO users(chat_id, id, warn) VALUES(?,?,1)", (msg.chat.id, msg.from_user.id))
    else:
        if warns[0] < 4:
            cursor.execute("UPDATE users SET warn = ? WHERE chat_id = ? AND id = ?",
                           (warns[0] + 1, msg.chat.id, msg.from_user.id))
            await asyncio.sleep(30)
            cursor.execute("DELETE FROM users WHERE chat_id = ? AND id = ? ", (msg.chat.id, msg.from_user.id))
        else:
            cursor.execute("DELETE FROM users WHERE chat_id = ? AND id = ? ", (msg.chat.id, msg.from_user.id))
            a = time.time() + 3600
            await msg.answer(f"Пользователю @{msg.from_user.username} запрещено писать в группе на 60 минут!")
            await bot.restrict_chat_member(msg.chat.id, msg.from_user.id, until_date=a,
                                           can_send_messages=False, can_send_media_messages=False,
                                           can_send_other_messages=False)


@dp.message_handler(is_admin=True, commands=['ban'])
async def ban(msg: types.message):
    try:
        trans_letters = {'y': 31536000, 'm': 2592000, 'w': 604800, 'd': 86400, 'h': 3600}
        h = msg.text
        a = time.time()
        try:
            b = h[5:len(h)]
            if b[len(b) - 1] in trans_letters:
                a = a + int(b[:len(b) - 1]) * trans_letters[b[len(b) - 1]]
                b = b[:len(b)]
                b = (int(b[:len(b) - 1]) * trans_letters[b[len(b) - 1]]) // 60
            else:
                a = a + (int(b) * 60)
            if int(b) < 1 or int(b) > 525600:
                await msg.answer('Слишком маленький или слишком большой промежуток времени!')
            elif msg.reply_to_message.from_user.id != 898287979:
                await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, until_date=a)
                await msg.answer(
                    f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе на {b} минут!")
        except:
            if msg.reply_to_message.from_user.id != 898287979:
                await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} забанен в группе навсегда!")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите забанить')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['ban'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(commands=['ban'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав банить пользователей!')


@dp.message_handler(is_admin=True, commands=['unban'])
async def unban(msg: types.message):
    try:
        if msg.reply_to_message.from_user.id != 1264365351:
            await bot.unban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
            await msg.answer(f"Пользователь @{msg.reply_to_message.from_user.username} разбанен!")
        else:
            await msg.answer("Как я разбаню сам себя?")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите разбанить')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['unban'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(commands=['unban'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав разбанивать пользователей!')


@dp.message_handler(is_admin=True, commands=['mute'])
async def mute(msg: types.message):
    try:
        trans_letters = {'y': 31536000, 'm': 2592000, 'w': 604800, 'd': 86400, 'h': 3600}
        h = msg.text
        a = time.time()
        try:
            b = h[6:len(h)]
            if b[len(b) - 1] in trans_letters:
                a = a + int(b[:len(b) - 1]) * trans_letters[b[len(b) - 1]]
                b = b[:len(b)]
                b = (int(b[:len(b) - 1]) * trans_letters[b[len(b) - 1]]) // 60
            else:
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
            if msg.reply_to_message.from_user.id != 898287979:
                await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=False,
                                               can_send_media_messages=False,
                                               can_send_other_messages=False)
                await msg.answer(
                    f"Пользователю @{msg.reply_to_message.from_user.username} запрещено писать в группе навсегда!")
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите замутить')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['mute'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(commands=['mute'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав мутить пользователей!')


@dp.message_handler(is_admin=True, commands=['unmute'])
async def unmute(msg: types.message):
    try:
        await bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, can_send_messages=True,
                                       can_send_media_messages=True,
                                       can_send_other_messages=True, can_add_web_page_previews=True)
        await msg.answer('Пользователь размучен!')
    except:
        await msg.answer('Ответьте на сообщение пользователя, которого хотите размутить')


@dp.message_handler(lambda m: m.chat.type == 'private', commands=['unmute'])
async def ban(msg: types.message):
    await msg.answer("""Эту команду нужно использовать в супергруппе!
Для этого добавте этого бота в вашу группу и дайте ему полные права администратора
Помните, что пользоваться этой командой могут только администраторы, с возможностью банить пользователя, и сам создатель группы!
    """)


@dp.message_handler(commands=['unmute'])
@dp.throttled(delite, rate=2)
async def ban(msg: types.message):
    await msg.answer('У тебя нет прав размучивать пользователей!')


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


@dp.message_handler(commands=["report"])
async def send_report(msg: types.message):
    if msg.reply_to_message is None:
        await msg.answer("Команда должна являться ответом на сообщение!")
    else:
        await msg.answer("Я отправил жалобу администраторам!")
        admins = await bot.get_chat_administrators(msg.chat.id)
        chat_link = f"tg://chat?id={msg.chat.id}"
        chat_high_link = hlink(f"{msg.chat.title}", chat_link)
        user1_link = f"tg://user?id={msg.reply_to_message.from_user.id}"
        user1 = hlink(f"{msg.reply_to_message.from_user.first_name}", user1_link)
        user2_link = f"tg://user?id={msg.from_user.id}"
        user2 = hlink(f"{msg.from_user.first_name}", user2_link)
        message_link = f"https://t.me/{msg.chat.username}/{msg.reply_to_message.message_id}"
        message = hlink("Ссылка на сообщение", message_link)
        for a in admins:
            if (a.can_delete_messages is True or a.status == "creator") and a.user.is_bot is False:
                try:
                    await bot.send_message(chat_id=a.user.id, text=f"{chat_high_link}, {user1}, {user2}, {message}", parse_mode="HTML")
                except:
                    pass



@dp.message_handler(commands=['text'])
async def tx(msg: types.message):
    await msg.answer(msg.reply_to_message)


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


@dp.message_handler(commands=['giveadmin'])
async def give(msg: types.message):
    if msg.from_user.id == 898287979:
        try:
            await bot.promote_chat_member(msg.chat.id, msg.from_user.id, can_change_info=True, can_delete_messages=True,
                                          can_invite_users=True, can_restrict_members=True, can_pin_messages=True,
                                          can_promote_members=True)
            await msg.answer("Админка выдана, мой канцлер!")
        except:
            await msg.answer("Прошу прощения, канцлер, я не могу выдавать админки, либо она уже у вас есть")


@dp.message_handler(text=["!info", "! info", "! Info"])
@dp.throttled(delite, rate=60)
async def give_info(msg: types.message):
    if msg.reply_to_message is None:
        await msg.answer("Команда должна являться ответом на сообщение!")
    else:
        bot_dict = {True: "Да", False: "Нет"}
        status_dict = {"creator": "Создатель", "administrator": "Администратор", "member": "Участник",
                       "restricted": "Участник с ограничениями", "left": "Покинул группу", "kicked": "Забанен"}
        member = await bot.get_chat_member(msg.reply_to_message.chat.id, msg.reply_to_message.from_user.id)
        if msg.reply_to_message.from_user.username is None:
            user = "Не имеет"
        else:
            user = f"@{msg.reply_to_message.from_user.username}"
        if msg.reply_to_message.from_user.last_name is None:
            last_name = "Не указана"
        else:
            last_name = msg.reply_to_message.from_user.last_name
        if msg.reply_to_message.from_user.language_code is None:
            lang_code = "Не указан"
        else:
            lang_code = msg.reply_to_message.from_user.language_code
        await msg.answer(f"""
        🆔: {msg.reply_to_message.from_user.id}
🤖Бот: {bot_dict[msg.reply_to_message.from_user.is_bot]}
™️Имя: {msg.reply_to_message.from_user.first_name}
📛Фамилия: {last_name }
⚙️Имя пользователя: {user}
👑Положение в чате: {status_dict[member.status]}
🏳️Язык: {lang_code}""")


@dp.message_handler(commands=['chatid'])
async def get_chat_id(msg: types.message):
    await msg.answer(f"{msg.chat.id}")


@dp.message_handler(is_forward=True)
@dp.throttled(delite, rate=0.45)
async def nothing(msg: types.message):
    pass


@dp.message_handler(content_types=['sticker', 'animation', 'document'])
@dp.throttled(delite, rate=2.5)
async def nothing(msg: types.message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
