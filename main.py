import json
import time
import traceback
from pyrogram import Client
from random import randint

class Main:
    def __init__(self):
        self.app = []
        self.chat_id = []
        self.query = []
        self.results = []
        self.api_id_and_hash = None
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
        self.collect_images()
        self.start_sending()

    def start_sending(self):
        while True:
            try:
                for id in self.chat_id:
                    for client in self.app:
                        for result in self.results:
                            client.send_inline_bot_result(chat_id = id, query_id = result[0], result_id = result[1][randint(0, len(self.results[0][1]) - 1)].id)
            except Exception:
                print(f"dibilniki\n{traceback.format_exc()}")
            finally:
                time.sleep(self.wait_time)

    def collect_images(self):
        for query in range(0, len(self.query)):
            result = self.app[0].get_inline_bot_results("pic", self.query[query])
            self.results.append((result.query_id, result.results))

if __name__ == '__main__':
    main = Main()
    main.start_app()
