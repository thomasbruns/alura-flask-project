import mysql.connector
from mysql.connector import errorcode

print("Connecting...")

try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something's wrong with the username or the password")
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS 'game_library';")

cursor.execute("CREATE DATABASE 'game_library';")

cursor.execute("USE 'game_library';")

# criando tabelas
Tables = {}

Tables['Games'] = ("""
      CREATE TABLE 'games' (
      'id' int(11) NOT NULL AUTO_INCREMENT,
      'name' varchar(50) NOT NULL,
      'category' varchar(40) NOT NULL,
      'platform' varchar(20) NOT NULL,
      PRIMARY KEY ('id')
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
""")

Tables['Usuarios'] = ("""
      CREATE TABLE 'users' (
      'name' varchar(20) NOT NULL,
      'nickname' varchar(8) NOT NULL,
      'password' varchar(100) NOT NULL,
      PRIMARY KEY ('nickname')
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
""")

for table_name in Tables:
      table_sql = Tables[table_name]
      try:
            print('Creating table {}:'.format(table_name), end=' ')
            cursor.execute(table_name)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Already exists')
            else:
                  print(err.msg)
      else:
            print('OK')


# Adding users
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
      ("Thomas Bruns", "Frits", "teste"),
      ("Barbara Oliveira", "Xu", "teste123"),
      ("Cadu Martins", "Duzi", "teste321")
]
cursor.executemany(user_sql, users)

cursor.execute('SELECT * FROM game_library.users')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# Adding games
game_sql = 'INSERT INTO games (name, category, platform) VALUES (%s, %s, %s)'
games = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(game_sql, games)

cursor.execute('SELECT * FROM game_library.games')
print(' -------------  Games:  -------------')
for game in cursor.fetchall():
    print(game[1])

# Commmiting
conn.commit()

cursor.close()
conn.close()
