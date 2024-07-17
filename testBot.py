import math
import telebot
from telebot import types

Token = '6683199231:AAHZiAE6UowMUyF6phRllNyhoRxgOtjF1mo'
bot = telebot.TeleBot(Token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item1 = types.KeyboardButton('Привет')
    markup.add(item1)
    bot.send_message(message.from_user.id, 'Привет! Нажмите кнопку для продолжения.', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Привет')
def say_hello(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    markup.add(item2)
    bot.send_message(message.from_user.id,
                     'Здравствуйте, я бот, который может зашифровывать и изменять ваши сообщения с помощью Афинного и '
                     'шифра Абатш. Нажмите на кнопку меню, чтобы перейти к разделам 1 и 2',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Меню')
def say_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    item3 = types.KeyboardButton('Раздел 1')
    item4 = types.KeyboardButton('Раздел 2')
    markup.add(item3, item4)
    bot.send_message(message.from_user.id,
                     'В разделе меню вам дается два раздела с рашифрованием и зашифрованием с помощью Афинного и Абатш шифров '
                     'соответвенно. Выберите нужный вам шифр и опцию!',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Раздел 1')
def say_Razdel1(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    item3 = types.KeyboardButton('Зашифровать с помощью Аффинного шифра')
    item4 = types.KeyboardButton('Расшифровать с помощью Аффинного шифра')
    markup.add(item2, item3, item4)
    bot.send_message(message.from_user.id,
                     'В этом разделе вам требуется ввести текст для его изменения с помощью Афинного шифра',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Зашифровать с помощью Аффинного шифра')
def say_AfCypher(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    markup.add(item2)
    bot.send_message(message.from_user.id,
                     'Введите два числа через пробел (например, "2 7"). Первое число (a) должно быть взаимно простым '
                     'с 33 (1, 2, 4, 5, 7, 8, 10, 12, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31), затем через пробел '
                     'введите ваш текст:',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_af_cipher_keys)


def get_af_cipher_keys(message):
    try:
        input_parts = message.text.split()
        a, b = map(int, input_parts[:2])
        user_message = ' '.join(input_parts[2:])

        if a not in [1, 2, 4, 5, 7, 8, 10, 12, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31]:
            raise ValueError

        encrypted_message = encrypt_af_cipher(user_message, a, b)

        bot.send_message(message.from_user.id, f'Зашифрованное сообщение: {encrypted_message}')

    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item2 = types.KeyboardButton('Меню')
        item3 = types.KeyboardButton('Попробовать снова')

        markup.add(item2, item3)
        bot.send_message(message.from_user.id,
                         'Произошла ошибка. Попробуйте ввести данные снова или вернитесь в меню.',
                         reply_markup=markup)
        bot.register_next_step_handler(message, handle_cipher_error)


def handle_cipher_error(message):
    if message.text == 'Попробовать снова':
        bot.send_message(message.from_user.id,
                         'Введите два числа через пробел (например, "2 7"). Первое число (a) должно быть взаимно '
                         'простым с 33 (1, 2, 4, 5, 7, 8, 10, 12, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31)'
                         'затем введите ваше сообщение:')
        bot.register_next_step_handler(message, get_af_cipher_keys)
    elif message.text == 'Меню':
        say_menu(message)


def encrypt_af_cipher(message, a, b):
    result = ''
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for i in range(len(message)):
        if message[i].lower() in alphabet:
            if message[i].isupper():
                letter = message[i].lower()
                indexOfLetter = alphabet.index(letter)
                result += alphabet[(a * indexOfLetter + b) % len(alphabet)].upper()
            else:
                letter = message[i]
                indexOfLetter = alphabet.index(letter)
                result += alphabet[(a * indexOfLetter + b) % len(alphabet)]
        else:
            result += message[i]

    return result


@bot.message_handler(func=lambda message: message.text == 'Расшифровать с помощью Аффинного шифра')
def say_AfDecipher(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    markup.add(item2)
    bot.send_message(message.from_user.id,
                     'Введите два числа через пробел (например, "2 7"). Первое число (a) должно быть взаимно простым '
                     'с 33 (1, 2, 4, 5, 7, 8, 10, 12, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31), затем через пробел '
                     'введите ваш текст:',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_af_decipher_keys)


def get_af_decipher_keys(message):
    try:
        input_parts = message.text.split()
        a, b = map(int, input_parts[:2])
        user_message = ' '.join(input_parts[2:])

        if math.gcd(a, 33) != 1:
            raise ValueError

        decrypted_message = decrypt_af_cipher(user_message, a, b)

        bot.send_message(message.from_user.id, f'Расшифрованное сообщение: {decrypted_message}')

    except ValueError:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        item2 = types.KeyboardButton('Меню')
        item3 = types.KeyboardButton('Попробовать снова')

        markup.add(item2, item3)
        bot.send_message(message.from_user.id,
                         'Произошла ошибка. Попробуйте ввести данные снова или вернитесь в меню.',
                         reply_markup=markup)
        bot.register_next_step_handler(message, handle_decipher_error)


def handle_decipher_error(message):
    if message.text == 'Попробовать снова':
        bot.send_message(message.from_user.id,
                         'Введите два числа через пробел (например, "2 7"). Первое число (a) должно быть равно 2:')
        bot.register_next_step_handler(message, get_af_decipher_keys)
    elif message.text == 'Меню':
        say_menu(message)


def decrypt_af_cipher(message, a, b):
    print(a)
    result = ''
    a_inv = 0
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for i in range(32):
        print(i)
        if (a * i) % 33 == 1:
            a_inv = i
    print(a_inv)
    for i in range(len(message)):
        if message[i].lower() in alphabet:
            if message[i].isupper():
                letter = message[i].lower()
                indexOfLetter = alphabet.index(letter)
                result += alphabet[(a_inv * (indexOfLetter - b)) % len(alphabet)].upper()
            else:
                letter = message[i]
                indexOfLetter = alphabet.index(letter)
                result += alphabet[(a_inv * (indexOfLetter - b)) % len(alphabet)]
        else:
            result += message[i]

    return result


@bot.message_handler(func=lambda message: message.text == 'Раздел 2')
def say_Razdel2(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item2 = types.KeyboardButton('Меню')
    item3 = types.KeyboardButton('Зашифрование с помощью Абатша')
    item4 = types.KeyboardButton('Расшифрование с помощью Абатша')
    markup.add(item2, item3, item4)
    bot.send_message(message.from_user.id,
                     'В этом разделе вам требуется ввести текст для его изменения с помощью Абатша',
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Зашифрование с помощью Абатша')
def say_Abatsha(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bot.send_message(message.from_user.id, 'Введите текст для зашифрования', reply_markup=markup)
    bot.register_next_step_handler(message, handle_abatsha_encrypt)


def handle_abatsha_encrypt(message):
    text = message.text
    result = ''
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for i in range(len(text)):
        if text[i].lower() not in alphabet:
            result += text[i]
        for j in range(len(alphabet)):
            if text[i].lower() == alphabet[j] and text[i].isupper():
                result += alphabet[len(alphabet) - j - 1].upper()
            elif text[i].lower() == alphabet[j] and text[i].islower():
                result += alphabet[len(alphabet) - j - 1]

    bot.send_message(message.from_user.id, f'Зашифрованный текст: {result}')


@bot.message_handler(func=lambda message: message.text == 'Расшифрование с помощью Абатша')
def say_Abatsha(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bot.send_message(message.from_user.id, 'Введите текст для расшифрования', reply_markup=markup)
    bot.register_next_step_handler(message, handle_abatsha_decrypt)


def handle_abatsha_decrypt(message):
    text1 = message.text
    print(text1)
    result1 = ''
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    for i in range(len(text1)):
        if text1[i].lower() not in alphabet:
            result1 += text1[i]
        for j in range(len(alphabet)):
            if text1[i].lower() == alphabet[j] and text1[i].isupper():
                result1 += alphabet[len(alphabet) - j - 1].upper()
            elif text1[i].lower() == alphabet[j] and text1[i].islower():
                result1 += alphabet[len(alphabet) - j - 1]

    bot.send_message(message.from_user.id, f'Расшифрованный текст: {result1}')


bot.infinity_polling()
