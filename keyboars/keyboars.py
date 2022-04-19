from aiogram import types


def get_keyboard_yes_or_no(text_for_yes, text_for_no, name_callback_data_yes, name_callback_data_no):

    keyboard_yes_no = types.InlineKeyboardMarkup(row_width=2)
    key_copy = types.InlineKeyboardButton(text=text_for_yes, callback_data=name_callback_data_yes)
    key_cancel_copy = types.InlineKeyboardButton(text=text_for_no, callback_data=name_callback_data_no)
    keyboard_yes_no.add(key_copy, key_cancel_copy)

    return keyboard_yes_no


def get_start_key_board():

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    key_information = types.InlineKeyboardButton(text="🧐 Информация о проекте", callback_data="key_information")
    key_download = types.InlineKeyboardButton(text="🚀 Где скачать софт", callback_data="key_download")
    key_important_info = types.InlineKeyboardButton(text="‼️Важное", callback_data="key_important_info")
    key_payments = types.InlineKeyboardButton(text="💸️ Оплата", callback_data="key_payments")
    key_subscription = types.InlineKeyboardButton(text="📟 Сведения о подписке", callback_data="key_subscription")

    keyboard.add(key_information, key_download, key_important_info, key_payments, key_subscription)

    return keyboard


def get_keyboard_to_make_payment():

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    key_to_make_payment = types.InlineKeyboardButton(text="Произвести оплату", callback_data="key_to_make_payment")
    keyboard.add(key_to_make_payment)

    return keyboard


def get_backup_keyboard():

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    key_backup = types.InlineKeyboardButton(text="ДА", callback_data="key_backup")
    keyboard.add(key_backup)

    return keyboard


def get_control_subscription_keyboard():

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    key_copy = types.InlineKeyboardButton(text="Продлить/оформить подписку", callback_data="key_renew_subscription")
    key_cancel_copy = types.InlineKeyboardButton(text="Отмена", callback_data="key_cancel_subscription")
    keyboard.add(key_copy, key_cancel_copy)

    return keyboard
