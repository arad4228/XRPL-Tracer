import smtplib
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv, find_dotenv, set_key
from pprint import pformat
from datetime import datetime
import os



def sendEmail(status_xrpl):
    ## load ENV Setting
    load_dotenv()
    listReceivedUser = list()
    i = 1
    while(True):
        if os.environ.get("user"+str(i)) == None:
            break
        listReceivedUser.append(os.environ.get("user"+str(i)))
        i=i+1
    
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d')
    form = MIMEBase('multipart', 'mixed')
    form['Subject'] = Header(f"[PET] Ripple Validatro Status {formatted_time}")
    form['From'] = "PET-RIPPLE-STATUS-Checker"
    form['to'] = ','.join(listReceivedUser)
    
    writter_data = f"발송시점을 기준으로 한 4일 간의 xrpl Validator 기록은 아래와 같습니다.\n{pformat(status_xrpl)}"
    # 이전 발송 기록에서 이미 서버 점검 문구가 나갔다면 다시 내보내지 않음.
    if int(status_xrpl[0]['missed']) >= 80 and os.environ.get('isUptolimit') == 0:
        writter_data = f"현재일자({formatted_time})에 오류가 많으니, 서버 점검을 진행하기 바랍니다.\n" + writter_data
        
        dotenv_file = find_dotenv()
        set_key(dotenv_file, 'isUptolimit', 1)
        set_key(dotenv_file, 'lastMissDate', formatted_time)
    
    env_Datetime = os.environ.get('lastMissDate')
    current_date = datetime.now()
    formatted_time = current_date.strftime('%Y-%m-%d')
    if formatted_time > str(env_Datetime):
        dotenv_file = find_dotenv()
        set_key(dotenv_file, 'isUptolimit', 0)

    content = MIMEText(writter_data.encode("UTF-8"), _subtype='plain', _charset="UTF-8")
    form.attach(content)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    try:
        if smtp_port == 587:
            smtp = smtplib.SMTP(smtp_server, smtp_port)
            rcode2, _ = smtp.starttls()
        else:
            smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        
        smtp.login(os.environ.get('account'), os.environ.get('password'))
        smtp.sendmail(os.environ.get('account'), listReceivedUser, form.as_string())
        smtp.quit
    except Exception as e:
        print("Error Occurred: " + str(e))
        
            