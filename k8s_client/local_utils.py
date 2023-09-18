""" Examples how to use function execute_shell_cmd()

    from cbis_common.shell_executor import execute_shell_cmd

    verbose = True
    cwd = '/tmp/'
    cmd1 = '/bin/ls -la /'
    cmd2 = ['/bin/ls', '-l', '/']
    cmd3 = '/bin/ls /x'
    (retcode, out) = execute_shell_cmd(cmd1, cwd, verbose)
    print("Return code: %s\nOutput: %s\n" % (retcode, out))
    (retcode, out) = execute_shell_cmd(cmd2, cwd, verbose)
    print("Return code: %s\nOutput: %s\n" % (retcode, out))
    (retcode, out) = execute_shell_cmd(cmd3, cwd, verbose)
    print("Return code: %s\nOutput: %s\n" % (retcode, out))

    rados read and write files:
    ---------------------------
    rados lspools
    rados -p <pool name> <put | get> <destination key> <input file path>
    rados -p backups put gtemp /var/lib/ceph/tmp/ex.json
    rados -p backups get gtemp /var/lib/ceph/tmp/out.json

"""
import json
import pipes
import subprocess

def execute_shell_cmd(in_cmd, logger, in_cwd=None, verbose=False, ):
    if __name__ == '__main__':
        logger.debug(mystr(["execute_shell_cmd :", in_cmd]))

    logger.debug(mystr(["execute_shell_cmd with in_cmd  type and value =:", type(in_cmd), in_cmd]))

    if not in_cmd:
        raise ValueError("Empty command")

    if isinstance(in_cmd, list):
        cmd = ' '.join(map(lambda s: pipes.quote(s), in_cmd))
    elif isinstance(in_cmd, str):
        cmd = in_cmd
    else:
        logger.debug(mystr(["in_cmd  type and value = ", type(in_cmd), in_cmd]))
        return -2, 'Unknown type of input command provided'

    if not in_cwd:
        in_cwd = '/'

    try:
        logger.info(mystr(["Exe cmd: ", cmd]))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, cwd=in_cwd,
                                shell=True, close_fds=True)
        (out, err) = proc.communicate()
        if verbose:
            print("Shell stdout: %s" % out)
            print("Shell stderr: %s" % err)
    except OSError:
        raise OSError("OSError: are you trying to execute a non-existent file")
    except ValueError:
        raise ValueError("ValueError: invalid arguments passed to command: %s"
                         % cmd)
    return proc.returncode, out, err

def mystr(item_list):
    return ' '.join([str(item) for item in item_list])

def get_ncs_token(ip, logger):
    ipp = "https://" + ip + ":8084"
    #cmd = 'curl -X POST ' + str(ipp) + '/ncm/api/v1/users/login -H ' + '\"accept: application/json" -H "Content-Type: application/json\" -d' + '\'{ \"username\": \"ncs-admin\", \"password\": \"goNokia123$\"}\' -k |jq \'.[\"accessToken\"]\' |sed -E \'s/\"//g\''
    #print('cmd: {} {}'.format(type(cmd), cmd))
    #token = execute_shell_cmd(cmd, logger, in_cwd=None, verbose=False, )
    #print("Token: {} {}".format(type(token), token))

    cmd = 'curl -k -X POST ' + str(ipp) + '/ncm/api/v1/users/login -H ' + '\"accept: application/json" -H "Content-Type: application/json\" -d' + '\'{ \"username\": \"ncs-admin\", \"password\": \"goNokia123$\"}\' '
    response = execute_shell_cmd(cmd, logger, in_cwd=None, verbose=False, )
    #print("Token: {} {}".format(type(token), token))
    token = json.loads(response[1].decode())
    accessToken = token['accessToken']
    print("***************** Access token: {}".format(accessToken))

    return accessToken

def add_storageClass_bcmt_api(ip, token, logger):
    ipp = "https://" + ip + ":8084"
    cmd = 'curl -k -X POST ' + str(ipp) + '/ncm/api/v1/bcmt/storage/externalstorage -H ' + \
          '\"accept: application/json\" -H "Content-Type: application/json" -d \'' + \
          '{\"system_name\": \"nfs\", \"storage_class_name\": \"pypy\",' + \
          '\"nfs_server_addr\": \"10.22.98.80\", \"share\": \"/nfs-ex\", \"mount_options\": \"\",' + \
          '\"allow_volume_expansion\": \"true\",  \"reclaim_policy\": \"Delete\"}\'' + \
           '-H \"Authorization: Bearer ' + token + '\"'
    print('cmd: {} {}'.format(type(cmd), cmd))
    response = execute_shell_cmd(cmd, logger, in_cwd=None, verbose=False, )
    print("respons: {}".format(response))
    return

def add_storageClass_ncs_manager(ip, logger):
    ipp = "https://" + str(ip)
    cmd = 'curl -k -X POST ' + str(ipp) + '/api/cluster_bm_external_storage_operations/deploy ' + \
          '-H \"Authorization: Basic bmNzLWFkbWluOnBhc3N3b3Jk\" ' + \
          '-H \"accept: application/vnd.cbis.v2+json\" -H \"Content-Type: application/json\" -d ' + \
          '\'{\"content\":{\"external_storage_main\":{\"general_info\":{\"patches_table\":[]},' + \
          '\"operation\":{\"operation\":\"Add a new external storage\"},' + \
          '\"parameters\":{\"external_storage_class_name\":\"csi-nfs-byapi\",' \
          '\"external_storage_nfs_allow_volume_expansion\":\"true\",\"external_storage_nfs_ip\":\"10.22.98.80\",' \
          '\"external_storage_nfs_mount_options\":\"hard, nfsvers=4.1\",' \
          '\"external_storage_nfs_reclaim_policy\":\"Delete\",\"external_storage_nfs_share\":\"/nfs-a\",' \
          '\"external_storage_system\":\"nfs\"}}},\"metadata\":{\"clusters\":[\"g80-ca\"]}}\''

    print(cmd)
    response = execute_shell_cmd(cmd, logger, in_cwd=None, verbose=False, )
    print("respons: {}".format(response))
    return


if __name__ == '__main__':
    import logging

    logging.basicConfig(filename='main.log', level=logging.DEBUG)
    logging.debug(' Message sent from the main file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    logger = logging.getLogger(__name__)

    token = get_ncs_token('10.22.98.80', logger)
    #add_storageClass('10.22.98.80', token, logger)
    add_storageClass_ncs_manager('10.22.98.80', logger)
