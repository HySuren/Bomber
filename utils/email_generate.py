import random
import string

def generate_random_string(length=9):
    letters = string.ascii_letters  # Все буквы (строчные и заглавные)
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string
