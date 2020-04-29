import configparser
import pathlib

config_parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config_file = "config.ini"
config_file_path = pathlib.Path(__file__).parent.absolute().joinpath(config_file)
config_parser.read(config_file_path)


def get_address():
    return config_parser["NETWORK"]["address"]

def get_port():
    return int(config_parser["NETWORK"]["port"])


def get_user_id():
    # TODO use the real function from oli
    return "fakeClientID";
