from __future__ import absolute_import, unicode_literals

import sys

from celery import shared_task
from django.core.management import call_command


@shared_task
def database_backup():
    sys.stdout = open("db.json", "w")
    call_command("dumpdata", "app3")
