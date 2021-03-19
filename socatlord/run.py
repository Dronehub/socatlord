import argparse

from socatlord.operations import start_all_socats, do_precheck, kill_all_socats, install_socatlord


def run():
    parser = argparse.ArgumentParser(prog='socatlord', usage='''Call with a single argument
    *install* will install and enable socatlord to work as a systemd service (socatlord.service)
    *run* will shut down all socats that it previously spawned (free-range socats won't be touched) and restart them
    *stop* will terminate socats''')
    parser.add_argument('-v', action='store_true', help='Display what commands are ran and pipe socats to stdout')
    parser.add_argument('--config', default='/etc/socatlord', help='Location of config file (default is /etc/socatlord)')
    parser.add_argument('operation', choices=['install', 'run', 'stop'], help='Operation to do')

    args = parser.parse_args()

    do_precheck(args.config, args.v)

    if args.operation == 'install':
        install_socatlord(args.v)
    else:
        kill_all_socats(args.v)
        if args.operation == 'run':
            start_all_socats(args.config, args.v)


if __name__ == '__main__':
    run()
