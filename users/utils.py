import random

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*!&$#?=@'


def generate_token(length=10):
    return ''.join(random.choice(CHARS) for _ in range(length))


def generate_password(length=10):
    return ''.join(random.choice(CHARS) for _ in range(length))