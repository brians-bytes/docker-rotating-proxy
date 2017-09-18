import os
import json

import jinja2

HA_CONFIG_TMPL_PATH = 'haproxy.cfg.tmpl'
HA_CONFIG_PATH = '/usr/local/etc/haproxy.cfg'
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


backends = [
    {
        'ipaddress': '127.0.0.1',
        'port': 2344
    },
    {
        'ipaddress': '127.0.0.1',
        'port': 2344
    },
    {
        'ipaddress': '127.0.0.1',
        'port': 2344
    },
    {
        'ipaddress': '127.0.0.1',
        'port': 2344
    },
]

print(preprocess_proxy_list())
