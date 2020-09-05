import argparse
import atexit
import threading

from kube import *
from config import Config


def main(config_file):
    config = Config()
    endpoints = config.read(config_file)
    atexit.register(endpoints.close_all_files)

    service_token_path, service_cert_path, namespace_path = config.get_kubernetes_config()
    api_instance, watch, namespace, pod_name = get_k8_instance(service_token_path, service_cert_path, namespace_path)

    # Launch a thread for each container
    for container_name in config.container_names:
        threading.Thread(target=watch_n_stream, args=(api_instance, watch, namespace, pod_name, endpoints, container_name)).start()


def watch_n_stream(api_instance, watch, namespace, pod_name, endpoints, container_name):
    for line in watch.stream(api_instance.read_namespaced_pod_log, name=pod_name, namespace=namespace,
                             container=container_name):
        endpoints.output(line, container_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kubernetes Logging Sidecar')
    parser.add_argument('configfile', type=str, help='Path of config file for Kubernetes Logging Sidecar to run')
    args = parser.parse_args()
    main(args.configfile)
