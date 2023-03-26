#!/usr/bin/env python3
import socket, codecs
import os
import threading, time

# Import of other files here
from config import config

# Constants
HOME = os.getenv('HOME')
ENCODE = 'utf-8'

def connectToServer(configfile: dict) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((configfile["server"], 6667))
    time.sleep(1)

    sock.send(f'NICK {configfile["creds"]["nick"]}\n'.encode(ENCODE))
    sock.send(f'USER {configfile["creds"]["username"]} {socket.gethostname()} {configfile["server"]} :{configfile["creds"]["realname"]}\n'.encode(ENCODE))

    return sock

def receive(sock):
    while True:
        res = sock.recv(1024).decode(ENCODE)
        if not res:
            break
        print(res)

        if res[0:4] == 'PING':
            sock.send(f'PONG {res[4:]}\n'.encode(ENCODE))
            print(sock.recv(1024).decode(ENCODE))

def main():
    config.createConfig(f'{HOME}/.config/ircpy', f'{HOME}/.config/ircpy/config.json')
    cfile = config.loadConfig(f'{HOME}/.config/ircpy/config.json')
    sock = connectToServer(cfile)

    receive_thread = threading.Thread(target=receive, args=(sock,))
    receive_thread.start()

    while True:
        prompt = input()
        sock.send(f'{prompt}\n'.encode(ENCODE))

    receive_thread.join()
    sock.close()

    return exit(0)

if __name__ == '__main__':
    main()