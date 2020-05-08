import psutil
import json
import paho.mqtt.client as mqtt

from src.common import config_reader


def on_connect(client, user_data, flags, rc):
    print("Connection returned with result code:", rc)


client = mqtt.Client("metrics_publisher")
client.on_connect = on_connect
client.username_pw_set(username=config_reader.get_username(), password=config_reader.get_password())
client.connect(config_reader.get_address(), 1883, 60)


def get_metrics():
    # Initial Dictionary
    metrics_dict = {"memory": {}, "disks": {}, "network": {}, "cpu": {}}

    # Memory metrics

    metrics_dict["memory"]["virtual"] = psutil.virtual_memory()._asdict()

    metrics_dict["memory"]["swap"] = psutil.swap_memory()._asdict()

    # Disks metrics

    disk_partitions = psutil.disk_partitions()
    metrics_dict["disks"]["disk_partitions"] = []
    for i in range(len(disk_partitions)):
        metrics_dict["disks"]["disk_partitions"].append(disk_partitions[i]._asdict())

    metrics_dict["disks"]["disk_usage"] = psutil.disk_usage("/")._asdict()

    # metrics_dict["disks"]["disk_io_counters"] = psutil.disk_io_counters(perdisk=True)

    # Network metrics

    # metrics_dict["network"]["net_io_counters"] = psutil.net_io_counters(pernic=True)

    # metrics_dict["network"]["net_connections"] = []
    # net_connections = psutil.net_connections()
    # for i in range(len(net_connections)):
    #     metrics_dict["network"]["net_connections"].append(net_connections[i]._asdict())

    net_if_addrs = psutil.net_if_addrs()
    metrics_dict["network"]["net_if_addrs"] = {}
    for el in net_if_addrs:
        metrics_dict["network"]["net_if_addrs"][el] = []
        data = net_if_addrs[el]
        for d in data:
            metrics_dict["network"]["net_if_addrs"][el].append(d._asdict())

    net_if_stats = psutil.net_if_stats()
    metrics_dict["network"]["net_if_stats"] = {}
    for el in net_if_stats:
        metrics_dict["network"]["net_if_stats"][el] = net_if_stats[el]._asdict()

    # CPU metrics

    metrics_dict["cpu"]["cpu_count"] = {}
    metrics_dict["cpu"]["cpu_count"]["physical"] = psutil.cpu_count(logical=False)
    metrics_dict["cpu"]["cpu_count"]["logical"] = psutil.cpu_count(logical=True)

    metrics_dict["cpu"]["cpu_stats"] = psutil.cpu_stats()._asdict()
    metrics_dict["cpu"]["cpu_freq"] = psutil.cpu_freq()._asdict()
    metrics_dict["cpu"]["load_average"] = psutil.getloadavg()

    metrics_dict["cpu"]["cpu_count"] = psutil.cpu_times()._asdict()

    metrics_dict["cpu"]["cpu_percent"] = psutil.cpu_percent(interval=1, percpu=True)

    cpu_times_percent = psutil.cpu_times_percent(interval=1, percpu=True)
    metrics_dict["cpu"]["cpu_times_percent"] = []
    for i in range(len(cpu_times_percent)):
        metrics_dict["cpu"]["cpu_times_percent"].append(cpu_times_percent[i]._asdict())

    json_object = json.dumps(metrics_dict)

    client.publish("metrics_topic", payload=json_object)
