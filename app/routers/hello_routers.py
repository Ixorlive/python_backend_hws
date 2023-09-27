from fastapi import APIRouter, Body

from app.helloworld.hello import get_hello_msg

router = APIRouter()


@router.get("/hello/{name}")
def read_hello_name(name: str):
    """
    Handle GET request and read the name from path.
    """
    return {"message": get_hello_msg(name)}


@router.get("/hello")
def read_hello_query(name: str):
    """
    Handle GET request and read the name from query parameter.
    """
    return {"message": get_hello_msg(name)}


@router.post("/hello")
def read_hello_body(name: str = Body(..., example="Igor")):
    """
    Handle POST request and read the name from request body.
    """
    return {"message": get_hello_msg(name)}
