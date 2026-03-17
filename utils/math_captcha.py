import random


def generate_captcha():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    op = random.choice(["+", "-"])

    if op == "+":
        return f"{a} + {b} = ?", a + b

    if a < b:
        a, b = b, a
    return f"{a} - {b} = ?", a - b
