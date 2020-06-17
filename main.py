import argparse

parser = argparse.ArgumentParser(description='A ping-pong over the LAN.')
parser.add_argument('--master', dest='master',
                    action='store_const',
                    const=True, default=False,
                    help='run in master mode (default: slave)')
# TODO accept master ip

args = parser.parse_args()

if args.master:
    from server import run_server
    run_server()
else:
    from game import run_game_loop
    from utils import get_master_address
    run_game_loop(master_address=get_master_address())
