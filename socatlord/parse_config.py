from satella.files import read_in_file
import sys

def parse_etc_socatlord(filename: str):
    try:
        data = read_in_file(filename, 'utf-8').replace('\r\n', '\n').split('\n')
        data = (line.strip() for line in data)
        data = (line for line in data if line)
        data = (line for line in data if not line.startswith('#'))
        data = (line.split('->') for line in data)
        data = ((host1.strip(), host2.strip()) for host1, host2 in data)

        for host1, host2 in data:
            if host1.startswith('udp '):
                proto = 'udp'
                host1 = host1.replace('udp ', '')
            else:
                if host1.startswith('tcp '):
                    host1 = host1.replace('tcp ', '')
                proto = 'tcp'

            if ':' not in host1:
                port1 = int(host1)
                host1 = '0.0.0.0'
            else:
                host1, port1 = host1.split(':')
                port1 = int(port1)

            host2, port2 = host2.split(':')
            port2 = int(port2)

            yield proto, host1, port1, host2, port2

    except (KeyError,ValueError,TypeError) as e:
        print('Error parsing /etc/socatlord: %s' % (e, ))
        sys.exit(1)
