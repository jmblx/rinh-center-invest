import base64
import os
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from src.config import SMTP_PASSWORD, SMTP_USER

from src.utils import render_email

from src.constants import SMTP_HOST, SMTP_PORT


# создание шаблона для отправки на почту
def get_email_template_dashboard(
    user_first_name: str,
    user_email: str,
    request_verdict
):
    email = EmailMessage()
    email['Subject'] = 'Отчет по заявке на кредит'
    email['From'] = SMTP_USER
    email['To'] = user_email

    current_script_path = os.path.abspath(__file__)

    script_directory = os.path.dirname(current_script_path)
    if request_verdict > 0.5:
        relative_image_path = "../static/НЕ_ОДОБРЕНО.png"
        verdict = "Не одобрено"
    else:
        relative_image_path = "../static/ОДОБРЕНО.png"
        verdict = "Одобрено"
    image_path = os.path.abspath(os.path.join(script_directory, relative_image_path))
    with open(image_path, "rb") as image_file:
        # Кодирование изображения в base64
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    email_content = render_email(user_first_name, encoded_image, verdict)
    email.set_content(
        email_content,
        subtype='html'
    )
    return email


# отправка на почту отчёта
def send_email_report_dashboard(
    user_first_name: str,
    user_email: str,
    request_verdict=0
):
    email = get_email_template_dashboard(user_first_name, user_email, request_verdict)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
