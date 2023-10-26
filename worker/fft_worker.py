import algos.fft as algos
from celery import Celery

app = Celery("tasks")
app.config_from_object("celery_config")


@app.task(name="fft", queue="fft")
def fft(array, mod=7340033, root=5, root_1=4404020, root_pw=1 << 20):
    return algos.fft(array, False, mod, root, root_1, root_pw)
