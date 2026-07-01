import time

from app.core.celery_app import celery_app


@celery_app.task
def send_email_task():

    print("Starting email task...")

    time.sleep(10)

    print("Email Sent!")

    return "Success"