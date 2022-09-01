from src.celery import app

from django.core.mail import send_mail

@app.task
def celery_send_mail(subject, body, from_email, to):
    send_mail(  
        subject,
        body,
        from_email,
        to
    )