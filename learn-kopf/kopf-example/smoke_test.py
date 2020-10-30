import kopf
import kubernetes


import os
import subprocess
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

def smoke_test(ilogger):
    kubernetes.config.load_kube_config(config_file=config_file, context=context)
    api = kubernetes.client.CoreV1Api()
    ret = api.list_pod_for_all_namespaces(watch=False)
    ilogger.debug("Printing existing pods")
    print("Printing existing pods:\n-----------------------\n")
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        ilogger.debug("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    print("*** end of smoke test *** \n\n")
    ilogger.info("*** end of smoke test *** \n")

def stam(spec, name, namespace, ilogger, **kwargs):
    size = spec
    print("just path: ", type(os.path.dirname(__file__)), os.path.dirname(__file__))
    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    path2 = os.path.dirname(__file__) + '/pvc.yaml'
    print("path2: ", type(path2), path2)
    print("path: ", path)
    tmpl = open(path, 'rt').read()
    print("templ type: ", type(tmpl))
    print(tmpl)
    text = tmpl.format(name=name, size=size)
    print("text: ", "\n", text)
    # data = yaml.safe_load(text)

    kubernetes.config.load_kube_config(config_file=config_file, context=context)
    api = kubernetes.client.CoreV1Api()

    ret = api.list_pod_for_all_namespaces(watch=False)
    print("Printing existing pods:\n-----------------------\n")
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    print("*** end of smoke test *** \n\n")

    str1 = "aaa"
    str2 = "bbbbbb"
    str3 = "ccccccccccc"
    logger.debug("%s\t%s\t%s" % (str1, str2, str3))

stam("1G", "myname", "myns", logger)

exit (0)

cmd = "c:\kubectl\kubectl182 --kubeconfig c:\kubectl\kubeconfig-win10 cluster-info"
#clusterinfo = os.system(cmd) # the old way
#print(type(clusterinfo))  # got the shell return code only
reply = subprocess.run(cmd, capture_output=True)
reply_bytes = reply.stdout
print(reply_bytes.decode("utf-8"))

exit(0)
smoke_test(logger)
