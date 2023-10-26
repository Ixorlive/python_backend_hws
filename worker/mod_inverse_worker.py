from algos.mod_inverse import modInverse
from celery import Celery

app = Celery("tasks")
app.config_from_object("celery_config")


@app.task(name="mod_inverse", queue="mod_inverse")
def mod_inverse(value, modulus):
    return modInverse(value, modulus)
