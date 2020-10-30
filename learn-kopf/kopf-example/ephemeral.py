import kopf
import kubernetes


import os
import yaml
import logging
from Glogger import GLogger

mylog_level = logging.DEBUG
mylogger = GLogger(log_file="kopf_try.log", log_level=mylog_level)
logger = mylogger.get_logger()

linux_config_file = "/root/.kube/config"
win10_config_file = "c:\kubectl\kubeconfig-win10"
mode="win10"
if mode == "win10":
    config_file = win10_config_file
    context = "minikube"
else:
    config_file = linux_config_file
    context = "k8sb1"

@kopf.on.create('zalando.org', 'v1', 'ephemeralvolumeclaims')
def create_fn(spec, name, namespace, ilogger, **kwargs):

    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    print ("path: ", path)
    tmpl = open(path, 'rt').read()
    print ("templ type: ", type(tmpl))
    text = tmpl.format(name=name, size=size)
    data = yaml.safe_load(text)
    print("Data: ", str(data))

    # Set the hierarchy so the pvc will be owned by the evc, so when evc is deleted the pvc is deleted too!
    kopf.adopt(data)

    #ilogger(f"Data:\n%s",str(data))
    kubernetes.config.load_kube_config(config_file="/root/.kube/config", context="k8sb1")
    api = kubernetes.client.CoreV1Api()
    print("********")
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    ilogger.info(f"PVC child is created: %s", obj)


@kopf.on.update('zalando.org', 'v1', 'ephemeralvolumeclaims')
def update_fn(spec, status, namespace, logger, **kwargs):

    size = spec.get('size', None)
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    pvc_name = status['create_fn']['pvc-name']
    pvc_patch = {'spec': {'resources': {'requests': {'storage': size}}}}

    kubernetes.config.load_kube_config(config_file="/root/.kube/config", context="k8sb1")
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

