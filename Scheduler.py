import threading
import time

import schedule
import os


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def send_quote_emails():
    os.system("java -jar SchwartzBot.jar")
    print("Sending out motivation emails!")


def schedule_tasks():
    schedule.every().minute.do(send_quote_emails)
    run_continuously()


class Scheduler:

    def __new__(cls):
        return super().__new__(cls)
