import json
import time
import traceback
from pyrogram import Client
from random import randint

class Main:
    def __init__(self):
        self.api_id_and_hash = None
        self.app = []
        self.chat_id = []
        self.query = []
        self.wait_time = None

    def read_config(self):
        with open('config.json', 'r', encoding='utf-8') as cfg:
            data = json.load(cfg)
            self.api_id_and_hash = data["config"]["api_id_and_hash"].split("|")
            self.api_hash = data["config"]["api_id_and_hash"].split("|")
            self.wait_time = data["config"]["wait_time"]
            self.chat_id = data["config"]["chat_ids"].split("|")
            self.query = data["config"]["queries"].split("|")
        for id_x_hash in self.api_id_and_hash:
            self.app.append(Client("my_account", id_x_hash.split(" ")[0], id_x_hash.split(" ")[1]))

    def start_app(self):
        self.read_config()
        for client in self.app:
            client.start()
        self.start_sending()

    def start_sending(self):
        while True:
            try:
                result = []
                for client in self.app:
                    result.append(client.get_inline_bot_results("pic", self.query[randint(0, len(self.query) - 1)]))
                for id in self.chat_id:
                    i = 0
                    for client in self.app:
                        client.send_inline_bot_result(id, result[i].query_id, result[i].results[randint(0, len(result[i].results) - 1)].id)
                        i += 1
            except Exception:
                print(f"dibilniki\n{traceback.format_exc()}")
            finally:
                time.sleep(self.wait_time)

if __name__ == '__main__':
    main = Main()
    main.start_app()
