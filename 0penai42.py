import openai
import logging
import aiogram.utils.markdown as md
import sqlite3

from time import sleep
from sqlite3 import Error
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types.message import ContentTypes

logging.basicConfig(level=logging.INFO)

#TEST TOKENS
openai.api_key = "token"
API_TOKEN = 'token' 
PAYMENTS_PROVIDER_TOKEN = 'token'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect('path')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()

conn = sqlite3.connect(r'path')

#GPT PROCESS

def gpt3_completition(prompt, model="text-davinci-003", temperature=0.7, max_tokens=1500):
    promt = prompt.encode(encoding='ASCII', errors = 'ignore').decode()

    response = openai.Completion.create(
        model = model,
        prompt = prompt,
        temperature = temperature,
        max_tokens = max_tokens, 
    )
    text = response['choices'][0]['text'].strip()
    words = text.split()
    global num_words
    num_words = len(words)

    return text

def available_balance(user_id):

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    row = cursor.fetchone()
    column_value = row[1]
    print(column_value)
    cursor.close()

    return column_value


#BUTTONS

button1 = InlineKeyboardButton("Написать сочинение", callback_data="gen")
button2 = InlineKeyboardButton("Профиль", callback_data="prof")
button3 = InlineKeyboardButton("Купить Слова", callback_data="buy")

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button1],
        [button2, button3]
    ]
)

keyboard_words = InlineKeyboardMarkup()
keyboard_words.add(
    InlineKeyboardButton("1000 слов", callback_data = "w1000"),
    InlineKeyboardButton("2800 слов", callback_data = "w2800"),
    InlineKeyboardButton("5000 слов", callback_data = "w5000"),
    InlineKeyboardButton("13500 слов", callback_data = "w13500") 
)

keyboard_back = InlineKeyboardMarkup()
keyboard_back.add(
    InlineKeyboardButton("Назад", callback_data="bk")
)

keyboard_backwords = InlineKeyboardMarkup()
keyboard_backwords.add(
    InlineKeyboardButton("Назад", callback_data="bkwords")
)

keyboard_backdel = InlineKeyboardMarkup()
keyboard_backdel.add(
    InlineKeyboardButton("Назад", callback_data="bkdel")
)

#BOT CODE

class Form(StatesGroup):
    get_user_msg = State() 
    welcome = State()
    amount = State()
    words_amont = State()
    global_user_id = State()
    global_user_name = State()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message, state: FSMContext):

    
    print(message.from_user.id)

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id=?', (message.from_user.id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', '{500}')")
    else:
        print('User exists')
    
    conn.commit()

    await bot.send_message(
        message.from_user.id, 
        text=f"Привет, {message.from_user.first_name}!\n\nНужна помощь со следующим эссе? Просто укажи тему и требования, а я уже сделаю все остальное. \nНаши передовые технологии позволяют нам исследовать, обрисовывать в общих чертах и писать первоклассные эссе с учетом твоих конкретных потребностей.\n\nНажми кнопку 'Написать сочинение' чтобы начать!", 
        reply_markup = keyboard)

