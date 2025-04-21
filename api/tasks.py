from celery import shared_task
from django.http import HttpResponse

@shared_task
def sample_task():
    print("This is a sample task.")
    return {"message": "Task completed"}