BROKER_URL = "pyamqp://python:backend@localhost:5672//"
CELERY_RESULT_BACKEND = "rpc://"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
