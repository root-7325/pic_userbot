import json
import time
import traceback
from pyrogram import Client
from random import randint

class Main:
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.app = None
        self.wait_time = None
        self.chat_id = None
        self.query = None

    def read_config(self):
        with open('config.json', 'r', encoding='utf-8') as cfg:
            data = json.load(cfg)
            self.api_id = data["config"]["api_id"]
            self.api_hash = data["config"]["api_hash"]
            self.wait_time = data["config"]["wait_time"]
            self.chat_id, self.query = [], []
            for i in range(0, int(data["config"]["total_query"])):
                self.query.append(data["search_query"][str(i + 1)])
            for i in range(0, int(data["config"]["total_chat_id"])):
                self.chat_id.append(data["chat_ids"][str(i + 1)])
            self.app = Client("my_account", self.api_id, self.api_hash)

    def start_app(self):
        self.read_config()
        self.app.start()
        self.start_sending()

    def start_sending(self):
        while True:
            try:
                result = self.app.get_inline_bot_results("pic", self.query[randint(0, len(self.query) - 1)])
                for id in self.chat_id:
                    self.app.send_inline_bot_result(id, result.query_id, result.results[randint(0, len(result.results) - 1)].id)
            except Exception:
                print(f"dibilniki\n{traceback.format_exc()}")
            finally:
                time.sleep(self.wait_time)

if __name__ == '__main__':
    main = Main()
    main.start_app()
