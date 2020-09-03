import logging
import os
from kubernetes.client.rest import ApiException
from kubernetes import client, config, watch

logging.warning('sidecar-test logging...')
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as fin:
    nameyspacey = fin.read()

SERVICE_TOKEN_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/token"
SERVICE_CERT_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
KUBERNETES_HOST = "https://%s:%s" % (os.getenv("KUBERNETES_SERVICE_HOST"), os.getenv("KUBERNETES_SERVICE_PORT"))

## configure 
configuration = client.Configuration()
configuration.host = KUBERNETES_HOST
if not os.path.isfile(SERVICE_TOKEN_FILENAME):
    raise ApiException("Service token file does not exists.")
with open(SERVICE_TOKEN_FILENAME) as f:
    token = f.read()
    if not token:
        raise ApiException("Token file exists but empty.")
    configuration.api_key['authorization'] = "bearer " + token.strip('\n')
if not os.path.isfile(SERVICE_CERT_FILENAME):
    raise ApiException("Service certification file does not exists.")
with open(SERVICE_CERT_FILENAME) as f:
    if not f.read():
        raise ApiException("Cert file exists but empty.")
    configuration.ssl_ca_cert = SERVICE_CERT_FILENAME
client.Configuration.set_default(configuration)

api_instance = client.CoreV1Api()
w = watch.Watch()

with open("logs.txt", "wb", buffering=0) as f:
    for line in w.stream(api_instance.read_namespaced_pod_log, name=os.environ['POD_NAME'], namespace=nameyspacey, container='app-test'):
        logging.warning(line)
        line+='\n'
        f.write(line.encode('utf-8'))
