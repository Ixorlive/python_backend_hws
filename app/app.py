from fastapi import FastAPI

from app.routers.tc_manager import router

app = FastAPI()


@app.get("/")
def read_root():
    """
    A simple entry point to return a greeting message.
    """
    return {"message": "Welcome to Transport Catalogue manager"}


app.include_router(router, prefix="/", tags=["hello"])
