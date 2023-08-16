RED = 0xFF0000
GREEN = 0x00FF00
BLUE = 0x0000FF
WHITE = 0xFFFFFF
BLACK = 0x000000


def print_set(text: str, tag: str = 'NORMAL', debug_flag: bool = False, log=False, special_color='FFFFFF', end='\n'):
    begin_str = ''
    end_str = '\033[0m'
    match tag:
        case 'SYSTEM': begin_str = '\033[91m[SYSTEM]'  # Red bright
        case 'LIVE_SYS': begin_str = '\033[38;2;125m[LSYS]'  # half red
        case 'ERROR': begin_str = '\033[41m[ERROR]'  # Red bottom
        case 'WARNING': begin_str = '\033[43m[WARNING]'  # Yellow bottom
        case 'SUCCESS': begin_str = '\033[42m[SUCCESS]'  # Green bottom
        case 'GIFT' | 'GIFT_COMBO': begin_str = '\033[93m'  # Yellow bright
        case 'UP': begin_str = '\033[92m'  # Green bright
        case 'CTRL': begin_str = '\033[96m'  # Sky blue bright
        case 'FANS': end_str = ''  # Normal
        case 'CAPTAIN': begin_str = '\033[94m'  # Blue bright
        case 'CAPTAIN_BUY_3': begin_str = '\033[38;2;0;191;255m'  # Deep Sky Blue
        case 'CAPTAIN_BUY_2': begin_str = '\033[38;2;30;144;255m'  # Doder Blue
        case 'CAPTAIN_BUY_1': begin_str = '\033[38;2;65;105;255m'  # Royal Blue
        case 'NORMAL': begin_str = '\033[90m'  # Gray
        case 'ENTER': begin_str = '\033[38;2;150;150;150m'  # light gray
        case 'SC' | 'SC_JPN':  # customizing color
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'
        case 'SPECIAL':
            color_str = hex2dec_str(special_color)
            begin_str = f'\033[38;2;{color_str}m'
        case _: end_str = ''
    # print format:
    # color_CTRL head prefix text suffix color_CTRL_end
    # \033[xxm[HEAD->PREFIX]TEXT[SUFFIX]\033[m
    # \033[91m[SYSTEM->REPLY MODULE]xxxxxxxxx\033[m
    print(begin_str, end='')
    print(text, end='')
    print(end_str, end=end)
    if log:
        log_file = open("./logging.txt", mode='a', encoding='utf-8')
        log_file.write(text+end)
        log_file.close()


def print_head():
    pass


def hex2dec_str(str16: str = '#FFFFFF') -> str:
    if str16[0] == '#':
        str16 = str16[1:]
    if len(str16) > 6:
        print_set('A wrong RGB color set', tag='WARNING')
        str16 = str16[0:6]
        print_set(f'new slice is {str16}', tag='WARNING')
    R_channel = '0x'+str16[0:2]
    G_channel = '0x'+str16[2:4]
    B_channel = '0x'+str16[4:]
    try:
        decR = int(R_channel, 16)
        decG = int(G_channel, 16)
        decB = int(B_channel, 16)
    except ValueError:
        print_set('You set a WRONG RGB code, color has been reset to 0x000000', tag='ERROR')
        decR = decG = decB = 0
    trans_str = str(decR)+';'+str(decG)+';'+str(decB)
    return trans_str  # str -> xx;xx;xx



