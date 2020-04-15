import configparser
import pathlib

config_parser = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
config_file = "config.ini"
config_file_path = pathlib.Path(__file__).parent.absolute().joinpath(config_file)
config_parser.read(config_file_path)


def get_address():
    return config_parser["NETWORK"]["address"]
