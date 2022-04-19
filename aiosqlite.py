# import aiosqlite
#
# import sqlite3
# import datetime
# import calendar
# from contextlib import contextmanager
# from contextlib import asynccontextmanager
#
# from dt_functions.data_formatting_functions import change_str_to_date_format
# from config import PATH_TO_DB, PATH_TO_BACKUP_DB
#
#
# # Connect to database
# @asynccontextmanager
# async def open_db():
#     connection = await aiosqlite.connect(PATH_TO_DB)
#     try:
#         yield connection
#     finally:
#         await connection.commit()
#         await connection.close()
#
#
# # Get a generator that contains active users from database
# async def get_id_list():
#
#     async with open_db() as db:
#         async with db.execute("SELECT id FROM users") as cursor:
#             # rows = await cursor.fetchall
#             res = await cursor.fetchall()
#             res = (id[0] for id in res)
#             print(*res)
#             return res
#
#
# # Add new user to database
# async def add_user_to_db(id, username, first_name, last_name):
#
#     async with open_db() as cursor:
#         # id, username, first_name, last_name, start_date, notification, status, link_name, link_address
#         insert_query = "INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
#         user_data = (id, username, first_name, last_name, "2000-01-01", "2000-01-01", 0, None, None)
#         await cursor.execute(insert_query, user_data)
#
#
# # Create a database backup
# async def create_backup_db():
#
#     con = await aiosqlite.connect(PATH_TO_DB)
#     bck = await aiosqlite.connect(PATH_TO_BACKUP_DB)
#     async with bck:
#         await con.backup(bck, pages=1)
#     await bck.close()
#     await con.close()
#
#
# # Return from database subscription finish date
# async def get_finish_date(user_id):
#
#     async with open_db() as cursor:
#         sql_finish_date = f"SELECT finish_date FROM users WHERE id IS ?"
#         await cursor.execute(sql_finish_date, (user_id,))
#         res = await cursor.fetchone()[0]
#
#     return res
#
#
# # Get subscription status for a specific user from database
# async def get_status(user_id):
#
#     async with open_db() as cursor:
#         sql_status = f"SELECT status FROM users WHERE id IS ?"
#         await cursor.execute(sql_status, (user_id,))
#         res = await cursor.fetchone()[0]
#
#     return res
#
#
# # Get the date to send a notification to the user when their subscription expires
# # Based on the module Datetime, the date is calculated from the principle: finish date minus 3 days
# async def get_payment_notice(user_id):
#
#     finish_date = await get_finish_date(user_id)
#     finish_date = change_str_to_date_format(finish_date)
#     payment_notice = str(finish_date - datetime.timedelta(days=3))
#
#     return payment_notice
#
#
# # change user status to active
# async def update_status(user_id):
#
#     async with open_db() as cursor:
#         sql_update_status = f"UPDATE users SET status = 1 WHERE id = ?"
#         await cursor.execute(sql_update_status, (user_id,))
#
#
# # change user status to inactive
# async def cancel_status(user_id):
#
#     async with open_db() as cursor:
#         sql_update_status = f"UPDATE users SET status = 0 WHERE id = ?"
#         await cursor.execute(sql_update_status, (user_id,))
#
#
# # When renewing a subscription for 1 month, it extends the expiration date
# async def update_finish_day(user_id):
#
#     async with open_db() as cursor:
#         finish_date = await get_finish_date(user_id)
#         finish_date = change_str_to_date_format(finish_date)
#
#         days = calendar.monthrange(finish_date.year, finish_date.month)[1]
#         next_month_date = str(finish_date + datetime.timedelta(days=days))
#
#         sql_update_finish_date = "UPDATE users SET finish_date= ? WHERE id = ?"
#         data = (next_month_date, user_id)
#         await cursor.execute(sql_update_finish_date, data)
#
#
# # Returns today's date
# async def get_today_date() -> str:
#
#     today = datetime.date.today()
#     today = str(today)
#
#     return today
#
#
# # Changes the default value to a the subscription date to the database
# async def update_start_day(user_id):
#
#     async with open_db() as cursor:
#         today = await get_today_date()
#         sql_update_start_date = "UPDATE users SET start_date= ? WHERE id = ?"
#         data = (today, user_id)
#         await cursor.execute(sql_update_start_date, data)
#
#
# # Assigns an expiration date for the subscription based on today's date
# async def set_finish_date(user_id):
#
#     async with open_db() as cursor:
#         today = await get_today_date()
#         today = change_str_to_date_format(today)
#
#         days = calendar.monthrange(today.year, today.month)[1]
#         finish_date = str(today + datetime.timedelta(days=days))
#
#         sql_get_finish_date = "UPDATE users SET finish_date= ? WHERE id = ?"
#         data = (finish_date, user_id)
#         await cursor.execute(sql_get_finish_date, data)
#
#
# # Get data(id, username, first_name, last_name) about a specific user from database
# async def get_information_from_db(user_id):
#
#     async with open_db() as cursor:
#         sql_get_info_query = "SELECT username, first_name, last_name FROM users WHERE id IS ?"
#         await cursor.execute(sql_get_info_query, (user_id,))
#         result = await cursor.fetchall()
#
#     return result
#
#
# # Return tuple(link_name, link_address) from db
# async def get_link_to_connection() -> tuple:
#     async with open_db() as cursor:
#         await cursor.execute("SELECT * FROM links")
#         link_data = await cursor.fetchone()
#
#         return link_data
#
#
# # Delete link_name and link_address from database
# async def delete_address_data(link_address):
#     async with open_db() as cursor:
#         sql_delete_link = "DELETE FROM links WHERE link_address IS ?"
#         await cursor.execute(sql_delete_link, (link_address,))
#
#
# # Update link_address assigned a specific user from database
# async def update_link_address(user_id, link_address):
#     async with open_db() as cursor:
#         sql_update_link_address = "UPDATE users SET link_address = ? WHERE id = ?"
#         await cursor.execute(sql_update_link_address, (link_address, user_id))
#
#
# # Update link_name assigned a specific user from database
# async def update_link_name(user_id, link_name):
#     async with open_db() as cursor:
#         sql_update_link_address = "UPDATE users SET link_name = ? WHERE id = ?"
#         await cursor.execute(sql_update_link_address, (link_name, user_id))
