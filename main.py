from typing import Annotated
from fastapi import FastAPI, Query
from data import get_lotes


app = FastAPI()


@app.get("/api/{mun}")
def user_api(mun: str, q: Annotated[list[str], Query()]):
    if q is None:
        return "q = endereço, dsqfl ou sequencial"

    lotes = get_lotes(mun, q)

    return lotes

