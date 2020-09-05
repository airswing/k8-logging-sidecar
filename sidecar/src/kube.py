from kubernetes.client.rest import ApiException
from kubernetes import client, config, watch
import os


def get_k8_instance(service_token_path, service_cert_path, namespace_path):
    configuration = client.Configuration()
    # Get K8 service host and port from environment
    configuration.host = "https://%s:%s" % (os.getenv("KUBERNETES_SERVICE_HOST"), os.getenv("KUBERNETES_SERVICE_PORT"))

    # Pull service account token from secrets and add to configuration
    #service_token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    if not os.path.isfile(service_token_path):
        raise ApiException("Service token file does not exist.")
    with open(service_token_path) as f:
        token = f.read()
        if not token:
            raise ApiException("Token file exists but is empty.")
        configuration.api_key['authorization'] = "bearer " + token.strip('\n')

    # Pull service cert from secrets and add to configuration
    #service_cert_path = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    if not os.path.isfile(service_cert_path):
        raise ApiException("Service certification file does not exist.")
    with open(service_cert_path) as f:
        if not f.read():
            raise ApiException("Cert file exists but is empty.")
        configuration.ssl_ca_cert = service_cert_path

    client.Configuration.set_default(configuration)

    # Pull namespace from secrets
    #namespace_path = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
    with open(namespace_path, 'r') as fin:
        namespace = fin.read()

    # Pull pod name from environment
    pod_name = os.environ['POD_NAME']
    if pod_name == None or pod_name == "":
        raise EnvironmentError("Pod name not found in POD_NAME.")

    return client.CoreV1Api(), watch.Watch(), namespace, pod_name
