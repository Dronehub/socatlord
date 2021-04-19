import os
import subprocess
import sys
import time

import pkg_resources
from satella.coding import silence_excs
from satella.coding.sequences import smart_enumerate
from satella.files import write_to_file, read_in_file

from socatlord.parse_config import parse_etc_socatlord


def install_socatlord(verbose: bool = False) -> None:
    filename = pkg_resources.resource_filename(__name__, 'systemd/socatlord.service')
    contents = read_in_file(filename, 'utf-8')
    if verbose:
        print('Writing /lib/systemd/system/socatlord.service')
    write_to_file('/lib/systemd/system/socatlord.service', contents, 'utf-8')
    if verbose:
        print('Calling systemctl daemon-reload')
    os.system('systemctl daemon-reload')
    if verbose:
        print('Calling systemctl enable socatlord.service')
    os.system('systemctl enable socatlord.service')


def start_all_socats(config_file: str, verbose: bool = False) -> None:
    processes_and_args = []

    for i, proto, host1, port1, host2, port2 in smart_enumerate(parse_etc_socatlord(config_file)):
        command = ['socat', '%s-listen:%s,bind=%s,reuseaddr,fork' % (proto, port1, host1),
                   '%s:%s:%s' % (proto, host2, port2)]
        kwargs = {'stdin': subprocess.DEVNULL, 'stdout': subprocess.DEVNULL,
                  'stderr': subprocess.DEVNULL}
        if verbose:
            print('Calling %s' % (command,))
            kwargs = {}
        proc = subprocess.Popen(command, **kwargs)
        processes_and_args.append((proc, command))
        write_to_file(os.path.join('/var/run/socatlord', str(i)), str(proc.pid), 'utf-8')

    if verbose:
        print('All socats launched, checking for liveness...')
    time.sleep(1)

    for i, proc, cmd in smart_enumerate(processes_and_args):
        with silence_excs(subprocess.TimeoutExpired):
            proc.wait(timeout=0.0)
            rc = proc.returncode
            print('socat no %s (PID %s) died (RC=%s), command was "%s", aborting' % (i+1, proc.pid,
                                                                                     rc, cmd))
            os.unlink(os.path.join('/var/run/socatlord', str(i)))
            sys.exit(1)

    if verbose:
        print('All socats alive, finishing successfully')


def do_precheck(config_file: str, verbose: bool = False):
    if os.geteuid():
        print('Must run as root. Aborting.')
        sys.exit(1)

    if not os.path.exists(config_file):
        write_to_file(config_file, b'''# Put your redirections here
# eg. 
# 443 -> 192.168.1.1:443
# will redirect all TCP traffic that comes to this host (0.0.0.0) to specified host and port
# to redirect UDP traffic just prefix your config with udp, eg.
# udp 443 -> 192.168.1.1:443
# You can additionally specify explicit interfaces to listen on eg.
# 192.168.1.2:443 -> 192.168.1.1:443
''')
        if verbose:
            print('%s created' % (config_file,))

    if not os.path.exists('/var/run/socatlord'):
        if verbose:
            print('Making directory /var/run/socatlord')
        os.mkdir('/var/run/socatlord')
    os.chmod('/var/run/socatlord', 0o600)


def kill_all_socats(verbose: bool = False):
    for socat in os.listdir('/var/run/socatlord'):
        path = os.path.join('/var/run/socatlord', socat)
        pid = int(read_in_file(path, 'utf-8'))
        try:
            if verbose:
                print('Killing %s' % (pid, ))
            os.kill(pid, 9)
        except PermissionError:
            print('Failed to kill %s with EPERM' % (pid, ))
        except OSError:
            print('Failed to kill %s' % (pid, ))
        os.unlink(path)
