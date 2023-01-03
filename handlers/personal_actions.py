from aiogram import types
from dispatcher import dp
import re
import config
from bot import BotDB


@dp.message_handler(commands='start')
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    else:
        BotDB.get_user_id(message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")

@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.bot.send_message(message.from_user.id, '''Список команд:\n\n/spent + сумма - добавить расход
/earn + сумма - добавить доход\n/history - история операций
    ''')

@dp.message_handler(commands=('spent', 's', 'earned', 'e'), commands_prefix='!/')
async def record(message: types.Message):
    cmd_variants = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if len(value):
        x = re.findall(r'\d+(?:.\d+)?', value)
        if len(x):
            value = float(x[0].replace(',', '.'))
            BotDB.add_record(message.from_user.id, operation, value)
            if operation == '-':
                await message.reply('✔ Запись о <u><b>расходе</b></u> успешно добавлена!')
            else:
                await message.reply('✔ Запись о <u><b>доходе</b></u> успешно добавлена!')
        else:
            await message.reply("Не удалось определить сумму!")

    else:
        await message.reply('Не введена сумма!')

@dp.message_handler(commands=('history', 'h'), commands_prefix='!/')
async def record(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        'day': ('today', 'day', 'сегодня', 'день'),
        'week': ('week', 'неделя'),
        'month': ('month', 'месяц'),
        'year': ('year', 'год')
    }
    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()
    
    within = 'day'
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k

    records = BotDB.get_records(message.from_user.id, within)

    if len(records):
        answer = f"⏱ История операций за {within_als[within][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            answer += f'- {r[3]}'
            answer += f'<i>({r[4]})</i>\n'

        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")
    