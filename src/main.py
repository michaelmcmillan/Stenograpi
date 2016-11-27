from argparse import ArgumentParser

parser = ArgumentParser(prog='stenograpi.py',
                        description='Document your HTTP API automatically through tests.')

parser.add_argument('--hostname', type=str, help='hostname of Stenograpi')
parser.add_argument('--port', type=int, help='port Stenograpi should listen on')

parser.add_argument('--app-hostname', type=str, help='hostname of your app')
parser.add_argument('--app-port', type=int, help='port your app is listening on')

if __name__ == '__main__':
    arguments = parser.parse_args()
