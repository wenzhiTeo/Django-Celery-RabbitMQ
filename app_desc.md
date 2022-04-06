# A simple task to understand the basic usage of Celery

rabbitmq-server

sudo apt-get install rabbitmq-server
sudo service rabbitmq-server start
sudo service rabbitmq-server status
sudo service rabbitmq-server stop

## Start Celery
celery -A project worker -l info


## Relevant Operation on app1
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

## Relevant Operartion on app2
Created a simple page to send the review email

## Relevant Operation on app3
pip install flower
celery -A project flower  --port=5566

celery -A project beat -l INFO

### We have multiple way to run the beat schedule task

Set the beat schedule in settings.py

`CELERY_BEAT_SCHEDULE={
    "scheduled_task":{
        "task":"app1.tasks.add",
        "schedule":5.0,
        "args":(10,10),
    },
}`

result = `[2022-04-05 11:57:59,087: INFO/MainProcess] Scheduler: Sending due task scheduled_task (app1.tasks.add)`

let the celery beat run the the scheduler set in database
`celery -A project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`
