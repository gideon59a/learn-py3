from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.config import kube_config
import yaml


def run_locally_option():
    # OPTION 1: Run on the node where k8s is installed. See the config by running # kubectl config view
    #           An example for a config file location is /etc/kubernetes/cluster-admin.kubeconfig
    # REF: https://github.com/kubernetes-client/python

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# ---------------------------------------------------------------------------------------------------------

# Option 2: Explicit ref to the kubeconfig file
# REF:https://stackoverflow.com/questions/44691267/kubernetes-api-server


class K8s(object):
    def __init__(self, configuration_yaml, logger):
        self.configuration_yaml = configuration_yaml
        self._configuration_yaml = None
        self.logger = logger

    @property
    def config(self):
        with open(self.configuration_yaml, 'r') as f:
            if self._configuration_yaml is None:
                print("self.configuration_yaml: {}".format(self.configuration_yaml))
                self.logger.debug("self.configuration_yaml: {}".format(self.configuration_yaml))
                self._configuration_yaml = yaml.safe_load(f)
        return self._configuration_yaml

    @property
    def client(self):
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.CoreV1Api()


def run_with_my_config(configuration_yaml):
    # Instantiate your kubernetes class and pass in config
    kube_one = K8s(configuration_yaml=configuration_yaml)  # e.g. '/root/.kube/config'
    pod_list = kube_one.client.list_pod_for_all_namespaces(watch=False)
    for i in pod_list.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# ---------------------------------------------------------------------------------------------------------

# Option 3: Run from laptop using local config file
# REF:https://stackoverflow.com/questions/44691267/kubernetes-api-server



# ---------------------------------------------------------------------------------------------------------
def get_pods_list(k8s_client):
    pod_list = k8s_client.client.list_pod_for_all_namespaces(watch=False)
    for i in pod_list.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # run_locally_option()  # Option 1
    # run_with_my_config('/root/.kube/config')  # Option 2, run at the target server using a specific config file

    import os
    print('getcwd:      ', os.getcwd())
    print('__file__:    ', __file__)

    runs_on = 'master'
    if runs_on == 'master':
        config_file_abs_path = '/root/.kube/config'  # when run from cluster's master
    elif runs_on == 'wsl':
        config_file_abs_path = 'config'
    #config_file_rel_path = "..\kubectl.kubeconfig"
    #config_file_abs_path = os.path.join(os.path.dirname(__file__), config_file_rel_path)
    with open(config_file_abs_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
    print("config_file_abs_path: {}".format(config_file_abs_path))
    #run_with_my_config(config_file_abs_path)

    k8s_client = K8s(configuration_yaml=config_file_abs_path)
    get_pods_list(k8s_client)

