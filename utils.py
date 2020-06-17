import itertools
import ifcfg
import socket


def is_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, int(port)))
        sock.shutdown(2)
        return True
    except:
        return False


def get_master_address():
    ifaces = ifcfg.interfaces()
    iface = [
        iface
        for name, iface in ifaces.items()
        if name.startswith('eth')
    ][0]

    ip_range = []
    if iface['inet'].startswith('10.'):
        # 10.x.x.x
        ip_range = [
            '10.{}.{}.{}'.format(x, y, z)
            for x, y, z in itertools.combinations_with_replacement(range(255), 3)
        ]
    elif iface['inet'].startswith('172.16.'):
        # 172.16.x.x-172.31.x.x
        ip_range = [
            '172.{}.{}.{}'.format(x, y, z)
            for x, y, z in zip(
                range(16, 32), # TODO rewrite this zip to work
                itertools.combinations_with_replacement(range(255), 2)
            )
        ]
    elif iface['inet'].startswith('192.168.'):
        # 192.168.x.x
        ip_range = [
            '192.168.{}.{}'.format(x, y)
            for x, y in itertools.combinations_with_replacement(range(255), 2)
        ]
    else:
        raise Exception('This does not seem to be a local network.')


    for ip_addr in ip_range:
        if is_open(ip_addr, 5005):
            # maybe curl some index page
            return ip_addr + ':5005'