from fastapi import FastAPI
from command_listener import CommandListener

app = FastAPI()

cmdListener = CommandListener('nikola')
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/create')
def create_command_listener():
    # TODO get address and port from consul
    cmdListener.start_listening("192.168.1.224", 1883)

@app.get('/stop')
def create_command_listener():
    cmdListener.stop_listening('nikola')


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}