from sys import argv
from stenograpi import Stenograpi
from argparse import ArgumentParser

def parse_args(args):
    parser = ArgumentParser(prog='stenograpi.py',
                            description='Document your HTTP API automatically through tests.')

    parser.add_argument('hostname', type=str, help='hostname of Stenograpi')
    parser.add_argument('port', type=int, help='port Stenograpi should listen on')

    parser.add_argument('app-hostname', type=str, help='hostname of your app')
    parser.add_argument('app-port', type=int, help='port your app is listening on')
    return parser.parse_args(args)

if __name__ == '__main__':
    args = parse_args(argv[1:])
    stenograpi = Stenograpi(args.hostname, args.port, getattr(args, 'app-port'))
    stenograpi.listen()
    request = stenograpi.get_latest_request()
    print(request)
