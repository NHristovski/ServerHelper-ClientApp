import uuid


def get_client_id():
    return hex(uuid.getnode())