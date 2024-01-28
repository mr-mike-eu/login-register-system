### Libery
import sqlite3
import socket
import threading
import random
import time


### Config
server_ip = "localhost"
server_port = 12345
app_version = "1.0.0"
app_download = "https://github.com/mr-mike-eu/login-register-system"
sql_path = "sqlite_database.db"
header_lenght = 9999999999


### Functions
def handle_client(connection, address):# Functions - Client Handle
    print(f"Nový klient pripojený\nIP: {address}")
    while True:
        data = connection.recv(header_lenght).decode()
        if not data:
            print(f"Klient odpojený\nIP: {address}")
            break
        data_split = data.split(",")
        sql_conn = sqlite3.connect(sql_path)
        sql_cursor = sql_conn.cursor()
        ### LOGIN CHECKER - "LOGIN,{log_user},{log_pass}"
        if data_split[0] == "LOGIN":
            sql_cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (data_split[1], data_split[2]))
            sql_row = sql_cursor.fetchone()
            if sql_row is not None:
                connection.sendall(("TRUE").encode())
            else:
                connection.sendall(("FALSE").encode())
        # REGISTER CHECKER - "REGISTER,{reg_user},{reg_pass}"
        elif data_split[0] == "REGISTER":
            sql_cursor.execute("SELECT * FROM users WHERE username=?", (data_split[1],))
            sql_row = sql_cursor.fetchone()
            if sql_row:
                connection.sendall(("FALSE-USER").encode())
            else:
                sql_cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (data_split[1], data_split[2],))
                sql_conn.commit()
                connection.sendall(("TRUE").encode())
    sql_cursor.close()
    sql_conn.close()
    connection.close()


### Server Setting
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (server_ip, server_port)
server_socket.bind(server_address)

### Waiting For Client
while True:
    print("Atomic Private Comunity - Server\nČakanie na klienta...")
    server_socket.listen(5)
    connection, address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    client_thread.start()
