from loader import dp, bot
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline.choice_buttons import *
from keyboards.reply.choice_buttons import *
from utils import TestStates
from data import db
from data.api import activate, qiwi, smshub
from config import ADMIN


lib = globals()["smshub"]
global services
services = lib.smshub
global users
users = {}


@dp.message_handler(Command('start'))  # Начало начал
async def start_command(message):
    db.user_create(message.chat.id)
    await bot.send_message(  
        message.chat.id,  
        'Здравствуй, Повелитель 👑,\n' +  
        'Я бот, созданный для экономии вашего времени🕞 ',
        reply_markup=menu() 
                    )
    await bot.send_message(message.chat.id, 'ВАЖНО!\nЦены в боте не постояны! \nВ любой момент цена на товар может резко упасть или плавно подняться', reply_markup=menu())


@dp.message_handler(Command('cupon'))
async def cupon(message):
    if message.chat.id == ADMIN:
        l = list(map(str, message.text.split()))
        if len(l) != 2:
            await bot.send_message(message.chat.id, "Пожалуйста, отправьте команду по формату /cupon цена")
        else:
            await bot.send_message(message.chat.id, "Купон генерируеться...")
            cupon = db.get_cupon(l[1])
            await bot.send_message(message.chat.id, cupon)


@dp.message_handler(Command('info'))
async def info(message):
    if message.chat.id == ADMIN:
        await bot.send_message(message.chat.id, db.info(), reply_markup=menu())


@dp.message_handler(Command('send'))
async def send(message):
    if message.chat.id == ADMIN:
        await bot.send_message(ADMIN, "Рассылка создана=")
        s = message.text[5:]
        users = db.get_users()
        print(users)
        came = 0
        notcame = 0
        for user in users:
            try:
                await bot.send_message(user, s, reply_markup=tomenu())
                came += 1
                print(1)
            except:
                notcame += 1
        print(came, notcame)
        s = "Данная рассылка дошла до " + str(came) + " пользователей\nНедошла до " + str(notcame) + " пользователей"
        await bot.send_message(ADMIN, s)


@dp.message_handler(Command('admin'))
async def admin(message):
    if message.chat.id == ADMIN:
        await bot.send_message(message.chat.id, "Команды\n/cupon цена - генерация купона\n/info - подробная информация о боте\n/send text - рассылка")


@dp.callback_query_handler(lambda call: call.data.isdigit())
async def check_button(call: CallbackQuery):
    comments = qiwi.get_comments()
    if call.data in list(comments.keys()):
        cash = comments[call.data]
        db.replenishment(call.message.chat.id, cash)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, "Оплата подтверждена")
        s = ""
        try:
            s = "@" + str(call.message.chat.username)
        except:
            try:
                s += call.message.chat.first_name
            except:
                pass
            try:
                s += call.message.chat.last_name
            except:
                pass
        await bot.send_message(ADMIN, "Пополнение на сумму {} руб.\nID: {}\nПользователь: {}".format(cash, call.message.chat.id, s))
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await call.message.answer("Оплата не пришла, попытайтесь снова", reply_markup=cash_check(call.data))


@dp.callback_query_handler(lambda call: call.data == "Закончить")
async def end_number(call: CallbackQuery):
    global users
    number = users[str(call.message.chat.id)]['number']
    number.edit_status(6)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Аренда номера была закончена", reply_markup=menu())


@dp.callback_query_handler(lambda call: call.data == "Ещё смс")
async def end_number(call: CallbackQuery):
    global users
    number = users[str(call.message.chat.id)]['number']
    number.edit_status(3)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer("Ожидайте прихода ещё одного смс", reply_markup=number_end())
    s = await number.get_sms()
    print(s)
    if s == 'Аренда номера была отменена':
        number.edit_status(6)
        await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
    else:
        await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        await call.message.answer("Ваш код: ```" + str(s) + '```\nПожалуйста, выберете одно из предложенных действий', reply_markup=number_sms(), parse_mode="Markdown")


@dp.callback_query_handler(lambda call: call.data == "Отменить")
async def cancel(call: CallbackQuery):
    number = users[str(call.message.chat.id)]['number']
    number.edit_status(8)
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Вы в главном меню', reply_markup=menu())


@dp.callback_query_handler(lambda call: call.data == "В главное меню")
async def gotomenu(call: CallbackQuery):
    await call.message.answer('Вы в главном меню', reply_markup=menu())


@dp.callback_query_handler(lambda call: call.data in services.keys())
async def service_btn(call: CallbackQuery):
    await call.message.answer('Пожалуйста, выберете предпочитаемую подкатегорию', reply_markup=web())
    global users
    choice = call.data
    users[str(call.message.chat.id)] = {'choice': choice}


@dp.callback_query_handler(lambda call: call.data in ['sms-hub', "sms-activate"])
async def get_sms(call: CallbackQuery):
    global users
    choice = users[str(call.message.chat.id)]['choice'] # Определяем переменную choice
    if call.data == 'sms-activate':
        lib = globals()["activate"]
    elif call.data == 'sms-hub':
        lib = globals()["smshub"]
    users[str(call.message.chat.id)]['lib'] = lib
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer('Выберете страну', reply_markup=country_btns(lib, services, choice))


