#!/home/maxim/.env/bin/python
from time import sleep
from flask import Flask
from purchases import Purchases
from telegram_bot import TelegramBot


telegram = TelegramBot()
purchases = Purchases()

if __name__ == '__main__':
    while True:
        telegram.check_new_messages()
        msgs = telegram.get_messages()
        for msg in msgs:
            purchases.check_action(msg['text'])
            text = purchases.get_purchases()
            telegram.send_message(text, msg['chat_id'])
        telegram.messages = []
        sleep(5)
    while True:
        sleep(5)
        print('Request')
        result = telegram.get_message()
        print(result)
        if result != []:
            message = result[0]['message']
            if message.startswith(('+', '-')):
                start = message[0]
                last = message[1:].split(',')
                
                if start == '+':
                    purchases.add_purchases(last)
                if start == '-':
                    purchases.remove_purchases(last)
                p = '\n'.join(purchases.get_purchases())
                mess = f'Список покупок:\n{p}'
                telegram.send_message(mess)
