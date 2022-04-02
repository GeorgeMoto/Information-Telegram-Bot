import sqlite3
#
conn = sqlite3.connect("sql_data/users_db.db")
cursor = conn.cursor()
#
# #
# insert_query = "INSERT INTO users VALUES (?, ?, ?, ?)"
# users_data = [
#     (425895564, 'Georgetheframe', 'George', 'M'),
#     (0000, 'Ge', 'Geor', 'Moto',)
# ]
#
# cursor.executemany(insert_query, users_data)
#
# cursor.execute("SELECT id, username, first_name, last_name FROM users")
# result = cursor.fetchall()
# for tup in result:
#     print(tup)

# id = 425895564
# username = 'Georgetheframe'
# first_name = 'George'
# last_name = 'fff'


# Безопасный импорт файлов в таблицу
# insert_query = "INSERT INTO users VALUES (?, ?, ?, ?)"
# cursor.execute(insert_query, user_data)

# Извлечние данных из таблицы
# cursor.execute("SELECT id, username, first_name, last_name FROM users")
# result = cursor.fetchall()
# print(result)
#for row in result:
#    print(row)

# Проверка на наличие юзера в Таблице
# print(all(map(lambda x: 425895564 not in x, result)))

# Извлечение строк по словию
cursor.execute("SELECT * FROM users WHERE first_name IS 'George'")
# for row in cursor:
#     print(row)
print(cursor.fetchone())

conn.commit()
conn.close()



