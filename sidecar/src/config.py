import json
import logging
from endpoints import Endpoints


class Config:
    config_file_path = ''
    kubernetes = {}
    container_names = []

    def read(self, filename):
        try:
            with open(filename, 'r') as config_file_handle:
                config = json.load(config_file_handle)
                self.config_file_path = filename
                self.kubernetes = config['kubernetes']
                endpoints = Endpoints(config['endpoints'])
                self.container_names = config['kubernetes']['containers']
        except FileNotFoundError:
            logging.error(f'Config file {self.config_file_path} not found!'
                          'See example.config.json for config examples.')
        return endpoints

    def get_kubernetes_config(self):
        try:
            service_token_path = self.kubernetes['service_token_path']
            service_cert_path = self.kubernetes['service_cert_path']
            namespace_path = self.kubernetes['namespace_path']
        except KeyError:
            logging.error(f'Kubernetes config values invalid. Check {self.config_file_path}')
        return service_token_path, service_cert_path, namespace_path

