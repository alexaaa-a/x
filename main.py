import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
import random

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6327333086:AAFdVJxe0Sy9TAQgGDDiTVILHdt9tcr2E74",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll =  "Хочу рассказать о себе" # Можно менять текст
text_button_1 = "Случайный факт"  # Можно менять текст
text_button_2 = "Комплимент"  # Можно менять текст
text_button_3 = "Анекдот"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Доброго врменени! Чем могу быть полезен?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Хорошо! Для начала: как Вас зовут?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Красивое имя! А сколько Вам лет?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Думаю, пока хватит. Спасибо, что поделились!', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)



@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    facts = ['Ежедневно 60 человек становятся миллионерами.',
         'Корова может подняться по лестнице, но не может спуститься.',
         'Шесть месяцев жизни человек проводит, стоя перед красным сигналом светофора.',
         'Кетчуп вытекает из бутылки со скоростью 30 километров в год.',
         'Объём Луны равен объёму воды в Тихом океане.']
    bot.send_message(message.chat.id, str(random.choice(facts)), reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Вы очень необычный и уникальный человек :)", reply_markup=menu_keyboard)  # Можно менять текст


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Штирлиц долго смотрел в одну точку. Потом в другую. "Двоеточие!" - наконец-то смекнул Штирлиц.', reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()