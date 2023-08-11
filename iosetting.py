RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
WHITE = 0xFFFFFF
BLACK = 0x000000


def print_set(text: str, tag: str = 'NORMAL', debug_flag: bool = False, log = False, special_color='FFFFFF'):
    begin_str = ''
    end_str = '\033[0m'
    if special_color != 'FFFFFF':
        tag = 'SPECIAL'
    match tag:
        case 'SYSTEM': begin_str = '\033[91m[SYSTEM]'  # Red bright
        case 'LIVE_SYS': begin_str = ''
        case 'ERROR': begin_str = '\033[41m[ERROR]'  # Red bottom
        case 'WARNING': begin_str = '\033[43m[WARNING]'  # Yellow bottom
        case 'SUCCESS': begin_str = '\033[42m[SUCCESS]'  # Green bottom
        case 'GIFT' | 'GIFT_COMBO': begin_str = '\033[93m'  # Yellow bright
        case 'SC': pass
        case 'SC_JPN': pass
        case 'UP': begin_str = '\033[92m'  # Green bright
        case 'CTRL': begin_str = '\033[96m'  # Sky blue bright
        case 'FANS': end_str = ''  # Normal
        case 'CAPTAIN': begin_str = '\033[94m'  # Blue bright
        case 'CAPTAIN_BUY_3': begin_str = '\033[38;2;0;191;255m'  # Deep Sky Blue
        case 'CAPTAIN_BUY_2': begin_str = '\033[38;2;30;144;255m'  # Doder Blue
        case 'CAPTAIN_BUY_1': begin_str = '\033[38;2;65;105;255m'  # Royal Blue
        case 'NORMAL': begin_str = '\033[90m'  # Gray
        case 'ENTER': pass
        case 'SPECIAL': pass
        case _: end_str = ''
    # print format:
    # color_CTRL head prefix text suffix color_CTRL_end
    # \033[xxm[HEAD->PREFIX]TEXT[SUFFIX]\033[m
    # \033[91m[SYSTEM->REPLY MODULE]xxxxxxxxx\033[m
    print(begin_str, end='')
    print(text, end='')
    print(end_str)
    if log:
        log_file = open("./logging.txt", mode='a')
        log_file.write(text+'\n')
        log_file.close()

def print_head():
    pass

def hex2dec_lst(self, str16: str = '#FFFFFF') -> list:
    pass


