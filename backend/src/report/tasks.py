import smtplib
from email.message import EmailMessage

from celery import Celery
from jinja2 import Environment, FileSystemLoader

from src.config import SMTP_PASSWORD, SMTP_USER, REDIS_HOST, REDIS_PORT

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template_dashboard(
    user_first_name: str,
    user_email: str,
    request_verdict
):
    email = EmailMessage()
    email['Subject'] = 'Отчет по заявке на кредит'
    email['From'] = SMTP_USER
    email['To'] = "zhora.zhilin.06@mail.ru"
    env = Environment(loader=FileSystemLoader('src/templates'))
    if request_verdict == 0:
        template = env.get_template('positive.html')
    else:
        template = env.get_template('negative.html')
    rendered_html = template.render(username=user_first_name)
    email.set_content(
        rendered_html,
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(
    user_first_name: str,
    user_email: str,
    request_verdict=0
):
    email = get_email_template_dashboard(user_first_name, user_email, request_verdict)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