@dp.callback_query_handler(lambda call: call.data in ["Россия", "Украина", "Казахстан"])
async def get_number(call: CallbackQuery):
    global users
    choice = users[str(call.message.chat.id)]['choice'] # Определяем переменную choice
    lib = users[str(call.message.chat.id)]['lib'] # Определяем переменную lib
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    number = lib.Number(services[choice], call.data)
    users[str(call.message.chat.id)]['number'] = number
    price = lib.get_price(services[choice], call.data)
    if price == "Нет в наличии":
        await call.message.answer("Просим прощения, но в наличие нету номеров с заданными параметрами, попробуйте позже, или поменяйте страну, подкатегорию")
    elif str(number) and float(price[::-1][2:][::-1]) <= db.get_balance(call.message.chat.id):
        s = 'Сервис: {}\nНомер:  {}\nОжидайте прихода смс\n\nЕсли в течении 4 минут смс не прийдёт, аренда будет отменена, после деньги, потраченные на аренду данного номера, будут зачислены к вам на счёт'.format(choice, str(number))
        await call.message.answer(s, reply_markup=end_sms())
        s = await number.get_sms()
        print(s)
        if s == 'Аренда номера была отменена':
            number.edit_status(8)
            await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
        else:
            await bot.delete_message(call.message.chat.id, call.message.message_id + 1)
            db.buy(choice, str(number), call.message.chat.id, float(price[::-1][2:][::-1]))
            await call.message.answer("Ваш код: ```" + str(s) + '```\nПожалуйста, выберете одно из предложенных действий', reply_markup=number_sms(), parse_mode="Markdown")

    else:
        try:
            number.edit_status(8)
        except:
            pass
        await call.message.answer("На балансе недостаточно средств", reply_markup=menu())


@dp.message_handler(state=TestStates.TEST_STATE_1)
async def cupon_activate(message: Message):
    s = db.cupon_activate(message.chat.id,  message.text)
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer(s, reply_markup=menu())


@dp.message_handler()
async def echo_message(message: Message):
    s = message.text
    if s == "🔥 Номера":
        await message.answer("Пожалуйста, выберете для каких целей вы хотите арендовать номер", reply_markup=num())
    elif s == "🆘 Правила":
        await message.answer("1. Главное:\n1.1 Мы продаем номера, без инструкций к их использованию. Вся ответственность после покупки номеров только на вас.\n1.2 Если комментарий при оплате был указан неверно, администрация имеет полное право не делать замену\n1.3 Администрация оставляет за собой право вносить любые изменения и дополнения в Правила, без предупреждения!\n1.4 Администрация вправе обнулить ваш лицевой счет.\n\nФОРМА ОБРАЩЕНИЯ\n1) Переписка с ботом + скрины переписки + скрин оплаты\n2) Предоставляйте видеозапись проверки номера с момента покупки в магазине и проверки на офф.сайте сервиса, который купили. Видео должно быть одно и цельное. ( ОБЯЗАТЕЛЬНО ) Отклонения от формы будут игнорироваться!!!", reply_markup=menu())
    elif s == "💰 Баланс":
        b = db.get_balance(message.chat.id)
        s = int(b) if int(b) == float(b) else float(b)
        await message.answer("Ваш баланс: " + str(s) + 'р.', reply_markup=balance())
    elif s == '💩 Помощь':
        await message.answer('Обратитесь к @Iyingien ', reply_markup=menu())
    elif s == "↪ В главное меню ↩":
        await message.answer("Вы в главном меню", reply_markup=menu())
    elif s == "💼 Мой профиль":
        lst = db.get_info(message.chat.id)
        print(lst, sum(lst) / 100)
        await message.answer('id: {}\nКоличество заказов: {}шт. \nСумма всех ваших покупок: {}р.'.format(message.chat.id, len(lst), sum(lst) / 100), reply_markup=menu())
    elif s == '🎁 Купон 🎁':
        await message.answer("Введите купон")
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(TestStates.all()[1])
    elif s == "💣 Пополнить 💣":
        await message.answer("Выберете метод оплаты", reply_markup=method_payment())
    elif s == "↪ В главное меню ↩":
        await message.answer("Вы в главном меню", reply_markup=menu())
    elif message.text == "🥝 Киви":
        comment = db.get_comment()
        await message.answer("➖➖➖➖➖➖➖➖➖➖\nИнформация об оплате\n🥝 QIWI-кошелек: +{}\n📝 Комментарий к переводу: ```{}``` \n➖➖➖➖➖➖➖➖➖➖\n\nВнимание\nПереводите ту сумму, на которую хотите пополнить баланс!\nЗаполняйте номер телефона и комментарий при переводе внимательно!\nАдминистрация не несет ответственности за ошибочный перевод, возврата в данном случае не будет!\nПосле перевода нажмите кнопку 'Проверить оплату'!\n➖➖➖➖➖➖➖➖➖➖".format(qiwi.NUMBER, comment), parse_mode="Markdown", reply_markup=tomenu())
        await message.answer("Нажмите для проверки оплаты", reply_markup=cash_check(comment))
    elif message.text == '↪ В главное меню ↩':
        await message.answer("Вы в главном меню", reply_markup=menu())
    else:
        await message.answer('Воспользуйтесь клавиатурой', reply_markup=menu())