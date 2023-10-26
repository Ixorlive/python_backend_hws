import algos.fft as algos
from celery import Celery

app = Celery("tasks")
app.config_from_object("celery_config")


@app.task(name="fft_inverse", queue="fft_inverse")
def fft_inverse(array, mod=7340033, root=5, root_1=4404020, root_pw=1 << 20):
    return algos.fft(array, True, mod, root, root_1, root_pw)
