import inspect
from datetime import datetime

class bcolors:
    WHITE = '\033[37m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def log(message: str, color=bcolors.RESET):
    now = datetime.now()
    caller_func_name = inspect.stack()[1].function
    print(f'{color}[{now.strftime("%Y-%m-%d %H:%M:%S")}] {caller_func_name}: {message}{bcolors.RESET}')