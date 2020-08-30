import schedule
import os


class Scheduler:

    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        schedule.every().monday.at("12:00").do(self.send_quote_emails())

    def send_quote_emails(self):
        os.system("java -jar SchwartzBot.jar")
        print("Sending out motivation emails!")
