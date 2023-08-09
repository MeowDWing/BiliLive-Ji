RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
WHITE = 0xFFFFFF
BLACK = 0x000000


def print_set(text: str, tag: str = 'NORMAL', debug_flag: bool = False):
    begin_str = ''
    end_str = '\033[0m'
    match tag:
        case 'SYSTEM': begin_str = '\033[91m[SYSTEM]'  # Red bright
        case 'ERROR': begin_str = '\033[41m[ERROR]'  # Red bottom
        case 'WARNING': begin_str = '\033[43m[WARNING]'  # Yellow bottom
        case 'SUCCESS': begin_str = '\033[42m[SUCCESS]'  # Green bottom
        case 'GIFT': begin_str = '\033[93m'  # Yellow bright
        case 'SC': pass
        case 'UP': begin_str = '\033[92m'  # Green bright
        case 'CTRL': begin_str = '\033[96m'  # Sky blue bright
        case 'FANS': end_str = ''  # Normal
        case 'CAPTAIN': begin_str = '\033[94m'  # Blue bright
        case 'NORMAL': begin_str = '\033[90m'  # Gray
        case _: end_str = ''
    # print format:
    # color_CTRL head prefix text suffix color_CTRL_end
    # \033[xxm[HEAD->PREFIX]TEXT[SUFFIX]\033[m
    # \033[91m[SYSTEM->REPLY MODULE]xxxxxxxxx\033[m
    print(begin_str, end='')
    print(text, end='')
    print(end_str)


def print_head():
    pass


