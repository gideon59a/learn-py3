from kubernetes import client, config
from kubernetes.client import Configuration
from kubernetes.config import kube_config
import yaml

# REFs:
# https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md
# https://stackoverflow.com/questions/44691267/kubernetes-api-server


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

class  K8s_client():
    def __init__(self, configuration_yaml, logger):
        self.configuration_yaml = configuration_yaml
        self.logger = logger
        self.client = K8s(configuration_yaml=configuration_yaml, logger=logger).client

    def get_pods_list(self):
        pod_list = self.client.list_pod_for_all_namespaces(watch=False)
        for i in pod_list.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        #pp = self.client.connect_get_namespaced_pod_attach(name="nfs-server-84f75586fb-hh5tc", namespace='default')

    def get_pod(self, name, namespace):
        pod_get = self.client.read_namespaced_pod(name="nfs-server-84f75586fb-hh5tc", namespace='default')
        print("pod_get: {}".format(pod_get))
        print("pod_get keys: {}".format(pod_get.keys()))

if __name__ == "__main__":
    from Glogger import GLogger  ## fails to look at the upper dir
    mylogger = GLogger(log_file='k8s_client.log', log_level="DEBUG")
    logger = mylogger.get_logger()
    logger.info("Starting k8s client main")
    logger.debug("Printed when debug level")

    import os
    print('getcwd:      ', os.getcwd())
    print('__file__:    ', __file__)
    runs_on = 'master'
    if runs_on == 'master':
        config_file_abs_path = '/root/.kube/config'  # when run from cluster's master
    else:  # runs_on == 'wsl':
        config_file_abs_path = 'config'
    with open(config_file_abs_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line)
    print("config_file_abs_path: {}".format(config_file_abs_path))


    k8s_client = K8s_client(configuration_yaml=config_file_abs_path, logger=logger)
    k8s_client.get_pods_list()
