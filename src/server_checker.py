from paramiko import SSHClient
import json


def load_configuration_file():
    str_json = None
    with open("./config/config.json","r") as f:
        str_json = f.read()
    return str_json

#TODO: 
def get_ssh_client(hostname, username=None,password=None,key_file=None):
    client = SSHClient()
    client.load_system_host_keys()
    client.connect(hostname,username=username,password=password)
    return client

def get_configuration():
    return json.loads(load_configuration_file())


def process_hosts(cmd, hosts):
    output_set = set()
    for host in hosts:
        client =get_ssh_client(host['hostname'],host['username'],host['password'])
        _, stdout, _ = client.exec_command(cmd)
        output = stdout.read().decode("utf-8")
        output_set.add(output)
        print(output)
        client.close()
    print(len(output_set))



def process_validator(validators):
    for  item in validators:
        print("Exec the cmd: {}".format(item['cmd']))
        process_hosts(item['cmd'],item['hosts'])

def process():
    config = get_configuration()
    process_validator(config['validators'])

if __name__ == "__main__":
    process()