@dp.callback_query_handler()
async def generate_text(call: types.CallbackQuery):

    call_user_firstname = call.from_user.first_name
    print(call_user_firstname)
    call_user_id = call.from_user.id
    print(call_user_id)


    #BACKS

    if call.data == "bk":
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

        chat_id = call.message.chat.id
        await bot.send_message( 
            chat_id=chat_id,
            text=f"Привет, {call_user_firstname}!\n\nНужна помощь со следующим эссе? Просто укажи тему и требования, а я уже сделаю все остальное. \nНаши передовые технологии позволяют нам исследовать, обрисовывать в общих чертах и писать первоклассное эссе с учетом твоих конкретных потребностей.", 
            reply_markup = keyboard)

    elif call.data == "bkwords":
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id - 1)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

        chat_id = call.message.chat.id
        await bot.send_message( 
            chat_id=chat_id,
            text=f"Привет, {call_user_firstname}!\n\nНужна помощь со следующим эссе? Просто укажи тему и требования, а я уже сделаю все остальное. \nНаши передовые технологии позволяют нам исследовать, обрисовывать в общих чертах и писать первоклассное эссе с учетом твоих конкретных потребностей.", 
            reply_markup = keyboard)

    elif call.data == "bkdel":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text)
        chat_id = call.message.chat.id
        await bot.send_message( 
            chat_id=chat_id,
            text=f"Привет, {call_user_firstname}!\n\nНужна помощь со следующим эссе? Просто укажи тему и требования, а я уже сделаю все остальное. \nНаши передовые технологии позволяют нам исследовать, обрисовывать в общих чертах и писать первоклассное эссе с учетом твоих конкретных потребностей.", 
            reply_markup = keyboard)
        

    #KEYBOARD BUTTONS

    elif call.data == "gen":

        if int(available_balance(call_user_id)) <= 0:
            await call.message.answer(f"Ваш баланс: {available_balance(call_user_id)} слов. Пополните баланс через кнопку 'Купить Слова' в главном меню. Цены мизерные", reply_markup=keyboard_backwords)
        else:
            await call.message.delete()
            await call.message.answer("""Напиши в этот чат сообщение с твоей темой сочинения и я сразу же начну! 

Вот несколько примеров, если не знаешь с чего начать:
- Izveidot publisko runu pusotras minūtes ilgumā par Latvijas Kultūras kanonu.
- Напиши аргументированное эссе на 200 слов о причине смерти Пушкина. Добавь мнение о том что могло произойти если бы он выжил.
- How does the current animal farm life compare to what Old Major said life should be? Are all of the pigs’ lives suffering and misery?""")
            await Form.get_user_msg.set()

    elif call.data == "prof":
        await call.message.delete()
        await bot.send_message (
            call.message.chat.id, f"Ваш баланс: {available_balance(call_user_id)} слов(а)")
        await bot.send_message (
            call.message.chat.id, f"Сделано с ♥️ из 🇱🇻 этим челом - @vorobjovs. Пиши если заметил баг или есть вопросы", reply_markup = keyboard_backwords)

    elif call.data == "buy":
        await call.message.delete()
        await call.message.answer("Сколько слов хочешь купить? Цены просто мизерные", 
            reply_markup = keyboard_words)

    #BUYING WORDS BUTTONS

    elif call.data == "w1000":
        await call.message.delete()
        await bot.send_invoice(
            call.message.chat.id,
            title="1000 words",
            description="1000 words will be added to your balance",
            payload="1000_words",
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            start_parameter="1000_words",
            currency="USD",
            prices=[types.LabeledPrice(label="1000 words", amount=199)])
            
        await call.message.answer ("1000 words will arrive at your balance immidiately after payment.\nPress'back button after purchase'", 
            reply_markup=keyboard_backwords)
        
    elif call.data == "w2800": 
        await call.message.delete()                    
        await bot.send_invoice(
            call.message.chat.id,
            title="2800 слов",
            description="Пополнене баланса на 2800 слов",
            payload="2800_words",
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            start_parameter="2800_words",
            currency="USD",
            prices=[types.LabeledPrice(label="2800 words", amount=499)])
        await call.message.answer ("2800 слов появятся на твоем балансе в ту же секундку после оплаты инвойса сверху.\nНажми кнопку 'назад' чтобы вернуться в меню", 
            reply_markup=keyboard_backwords)

    elif call.data == "w5000":
        await call.message.delete()
        await bot.send_invoice(
            call.message.chat.id,
            title="5000 слов",
            description="WПополнене баланса на 5000 слов",
            payload="5000_words",
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            start_parameter="5000_words",
            currency="USD",
            prices=[types.LabeledPrice(label="5000 words", amount=799)])
        await call.message.answer ("5000 слов появятся на твоем балансе в ту же секундку после оплаты инвойса сверху.\nНажми кнопку 'назад' чтобы вернуться в меню",
            reply_markup=keyboard_backwords)

    elif call.data == "w13500":
        await call.message.delete()
        await bot.send_invoice(
            call.message.chat.id,
            title="13500 слов",
            description="Пополнене баланса на 13500 слов",
            payload="13500_words",
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            start_parameter="13500_words",
            currency="USD",
            prices=[types.LabeledPrice(label="13500 words", amount=1399)])
        await call.message.answer ("13500 слов появятся на твоем балансе в ту же секундку после оплаты инвойса сверху.\nНажми кнопку 'назад' чтобы вернуться в меню", 
            reply_markup=keyboard_backwords)

@dp.pre_checkout_query_handler(lambda query: True)
async def handle_pre_checkout(query: types.PreCheckoutQuery):

    await bot.answer_pre_checkout_query(
        query.id,
        ok=True,
        )

@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def handle_successful_payment(successful_payment: types.Message):

    # Get the invoice payload from the successful payment message
    invoice_payload = successful_payment.successful_payment.invoice_payload

    cursor = conn.cursor()
    user_id = successful_payment.from_user.id

    # Update the user's balance in the database
    if invoice_payload == "1000_words":
        cursor.execute("UPDATE users SET balance = balance+1000 WHERE user_id = ?", (successful_payment.from_user.id,))
    elif invoice_payload == "2800_words":
        cursor.execute("UPDATE users SET balance=balance+2000 WHERE user_id = ?", (successful_payment.from_user.id,))
    elif invoice_payload == "5000_words":
        cursor.execute("UPDATE users SET balance=balance+2000 WHERE user_id = ?", (successful_payment.from_user.id,))
    elif invoice_payload == "13500_words":
        cursor.execute("UPDATE users SET balance=balance+2000 WHERE user_id = ?", (successful_payment.from_user.id,))

    # Save the changes to the database
    conn.commit()
    
@dp.callback_query_handler()
async def text(message: types.Message):
    message = message.text

@dp.message_handler(state=Form.get_user_msg)
async def setFoto(message: types.Message, state: FSMContext):

    await message.answer("Начинаю писать текст")
    sleep(1)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text="Начинаю писать текст.")
    sleep(1)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text="Начинаю писать текст..")
    sleep(1)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text="Начинаю писать текст...")

    await message.reply(gpt3_completition(message.text))
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id + 1)

    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance=balance-? WHERE user_id = ?", (num_words, message.from_user.id,))
    conn.commit()
    
    await bot.send_message (
        message.chat.id, 
        f"Текст состоит из {num_words} слов. Твой оставшийся баланс: {available_balance(message.from_user.id)} слов(а)", 
        reply_markup = keyboard_backdel)
    await state.finish()


#MAIN CODE
if __name__ == "__main__":
    create_connection(r"path")
    executor.start_polling(dp, skip_updates=True)



