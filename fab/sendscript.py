#/usr/bin/python
# -*- encoding:utf-8

import paramiko
from paramiko.ssh_exception import AuthenticationException
from scp import SCPClient

import logging

USER="andesil"
SERVER='127.0.0.1'
PORT=22

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


if __name__ == "__main__":
    #logger = logging.getLogger("paramiko").setLevel(logging.NOTSET)
    logging.basicConfig(filename="test.log", level=logging.INFO)
    f = open("./passfile.py", mode='r')

    password = f.read().split('\n')[0]
    ssh = createSSHClient(SERVER, PORT, USER, password)

    try:
        ssh = createSSHClient(SERVER, PORT, USER, password)
        scp = SCPClient(ssh.get_transport())
        scp.put("test.log", remote_path="~/uploads")
    except AuthenticationException:
        logging.error("Authentication failed")
        pass
    logging.info("Finished")

# EOF
