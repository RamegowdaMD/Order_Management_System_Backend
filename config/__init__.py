from .celery import app as celery_app

__all__ = ('celery_app',)


# yaradru import madidre package , then expose celery_app

# celery.py creates engine and __init__.py registers engine when project holds


