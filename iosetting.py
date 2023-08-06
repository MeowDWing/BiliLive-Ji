RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
WHITE = 0x000000
BLACK = 0xFFFFFF


def print_set(text: str, content: str = 'NORMAL'):
    begin_str = ''
    end_str = '\033[0m'
    match content:
        case 'SYSTEM': begin_str = '\033[91m'  # Red bright
        case 'ERROR': begin_str = '\033[41m'  # Red bottom
        case 'WARNING': begin_str = '\033[43m'  # Yellow bottom
        case 'SUCCESS': begin_str = '\033[42m'  # Green bottom
        case 'UP': begin_str = '\033[92m'  # Green bright
        case 'CTRL': begin_str = '\033[96m'  # Sky blue bright
        case 'FANS': end_str = ''  # Normal
        case 'CAPTAIN': begin_str = '\033[94m'  # Blue bright
        case 'NORMAL': begin_str = '\033[90m'  # Gray
        case _: end_str = ''
    print(begin_str, end='')
    print(text, end='')
    print(end_str)

