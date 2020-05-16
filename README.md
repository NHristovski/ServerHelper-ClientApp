## How to start multiple client applications
Assuming `clientapp_env` and `clientapp_config` are different users.
We create new services for each user, while the scaling factor represents
the number of servers they own.
```shell script
docker-compose up --scale clientapp_env=5 --scale clientapp_config=3
```

# Topics

## Login
### Outgoing
We send to topic `/login` message:
```
{
    "user_id": "{user id from config file: string}",
    "client_id": "{client id mac address: string}"
}
```
### Incoming
We listen on topic `/login/{user_id}/{client_id}` message:
```
success|failure
```

## Commands
### Incoming
We listen on topic `/commands/{user_id}/{client_id}` message:
```
{
    "command_id": {id: integer},
    "command_type": {"start"|"stop": string},
    "body": {"command": string} [OPTIONAL (must only appear for "command_type": "start")]
}
```
### Outgoing
We send to topic `/command_output/{user_id}/{client_id}` either:
```
{
    "command_id": {id: integer},
    "final": false,
    "line": {line of output: string}
}
```
or
```
{
    "command_id": {id: integer},
    "final": true,
    "output": {output lines (usually empty): string},
    "result_code": integer,
    "killed": boolean
}
```

## Metrics
### Outgoing
We send to topic `/metrics/{user_id}/{client_id}`
message [of format](https://github.com/NHristovski/ServerHelper-ClientApp/blob/master/src/metrics/output_format.json).

## Logs
### Outgoing
We send to topic `/logs/{user_id}/{client_id}` string message:
```
[ {date and time in UTC} ] [ INFO|WARN|ERROR ] [ {user_id}:{client_id} ] {message} 
```

