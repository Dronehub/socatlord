import pkg_resources
from satella.files import write_to_file, read_in_file
from whereis.cli import where_is_executable
from .parse_config import parse_etc_socatlord
import subprocess
import os
import sys


verbose = False

def where_is_socatlord():
    return where_is_executable('socatlord')[0]


def kill_all_socats():
    global verbose
    for socat in os.listdir('/var/run/socatlord'):
        path = os.path.join('/var/run/socatlord', socat)
        pid = int(read_in_file(path, 'utf-8'))
        try:
            if verbose:
                print('Killing %s' % (pid, ))
            os.kill(pid, 9)
            if verbose:
                print('Killed %s OK' % (pid, ))
        except OSError:
            print('Failed to kill %s' % (pid, ))
        os.unlink(path)


def run():
    global verbose
    verbose = '-v' in sys.argv
    if verbose:
        del sys.argv[sys.argv.index('-v')]

    if len(sys.argv) > 1:
        if sys.argv[1] == 'install':
            filename = pkg_resources.resource_filename(__name__, 'systemd/socatlord.service')
            contents = read_in_file(filename, 'utf-8')
            contents = contents % (where_is_socatlord(), )
            write_to_file('/lib/systemd/system/socatlord.service', contents, 'utf-8')
            os.system('systemctl daemon-reload')
            os.system('systemctl enable socatlord.service')
            sys.exit(0)
        elif sys.argv[1] == 'run':

            if not os.path.exists('/var/run/socatlord'):
                os.mkdir('/var/run/socatlord')

            kill_all_socats()

            for i, row in enumerate(parse_etc_socatlord()):
                proto, host1, port1, host2, port2 = row
                if proto == 'tcp':
                    command = ['socat', 'TCP4-LISTEN:%s,bind=%s' % (port1, host1),
                               'TCP4:%s:%s' % (host2, port2)]
                else:
                    command = ['socat', 'UDP4-LISTEN:%s,bind=%s' % (port1, host1),
                               'UDP4:%s:%s' % (host2, port2)]
                if verbose:
                    print('Calling %s' % (command, ))
                proc = subprocess.Popen(command)
                write_to_file(os.path.join('/var/run/socatlord', str(i)), str(proc.pid), 'utf-8')
            sys.exit(0)
    print('''Usage:

socatlord install - installs itself as a systemd service
socatlord run - stop all currently running socats and launch them anew
''')


