# Operator code per https://kopf.readthedocs.io/en/latest/walkthrough/starting/
import kopf
import kubernetes
import os
import yaml
import logging

# If we want a separated log into a file, the following worked at least outside the functions:
from Glogger import GLogger
mylog_level = logging.DEBUG
mylogger = GLogger(log_file="kopf_try.log", log_level=mylog_level)
glogger = mylogger.get_logger()
glogger.debug("STARTING LOG")


'''
# The current log is embedded into KOPF one
# mylog_level = logging.DEBUG  ## makes not differce
# logging.basicConfig(filename='main.log', level=logging.DEBUG)  ## makes not differce
logging.debug(' Message sent from the main file')
logging.info('So should see this')
logging.warning('And this too')
xlogger = logging.getLogger(__name__)
xlogger.debug("local (non KOPFD) logger initialized")
'''

''' Its output is:
root@d00609c69511:~/learn-kopf/kopf-example# kopf run ephemeral.py --verbose
[2020-11-05 14:23:00,882] root                 [DEBUG   ]  Message sent from the main file
[2020-11-05 14:23:00,883] root                 [INFO    ] So should see this
[2020-11-05 14:23:00,883] root                 [WARNING ] And this too
[2020-11-05 14:23:00,883] ephemeral            [DEBUG   ] local (non KOPFD) logger initialized

'''



linux_config_file = "/root/.kube/config"
win10_config_file = "c:\kubectl\kubeconfig-win10"
#mode="win10"
mode = "linux"
if mode == "win10":
    config_file = win10_config_file
    context = "minikube"
else:
    config_file = linux_config_file
    #context = "k8sb1"
    context = "kubernetes-admin@kubernetes"

@kopf.on.create('zalando.org', 'v1', 'ephemeralvolumeclaims')
def create_fn(spec, name, namespace, logger, **kwargs):
#Note: The name "logger" is required)

    logger.info("ENTERING INTO EVC CREATE")
    glogger.debug("ALSO INTO A FILE: ENTERING INTO EVC CREATE")

    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    print("path: ", path)
    tmpl = open(path, 'rt').read()  # read the file into str
    # print("templ type: ", type(tmpl))
    text_str = tmpl.format(name=name, size=size)
    # print("text type: ", type(text))
    data = yaml.safe_load(text_str)  # Load into dict
    print("\nData type: ", type(data), "\nData: ", str(data), "\n")

    # Set the hierarchy so the pvc will be owned by the evc, so when evc is deleted the pvc is deleted too!
    kopf.adopt(data)

    logger.info(f"Data:\n%s", str(data))
    kubernetes.config.load_kube_config(config_file="/root/.kube/config", context=context)
    api = kubernetes.client.CoreV1Api()
    print("********")
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logger.info(f"\n ******** PVC child is created: %s ********* \n\n", obj)


@kopf.on.update('zalando.org', 'v1', 'ephemeralvolumeclaims')
def update_fn(spec, status, namespace, logger, **kwargs):
    ''' Update the PVC size '''

    size = spec.get('size', None)
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    pvc_name = status['create_fn']['pvc-name']
    pvc_patch = {'spec': {'resources': {'requests': {'storage': size}}}}

    kubernetes.config.load_kube_config(config_file="/root/.kube/config", context=context)
    api = kubernetes.client.CoreV1Api()
    obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )

    logger.info(f"PVC child is updated: %s", obj)


@kopf.on.field('zalando.org', 'v1', 'ephemeralvolumeclaims', field='metadata.labels')
def relabel(old, new, status, namespace, **kwargs):

    pvc_name = status['create_fn']['pvc-name']
    pvc_patch = {'metadata': {'labels': new}}

    kubernetes.config.load_kube_config(config_file="/root/.kube/config", context="k8sb1")
    api = kubernetes.client.CoreV1Api()
    obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )

