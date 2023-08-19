import time

CYAN = '\033[96m'
GREEN = '\033[92m'
RESET = '\033[0m'

def cool_print_cyan(message):
    print(CYAN + message + RESET)
    time.sleep(0.3)

def cool_print_green(message):
    print(GREEN + message + RESET)
    time.sleep(0.3)

def cool_progress_bar(segments):
    for i in range(segments):
        print(GREEN + "▓", end='', flush=True)
        time.sleep(0.15)
    print(RESET)
