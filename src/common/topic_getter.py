from src.common import config_reader, client_information


class Topics:
    @staticmethod
    def commands_topic():
        return f"/commands/{config_reader.get_user_id()}/{client_information.get_client_id()}"

    @staticmethod
    def metrics_topic():
        return f"/metrics/{config_reader.get_user_id()}/{client_information.get_client_id()}"

    @staticmethod
    def commands_output_topic():
        return f"/command_output/{config_reader.get_user_id()}/{client_information.get_client_id()}"

    @staticmethod
    def logs_topic():
        return f"/logs/{config_reader.get_user_id()}/{client_information.get_client_id()}"

    @staticmethod
    def login_topic():
        return f"/login"

    @staticmethod
    def response_login_topic():
        return f"/login/{config_reader.get_user_id()}/{client_information.get_client_id()}"
