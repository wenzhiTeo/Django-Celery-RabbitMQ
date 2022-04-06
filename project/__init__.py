from __future__ import absolute_import, unicode_literals

# make sure the app is always imported
from .celery import app as celery_app

__all__ = "celery_app"
