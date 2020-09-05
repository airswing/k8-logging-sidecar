import logging
import abc
import logstash


class Endpoints:
    def __init__(self, config_endpoints):
        self.endpoints = config_endpoints
        self.instantiate_endpoints()

    def instantiate_endpoints(self):
        for endpoint in self.endpoints:
            if endpoint['enabled']:
                if endpoint['type'] == 'console':
                    endpoint['object'] = Console(endpoint)
                elif endpoint['type'] == 'file':
                    endpoint['object'] = File(endpoint)
                elif endpoint['type'] == 'logstash':
                    endpoint['object'] = Logstash(endpoint)
            else:
                self.endpoints.remove(endpoint)

    def close_all_files(self):
        for endpoint in self.endpoints:
            if endpoint['type'] == 'file':
                endpoint['object'].close()

    def output(self, output, container_name):
        for endpoint in self.endpoints:
            endpoint['object'].output(output, container_name)


class Endpoint(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def output(self, output, container_name):
        pass


class Console(Endpoint):
    def __init__(self, endpoint):
        self.name = endpoint['name']
        logging.basicConfig(level=endpoint['logging_level'])

    def output(self, output, container_name):
        logging.info(f'{container_name}:{output}')


class File(Endpoint):
    def __init__(self, endpoint):
        self.name = endpoint['name']
        self.filename = endpoint['path']
        self.encoding = endpoint['encoding']
        self.file_handle = open(self.filename, "wb", buffering=0)

    def output(self, output, container_name):
        output += '\n'
        self.file_handle.write(f'{container_name}:{output}'.encode(self.encoding))

    def close(self):
        self.file_handle.close()


class Logstash(Endpoint):
    def __init__(self, endpoint):
        self.name = endpoint['name']
        self.host_url = endpoint['host_url']
        self.host_port = endpoint['host_port']
        self.version = endpoint['version']

        self.logger = logging.getLogger('python-logstash-logger')
        self.logger.setLevel(logging.INFO)
        if endpoint['protocol'] == 'TCP':
            self.logger.addHandler(logstash.TCPLogstashHandler(self.host_url, self.host_port, version=self.version))
        else:
            # 'UDP'
            self.logger.addHandler(logstash.LogstashHandler(self.host_url, self.host_port, version=self.version))

    def output(self, output, container_name):
        self.logger.info(f'{container_name}:{output}')