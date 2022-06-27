#!/home/maxim/.env/bin/python

from email import message
from time import sleep
import requests
import os

class TelegramBot:
    def __init__(self) -> None:
        self.messages = []
        self.offset = None
        self.token = os.getenv('TELEGRAM_TOKEN')

    def get_messages(self) -> list:
        return self.messages
        
    def clean_messages(self) -> None:
        self.messages = []

    def get_url(self, method: 'str') -> str:
        telegram_api_url = 'https://api.telegram.org/bot'
        return (
            f'{telegram_api_url}'
            f'{self.token}/'
            f'{method}'
        )

    def get_updates(self) -> list:
        url = self.get_url('getUpdates')
        params = {'offset': self.offset}
        response = requests.get(url, params)
        if response.status_code != 200:
            print(f'Error: {response.status_code}')
            return
        
        response_json = response.json()
        result = response_json['result']
        return result

    def check_new_messages(self) -> None:
        updates = self.get_updates()

        if updates == []:
            return

        for item in updates:
            msg = item.get('message', 'management_task')
            if msg == 'management_task':
                continue
            
            text = msg.get('text', 'service_msg')
            if text == 'service_msg':
                continue

            event = {
                'chat_id': msg['chat']['id'],
                'name': msg['from']['first_name'],
                'text': msg['text'],
            }
            self.messages.append(event)
        self.offset = item['update_id'] + 1

    def send_message(self, text: str, chat_id: str) -> None:
        url = self.get_url('sendMessage')
        data = {
            'chat_id': chat_id,
            'text': text,
        }
        requests.post(url, data)

if __name__ == '__main__':
    telegram = TelegramBot()
    while True:
        telegram.check_new_messages()
        msgs = telegram.get_messages()
        for msg in msgs:
            telegram.send_message(msg['text'], msg['chat_id'])
            telegram.messages = []
        sleep(5)
