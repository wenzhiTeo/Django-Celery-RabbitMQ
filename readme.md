# A simple task to understand the basic usage of Celery

rabbitmq-server  
**Using WSL2 - Ubuntu**  
sudo apt-get install rabbitmq-server  
sudo service rabbitmq-server start  
sudo service rabbitmq-server status  
sudo service rabbitmq-server stop  

## Start Celery
celery -A project worker -l info  


## Relevant Operation on app1
- In this will focus on the basic setup and usage of Celery
Some operation can try & test in app1
```
(venv) wenzhi@DESKTOP-RCRN99U:~/code_folder/Django-Celery-RabbitMQ$ python manage.py shell
Python 3.8.10 (default, Nov 26 2021, 20:14:08)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from app1.tasks import add
>>> add.delay(1,2)
<AsyncResult: be2e5998-5566-4bf6-b13e-dd7ee38d6f69>
>>> add.apply_async((3,3),countdown=5)
<AsyncResult: 928dce39-c641-4fc5-a718-c1c987cc3151>
>>> add.apply_async((3,3),countdown=10)
<AsyncResult: 52750088-441e-49f9-8902-fd32b8612d2f>
>>>
```

## Relevant Operartion on app2
Created a simple page to send the review email via celery
- run the server and get into the review page to test.

## Another Option? Using Clound Redis
- Using Heroku create an app and add Heroku-Redis for testing
- Get the Redis URI from the credential to replace the CELERY_BROKER_URL
```
CELERY_BROKER_URL = os.getenv("REDIS_URI")
```

## GOOGLE SMTP Issues
- Ensure that the Email sender account allowed 2FA, so can generate the app password
- copy the 16-digit password to replace the EMAIL_HOST_PASSWORD
- There is a chance that prompt the `SMTPAuthenticationError`, just recreate the password, restart the celery.
- Some Related Settings:
```
# gmail settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "hellologomy@gmail.com"
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_PASSWORD"))
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "hellologomy@gmail.com"
```

## Relevant Operation on app3
- Some basic setup and usage for Celery-Scheduled Task  
pip install flower  
celery -A project flower  --port=5566  

celery -A project beat -l INFO  

### We have multiple way to run the beat schedule task  

Set the beat schedule in settings.py  

```
CELERY_BEAT_SCHEDULE={
    "scheduled_task":{
        "task":"app1.tasks.add",
        "schedule":5.0,
        "args":(10,10),
    },
}
```

result = `[2022-04-05 11:57:59,087: INFO/MainProcess] Scheduler: Sending due task scheduled_task (app1.tasks.add)`

**OR**  
let the celery beat run the the scheduler set in database  
`celery -A project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`


## Store the Celery result
`pip install django-celery-results`  
and `CELERY_RESULT_BACKEND = 'django-db'` to settings.py

## Cache Celery result
```
CELERY_CACHE_BACKEND='default'

CACHES={
    'dafault':{
        'BACKEND':'django.core.cache.backends.db.DatabaseCache',
        'LOCATION':'cachedb',
    }
}

```  

show sql code  
`python manage.py createcachetable --dry-run`  
create table
`python manage.py createcachetable`  

WSL2 environment need to install sqlite
`sudo apt install sqlite`
