# coding: utf-8
import time

import settings
from bot_ms.mail import Mail
from .models import BotUser
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

bot = TeleBot(settings.BOT_TOKEN)


class Keyboard(ReplyKeyboardMarkup):
    def __init__(self, resize: bool = True, text: list = None):
        super().__init__()
        self.resize_keyboard = resize
        self.text = text
        self.make_keyboard()

    def make_keyboard(self):
        for text in self.text:
            self.add(KeyboardButton(text))


def check(chat_id: int | str) -> bool:
    if BotUser.objects.filter(telegram_id=str(chat_id)).first() is not None:
        return True
    return False


buttons = [['Минимальные баллы на контракт', 'contract_points'],
           ['Стоимость обучения', 'price'],
           ['Узнать о ФБ подробно', 'https://business.nstu.ru'],
           ['Оплата контракта', 'how_to_pay'],
           ['Даты приёма',
            'https://nstu.ru/entrance/enrollment_campaign/calendar_bachelor'],
           ['Контакты', 'contacts'],
           ['Приемная кампания НГТУ',
            'https://nstu.ru/entrance/enrollment_campaign'],
           ['Задать вопрос зам. декана', 'send_message']]


def delete_messages(chat_id: int, message_id: int, iterations: int = 1):
    for _ in range(1, iterations + 1):
        try:
            bot.delete_message(chat_id, message_id - _)
        except Exception:
            pass


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    id_ = message.chat.id
    bot.send_message(id_, 'Добрый день, {}! Для доступа к интересующей'
                          ' вас информации, используйте кнопки.'.format(message.from_user.first_name),
                     reply_markup=InlineKeyboard(text=buttons))

    if len(BotUser.objects.filter(telegram_id=id_)) == 0:
        user = BotUser()
        user.name = message.from_user.username
        user.telegram_id = id_
        user.save()


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, width: int = 2, text: list = None):
        super().__init__()
        self.text = text
        if width == 2:
            self.row_width = len(text)
        else:
            self.row_width = width
        self.make_keyboard()

    def make_keyboard(self):
        for text in self.text:
            if 'http' in text[1]:
                self.add(InlineKeyboardButton(text[0], url=text[1]))
            else:
                self.add(InlineKeyboardButton(text[0], callback_data=text[1]))


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: CallbackQuery):
    if call.data != 'back':
        user = BotUser.objects.filter(telegram_id=call.message.chat.id).first()
        if call.data == 'contract_points':
            user.contract_points += 1
        elif call.data == 'price':
            user.price += 1
        elif call.data == 'how_to_pay':
            user.how_to_pay += 1
        elif call.data == 'contacts':
            user.contacts += 1
        user.save()

    if call.data == 'contract_points':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Экономика Бух.учет и финансы от <b>170 баллов</b>\n'
                                   'Экономика Предприятий и инвестиции <b>от 170 баллов</b>\n'
                                   'Менеджмент (Маркетинг, Логистика, Управление Бизнесом) <b>от 170 баллов</b>\n'
                                   'Менеджмент в индустрии питания <b>от 160 баллов</b>\n'
                                   'Менеджмент в туристкой индустрии <b>от 150 баллов</b>\n'
                                   'Индустриальный менеджмент и технологическое предпринимательство <b>от 150 баллов</b>\n'
                                   'Бизнес-информатика <b>от 170 баллов</b>\n'
                                   'Экономическая безопасность <b>от 155 баллов</b>', parse_mode='html',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))

    elif call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Для доступа к интересующей'
                                   ' вас информации используйте кнопки.'
                                   ''.format(call.message.from_user.first_name),
                              reply_markup=InlineKeyboard(text=buttons))

        user = BotUser.objects.filter(telegram_id=call.message.chat.id).first()
        user.mail_flag = False
        user.save()

    elif call.data == 'price':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='<b>119.000р</b> за год обучения\n'
                                   'При поступлении нужно оплатить <b>59.500р</b> за первый семестр',
                              parse_mode='html',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))

    elif call.data == 'how_to_pay':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Чтобы оплатить контракт необходимо подать в приемную комиссию оригинал документа'
                                   ' об образовании и согласие на зачисление на выбранное направление\n'
                                   'Инструкция по онлайн оплате:\nhttps://nstu.ru/entrance/enrollment_campaign/contract',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))

    elif call.data == 'contacts':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='<b>8-383-249-64-49</b> - Заместитель декана ФБ Долгов Алексей Семенович\n'
                                   '<b>8-960-788-30-23</b> - 11 Окно приемной комиссии ФБ\n'
                                   'Пн. - пт. С 10.00 до 16.30',
                              parse_mode='html',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))

    elif call.data == 'send_message':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Напишите ваш вопрос, указав <b>контакты для обратной связи</b>',
                              parse_mode='html',
                              reply_markup=InlineKeyboard(1, [['<- Назад', 'back']]))
        user = BotUser.objects.filter(telegram_id=call.message.chat.id).first()
        user.mail_flag = True
        user.save()


@bot.message_handler(content_types=['text'])
def send_text(message):
    if not check(message.chat.id):
        start_message(message)

    id_ = message.chat.id
    text = message.text
    current_user = BotUser.objects.get(telegram_id=int(id_))

    if current_user.mail_flag:
        Mail(text, 'Сообщение от бота ФБ', ['daneel453@gmail.com'], current_user.name).send_mail()
        bot.send_message(id_, 'Сообщение отправлено!', reply_markup=InlineKeyboard(text=buttons))
        current_user.mail_flag = False
        current_user.save()
    else:
        bot.send_message(id_, 'Я вас не понял. Попробуйте еще раз')
# 'dolgov.als@yandex.ru'