import random

def generate_new_random(history, total_count):
    new_random = random.randint(0, total_count - 1)
    while new_random in history:
        new_random = random.randint(0, total_count - 1)
    return new_random
