from celery import Celery

app = Celery("tasks")
app.config_from_object("celery_config")


@app.task(name="fft", queue="fft")
def fft(array):
    pass


@app.task(name="fft_inverse", queue="fft_inverse")
def fft_inverse(array):
    pass


@app.task(name="mod_inverse", queue="mod_inverse")
def mod_inverse(value, modulus):
    pass
