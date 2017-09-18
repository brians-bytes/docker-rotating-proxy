import os
import jinja2


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

HA_CONFIG_TMPL_PATH = 'haproxy.cfg.tmpl'
HA_CONFIG_PATH = '/usr/local/etc/haproxy.cfg'

context = {
    'backends': [
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
}

result = render(HA_CONFIG_TMPL_PATH, context)

print(result)