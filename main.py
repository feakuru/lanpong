import sys
import argparse

parser = argparse.ArgumentParser(description='A ping-pong over the LAN.')
parser.add_argument('--master', dest='master',
                    action='store_const',
                    const=True, default=False,
                    help='run in master mode (default: slave)')
parser.add_argument('--connect',
                    dest='master_address',
                    default=None,
                    help='master address to connect to')
# TODO accept master ip

args = parser.parse_args()

if args.master:
    from server import run_server
    run_server()
else:
    from game import run_game_loop
    if not args.master_address:
        print('Please provide a master address like this: --connect=1.1.1.1')
        sys.exit(1)
    run_game_loop(master_address=args.master_address)
