from Event import event_handle, on_message_func_list
from fastapi import FastAPI, Body

app = FastAPI()


@app.post("/")
def _(data=Body(...)):
    event_handle(data)


def on_message(func):
    on_message_func_list.append(func)
