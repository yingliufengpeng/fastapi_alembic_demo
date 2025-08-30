import sys


print(f'sys is {sys.executable}')
print(f"sys's args is {sys.argv}")

i = 0

j = 2


def m():
    return i + j



m()