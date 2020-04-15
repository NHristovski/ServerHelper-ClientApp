import uvicorn
from fastapi import FastAPI
from src.common import config_reader
from src.commands.command_listener import CommandListener


""" uvicorn src.main:app --reload """

app = FastAPI()

command_listener = CommandListener("nikola")


# TODO: make this /health. We should check if still connected to mqtt server, return
#  { "status" : "{if all the services are ok then "ok", else "failed"}
#  , "services" : ["mqtt" : "ok (connected) / "failed" (not connected) ]
@app.get("/")
def read_root():
    return "healthy"


@app.get("/create")
def create_command_listener():
    # TODO get address and port from consul
    command_listener.start_listening(config_reader.get_address(), 1883)


@app.get("/stop")
def create_command_listener():
    command_listener.stop_listening("nikola")


if __name__ == "__main__":
    # Purpose: to allow debugging
    # To launch: python -m src.main
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("src.main:app", reload=True)
