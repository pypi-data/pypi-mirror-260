from clint.textui import puts, colored, indent
from threading import Timer
from pick import pick
import colorama, keyboard, random, numpy, time

try: import msvcrt
except ImportError: windows = False
else: windows = True

colorama.init()

class Choice:
    def __init__(self, index: int, option: str):
        self.index = index
        self.option = option

def choose_from_list(title: str, options: list, indi: str = "*", minselcont: int = 1) -> Choice:
    option, index = pick(options, title, indi, min_selection_count=minselcont)
    index += 1
    return Choice(index, option)

class RepeatedTimer:
    def __init__(self, interval: float, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def isdebug(args: list) -> bool: args.pop(0); return '-d' in args

def progress_bar(current: int, total: int, name: str = "Progress", bar_length: int = 50):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current >= total else '\r'
    print(f'{name}: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

def ask_bool(prompt: str) -> bool:
    try: return {"true": True, "yes": True, "y": True, "false": False, "no": False, "n": False}[input(prompt).lower()]
    except KeyError: print("invalid input")

def ask_int(prompt: str) -> int:
    while True:
        try: return int(input(prompt))
        except ValueError: print("not a number")

def printc(n: str, *d, f: bool = False, sepL: int = 0, sepC: str = ' ', Beg: str = colored.green('//|'), BegL: int = 4, end: str = '\n'):
    sep = sepC * sepL
    w = ''.join(map(str, d))
    with indent(BegL, quote=Beg):
        if not f: puts(colored.blue(n) + sep + w + end, newline=False)
        else: puts(colored.blue(w) + sep + n + end, newline=False)

def stringc(n: str, d: str = '', f: bool = False, sepL: int = 0, sepC: str = ' ', Beg: str = colored.green('//|'), BegL: int = 4, end: str = '\n') -> str:
    sep = sepC * sepL
    air = " " * (BegL - len(Beg))
    if not f: return f"{Beg}{air}{colored.blue(n)}{sep}{d}{end}"
    else: return f"{Beg}{air}{colored.blue(d)}{sep}{n}{end}"

def printd(n: str, d: str = '', f: bool = False, A: bool = False, sepL: int = 0, sepC: str = ' ', Beg: str = colored.red('>>|'), BegL: int = 4):
    if A:
        sep = sepC * sepL
        with indent(BegL, quote=Beg):
            if not f: puts(colored.blue(n) + sep + d)
            else: puts(colored.blue(d) + sep + n)

def wind_getonekey(f: bool = True) -> str:
    if not windows: return ''
    if f: return str(msvcrt.getch(), 'utf-8')
    else: return msvcrt.getch()

def clearsc(type: int = 1):
    if type == 1: print('\033[2J')
    elif type == 2: print('\n' * 25)

def clearinp(t: int = 25, e: bool = False):
    for i in range(t):
        keyboard.press_and_release("\b")
        if e: printc(f"on the {i + 1} backspace")

if __name__ == '__main__': exit()
