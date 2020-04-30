import configparser
import pathlib

config_parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config_file = "config.ini"
config_file_path = pathlib.Path(__file__).parent.absolute().joinpath(config_file)
config_parser.read(config_file_path)


def get_address():
    return config_parser["USER-CONFIG"]["mqtt-url"]


def get_port():
    return int(config_parser["USER-CONFIG"]["mqtt-port"])


def get_user_id():
    return config_parser["USER-CONFIG"]["user-id"]
