import argparse

parser = argparse.ArgumentParser(description='A ping-pong over the LAN.')
parser.add_argument('--master', dest='master',
                    action='store_const',
                    const=True, default=False,
                    help='run in master mode (default: slave)')

args = parser.parse_args()

if args.master:
    pass
else:
    from game import run_game_loop
    run_game_loop()
