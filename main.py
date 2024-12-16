from parser import *
from sendingEmail import *
import schedule
import time

def checkStatusandSendEmail():
    status_xrpl = run_status_tracer()
    sendEmail(status_xrpl)

if __name__ == '__main__':
    schedule.every(6).hours.do(checkStatusandSendEmail)

    while True:
        schedule.run_pending()
        time.sleep(1)