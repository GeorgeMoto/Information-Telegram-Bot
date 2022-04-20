import asyncio

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions

from main import bot, dp
from config import admins
from keyboars.keyboars import *
from Data import *
from sql.sql_functions import *
from dt_functions.data_formatting_functions import *

# send greening message to admin when bot started
async def send_greeting_to_admin(dp):
    await bot.send_message(chat_id=admins["George"], text="<b>Бот запущен</b>")


@dp.message_handler(Command("start"))
async def start(message: Message):

    id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    id_list = get_id_list()

    if not message.from_user.is_bot and id not in id_list:
        add_user_to_db(id, username, first_name, last_name)
        create_backup_db()

    keyboard = get_start_key_board()

    await message.answer(text=greetings, reply_markup=keyboard)


@dp.message_handler(Command("links"))
async def get_number_of_links_(message):
    if message.from_user.id in admins.values():

        number_of_link_address = get_number_of_link_address()
        print(number_of_link_address)

        await message.answer(text=f"В базе осталось ссылок для подключений: {number_of_link_address}")


@dp.callback_query_handler(lambda call: call.data == "key_information")
async def get_information(call: CallbackQuery):

    await call.message.answer(information_text)
    await call.answer(cache_time=30)


@dp.callback_query_handler(lambda call: call.data == "key_download")
async def get_info_download(call: CallbackQuery):

    await call.message.answer(download_text)
    await call.answer(cache_time=30)


@dp.callback_query_handler(lambda call: call.data == "key_important_info")
async def get_important_info(call: CallbackQuery):

    await call.message.answer(important_info_text)
    await call.answer(cache_time=30)


@dp.callback_query_handler(lambda call: call.data == "key_payments")
async def get_payments_info(call: CallbackQuery):

    await call.message.answer(payments_text, reply_markup=get_keyboard_to_make_payment())
    await call.answer(cache_time=30)


@dp.callback_query_handler(lambda call: call.data == "key_subscription")
async def get_subscription_info(call: CallbackQuery):
    if get_status(call.from_user.id):

        date = change_date_format(get_finish_date(call.from_user.id))
        paynot = change_date_format(get_payment_notice(call.from_user.id))

        await call.message.answer(payment_notice_text.format(date, paynot))
        await call.answer(cache_time=30)

    else:

        await call.message.answer("Вы еще не оформили подписку")
        await call.answer(cache_time=30)


@dp.message_handler(Command("help"))
async def get_help(message):

    await message.answer(text=help_text)


@dp.message_handler(Command("backup"))
async def backup(message):

    if message.from_user.id in admins.values():
        await message.answer(text="Хочешь сделать backup бд?", reply_markup=get_backup_keyboard())


@dp.callback_query_handler(lambda call: call.data == "key_backup")
async def get_make_backup(call: CallbackQuery):

    keyboard = get_keyboard_yes_or_no("ДА", "НЕТ", "key_copy", "key_cancel_copy")
    create_backup_db()

    await call.message.answer("Backup Запущен. Выслать копию бд?", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data in ("key_copy", "key_cancel_copy"))
async def make_backup(call: CallbackQuery):

    if call.data == "key_copy":
        await call.message.answer("Отправляю копиию бд")
        with open(PATH_TO_BACKUP_DB, "rb") as file:
            db = file.read()
        await bot.send_document(admins["George"], ("copy_backup_db.db", db))

    elif call.data == "key_cancel_copy":
        await call.message.answer("Отправка отменена")
        await call.answer(cache_time=30)


@dp.message_handler(content_types=["text"])
async def send_msg(message_to_send):

    if message_to_send.from_user.id in admins.values():
        msg = message_to_send.text

        if msg.startswith("#"):
            msg = msg.lstrip("#")
            id_list = get_id_list()
            message_counter = 0

            for id_user in id_list:
                try:
                    if message_counter < 45:
                        await bot.send_message(id_user, text=msg)
                        message_counter += 1
                    else:
                        await asyncio.sleep(5)
                        message_counter = 0
                except exceptions.ChatNotFound:
                    continue
        else:
            await message_to_send.answer(text="Для массовой рассылки необходимо чтобы текст начинался с символа '#'")


@dp.message_handler(content_types=["photo"])
async def send_photo(received_photo):

    keyboard = get_control_subscription_keyboard()

    id_for_subscription = received_photo.from_user.id
    user_name = received_photo.from_user.username
    first_name = received_photo.from_user.first_name
    last_name = received_photo.from_user.last_name

    await bot.send_photo(admins["George"], received_photo.photo[-1].file_id,
                         caption=f"Пользователь с даными: &??&{id_for_subscription}\n{user_name}\n{first_name}\n"
                                 f"{last_name}&??& \nхочет оформить/продлить подписку",
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda call: call.data == "key_renew_subscription")
async def will_subscribe(callback: types.CallbackQuery):

    user_data_for_subscription = get_users_data_from_photo(callback.message.caption)
    id_for_subscription = int(user_data_for_subscription[0])

    if not get_status(id_for_subscription):
        update_status(id_for_subscription)
        update_start_day(id_for_subscription)
        set_finish_date(id_for_subscription)

        link_name, link_address = get_link_to_connection()
        update_link_address(id_for_subscription, link_address)
        update_link_name(id_for_subscription, link_name)
        delete_address_data(link_address)
        await bot.send_message(id_for_subscription, "Подписка оформлена. "
                                                    "Ссылка для подключения:\n{}".format(link_address))
        await bot.send_message(admins["George"], "Пользователю с данными: \n {} \nприсвоена ссылка "
                                                 "с именем:\n""'{}'".format(user_data_for_subscription, link_name))

    elif get_status(id_for_subscription):
        update_status(id_for_subscription)
        update_finish_day(id_for_subscription)
        await bot.send_message(id_for_subscription, "Вы успешно продлили подписку.")
        await bot.send_message(admins["George"], "Пользователь с данными: \n {} \nпродлил "
                                                 "подписку.".format(user_data_for_subscription))


@dp.callback_query_handler(lambda call: call.data == "key_cancel_subscription")
async def cancel_subscription(callback: types.CallbackQuery):

    user_data_for_subscription = get_users_data_from_photo(callback.message.caption)
    id_for_subscription = int(user_data_for_subscription[0])

    await bot.send_message(id_for_subscription, "Что-то пошло не так. Попробуйте повторить оплату чуть позже. "
                                                "Если проблема не решится то наша поддержка на связи "
                                                "в боте @Butter_robot_supportBot")


@dp.callback_query_handler(lambda call: call.data == "key_to_make_payment")
async def will_payment(call: CallbackQuery):

    if get_status(call.from_user.id):
        keyboard = get_keyboard_yes_or_no("ДА", "НЕТ", "key_make_payment", "key_cancel_payment")
        await call.message.answer(f"Ваша подписка в настоящий момент активна. "
                                  f"Срок действия подписки закончится "
                                  f"<b>{change_date_format(get_finish_date(call.from_user.id))}</b>."
                                  f" Продолжить оплату?", reply_markup=keyboard)
        await call.answer(cache_time=30)

    else:
        await call.message.answer(how_to_pay_text)
        await call.answer(cache_time=30)


@dp.callback_query_handler(lambda call: call.data in ("key_make_payment", "key_cancel_payment"))
async def continue_payment(call: CallbackQuery):

    if call.data == "key_make_payment":
        await call.message.answer(how_to_pay_subscriber)
        await call.answer(cache_time=30)

    elif call.data == "key_cancel_payment":
        await call.message.answer("Оплата отменена")
        await call.answer(cache_time=30)
