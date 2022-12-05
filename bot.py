from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from xml.etree import ElementTree

text = ElementTree.parse('text.xml').getroot()
token = ElementTree.parse('token.xml').getroot()
bot = Bot(token.text)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_base = [
    [
        KeyboardButton(root[0].text),
        KeyboardButton('Поиск исполнителя'),
        KeyboardButton('Профиль')
    ],
    [
        KeyboardButton('Помощь'),
        KeyboardButton('Информация о человеке'),
        KeyboardButton('Контакты'),
    ],
    [
        KeyboardButton('BIM-meetap'),
    ]
]

kb_dell = [[KeyboardButton('Назад')]]
markup_base = ReplyKeyboardMarkup(kb_base, resize_keyboard=True)
markup_dell = ReplyKeyboardMarkup(kb_dell, resize_keyboard=True)


class create_chat(StatesGroup):
    user = State()


@dp.message_handler(commands=['start'])
# /start
async def start(message):
    await message.answer('Привет! \nДобро пожаловать в неформальное сообщество бим сферы!\nПозволь мне ввести тебя в '
                         'курс дела и рассказать, что тут  у нас происходит :)', parse_mode='html',
                         reply_markup=markup_base)
    await help(message)


# помощь
@dp.message_handler(lambda message: message.text == "Помощь")
async def help(message: types.Message):
    await message.answer("Я что-то умею", parse_mode='html')


# кнопка чаты
@dp.message_handler(lambda message: message.text == "Чаты")
async def chat(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=3)
    kb1 = InlineKeyboardButton("Москва", url='https://t.me/bimbeermeetup')
    kb2 = InlineKeyboardButton("Санкт-Петербург", url='https://t.me/bimbeermeetupspb')
    kb3 = InlineKeyboardButton("Нижний-Новгород", url='https://t.me/bimbeermeetupnnovgorod')
    kb4 = InlineKeyboardButton("Краснодар", url='https://t.me/RnD_BIM_Beer_Tea')
    kb5 = InlineKeyboardButton("Ростов-на-Дону", url='https://t.me/bimbeermeetupkrasnodar')
    kb6 = InlineKeyboardButton("Казань", url='https://t.me/bimbeermeetupkazan')
    kb7 = InlineKeyboardButton("Сочи", url='https://t.me/bimbeermeetupsochi')
    kb8 = InlineKeyboardButton("Пермь", url='https://t.me/bimbeermeetupperm')
    kb9 = InlineKeyboardButton("Красноярск", url='https://t.me/bimbeermeetupkrasno')
    kb10 = InlineKeyboardButton("Екатеренбург", url='https://t.me/bimbeermeetupekb')
    kb11 = InlineKeyboardButton("Минск", url='https://t.me/bimbeermeetupminsk')
    kb12 = InlineKeyboardButton("Тюмень", url='https://t.me/bimbeermeetuptyumen')
    kb13 = InlineKeyboardButton('Хочу создать чат по своему городу!', callback_data='create')
    markup.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10, kb11, kb12, kb13)
    await message.answer("Города:", parse_mode='html', reply_markup=markup)


# запрос о создании чата
@dp.callback_query_handler(text="create")
async def create(callback: types.CallbackQuery):
    await callback.message.answer('Опиши, пожалуйста, почему тебе это интересно?\nОтправь мне свое сообщение,'
                                  '\nЯ передам твое желание организатором и они с тобой свяжутся.\nСпасибо за '
                                  'проявленный интерес!!', parse_mode='html', reply_markup=markup_dell)
    await callback.message.delete()
    await create_chat.user.set()


