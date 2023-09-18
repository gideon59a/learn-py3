from Glogger import GLogger
from k8s_client_utils.k8s_client_alternatives import *

mylogger = GLogger(log_file='main.log', log_level="DEBUG")
logger = mylogger.get_logger()
logger.info("Starting k8s client main")
logger.debug("Printed when debug level")

k8s_client = K8s(configuration_yaml='/root/.kube/config', logger=logger)
get_pods_list(k8s_client)

