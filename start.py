#!/usr/bin/env python

import os
import json

import jinja2

from subprocess import Popen

HA_CONFIG_TMPL_PATH = 'haproxy.cfg.tmpl'
HA_CONFIG_PATH = '/etc/haproxy/haproxy.cfg'
PROXY_PATH = 'proxies.json'
NUM_PROXIES = int(os.environ.get('NUM_PROXIES', 5))


def render(tpl_path, context):
    """render haconfig from template

    Parameters
    -----------------
    tpl_path : str
        location of the template file to render
    context : dict
        information to include in the template i.e proxy details

    Returns
    ----------------
    str
        rendered haproxy config as string
    """
    path, filename = os.path.split(tpl_path)
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './'), autoescape=True
    ).get_template(filename)
    return template.render(context)


def create_proxy_config(backends):
    """create haproxy config using the data from proxy list

    Parameters
    --------------
    backends : list(dict)
        list of proxy details i.e ipaddress and port

    Returns
    -------------
    str
        rendered haproxy config containing proxies defined in the backends parameters
    """
    context = {'backends': backends}
    return render(HA_CONFIG_TMPL_PATH, context)


def preprocess_proxy(proxy):
    """fix proxy list to IPAddress,Port format from dictionary to ipaddress,port

    Parameters
    ----------------
    proxy : dict
        proxy details form the proxy json file

    Returns
    ---------------
    dict
        constaining keys ipaddress and port for the proxy
    """
    return {'ipaddress': proxy['IPAddress'], 'port': proxy['Port']}


def preprocess_proxy_list():
    """convert json proxy file to proxy formet list

    Returns
    ---------------
    list(dict)
        list of proxies with ipaddress and ports
    """
    proxies_list = read_proxy_config(PROXY_PATH)

    return [ preprocess_proxy(proxy) for proxy in proxies_list ]


def read_proxy_config(file_name):
    """convert proxy file from json file to python data structure

    Parameters
    --------------
    file_name : str
        location of proxies json list file

    Returns
    -------------
    object
        datastructure representation of json file
    """
    with open(file_name) as data_file:
        data = json.load(data_file)
    return data


def write_ha_proxy_config(config):
    """write haproxy file to location `HA_CONFIG_PATH`

    Parameters
    --------------
    config : str
        haproxy config string
    """
    with open(HA_CONFIG_PATH, 'w') as file:
        file.write(config)
        file.flush()


def prepare_requested_proxies(backends, num_proxies):
    """validate the proxies and select that match the requested numbers form json list

    Parameters
    --------------
    backends : list(dict)
        list of proxy config i,e ipaddress and port
    num_proxies: int
        number of proxies to create

    Returns
    -------------
    list(dict)
        spliced list of proxies based on the `num_proxies`
    """
    if len(backends) < num_proxies:
        return backends
    # TODO check for active proxies
    return backends[:num_proxies]


backends = preprocess_proxy_list()
active_backends = prepare_requested_proxies(
    backends=backends, num_proxies=NUM_PROXIES
)

ha_config = create_proxy_config(active_backends)
write_ha_proxy_config(ha_config)

p = Popen(['haproxy -d -f {}'.format(HA_CONFIG_PATH)], shell=True)
p.wait()
print('done running')
