import pkg_resources
from satella.files import write_to_file, read_in_file
from .parse_config import parse_etc_socatlord
import subprocess
import os
import sys


verbose = False



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
        except PermissionError:
            print('Failed to kill %s with EPERM' % (pid, ))
        except OSError:
            print('Failed to kill %s' % (pid, ))
        os.unlink(path)


def run():
    global verbose

    verbose = '-v' in sys.argv
    if verbose:
        del sys.argv[sys.argv.index('-v')]

    if not os.path.exists('/etc/socatlord'):
        write_to_file('/etc/socatlord', b'''# Put your redirections here
# eg. 
# 443 -> 192.168.1.1:443
# will redirect all TCP traffic that comes to this host (0.0.0.0) to specified host and port
# to redirect UDP traffic just prefix your config with udp, eg.
# udp 443 -> 192.168.1.1:443
# You can additionally specify explicit interfaces to listen on eg.
# 192.168.1.2:443 -> 192.168.1.1:443
''')
        if verbose:
            print('/etc/socatlord created')

    if len(sys.argv) > 1:
        if sys.argv[1] == 'install':
            filename = pkg_resources.resource_filename(__name__, 'systemd/socatlord.service')
            contents = read_in_file(filename, 'utf-8')
            write_to_file('/lib/systemd/system/socatlord.service', contents, 'utf-8')
            os.system('systemctl daemon-reload')
            os.system('systemctl enable socatlord.service')
            sys.exit(0)
        elif sys.argv[1] == 'stop':
            kill_all_socats()
            sys.exit(0)
        elif sys.argv[1] == 'run':

            if not os.path.exists('/var/run/socatlord'):
                os.mkdir('/var/run/socatlord')

            kill_all_socats()

            for i, row in enumerate(parse_etc_socatlord()):
                proto, host1, port1, host2, port2 = row
                command = ['socat', '%s-listen:%s,bind=%s,reuseaddr,fork' % (proto, port1, host1),
                           '%s:%s:%s' % (proto, host2, port2)]
                kwargs = {'stdin': subprocess.DEVNULL, 'stdout': subprocess.DEVNULL,
                        'stderr': subprocess.DEVNULL}
                if verbose:
                    print('Calling %s' % (command, ))
                    kwargs = {}
                proc = subprocess.Popen(command, **kwargs)
                write_to_file(os.path.join('/var/run/socatlord', str(i)), str(proc.pid), 'utf-8')
            sys.exit(0)
    print('''Usage:

socatlord install - installs itself as a systemd service
socatlord run - stop all currently running socats and launch them anew
''')


