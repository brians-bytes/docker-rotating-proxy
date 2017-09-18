#!/usr/bin/env python

import os
import json

import jinja2

from subprocess import Popen,PIPE

HA_CONFIG_TMPL_PATH = 'haproxy.cfg.tmpl'
HA_CONFIG_PATH = '/etc/haproxy/haproxy.cfg'
PROXY_PATH = 'proxies.json'


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(
        path or './')).get_template(filename).render(context)


def create_proxy_config(backends):
    context = {'backends': backends}
    return render(HA_CONFIG_TMPL_PATH, context)


def preprocess_proxy(proxy):
    return {'ipaddress': proxy['IPAddress'], 'port': proxy['Port']}


def preprocess_proxy_list():
    proxies_list = read_proxy_config(PROXY_PATH)

    return list(map(lambda proxy: preprocess_proxy(proxy), proxies_list))


def read_proxy_config(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data


def write_ha_proxy_config(config):
    with open(HA_CONFIG_PATH, 'w') as file:
        file.write(config)
        file.flush()


backends = preprocess_proxy_list()

ha_config = create_proxy_config(backends)
write_ha_proxy_config(ha_config)

p = Popen(['haproxy -d -f {}'.format(HA_CONFIG_PATH)],  shell=True)
p.wait()
print ('done running')
