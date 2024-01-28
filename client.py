### Libery
import os
import time
import socket
import random
from unidecode import unidecode
import re
import string


### Config
main_server_ip = "localhost"
main_server_port = 12345
app_version = "1.0.0"
notify_time = 2


### Functions
def pass_user_check(_username, _password):# Functions - Password/Username Ruls Check
    _final = False
    if _username != None:
        if len(_username) >= 3 and unidecode(_username) == _username:
            _final = True
        else:
            _final = False
    if _password != None:
        if len(_password) >= 10 and unidecode(_password) == _password and re.search(r'\d', _password) and re.search(r'[A-Z]', _password) and re.search(r'[a-z]', _password) and re.search(r'[^\w\s]', _password):
            _final = True
        else:
            _final = False
    return _final
def server_contact(send_msg):# Functions - Server Contact
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_connect:
        server_connect.connect((main_server_ip, main_server_port))
        server_connect.sendall((send_msg).encode())
        time.sleep(2)
        global server_data
        server_data = server_connect.recv(1024).decode()
        time.sleep(1)
def reset():# Functions - Reset
    global server_data, _verify_gen, verify, hl_prompt, sl_prompt, server_data_list, _link, _aprove, log_prompt, reg_user, reg_pass, _reg_pass, reg_invite
    server_data = _verify_gen = verify = hl_prompt = sl_prompt = server_data_list = _link = _aprove = log_prompt = reg_user = reg_pass = _reg_pass = reg_invite = None

### Log Panel
while True:
    os.system("cls")
    print(f"Atomic Private Comunity - {app_version}\n1|Prihlásenie\n2|Zaregistrovanie\n3|Exit")
    log_prompt = input("Vyberte si možnosť: ")
    os.system("cls")
    ### Prihlásenie
    if log_prompt == "1":
        print(f"Atomic Private Comunity - Prihlásenie")
        log_user = input("Meno: ")
        log_pass = input("Heslo: ")
        _verify_gen = random.randint(11111111, 99999999)
        verify = input(f"Overovací kód ({_verify_gen}): ")
        if verify == str(_verify_gen):
            if pass_user_check(log_user, log_pass):
                server_contact(f"LOGIN,{log_user},{log_pass}")
                if server_data in "TRUE":
                    print("Boli ste prihlásený!")
                    time.sleep(notify_time)
                    break
                else:
                    print("Heslo alebo meno nie je správne!")
                    time.sleep(notify_time)
            else:
                print("Heslo alebo meno nie je správne!")
                time.sleep(notify_time)
        else:
            print("Overovací kód nie je správne!")
            time.sleep(notify_time)
        reset()

    ### Zaregistrovanie
    elif log_prompt == "2":
        print(f"Atomic Private Comunity - Registrácia\nMeno musí obsahovať minimálne 3 znaky\nHeslo musí obsahovať:\n    - Minimálne 10 znakov\n    - Žiadnu diakritiku\n    - 1 špeciálny znak\n    - 1 veľké písmeno\n    - 1 malé písmeno\n    - 1 číslo")
        reg_user = input("Meno: ")
        reg_pass = input("Heslo: ")
        _reg_pass = input("Znova Heslo: ")
        _verify_gen = random.randint(11111111, 99999999)
        verify = input(f"Overovací Kód ({_verify_gen}): ")
        if verify == str(_verify_gen):
            if reg_pass == _reg_pass and pass_user_check(reg_user, reg_pass):
                server_contact(f"REGISTER,{reg_user},{reg_pass}")
                if server_data in "TRUE":
                    print("Boli ste zaregistrovaný!")
                elif server_data in "FALSE-USER":
                    print("Meno už je zaregistrované!")
                time.sleep(notify_time)
            else:
                print("Heslo alebo meno nie je správne!")
                time.sleep(notify_time)
        else:
            print("Overovací kód nie je správne!")
            time.sleep(notify_time)
        reset()

    ### Exit
    elif log_prompt == "3": exit()