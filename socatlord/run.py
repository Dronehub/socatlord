import pkg_resources
from satella.files import write_to_file, read_in_file

from .parse_config import parse_etc_socatlord
import subprocess
import os
import sys


def run():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'install':
            filename = pkg_resources.resource_filename(__name__, 'systemd/socatlord.service')
            contents = read_in_file(filename)
            write_to_file('/lib/systemd/system/socatlord.service', contents)
            os.system('systemctl daemon-reload')
            os.system('systemctl enable socatlord.service')
            sys.exit(0)
        elif sys.argv[1] == 'run':
            for proto, host1, port1, host2, port2 in parse_etc_socatlord():
                if proto == 'tcp':
                    command = ['socat', 'TCP4-LISTEN:%s,bind=%s' % (port1, host1), 'TCP4:%s:%s' % (host2, port2)]
                else:
                    command = ['socat', 'UDP4-LISTEN:%s,bind=%s' % (port1, host1),
                               'UDP4:%s:%s' % (host2, port2)]
                subprocess.Popen(command, shell=True)
            sys.exit(0)
    print('''Usage:

socatlord install - installs itself as a systemd service
socatlord run - runs socats
''')