# передача запроса админу
@dp.message_handler(state=create_chat.user)
async def answer_user(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await message.answer('Вы передумали? Жаль', parse_mode='html', reply_markup=markup_base)
        return
    await bot.send_message(-626514804, 'Запрос на создание чата: @{user_name}'.format
    (user_name=message.from_user.username), parse_mode='html')
    await message.forward(chat_id=-626514804)
    await message.answer('Спасибо за проявленный интерес! Я передал ваше сообщение администратору.', parse_mode='html',
                         reply_markup=markup_base)
    await state.finish()


# кнопка контакты
@dp.message_handler(lambda message: message.text == "Контакты")
async def contacts(message: types.Message):
    await message.answer('Ну здесь типо есть главные. Но их контактов пока нет, а может их просто нет, я не знаю',
                         parse_mode='html')


# кнопка BIM-meetap
@dp.message_handler(lambda message: message.text == "BIM-meetap")
async def meetap(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    kb_what = InlineKeyboardButton('Что такое BIM-meetap?', callback_data='what')
    kb_purpose = InlineKeyboardButton('Цели BIM-meetap', callback_data='purpose')
    kb_data = InlineKeyboardButton('Расписание', url='https://calendar.google.com/calendar/u/0?cid'
                                                     '=MWM1OWNiY2M3YTkyNWNmYmFiZjIyMzllYWVlZTNhZGY'
                                                     'xMDhjNjRiMjgyZmE0YWFhOTFhYmNmZTEwMjkzOTY4M0B'
                                                     'ncm91cC5jYWxlbmRhci5nb29nbGUuY29t')
    kb_principles = InlineKeyboardButton('Принципы BIM-meetup', callback_data='principles')
    kb_meeting = InlineKeyboardButton('Как проходят встречи', callback_data='meeting')
    markup.add(kb_what, kb_purpose, kb_principles, kb_meeting, kb_data)
    await message.answer('Meet Up - Встреча людей со схожими интересами в очном режиме. Здесь ты можешь узнать всю '
                         'интересующую тебя информацию', parse_mode='html', reply_markup=markup)


# что такое BIM-meetap
@dp.callback_query_handler(text="what")
async def what(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton('Всё. Спасибо!', callback_data='thank')
    kb_next = types.InlineKeyboardButton('Далее', callback_data='purpose')
    markup_BIM.add(kb_next, kb_thank)
    await callback.message.answer('Что такое BIM-meetap\nMeet Up - Встреча людей со схожими интересами в очном '
                                  'режиме.\nНаше сообщество BIM-meetup занимается\n• Для людей из сферы '
                                  'проектирования и строительства.\n• Людей, уже работающих с BIM технологиями, '
                                  'или пока только наблюдающих за ними.\n• Нетворкинг и общение в теплой, '
                                  'дружеской атмосфере.\n• Отдых и релакс после тяжелых трудовых будней. Можно выпить '
                                  'и поесть (по желанию).\n• Повод съездить в другой город и встретиться с '
                                  'коллегами.', parse_mode='html', reply_markup=markup_BIM)
    await callback.message.delete()


# цели BIM-meetap
@dp.callback_query_handler(text="purpose")
async def purpose(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton('Всё. Спасибо!', callback_data='thank')
    kb_next = types.InlineKeyboardButton('Далее', callback_data='principles')
    kb_back = types.InlineKeyboardButton('Назад', callback_data='what')
    markup_BIM.add(kb_back, kb_next, kb_thank)
    await callback.message.answer('Цели BIM-meetap\n• Отдых. Возможность выпить с коллегами\n• Неформальное общение. '
                                  'Создание среды, где можно собраться в неформальной обстановке и обсудить проблемы '
                                  'насущные и просто неплохо провести время. Помочь профессиональному сообществу '
                                  'реализовать неформальную коммуникацию\n• Свобода слова. Можно честно высказывать '
                                  'свои мысли. Давать честную обратную связь о том, что где и как работает. Дать '
                                  'возможность людям видеть реальную картину.\nПиджаков и галстуков хватает на '
                                  'конференциях, вещающих, что все везде хорошо и работает, на неформальной же '
                                  'встрече можно обсудить все так, как оно есть :) Ценно получить объективный взгляд '
                                  'на отрасль в целом, понять куда дует ветер, но без прикрас, без купюр.\n• '
                                  'Нетворкинг. Организация площадки для общения людей разного уровня, '
                                  'разных направлений, но объединенных одной сферой BIM. Обретение новых полезных '
                                  'связей.\nДать людям возможность пообщаться вживую, поделиться опытом, обзавестись '
                                  'новыми знакомствами, найти решение своих проблем. Обмен информацией о технологии, '
                                  'тенденциях и пр. Добавить больше нетворкинга в профессиональную среду.\n• Создать '
                                  'позитивную атмосферу, которая притягивает и располагает людей к обществу своей '
                                  'профессии. Создать положительную ассоциацию. Показать, что можно быть счастливым, '
                                  'занимаясь. За счет позитива и заинтересованности - привлечение новых '
                                  'специалистов\n• Объединение BIM (ТИМ) сообщества. Развитие Бима в каждом отдельном '
                                  'городе. Координация информации между городами. Повышение информированности, '
                                  'компетентности, кругозора специалистов. Идея: Мы все в одной лодке и трудимся на '
                                  'одну цель и благо', parse_mode='html', reply_markup=markup_BIM)
    await callback.message.delete()


# принципы BIM-meetap
@dp.callback_query_handler(text="principles")
async def principles(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton('Всё. Спасибо!', callback_data='thank')
    kb_next = types.InlineKeyboardButton('Далее', callback_data='meeting')
    kb_back = types.InlineKeyboardButton('Назад', callback_data='purpose')
    markup_BIM.add(kb_back, kb_next, kb_thank)
    await callback.message.answer('Принципы BIM-meetap\n• Открытые встречи. Может прийти любой желающий, связанный с '
                                  'темой проектирования и строительства. Не замыкаться в свою закрытую компанию.\n• '
                                  'Неформальная обстановка. Свободное обсуждение. Возможность расслабиться. Это '
                                  'располагает к теме и привлекает больше людей.\n• Важно, чтобы встреча не '
                                  'переходила в банальную пьянку, но сохранялось неформальное общение. И приносила '
                                  'пользу, но не становилась масштабным официальным мероприятием с пиджаками и '
                                  'галстуками\n• Соблюдение нейтралитета. У нас собираются представители разных '
                                  'компаний. Важен разносторонний подход, честная обратная связь. Не допускается '
                                  'реклама. Не учитываются интересы конкретно выделенных компаний. По изначальной '
                                  'задумке никаким спонсорам тут места нет и не было. Можно только высказывать свое '
                                  'мнение. Нельзя допускать непосредственного влияния и лоббизма вендоров. Нельзя '
                                  'допускать вражды между собой и конкуренции.\n• Ориентированность на расширение '
                                  'круга специалистов, привлечение новых, молодых людей, взаимодействие преимуществ '
                                  'специалистов с разным опытом (большим и маленьким), обмен информацией, находками, '
                                  'мыслями, идеями.\n• Нельзя допускать политических публичных обсуждений. Это '
                                  'профессиональное сообщество вне политики.', parse_mode='html',
                                  reply_markup=markup_BIM)
    await callback.message.delete()


# как проходят встречи
@dp.callback_query_handler(text="meeting")
async def meeting(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton('Всё. Спасибо!', callback_data='thank')
    kb_back = types.InlineKeyboardButton('Назад', callback_data='principles')
    markup_BIM.add(kb_back, kb_thank)
    await callback.message.answer('Как проходят встречи\n• Некоторые встречи происходят организованно, некоторые '
                                  'спонтанные и формируются стихийно по приглашению активных людей напрямую в чате. '
                                  'Как правило, встречи не привязываются к каким-то особым событиям, '
                                  'но можно собираться после различных мероприятий .\n• За встречи более 10 человек '
                                  'отвечают организаторы.\n• Малые мероприятия можно собрать автономно. В любой '
                                  'момент можно договориться встретиться в чате.\n• Каждый платит за себя сам. '
                                  'Выпивку приносим свою (можно захватить вкусняшки). Если берется в аренду лофт, '
                                  'нужно рассчитывать на одну-две тысячи рублей (вместе с едой). Безвозмездное '
                                  'спонсорство приветствуется! :)\n• В начале встречи знакомимся с коллегами. Каждый '
                                  'представляется по очереди. Таким образом происходят первые вбросы обсуждаемых  тем '
                                  'и можно присмотреться с кем хотелось бы пообщаться.\n• Дальше все развивается '
                                  'стихийно. Обычно люди разбиваются на небольшие группки по 3-5 человек и говорят об '
                                  'интересных им темах. Потом периодически тасуются между собой.', parse_mode='html',
                                  reply_markup=markup_BIM)
    await callback.message.delete()


# возврат
@dp.callback_query_handler(text="thank")
async def thank(callback: types.CallbackQuery):
    await meetap(callback.message)
    await callback.message.delete()


# если введены не команды данные
@dp.message_handler(content_types=['text'])
async def create(message: types.Message):
    await message.answer('Я не понимаю о чём ты', parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
