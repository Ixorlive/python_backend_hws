from fastapi import FastAPI

from .routers.hello_routers import router

app = FastAPI()


@app.get("/")
def read_root():
    """
    A simple entry point to return a greeting message.
    """
    return {"message": "Hello, World!"}


app.include_router(router, prefix="/api", tags=["hello"])
