from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from xml.etree import ElementTree
from token_bot import token

text = ElementTree.parse('text.xml').getroot()
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_base = [
    [
        KeyboardButton(text[0][0][0].text),
        KeyboardButton(text[0][1][0].text),
        KeyboardButton(text[0][2][0].text)
    ],
    [
        KeyboardButton(text[0][3][0].text),
        KeyboardButton(text[0][4][0].text),
        KeyboardButton(text[0][5][0].text),
    ],
    [
        KeyboardButton(text[0][6][0].text),
    ]
]

markup_base = ReplyKeyboardMarkup(kb_base, resize_keyboard=True)


# состояние во время отправки запроса на создание чата
class create_chat(StatesGroup):
    user = State()


@dp.message_handler(commands=['start'])
# /start
async def start(message):
    await message.answer(text[1].text, reply_markup=markup_base)
    await help(message)


# помощь
@dp.message_handler(lambda message: message.text == text[0][3][0].text)
async def help(message: types.Message):
    await message.answer(text[0][3][1].text)


# кнопка чаты
@dp.message_handler(lambda message: message.text == text[0][0][0].text)
async def chat(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=3)
    kb1 = InlineKeyboardButton(text[0][0][1][0][0].text, url=text[0][0][1][0][1].text)
    kb2 = InlineKeyboardButton(text[0][0][1][1][0].text, url=text[0][0][1][1][1].text)
    kb3 = InlineKeyboardButton(text[0][0][1][2][0].text, url=text[0][0][1][2][1].text)
    kb4 = InlineKeyboardButton(text[0][0][1][3][0].text, url=text[0][0][1][3][1].text)
    kb5 = InlineKeyboardButton(text[0][0][1][4][0].text, url=text[0][0][1][4][1].text)
    kb6 = InlineKeyboardButton(text[0][0][1][5][0].text, url=text[0][0][1][5][1].text)
    kb7 = InlineKeyboardButton(text[0][0][1][6][0].text, url=text[0][0][1][6][1].text)
    kb8 = InlineKeyboardButton(text[0][0][1][7][0].text, url=text[0][0][1][7][1].text)
    kb9 = InlineKeyboardButton(text[0][0][1][8][0].text, url=text[0][0][1][8][1].text)
    kb10 = InlineKeyboardButton(text[0][0][1][9][0].text, url=text[0][0][1][9][1].text)
    kb11 = InlineKeyboardButton(text[0][0][1][10][0].text, url=text[0][0][1][10][1].text)
    kb12 = InlineKeyboardButton(text[0][0][1][11][0].text, url=text[0][0][1][11][1].text)
    kb13 = InlineKeyboardButton(text[0][0][3][0].text, callback_data='create')
    markup.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10, kb11, kb12, kb13)
    await message.answer(text[0][0][2].text, reply_markup=markup)


# запрос о создании чата
@dp.callback_query_handler(text="create")
async def create(callback: types.CallbackQuery):
    kb_dell = [[KeyboardButton(text[0][0][3][1][3].text)]]
    markup_dell = ReplyKeyboardMarkup(kb_dell, resize_keyboard=True)
    await callback.message.answer(text[0][0][3][1][0].text, reply_markup=markup_dell)
    await callback.message.delete()
    await create_chat.user.set()


# передача запроса админу
@dp.message_handler(state=create_chat.user)
async def answer_user(message: types.Message, state: FSMContext):
    if message.text == text[0][0][3][1][3].text:
        await state.finish()
        await message.answer(text[0][0][3][1][4].text, reply_markup=markup_base)
        return
    await bot.send_message(-626514804, text[0][0][3][1][2].text.format(user_name=message.from_user.username))
    await message.forward(chat_id=-626514804)
    await message.answer(text[0][0][3][1][1].text, reply_markup=markup_base)
    await state.finish()


# кнопка контакты
@dp.message_handler(lambda message: message.text == text[0][5][0].text)
async def contacts(message: types.Message):
    await message.answer(text[0][5][1].text)


# кнопка BIM-meetap
@dp.message_handler(lambda message: message.text == text[0][6][0].text)
async def meetap(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2)
    kb_what = InlineKeyboardButton(text[0][6][2][0][0].text, callback_data='what')
    kb_purpose = InlineKeyboardButton(text[0][6][2][1][0].text, callback_data='purpose')
    kb_principles = InlineKeyboardButton(text[0][6][2][2][0].text, callback_data='principles')
    kb_meeting = InlineKeyboardButton(text[0][6][2][3][0].text, callback_data='meeting')
    kb_data = InlineKeyboardButton(text[0][6][2][4][0].text, url=text[0][6][2][4][1].text)
    markup.add(kb_what, kb_purpose, kb_principles, kb_meeting, kb_data)
    await message.answer(text[0][6][1].text, reply_markup=markup)


# что такое BIM-meetap
@dp.callback_query_handler(text="what")
async def what(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton(text[0][6][3][2].text, callback_data='thank')
    kb_next = types.InlineKeyboardButton(text[0][6][3][0].text, callback_data='purpose')
    markup_BIM.add(kb_next, kb_thank)
    await callback.message.answer(text[0][6][2][0][1].text, reply_markup=markup_BIM)
    await callback.message.delete()


# цели BIM-meetap
@dp.callback_query_handler(text="purpose")
async def purpose(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton(text[0][6][3][2].text, callback_data='thank')
    kb_next = types.InlineKeyboardButton(text[0][6][3][0].text, callback_data='principles')
    kb_back = types.InlineKeyboardButton(text[0][6][3][1].text, callback_data='what')
    markup_BIM.add(kb_back, kb_next, kb_thank)
    await callback.message.answer(text[0][6][2][1][1].text, reply_markup=markup_BIM)
    await callback.message.delete()


# принципы BIM-meetap
@dp.callback_query_handler(text="principles")
async def principles(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton(text[0][6][3][2].text, callback_data='thank')
    kb_next = types.InlineKeyboardButton(text[0][6][3][0].text, callback_data='meeting')
    kb_back = types.InlineKeyboardButton(text[0][6][3][1].text, callback_data='purpose')
    markup_BIM.add(kb_back, kb_next, kb_thank)
    await callback.message.answer(text[0][6][2][2][1].text, reply_markup=markup_BIM)
    await callback.message.delete()


# как проходят встречи
@dp.callback_query_handler(text="meeting")
async def meeting(callback: types.CallbackQuery):
    markup_BIM = types.InlineKeyboardMarkup()
    kb_thank = types.InlineKeyboardButton(text[0][6][3][2].text, callback_data='thank')
    kb_back = types.InlineKeyboardButton(text[0][6][3][1].text, callback_data='principles')
    markup_BIM.add(kb_back, kb_thank)
    await callback.message.answer(text[0][6][2][3][1].text, reply_markup=markup_BIM)
    await callback.message.delete()


# возврат
@dp.callback_query_handler(text="thank")
async def thank(callback: types.CallbackQuery):
    await meetap(callback.message)
    await callback.message.delete()


# если введены не команды данные
@dp.message_handler(content_types=['text'])
async def create(message: types.Message):
    await message.answer(text[2].text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
